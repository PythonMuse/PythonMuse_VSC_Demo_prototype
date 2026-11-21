---
name: trial-balance-comparison
description: Compare two trial balances year over year and month over month, flag accounts that clear both a dollar and a percent bar, and write the flags with reconciliation evidence. Use for CodeCritters Inc. style trial balances (Account Code, Account, Type, monthly columns).
---
# Skill: trial-balance-comparison

## When to use

Use when the reviewer asks to run, rerun or extend the trial-balance comparison for CodeCritters Inc.

## When not to use

- A different chart of accounts or a different company, until the account types and contras are documented in `plan.md`.
- A different period range, until `plan.md` and the script are updated.
- Any request to explain causes, post entries or decide whether a variance is acceptable. Those are the reviewer's.

## Inputs

| File | Location | Notes |
|---|---|---|
| Prior-year trial balance | `data/raw/trial_balance_2025.csv` | Read-only. |
| Current-year trial balance | `data/raw/trial_balance_2026.csv` | Read-only. |
| Plan and thresholds | `plan.md` front matter | `yoy_threshold` and `mom_threshold`. |

## Steps

1. Read `plan.md` and `AGENTS.md`. Read the thresholds from the `plan.md` front matter.
2. Confirm both files are present, have the expected headers and have identical account lists. Stop if not.
3. Reconcile every month of both files: Assets (less Accumulated Depreciation) = Liabilities + Equity (less Owner Draws) + YTD net income. Stop if any month does not balance.
4. Classify each account as balance sheet (month-end balance) or P&L (that month's activity). Never total balance-sheet months.
5. Run year over year: same month, 2026 against 2025.
6. Run month over month: sequential months within 2026 only. Keep it separate from step 5.
7. Flag an account only when the dollar change and the percent change both exceed the bars. Measure percent against the absolute earlier value.
8. Label each month-over-month flag that also happened in the same months of 2025 as recurring.
9. Run `python scripts/tb_compare.py --full`.

## Output format

| File | Content |
|---|---|
| `outputs/yoy_flags.csv` | One row per YoY flag with dollar and percent change |
| `outputs/mom_flags.csv` | One row per MoM flag, with the recurring label |
| `outputs/flag_summary.md` | Flags with dollar and percent change together, plus accounts with no flags |
| `evidence/reconciliation.md` | Monthly reconciliation for both files |
| `evidence/run_log.md` | One entry per run: script and plan versions, input hashes, counts |

## Review checklist

- [ ] Both files reconcile in every month, difference 0.
- [ ] Row counts: 32 in, 32 out, 0 excluded.
- [ ] Thresholds in the run log match the `plan.md` front matter.
- [ ] Every flag shows both a dollar and a percent change.
- [ ] Recurring month-over-month flags are labeled.
- [ ] No cause is stated for any flag.
- [ ] `data/raw/` is unchanged (input hashes match the earlier run).
