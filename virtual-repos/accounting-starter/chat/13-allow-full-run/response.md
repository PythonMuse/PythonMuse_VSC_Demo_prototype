I ran the same script for the full comparison: `python scripts/tb_compare.py --full`. It reconciled both files again before doing anything else. Both reconcile in every month. It then ran year over year for January to April and month over month within 2026 as two separate passes.

## Counts

| Pass | Flags |
|---|---|
| Year over year (more than $2,500 and more than 15%) | 21, on 8 accounts |
| Month over month (more than $2,500 and more than 20%) | 7 |

17 of the 21 YoY flags are on five balance-sheet accounts. Four are on P&L accounts.

## Year over year, by account

| Account | Flagged months | Change |
|---|---|---|
| 1000 Checking | Jan, Feb, Mar, Apr | +94,690, +95,345, +81,930, +73,435 |
| 1200 Accounts Receivable | Apr | +9,600 (63.2%) |
| 1510 Accumulated Depreciation | Jan, Feb, Mar, Apr | +9,620 to +9,680 (98.2% to 79.3%) |
| 2400 Loan Payable - Equipment | Jan, Feb, Mar, Apr | -4,800 each month |
| 3100 Retained Earnings | Jan, Feb, Mar, Apr | +89,580 each month (179.2%) |
| 4000 Sales - PyPal | Apr | +4,800 (29.6%) |
| 5000 COGS - Materials | Mar, Apr | +4,100 (43.6%), +4,600 (47.9%) |
| 6030 Marketing & Advertising | Mar | +8,200 (512.5%) |

## Month over month, 2026

| Account | Months | Change | Recurring in 2025? |
|---|---|---|---|
| 1200 Accounts Receivable | Mar to Apr | +8,700 (54.0%) | No |
| 4000 Sales - PyPal | Mar to Apr | +4,000 (23.5%) | No |
| 5000 COGS - Materials | Feb to Mar | +3,800 (39.2%) | No |
| 6030 Marketing & Advertising | Feb to Mar | +8,200 (512.5%) | No |
| 6030 Marketing & Advertising | Mar to Apr | -6,600 (-67.3%) | No |
| 6060 Professional Fees | Jan to Feb | +3,650 (663.6%) | Yes, +3,300 in 2025 |
| 6060 Professional Fees | Feb to Mar | -3,700 (-88.1%) | Yes, -3,350 in 2025 |

Professional Fees is labeled recurring because the same move happened in the same months of 2025. It is not flagged year over year.

## Accounts with no flags

23 of 32 accounts have no flag in either pass. They include Rent Expense, Utilities, Insurance Expense, Depreciation Expense, Payroll Expense, Software Subscriptions and Office Supplies. The full list is in `outputs/flag_summary.md`.

## Assumptions, exclusions, errors, open questions

- **Assumptions:** the same as the test. Percent is measured against the absolute earlier value.
- **Exclusions:** none. 32 + 32 rows read and used.
- **Errors:** none.
- **Unresolved:** a prior-year value of zero would make the percent incalculable, and the line would not be flagged. No account in this data hit that case.

I have not explained the causes of any flag.

**Changes**

- `data/processed/tb_long.csv` — new. Both years in one tidy file, 256 rows.
- `outputs/yoy_flags.csv`, `outputs/mom_flags.csv`, `outputs/flag_summary.md` — new.
- `evidence/run_log.md` — run 2 added.
- `status_update.md` — log updated.
