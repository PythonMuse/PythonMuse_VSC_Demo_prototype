# CLAUDE.md

Instructions for AI assistants (Claude, GitHub Copilot, or any other) working in this repository.

## What this repo is

A demo workspace for PythonMuse's Fraud & Forensics Seminar session, walking the **ONBOARD framework** (Organize, Name, Brief, Obtain, Allow, Review, Document) against a synthetic AP disbursement population. See `plan.md` for the full walkthrough and `README.md` for the folder map.

**All data is synthetic.** CodeCritters Inc. is a fictional company; nothing here is real client, firm, or vendor data. Treat it as realistic training material, not as a template to paste real financial data into without masking — see `docs/scenario.md`.

## Rules

- **`raw-data/` is read-only.** Never modify `raw-data/ap-disbursements-h1-2026.csv`. It is the fixed source population everything else ties back to.
- **Writes are scoped to `outputs/` and `evidence/`.** `scripts/forensic_review.py` writes only there. If you're asked to extend the analysis, keep that boundary — don't have a script write back into `raw-data/`, `instructions/`, or `plans/`.
- **Never characterize a transaction, vendor, or person as fraudulent.** The workflow's output stops at "flagged for investigation." That prohibition is stated in `instructions/assignment.md` and is load-bearing for the whole demo — don't soften or drop it when extending the analysis or writing summaries.
- **Don't invent facts the population doesn't contain.** If a question requires vendor-master history, bank-account fields, or anything else not in `raw-data/`, say so and flag it as a matter for human investigation (see `instructions/assignment.md`'s "Matters requiring human judgment") rather than assuming an answer.
- **Read `instructions/` and `plans/approved-plan.md` before proposing changes to the test logic.** The nine tests, their thresholds, and the validation requirements were fixed in advance (the B and O steps) — changing them mid-review defeats the point of the exercise. Propose changes explicitly; don't silently "improve" a test.
- **Reconciliation is not optional.** Any change to `scripts/forensic_review.py` must still reconcile: analyzed row count = source row count, every exception traceable to source rows by `invoice_number`/`vendor_id`, and `evidence/population-reconciliation.md` regenerated and checked, not just the exception report.
- **`docs/ad-hoc-response-synthetic-example.md` is a labeled instructional artifact, not a real AI output.** Its own banner explains why — read it before citing, quoting, or reusing any part of it, and never present it as a captured tool output.
- **No instructor-only material here.** This repo deliberately excludes the answer key used to build/grade this scenario. Don't add planted-condition maps, scoring rubrics, or other presenter-only material to this repo — that lives in PythonMuse's internal working repo.

## Tone

Educational, practical, grounded in real AP/forensic workflows — not fear-based, not implying AI replaces professional judgment or investigator sign-off. Matches PythonMuse's brand voice (see `docs/scenario.md` for the fictional-firm framing this demo uses).

## The three memory files

| File | Purpose | When to update |
|------|---------|-----------------|
| `CLAUDE.md` | This file — rules and constraints | At project start; adjust as needed |
| `plan.md` | Project scope, ONBOARD steps, and what each artifact demonstrates | At project start; revise as scope changes |
| `status_update.md` | Rolling record of what's done, what's outstanding | After each milestone |

## Folder map (quick reference)

Read-only: `raw-data/`
Write-enabled: `outputs/`, `evidence/`, `evidence/run-logs/`, `status_update.md`
Reference only (don't script against, don't silently edit): `instructions/`, `plans/`, `reviewer-notes/`, `docs/`

See `README.md` for the full folder-by-folder description.
