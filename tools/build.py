#!/usr/bin/env python3
"""Build the data bundle the web viewer loads.

Layout (one folder per virtual repo):

  virtual-repos/<id>/
    meta.json   id, order, tabLabel, name, branch, commitMessage, source,
                pipeline (shell-like commands), generated (files/folders)
    working/    snapshot of a real GitHub repo
    chat/       optional, one subfolder per chat step (sorted by name)
      <step>/prompt.md     required; optional "---\\ntitle: ...\\n---" front matter
      <step>/response.md   required
      <step>/files/...     optional; files the step creates/changes
      <step>/step.json     optional: deletes [paths], terminal [{command,output}],
                           block "message", fromPipeline true|false

The STARTING state of a repo is working/ minus everything in meta.generated.
If meta.pipeline is set, it is run in a temp copy of that starting state; the
new or changed files plus the transcript are the "pipeline result", which a
chat step may pull in with "fromPipeline": true.

Output: public/repo-data.js (window.REPOS = [...]) and
public/repo-assets/<id>/ (images: base/ for the starting state,
chat/<step>/ for step files).

Usage:  python tools/build.py   (needs pandas/matplotlib/openpyxl for pipelines)
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS = ROOT / "virtual-repos"
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "repo-assets"
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
SKIP = {".git", "__pycache__", ".DS_Store", ".venv"}
BINARY_NOTE = "(binary file — not shown in this preview)"
MAX_ROWS, MAX_COLS = 200, 30


def load_meta(repo_dir: Path) -> dict:
    return json.loads((repo_dir / "meta.json").read_text(encoding="utf-8"))


def list_files(tree: Path) -> dict[str, Path]:
    """All files under tree as {posix relative path: absolute path}."""
    return {
        p.relative_to(tree).as_posix(): p
        for p in sorted(tree.rglob("*"))
        if p.is_file() and not SKIP.intersection(p.relative_to(tree).parts)
    }


def is_generated(path: str, generated: list[str]) -> bool:
    for g in generated:
        g = g.strip("/")
        if path == g or path.startswith(g + "/"):
            return True
    return False


def read_text(abs_path: Path) -> str | None:
    try:
        text = abs_path.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError:
        return None
    return text.replace("\r\n", "\n")


def _json_value(v):
    if isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, (datetime, date, time)):
        return v.isoformat()
    return str(v)


def read_sheets(abs_path: Path) -> list[dict]:
    """Read an .xlsx into [{name, rows}] with cached values and formulas."""
    from openpyxl import load_workbook  # lazy: only needed when an xlsx exists

    wb_f = load_workbook(abs_path, data_only=False)
    wb_v = load_workbook(abs_path, data_only=True)
    sheets = []
    for ws_f in wb_f.worksheets:
        ws_v = wb_v[ws_f.title]
        n_rows = min(ws_f.max_row or 0, MAX_ROWS)
        n_cols = min(ws_f.max_column or 0, MAX_COLS)
        rows = []
        for r in range(1, n_rows + 1):
            row = []
            for c in range(1, n_cols + 1):
                raw = ws_f.cell(r, c).value
                if raw is None:
                    row.append(None)
                    continue
                is_formula = isinstance(raw, str) and raw.startswith("=")
                cached = ws_v.cell(r, c).value
                cell = {"v": _json_value(cached if cached is not None else raw)}
                if is_formula:
                    cell["f"] = raw
                row.append(cell)
            rows.append(row)
        while rows and all(c is None for c in rows[-1]):
            rows.pop()
        width = max((i + 1 for row in rows for i, c in enumerate(row) if c is not None), default=0)
        sheets.append({"name": ws_f.title, "rows": [row[:width] for row in rows]})
    return sheets


def file_entry(path: str, abs_path: Path, asset_dir: Path, url_prefix: str) -> dict:
    """Describe one file: {path, kind, content | url | sheets}.

    Images are copied to asset_dir/<path> and referenced as url_prefix/<path>.
    """
    suffix = Path(path).suffix.lower()
    if suffix in IMAGE_TYPES:
        dest = asset_dir / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(abs_path, dest)
        return {"path": path, "kind": "image", "url": f"{url_prefix}/{path}"}
    if suffix == ".xlsx":
        return {"path": path, "kind": "sheet", "sheets": read_sheets(abs_path)}
    text = read_text(abs_path)
    return {"path": path, "kind": "text", "content": BINARY_NOTE if text is None else text}


def starting_files(repo_id: str, repo_dir: Path, meta: dict) -> list[dict]:
    working = repo_dir / "working"
    out = []
    for path, abs_path in list_files(working).items():
        if is_generated(path, meta.get("generated", [])):
            continue
        e = file_entry(path, abs_path, ASSETS / repo_id / "base", f"repo-assets/{repo_id}/base")
        value = e.get("content", e.get("url", e.get("sheets")))
        out.append({"path": path, "kind": e["kind"], "status": "", "working": value})
    return sorted(out, key=lambda f: f["path"])


def run_pipeline(repo_dir: Path, meta: dict) -> tuple[list[dict], dict[str, Path], Path | None]:
    """Run meta.pipeline in a temp copy of the starting state.

    Returns (transcript, {path: abs path of new/changed file}, tempdir holder).
    The caller must keep the returned TemporaryDirectory alive while using the
    paths; the third item is that directory object (or None with no pipeline).
    """
    commands = meta.get("pipeline") or []
    if not commands:
        return [], {}, None
    working = repo_dir / "working"
    tmp = tempfile.TemporaryDirectory()
    tree = Path(tmp.name) / "tree"
    shutil.copytree(working, tree, ignore=shutil.ignore_patterns(*SKIP))
    for g in meta.get("generated", []):
        target = tree / g.strip("/")
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
        elif target.exists():
            target.unlink()
    before = {p: a.read_bytes() for p, a in list_files(tree).items()}

    env = dict(os.environ, MPLBACKEND="Agg", PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1",
               PYTHONIOENCODING="utf-8")
    transcript = []
    for command in commands:
        argv = shlex.split(command, posix=True)
        if argv and argv[0] in ("python", "python3"):
            argv[0] = sys.executable
        result = subprocess.run(argv, cwd=tree, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", env=env)
        output = (result.stdout + result.stderr) if result.returncode else result.stdout
        if result.returncode != 0:
            raise RuntimeError(f"Pipeline failed in {meta['id']}: {command}\n{output}")
        output = output.strip()
        # Show paths relative to the repo, the way they'd print in the attendee's own clone.
        for variant in (str(tree), tree.as_posix(), str(tree).replace("\\", "\\\\"), tmp.name,
                        Path(tmp.name).as_posix()):
            for sep in ("\\\\", "\\", "/", ""):
                output = output.replace(variant + sep, "")
        transcript.append({"command": command, "output": output})

    changed = {p: a for p, a in list_files(tree).items()
               if p not in before or a.read_bytes() != before[p]}
    return transcript, changed, tmp


def front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")
    return meta, text[m.end():]


def build_chat(repo_id: str, repo_dir: Path, pipeline: tuple) -> list[dict]:
    chat_dir = repo_dir / "chat"
    if not chat_dir.is_dir():
        return []
    transcript, changed, _tmp = pipeline
    steps = []
    for step_dir in sorted(p for p in chat_dir.iterdir() if p.is_dir()):
        sid = step_dir.name
        raw = (step_dir / "prompt.md").read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        fm, prompt = front_matter(raw)
        prompt = prompt.strip()
        title = fm.get("title")
        if not title:
            first = next((l for l in prompt.splitlines() if l.strip()), "")
            title = first.lstrip("#").strip()[:70]
        response = (step_dir / "response.md").read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()

        asset_dir = ASSETS / repo_id / "chat" / sid
        url_prefix = f"repo-assets/{repo_id}/chat/{sid}"
        files = []
        files_dir = step_dir / "files"
        if files_dir.is_dir():
            files = [file_entry(p, a, asset_dir, url_prefix) for p, a in list_files(files_dir).items()]

        cfg = {}
        if (step_dir / "step.json").exists():
            cfg = json.loads((step_dir / "step.json").read_text(encoding="utf-8-sig"))
        terminal = list(cfg.get("terminal", []))
        if cfg.get("fromPipeline"):
            have = {f["path"] for f in files}
            files += [file_entry(p, a, asset_dir, url_prefix)
                      for p, a in sorted(changed.items()) if p not in have]
            terminal += transcript
        steps.append({"id": sid, "title": title, "prompt": prompt, "response": response,
                      "files": files, "deletes": list(cfg.get("deletes", [])),
                      "terminal": terminal, "block": cfg.get("block")})
    return steps


def build_repo(repo_dir: Path) -> tuple[dict, str]:
    meta = load_meta(repo_dir)
    repo_id = meta["id"]
    shutil.rmtree(ASSETS / repo_id, ignore_errors=True)
    files = starting_files(repo_id, repo_dir, meta)
    pipeline = run_pipeline(repo_dir, meta)
    try:
        chat = build_chat(repo_id, repo_dir, pipeline)
    finally:
        if pipeline[2] is not None:
            pipeline[2].cleanup()
    repo = {"id": repo_id, "tabLabel": meta["tabLabel"], "name": meta["name"],
            "branch": meta["branch"], "commitMessage": meta.get("commitMessage", ""),
            "files": files, "terminal": [], "chat": chat}
    summary = (f"{repo_id}: {len(files)} files, {len(chat)} steps, "
               f"{len(meta.get('pipeline') or [])} pipeline commands")
    return repo, summary, meta.get("order", 0)


def main() -> None:
    for stale in ("head", "working"):
        shutil.rmtree(ASSETS / stale, ignore_errors=True)
    built = []
    for repo_dir in sorted(p for p in REPOS.iterdir() if (p / "meta.json").exists()):
        repo, summary, order = build_repo(repo_dir)
        built.append((order, repo))
        print(summary)
    repos = [r for _, r in sorted(built, key=lambda t: t[0])]
    PUBLIC.mkdir(exist_ok=True)
    out = PUBLIC / "repo-data.js"
    body = json.dumps(repos, ensure_ascii=False, separators=(",", ":"))
    out.write_text("// Generated by tools/build.py. Do not edit by hand.\n"
                   f"window.REPOS = {body};\n", encoding="utf-8")
    print(f"-> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
