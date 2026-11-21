I read `AGENTS.md`, `plan.md` and `backlog.md`, then added a proposed Execution Plan to `plan.md`. It is marked "not yet approved" and the approval line is still blank. I did not process data, write scripts or produce a report.

## The plan

| Area | Proposal |
|---|---|
| Required inputs | `data/raw/trial_balance_2025.csv` and `data/raw/trial_balance_2026.csv`. |
| Expected fields | Account Code, Account, Type, Jan, Feb, Mar, Apr. Every amount numeric and not blank. |
| Data preparation | Confirm 32 rows each and identical account codes. Classify each account from its Type as balance sheet or P&L. Save a tidy copy to `data/processed/`. |
| Calculations | For each account, total the monthly columns for 2025 and for 2026 and compare the totals. Then compare each month with the previous month within 2026. Variance is current minus prior. Percent is variance divided by the earlier value. |
| Materiality logic | Flag accounts over $2,500 or 15% for year over year, and over $2,500 or 20% for month over month. I'll determine which variances are material based on context. |
| Mapping | Join the two years on Account Code. Stop if the account lists differ. |
| Validation | Row counts 32 in, 32 out. Reconcile both files for every month with the two contra accounts subtracted. Recompute a sample of variances. |
| Exception handling | Flags go to the reviewer. Month-over-month flags are checked against the same months in 2025 and labeled recurring if they match. I do not explain causes. |
| Output files | `outputs/yoy_flags.csv`, `outputs/mom_flags.csv`, `outputs/flag_summary.md`. |
| Evidence | `evidence/reconciliation.md` and a run log. |
| Stop conditions | A trial balance does not balance, the account lists differ, a field is missing, or an account type is unclear. |

Writes go only to `data/processed/`, `outputs/` and `evidence/`. `data/raw/` is never touched.

## Assumptions, listed separately

1. Amounts are in dollars and have no rounding applied.
2. The percent bars apply to the absolute percent change.
3. Both files cover January to April only.

## Open questions

- What if the prior-year value is zero? The percent cannot be computed.
- Should the first run be limited to one month as a test?

Do you approve this plan, or would you like changes? I will not start until you approve.

**Planted mistakes (for the exercise):**

1. Materiality says "over $2,500 or 15%". The assignment says both bars. With "or" the comparison flags 29 YoY and 16 MoM lines instead of 21 and 7.
2. "I'll determine which variances are material based on context." Materiality is the reviewer's call, and it is already written in `plan.md`.
3. "Total each account's monthly columns and compare the totals." That adds up balance-sheet snapshots. Checking would show 65,155 in 2025 against 410,555 in 2026, which is meaningless.

**Changes**

- `plan.md` — proposed Execution Plan added, not approved.
- `status_update.md` — log updated.
