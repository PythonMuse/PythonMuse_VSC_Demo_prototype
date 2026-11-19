# Variance Memo: CodeCritters Inc., Jan-Apr 2026 vs 2025

Prepared by Varia. Source: `data/trial_balance_2025.csv` and `data/trial_balance_2026.csv`, via `skills/trial-balance-comparison/scripts/generate_visuals.py`.

## Basis

- Both trial balances reconcile every month (Assets = Liabilities + Equity + YTD Net Income).
- Result: 21 YoY flags and 7 MoM flags.
- A flag requires both a dollar and a percent condition. YoY: more than $2,500 and more than 15%. MoM: more than $2,500 and more than 20%.
- Balance sheet accounts are compared on point-in-time balances. P&L accounts are compared on monthly activity.
- Retained Earnings, Accumulated Depreciation, Loan Payable and Checking are flagged mostly by construction, because a full year of 2025 activity sits between the two files. They are excluded here.
- Each item below is a question for the reviewer, not a conclusion.

## Summary

| # | Account | Period | Prior | Current | $ variance | % variance |
|---|---|---|---|---|---|---|
| 1 | Marketing & Advertising | Mar, YoY | 1,600 | 9,800 | +8,200 | +512.5% |
| 2 | Accounts Receivable | Apr, YoY | 15,200 | 24,800 | +9,600 | +63.2% |
| 3 | COGS - Materials | Apr, YoY | 9,600 | 14,200 | +4,600 | +47.9% |
| 4 | Sales - PyPal | Apr, YoY | 16,200 | 21,000 | +4,800 | +29.6% |
| 5 | Professional Fees | Feb, MoM | 550 | 4,200 | +3,650 | +663.6% |

## 1. Marketing & Advertising

- March 2026 is 9,800 against 1,600 in March 2025: +$8,200 (+512.5%). The MoM figure from February is the same, +$8,200 (+512.5%).
- April falls back to 3,200, a MoM change of -$6,600 (-67.3%).
- Question: is March one campaign, or a miscoded invoice? Check the invoices behind the March balance.

## 2. Accounts Receivable

- AR is a balance, so the comparison is April ending balance to April ending balance: 24,800 against 15,200, +$9,600 (+63.2%).
- MoM from March is +$8,700 (+54.0%). The balance was 16,100 in March and moved in one month.
- Both the dollar and percent conditions are met on both passes.
- Question: which April invoices drove the increase, and is the balance current or past due?

## 3. COGS - Materials

- April 2026 is 14,200 against 9,600: +$4,600 (+47.9%). March is +$4,100 (+43.6%) YoY.
- The step-up came between February and March: +$3,800 (+39.2%) MoM.
- Question: is this vendor price inflation, a volume change, or a one-time purchase? Compare unit costs.

## 4. Sales - PyPal

- April 2026 is 21,000 against 16,200: +$4,800 (+29.6%) YoY. MoM from March is +$4,000 (+23.5%).
- Question: is the April increase related to the April AR increase in item 2? The data shows both moved in the same month. It does not show a link.

## 5. Professional Fees (recurring)

- February 2026 is 4,200 against 550 in January: +$3,650 (+663.6%) MoM. March reverses it by -$3,700 (-88.1%).
- The same February spike appears in 2025 (3,800 against 500 in January), and the account is not flagged YoY. This is a seasonal pattern, not a new finding.
- Question: confirm the February charge is the annual audit or tax engagement.

## Not flagged

- **Office Supplies:** March is 900 against 160 in March 2025 (+$740 YoY) and +$750 MoM. Large in percent, below the $2,500 bar, so not flagged.
- **Depreciation, Rent, Insurance, Utilities:** no flags, either year.

## Next steps for the reviewer

1. Obtain support for items 1 to 3.
2. Review the April AR aging.
3. Record each conclusion and who made it.
