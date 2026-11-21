# Session Status

> Update this at session start, after each major step, at session end, and whenever scope changes. This is the log a reviewer (or you, next month) reads to reconstruct what happened without re-reading every prompt.

---

## Session: 2026-12-16

### Prompt / Task Requested
Year-over-year and month-over-month comparison of CodeCritters Inc. trial balances, January to April 2026 against January to April 2025. Workflow name: `codecritters-tb-comparison`. Synthetic data.

### Plan
1. [x] 01 Organize: confirm the workspace
2. [x] 02 Organize: draft AGENTS.md
3. [x] 03 Organize: apply and check AGENTS.md
4. [x] Add the two trial balances to data/raw/
5. [x] Exercise: masking options
6. [x] Exercise: data shape
7. [x] 04 Name: draft the assignment
8. [x] Exercise: thresholds in plan.md front matter
9. [x] 05 Brief: business context
10. [x] 06 Obtain: execution plan
11. [x] 07 Allow: design the smallest test
12. [x] 07 Allow: run the approved test
13. [x] 07 Allow: full run
14. [x] 08 Review: review package
15. [x] 09 Document: propose updates
16. [x] 09 Document: apply approved updates
17. [x] Exercise: controller raises the dollar bar to $5,000

### Execution Log
- Step 1 - DONE: Workspace `codecritters-tb-comparison` confirmed. Folders and four starter files already exist. No data processed.
- Step 2 - DONE: Draft shown for review. Nothing saved.
- Step 3 - DONE: Approved draft saved to AGENTS.md. Review found 4 controls that rely on AI compliance; added to backlog.md.
- Step 4 - DONE: Files present in data/raw/, headers OK, 32 rows each. Contents not displayed.
- Step 5 - DONE: Masking options compared locally; only counts shown. Halved copies saved in data/processed/masked/.
- Step 6 - DONE: Join checks run on account codes only. Backlog updated.
- Step 7 - DONE: Interview complete. Assignment section written to plan.md.
- Step 8 - DONE: Front matter added to plan.md.
- Step 9 - DONE: Interview complete. Business Context written to plan.md.
- Step 10 - DONE: Execution plan proposed in plan.md. Not approved.
- Step 11 - DONE: Plan corrected and approved. Test design shown; waiting for approval to run.
- Step 12 - DONE: April YoY test run. Both files reconcile. 7 April YoY flags. Script written to scripts/tb_compare.py.
- Step 13 - DONE: Full run approved and executed. 21 YoY flags and 7 MoM flags.
- Step 14 - DONE: Review package written to outputs/review-package.md. Not described as complete or approved.
- Step 15 - DONE: Updates proposed. No files edited.
- Step 16 - DONE: Approved updates applied. Script now reads thresholds from plan.md. Results unchanged: 21 YoY, 7 MoM.
- Step 17 - DONE: Dollar bars changed in plan.md only. Rerun gives 14 YoY and 3 MoM flags.

### Remaining / Next Steps
Nothing pending in this session. Next cycle: apply backlog items.

### Blockers / Notes
- Rules that only work if the AI remembers them are listed in backlog.md as needing a technical control.
- Halving the amounts is only safe if the dollar bar is halved too.
- Join on account code, split from the name; report unmatched accounts as exceptions.
- Plan corrections applied at the reviewer's request: AND logic, thresholds read from plan.md, no summing of balance-sheet months, materiality is the reviewer's call.
