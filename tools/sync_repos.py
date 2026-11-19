"""Sync virtual-repos/<id>/working/ from each repo's source on GitHub.

For every virtual-repos/*/meta.json:
  1. Shallow-clone `source` into a temporary directory.
  2. Delete virtual-repos/<id>/working/ if it exists.
  3. Copy the clone into working/, skipping .git, .venv, __pycache__, .DS_Store.

Only the working/ folder of each repo is touched. Other folders (e.g. chat/) are never modified.

Usage:
  python tools/sync_repos.py            # sync every repo
  python tools/sync_repos.py <repo-id>  # sync only one repo
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VIRTUAL_REPOS = REPO_ROOT / "virtual-repos"
IGNORE = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".DS_Store")


def _clear_readonly_and_retry(func, path, exc):
    """rmtree error handler: make the entry writable and retry the failed operation."""
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
    func(path)


def rmtree_force(path):
    """Remove a directory tree, handling read-only files (common on Windows)."""
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=lambda func, p, exc: _clear_readonly_and_retry(func, p, exc))
    else:
        shutil.rmtree(path, onerror=lambda func, p, exc_info: _clear_readonly_and_retry(func, p, exc_info[1]))


def load_meta(meta_path):
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def count_files(root):
    return sum(len(files) for _, _, files in os.walk(root))


def sync_one(meta_dir, meta):
    repo_id = meta["id"]
    source = meta["source"]
    working = meta_dir / "working"

    with tempfile.TemporaryDirectory() as tmp:
        clone_dir = Path(tmp) / "clone"
        subprocess.run(["git", "clone", "--depth", "1", source, str(clone_dir)], check=True)

        # Replace working/ only after the clone has succeeded.
        if working.exists():
            rmtree_force(working)
        shutil.copytree(clone_dir, working, ignore=IGNORE)

        # Git marks pack files read-only, which stops TemporaryDirectory from cleaning up on Windows.
        rmtree_force(clone_dir)

    files = count_files(working)
    rel = working.relative_to(REPO_ROOT).as_posix()
    print(f"{repo_id}: {files} files -> {rel}")
    return files


def main(argv):
    only = argv[1] if len(argv) > 1 else None

    metas = []
    for meta_path in sorted(VIRTUAL_REPOS.glob("*/meta.json")):
        metas.append((meta_path.parent, load_meta(meta_path)))
    metas.sort(key=lambda item: item[1].get("order", 0))

    if only is not None:
        metas = [item for item in metas if item[1]["id"] == only]
        if not metas:
            print(f"error: no virtual-repos/{only}/meta.json found", file=sys.stderr)
            return 2

    failures = 0
    for meta_dir, meta in metas:
        try:
            sync_one(meta_dir, meta)
        except (subprocess.CalledProcessError, OSError) as exc:
            failures += 1
            print(f"{meta['id']}: FAILED - {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
