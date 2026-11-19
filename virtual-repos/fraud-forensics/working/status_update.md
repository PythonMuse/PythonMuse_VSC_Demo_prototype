# Status Update

## 2026-09-23 — Repo scaffolded

- Repo scaffolded from the [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit) structure (`CLAUDE.md`, `plan.md`, `status_update.md`, `.vscode/`, `docs/`, `skills/`, `requirements.txt`), with the ONBOARD workspace folder names (`raw-data/`, `instructions/`, `plans/`, `scripts/`, `outputs/`, `evidence/`, `reviewer-notes/`) kept exactly as used in the source session.
- Demo content copied in from PythonMuse-Training's `data/courses/external/2026-11-13-fraud-forensics-onboard/assets/` (source of truth for the live session remains that repo; this is a packaged, standalone copy):
  - `raw-data/ap-disbursements-h1-2026.csv` — the 34-row source population
  - `instructions/assignment.md`, `business-rules.md`, `validation-requirements.md`
  - `plans/approved-plan.md`
  - `scripts/forensic_review.py` — path constants adjusted for this repo's flat layout (was `assets/scripts/` → `assets/`; now `scripts/` → repo root, same depth, so logic is otherwise unchanged)
  - `outputs/exception-report.csv`, `outputs/summary.md`
  - `evidence/population-reconciliation.md`, `evidence/validation.md`, `evidence/execution-log.md`
  - `reviewer-notes/exception-disposition.md`
  - `docs/ad-hoc-response-synthetic-example.md`
- Added: `README.md`, `CLAUDE.md`, `plan.md` (this file's sibling), `requirements.txt`, `.gitignore`, `.vscode/settings.json` + `extensions.json`, `docs/scenario.md`, `skills/ap-disbursement-fraud-triage/SKILL.md`.
- Licensing set to PythonMuse's standard split (matching `ai-ledger` and the Workflow Kit): `LICENSE` (CC BY-NC-SA 4.0, written content) + `LICENSE-CODE` (MIT, `.py` files). Replaces the single MIT `LICENSE` the repo was created with.

## What was deliberately left out

- **Instructor-only material** — the answer key for this scenario (planted-condition map, expected test/result per condition, scoring rubric) is marked "instructor/presenter use only — do not distribute to participants or post publicly." It is **not** in this repo. It stays in PythonMuse's internal `PythonMuse-Training` repo.
- **Deck-building assets** — `build_deck.py`, `generate_visuals.py`, slide graphics, and animations from the source course folder are presentation-production tooling for the seminar deck itself, not part of the reusable demo workspace. Not copied here.
- **Nothing pushed to `origin` yet.** This repo's remote points at `github.com/PythonMuse/fraud_and_forensics_review_training_repo`. Per PythonMuse's rules of the road, publishing/GitHub changes need co-founder approval — everything above is committed locally only.

## Next steps

All review and confirmations (co-founder review, whether the source `PythonMuse-Training` course folder should link back to this repo) are complete. What's left is testing, done in a fresh clone after the original commit and push:

- Run `python scripts/forensic_review.py` to confirm the packaged version reproduces the checked-in `outputs/` and `evidence/population-reconciliation.md` exactly.
- Try the demo closing prompt in `docs/demo-closing-prompt.md`.
