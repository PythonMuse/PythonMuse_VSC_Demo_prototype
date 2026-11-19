I read `skills/trial-balance-comparison/SKILL.md` and ran `skills/trial-balance-comparison/scripts/generate_visuals.py`, which is the source of truth for the logic.

**Reconciliation:** passed. Both files reconcile every month, and the Apr 2025 to Jan 2026 roll-forward holds for Retained Earnings, Accumulated Depreciation and Loan Payable.

**Result:** 21 YoY flags and 7 MoM flags. The passes are kept separate. Balance sheet accounts are compared point-in-time and P&L accounts on monthly activity.

An account is flagged only when it clears both bars:

| Pass | Dollar condition | Percent condition |
|---|---|---|
| Year-over-Year (same month, 2026 vs 2025) | more than $2,500 | more than 15% |
| Month-over-Month (2026 only) | more than $2,500 | more than 20% |

Most YoY flags are balance sheet accounts that move by construction: Retained Earnings, Accumulated Depreciation, Loan Payable and Checking. A full year of 2025 activity sits between the two files. That leaves the flags below for a human.

- **COGS - Materials:** Mar +$4,100 (+43.6%) and Apr +$4,600 (+47.9%) YoY. MoM Feb to Mar is +$3,800 (+39.2%).
- **Marketing & Advertising:** Mar +$8,200 (+512.5%), both YoY and MoM. The following month drops $6,600 (-67.3%).
- **Accounts Receivable:** Apr +$9,600 (+63.2%) YoY, and +$8,700 (+54.0%) MoM.
- **Professional Fees:** MoM flags in February and March, but the same February spike appears in 2025. That is recurring, not new, and it is not flagged YoY.
- **Office Supplies:** not flagged. The March spike is +$750 MoM but stays under the $2,500 bar.

Depreciation, Rent, Insurance and Utilities: no flags, either year.

**Changes**

- Created [01_net_income_trend.png](outputs/visuals/01_net_income_trend.png)
- Created [02_yoy_variance_by_account.png](outputs/visuals/02_yoy_variance_by_account.png)
- Created [03_flagged_accounts_trend.png](outputs/visuals/03_flagged_accounts_trend.png)
- Created [CodeCritters_TB_Comparison_Report.xlsx](outputs/excel/CodeCritters_TB_Comparison_Report.xlsx)

Each flag is a question for a reviewer, not a conclusion. *Show me the trace, not the total.*
