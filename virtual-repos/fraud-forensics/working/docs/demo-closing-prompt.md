# Demo closing prompt — "how Claude runs this"

Use this at the end of the ONBOARD walkthrough, after the room has seen
`instructions/`, `plans/approved-plan.md`, and the before/after contrast in
`docs/ad-hoc-response-synthetic-example.md`. Paste it into a fresh Claude
Code session opened at the repo root.

Update the date in the output filename before pasting if you're running
this on a different day than 2026-09-23.

---

Read `skills/ap-disbursement-fraud-triage/SKILL.md`, then run
`scripts/forensic_review.py` per its "How to run it" section. Confirm the
reconciled row count and dollar totals match
`evidence/population-reconciliation.md`, run `git status` to confirm
nothing outside `evidence/run-logs/` changed, and write a short run record
(what you read first, what you ran, the reconciliation numbers, and the
`git status` result) to
`evidence/run-logs/2026-09-23-live-demo-run.md`.

---

## What this is designed to show

- Claude reads the skill and the approved plan before acting — not a fresh,
  unscoped analysis.
- It runs the existing controlled script rather than reasoning its own way
  to an exception list.
- The regenerated `outputs/` and `evidence/population-reconciliation.md`
  are byte-identical to what's already checked in — `git status` should
  show clean except for the new file in `evidence/run-logs/`, which is
  gitignored.
- The only new artifact is the run record itself, so there's nothing to
  reconcile against or conflict with.

## If you want to reset between rehearsals

`evidence/run-logs/` is gitignored, so anything Claude writes there during
a test run won't show up in `git status` or need to be cleaned up before
committing. Delete the file manually between rehearsals if you don't want
stale run records lying around locally.
