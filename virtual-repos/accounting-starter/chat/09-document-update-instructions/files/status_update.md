# Session Status

> Update this at session start, after each major step, at session end, and whenever scope changes. This is the log a reviewer (or you, next month) reads to reconstruct what happened without re-reading every prompt.

---

## Session: 2026-11-19

### Prompt / Task Requested
Set up and test a monthly prepaid-expense amortization review (CodeCritters Inc., fictional) using the ONBOARD steps, ending with a controlled test on synthetic data.

### Plan
1. Confirm the workspace and draft `AGENTS.md`.
2. Name the assignment and propose an execution plan in `plan.md`.
3. Run one controlled test on synthetic data and prepare a review package.
4. Document what was learned in the permanent instructions.

### Execution Log
- [09:05] Step 1 — DONE: Confirmed folders and starter files. Nothing recreated.
- [09:20] Step 2 — DONE: Applied the approved role, allowed and prohibited actions, and stop conditions to `AGENTS.md`. Six controls added to `backlog.md`.
- [09:45] Step 3 — DONE: Assignment section drafted in `plan.md`. Business Context partly blank.
- [10:10] Step 4 — DONE: Execution Plan proposed in `plan.md`. Approval line still blank.
- [10:40] Step 5 — DONE: Controlled test on 8 synthetic items. Output in `outputs/amortization_check.csv`. 6 OK, 2 flagged for review.
- [11:05] Step 6 — DONE: Review package drafted in `outputs/review-package.md`. Not approved.
- [11:30] Step 7 — DONE: Instruction updates applied to `AGENTS.md`.

### Remaining / Next Steps
- Controller to review the package and the open items H1 to H7.
- Obtain a real GL control total before any test on real data.
- Update `scripts/prepaid_amortization_check.py` to write `data/processed/` and `evidence/` files.
- Complete the Business Context section of `plan.md`.

### Blockers / Notes
- Learned: the test's GL control total was typed into the script, so the tie-out proved nothing independent. `AGENTS.md` now requires a human-supplied total.
- Learned: the script wrote only to `outputs/`. `AGENTS.md` now requires prepared data and evidence files on every run.
- Learned: items with no term (the rent deposit) are flagged, not amortized. Treatment is an open question.
- Learned: the rounding and start-month conventions are undocumented and pending Controller confirmation.
- The test also ran on synthetic data before Step 2 approval. Future runs should wait for approval.
- No real accounting data has been processed.
