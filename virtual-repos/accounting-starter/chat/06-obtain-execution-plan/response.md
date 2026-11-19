I read `AGENTS.md`, `plan.md` and `backlog.md`. I added a proposed Execution Plan to `plan.md` and kept the Assignment section from the previous step. I did not process data, write scripts or produce a report. The plan is marked "not approved", and the approval line is still blank.

## Summary of the plan

| Area | Proposal |
|---|---|
| Inputs | October 2026 prepaid schedule export, plus the GL prepaid balance as a single control total supplied by a human. |
| Calculations | Straight-line monthly amortization, months elapsed, expected ending balance, and variance against the recorded balance. |
| Materiality | Flag an item when the absolute variance is over $1.00. |
| Validations | Required fields, duplicate IDs, schedule total equals GL control total, row counts, no negative balances. |
| Exceptions | Items with no term, variances over $1.00 and any failed validation go to a human. AI does not propose entries. |
| Outputs and evidence | `outputs/amortization_check.csv`, `outputs/review-package.md`, and tie-outs in `evidence/`. |

## Assumptions, listed separately

1. Amortization is straight-line, beginning in the month of the start date.
2. The $1.00 threshold is a per-item rounding tolerance.
3. The GL control total is supplied by a human, so AI never reads the GL.

## Open questions

- How should the rent deposit be treated? With no term, it will be flagged, not amortized.
- Which GL account does each category map to? Until this is documented, AI will not map accounts.
- What sign convention applies to balances?

I will not fill these gaps with assumptions. The Business Context section of `plan.md` is still mostly blank, so please confirm that the plan agrees with what you know.

**Changes**

- `plan.md` — added the proposed Execution Plan and kept the approval line blank.

Do you approve this plan, or would you like changes? I will start nothing until you approve.
