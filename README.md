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
| `cloudflare.config.ts`          | Cloudflare config: the Worker name. No server code.        |

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
npm run preview
```

Then open http://localhost:8000. Opening `public/index.html` directly also works;
no server is required.

## Deploy to Cloudflare

This follows the same setup as `spectacle-sandbox`: the `cf` command-line tool and
a `cloudflare.config.ts` file. The difference is that this site is static files
only, so there is no Vite build, no Worker code, no database and no secrets. The
generated files are committed, so a deploy needs no Python either.

| Task | Command |
|---|---|
| Install the tools (once) | `npm install` |
| Check you are signed in to Cloudflare | `npx cf auth whoami` (sign in with `npx cf auth login`) |
| Check a deploy would work, without deploying | `npx cf deploy public --dry-run` |
| Publish `public/` | `npm run deploy` |

The Worker is named `code-demo` in `cloudflare.config.ts`, so on the PythonMuse
account it is served at `https://code-demo.pythonmuse.workers.dev`. Change the
name there to publish under a different address.

## Links you can share

The address updates as you browse, so any view can be linked:

- `/#file=data/raw/orders.csv` opens a file
- `/#diff=reports/monthly_trend.png` opens a change in the diff view
