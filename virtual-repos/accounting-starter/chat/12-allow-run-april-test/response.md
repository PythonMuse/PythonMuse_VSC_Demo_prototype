I wrote `scripts/tb_compare.py` and ran only the approved test: `python scripts/tb_compare.py --month Apr`. It read `data/raw/` and wrote only to `data/processed/`, `outputs/` and `evidence/`. The terminal shows the result.

## Result

| Check | Result |
|---|---|
| 2025 file reconciles | Every month, difference 0 |
| 2026 file reconciles | Every month, difference 0 |
| Rows read, used, excluded | 32 + 32, 32 + 32, 0 |
| Account lists | Identical |
| April YoY flags (more than $2,500 and more than 15%) | 7 |

## The seven April flags

| Account | Basis | Change | % change |
|---|---|---|---|
| 1000 Checking | Month-end balance | +73,435 | 267.7% |
| 1200 Accounts Receivable | Month-end balance | +9,600 | 63.2% |
| 1510 Accumulated Depreciation | Month-end balance | +9,680 | 79.3% |
| 2400 Loan Payable - Equipment | Month-end balance | -4,800 | -28.6% |
| 3100 Retained Earnings | Month-end balance | +89,580 | 179.2% |
| 4000 Sales - PyPal | Month activity | +4,800 | 29.6% |
| 5000 COGS - Materials | Month activity | +4,600 | 47.9% |

Each flag is a question for the reviewer. I have not explained any of them. Five of the seven are balance-sheet accounts.

## Assumptions, exclusions, errors, open questions

- **Assumptions:** percent is measured against the absolute prior-year value. Contras are subtracted in the reconciliation.
- **Exclusions:** none. Everything was used.
- **Errors:** none.
- **Unresolved:** what happens when a prior-year value is zero. The script skips the percent and does not flag, and nothing in this data hit that case.

**Planted mistake (for the exercise):** in `scripts/tb_compare.py` the thresholds are typed into the code, as `if abs(var) > 2500 and abs(pct) > 0.15:` and again for MoM. The approved plan says they are read from the `plan.md` front matter. Ask: who decided this, and where is it written down? The run log records "Source: typed in the script".

**Changes**

- `scripts/tb_compare.py` — new.
- `data/processed/tb_apr_pairs.csv` — new. April 2025 and April 2026 side by side, all 32 accounts.
- `outputs/2026-04-yoy-flags.csv` — new. The seven flags.
- `evidence/reconciliation.md`, `evidence/run_log.md` — new.
- `status_update.md` — log updated.
