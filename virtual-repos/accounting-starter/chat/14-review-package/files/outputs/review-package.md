# Review package: CodeCritters trial balance comparison

Status: **draft for review**. This package does not say the work is complete or approved. The controller reviews and approves.

Run covered: controlled test (April YoY), then the full run (YoY Jan to Apr, MoM within 2026). Run evidence is in `evidence/run_log.md`.

## Record counts

| Item | 2025 file | 2026 file |
|---|---|---|
| Source records (accounts) | 32 | 32 |
| Monthly columns | 4 | 4 |
| Processed records (accounts) | 32 | 32 |
| Processed account-months (`data/processed/tb_long.csv`) | 128 | 128 |
| Excluded records | 0 | 0 |
| Reason for exclusions | None excluded | None excluded |

## Control totals, January to April

| Total | 2025 source | 2025 processed | 2026 source | 2026 processed |
|---|---|---|---|---|
| Revenue | 179,870 | 179,870 | 194,420 | 194,420 |
| COGS | 61,800 | 61,800 | 72,700 | 72,700 |
| Expenses | 84,690 | 84,690 | 98,615 | 98,615 |
| Net income | 33,380 | 33,380 | 23,105 | 23,105 |

Balance-sheet columns are month-end balances and are not totaled across months.

## Reconciliation

Assets (less Accumulated Depreciation) equal Liabilities + Equity (less Owner Draws) + YTD net income. The difference is 0.00 in all 8 months (4 per file). Detail: `evidence/reconciliation.md`.

## Data quality

| Check | Result |
|---|---|
| Missing fields | None |
| Duplicate account codes | None |
| Unmapped accounts | None. Account lists identical, joined on Account Code |

## Assumptions used

1. Percent change is measured against the absolute earlier value.
2. The two contra accounts, Accumulated Depreciation and Owner Draws, are subtracted in the reconciliation.
3. A prior value of zero would not be flagged. No account in this data had one.

## Results

- Year over year: 21 flags on 8 accounts.
- Month over month: 7 flags.
- 23 of 32 accounts have no flag.

## Exceptions requiring judgment

| Exception | Why it needs a person |
|---|---|
| The 21 YoY and 7 MoM flags | Each is a question for the reviewer. No cause has been established. |
| Retained Earnings (4 flags) and Accumulated Depreciation (4 flags) | Listed in `plan.md` as expected. The reviewer should confirm. |
| Professional Fees (2 MoM flags) | Labeled recurring: same move in 2025. The reviewer decides if still acceptable. |
| Checking (4 flags), Loan Payable (4 flags) | Not listed as expected in `plan.md`. Needs a reviewer's view. |
| Accounts Receivable, Sales - PyPal, COGS - Materials, Marketing & Advertising | Flagged in both passes. Cause not established. |

## Traceability: one sample

Marketing & Advertising, March, year over year, `outputs/yoy_flags.csv`:

- Source: `data/raw/trial_balance_2026.csv`, account 6030, Mar = 9,800.0.
- Source: `data/raw/trial_balance_2025.csv`, account 6030, Mar = 1,600.0.
- Change = 9,800 - 1,600 = +8,200. Percent = 8,200 / 1,600 = 512.5%.

## Did every step follow the approved plan and AGENTS.md?

| Item | Result |
|---|---|
| Raw files unchanged | Yes. Input file hashes are identical in every run entry. |
| Writes only to `data/processed/`, `outputs/`, `evidence/` | Yes |
| Reconciled before comparing; stopped if not | Yes |
| Separate YoY and MoM passes; no monthly totals | Yes |
| Both bars required to flag | Yes |
| Thresholds read from `plan.md` front matter | **No.** The thresholds are typed in `scripts/tb_compare.py`. The values match `plan.md` today. If `plan.md` changes, the script would not follow. |

## Draft commentary for the controller (unchecked)

1. Net income for January to April fell $10,275 (30.8%), from $33,380 to $23,105.
2. Marketing reached $9,800 in March because of the spring product-launch campaign.
3. Office Supplies' March spike crossed both thresholds.
4. Professional Fees rise every February, in both years.
5. Accounts Receivable rose $9,600 (63.2%) year over year in April, a sign of collection problems.
6. All four revenue lines grew year to date.

## Items requiring human review

- Every claim in the draft commentary above.
- The exceptions table.
- The threshold deviation in the script.
- Whether the full run should be expanded or changed before the controller relies on it.
