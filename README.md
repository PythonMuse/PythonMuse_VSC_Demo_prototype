# code-demo

A read-only, editor-style walkthrough of a small repository, served as a static
web page. It lets people explore a repo with agent skills, pandas scripts and
seaborn charts without installing Git, Python, an editor or an AI assistant.

The page has a file explorer, tabs, syntax highlighting, a Markdown preview, a
CSV table view, a Source Control view with diffs, and a terminal panel showing
the scripts' real output. Nothing in it can be edited or run.

## What is in here

| Path                            | Purpose                                                    |
|---------------------------------|------------------------------------------------------------|
| `virtual-repo/working/`         | The repo people browse. Real, runnable files.              |
| `virtual-repo/head-overrides/`  | Older versions of a few files: the "last commit".          |
| `virtual-repo/meta.json`        | Repo name, branch, commit message, commands to run.        |
| `tools/build.py`                | Runs the scripts and bundles everything for the page.      |
| `public/`                       | The site. `repo-data.js` and `repo-assets/` are generated. |
| `.github/workflows/pages.yml`   | Publishes `public/` to GitHub Pages on each push to main.  |

## How the content is produced

The virtual repo (`store-sales`) holds two skills under `.github/skills/`, each
with a `SKILL.md`, a `references/` folder and a `scripts/` folder. The scripts
clean `data/raw/orders.csv` with pandas, write `data/processed/`, and draw three
seaborn charts into `reports/`.

`tools/build.py` runs that pipeline twice: once on the working tree, and once on
a temporary copy with `head-overrides/` applied. It compares the two results the
way `git status` would, so every "M" and "U" in the Source Control view, every
diff, and the terminal transcript come from real runs.

The story the changes tell: the point-of-sale system exported two orders twice,
which inflated one store's March revenue. The working tree adds a de-duplication
rule to the skill (reference and script), and the regenerated CSVs and charts
show the effect.

## Change the content

1. Edit files under `virtual-repo/working/`. To make a file show up as modified,
   put its previous version at the same path under `virtual-repo/head-overrides/`.
   Files that exist only in `working/` show as untracked.
2. Rebuild:

   ```bash
   pip install -r requirements.txt
   python3 tools/build.py
   ```

3. Commit the result, including `public/repo-data.js` and `public/repo-assets/`.

Code text is sized so a 33-line file fits on screen without scrolling. Keep files
at or under that if "no scrolling" matters; longer files still work and scroll.

## Preview locally

```bash
python3 -m http.server 8000 --directory public
```

Then open http://localhost:8000. Opening `public/index.html` directly also works;
no server is required.

## Publish with GitHub Pages

The site is static files, so GitHub Pages serves it directly. There is nothing to
install and no build step: the generated files in `public/` are committed.

One-time setup: in the repository on GitHub, go to **Settings > Pages** and set
**Source** to **GitHub Actions**.

After that, every push to `main` publishes `public/` (see
`.github/workflows/pages.yml`). The run appears under the **Actions** tab, where it
can also be started by hand. The site is served at
`https://patricktoohey.github.io/code-demo/`.

The repository can stay private (this needs a paid GitHub plan), but the published
site is public: anyone with the address can open it.

## Links you can share

The address updates as you browse, so any view can be linked:

- `/#file=data/raw/orders.csv` opens a file
- `/#diff=reports/monthly_trend.png` opens a change in the diff view
