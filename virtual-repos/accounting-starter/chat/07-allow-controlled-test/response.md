I read `AGENTS.md`, `plan.md` and `backlog.md`. Below is the smallest test that exercises the plan's core logic: recompute amortization, compare to the recorded balance, and tie the schedule total to a GL control total.

## Test design

| Element | Proposal |
|---|---|
| Data | `data/raw/prepaid_schedule_sample.csv`: 8 invented items (insurance, software, one rent deposit). No vendor names, account numbers or real amounts. |
| Scope | One period (October 2026), one entity, recompute and tie-out only. |
| Sample output | `outputs/amortization_check.csv`, with one row per item. |
| Validation evidence | Row count, schedule total versus GL control total, and a status for every item. |
| Stops | Required columns missing, or schedule total does not equal the GL control total. |
| Thresholds | $1.00 item variance, as written in `plan.md`. |

## Cloud check

The test uses synthetic data only and runs locally with pandas. No unmasked sensitive data would be sent to a cloud service. The GL control total is a made-up number placed in the script for the test.

## Drafts for your review

I drafted `scripts/prepaid_amortization_check.py` and the sample CSV. Because the data is synthetic, I ran the script once as a smoke test (shown in the terminal). The formal run, including saving files to `data/processed/` and `evidence/`, waits for your approval.

## What I expect you to see

- Six items marked OK. PP-008 differs by a rounding cent and stays within tolerance.
- PP-003 marked for review, with a variance of 200.00. I make no claim about the cause.
- PP-006, the rent deposit, marked for review because it has no amortization term.

These are results of the sample, not conclusions about real balances.

**Changes**

- `scripts/prepaid_amortization_check.py` — draft test script.
- `data/raw/prepaid_schedule_sample.csv` — synthetic sample data.
- `outputs/amortization_check.csv` — sample output from the smoke test.

Do you approve this test design? Please also confirm the $1.00 threshold and the straight-line assumption before I execute Step 2.
