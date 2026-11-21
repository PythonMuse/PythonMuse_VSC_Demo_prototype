---
workflow: codecritters-tb-comparison
period: 2026-01 to 2026-04
compare_to: 2025-01 to 2025-04
yoy_threshold: { dollars: 5000, percent: 15 }
mom_threshold: { dollars: 5000, percent: 20 }
reviewer: Controller
---
# Project Plan

> Fill this in using `prompts/04-name-the-assignment.md` and `prompts/05-brief-interview-me.md` — don't write it from scratch by hand. Let AI interview you one question at a time, then review its draft before it edits this file.

## Materiality

Flag only when **both** the dollar and the percent bar are cleared.

## Assignment (ONBOARD: Name)

- **Business objective:** Identify which CodeCritters accounts moved enough, year over year and month over month, to need a reviewer's question. Flag and trace only.
- **Reporting period:** January to April 2026 against January to April 2025, month by month. Month over month within 2026 only (Jan to Feb, Feb to Mar, Mar to Apr).
- **Included entities / departments:** CodeCritters Inc. only. No departments or classes.
- **Included accounts:** All 32 accounts in both files.
- **Excluded accounts:** None.
- **Materiality thresholds:** Flag an account only when both the dollar change and the percent change clear the bars in the front matter (`yoy_threshold` and `mom_threshold`). Percent change is measured against the earlier value.
- **Expected output:** A flagged-accounts file in `outputs/`, a reconciliation and tie-out note in `evidence/`, and a short summary giving each flag's dollar and percent change together and naming the accounts with no flags.
- **Intended users:** The controller and the CFO, for the monthly flux review.
- **Reviewer / approver:** The preparer prepares. The controller reviews and approves.
- **Out of scope:** Explaining causes, deciding whether a variance is acceptable, journal entries, budget versus actual, months after April, any change to the source files.

## Business Context (ONBOARD: Brief)

- **What each source report means:** QuickBooks-style trial balance exports, one column per month (Jan to Apr), one row per account. `trial_balance_2025.csv` is the prior year and `trial_balance_2026.csv` is the current year.
- **Period activity vs. ending balances:** Asset, liability and equity columns are month-end balances. Never add them across months. Revenue, COGS and expense columns are that month's activity, not year to date.
- **Account / department mappings:** None needed. Same chart of accounts both years, same order. Join on Account Code.
- **Sign conventions:** Every amount is stored positive on its normal side. Type tells you which side. Two contra accounts are stored positive and must be subtracted: Accumulated Depreciation (from assets) and Owner Draws (from equity). Variance is current minus prior. Percent change is measured against the earlier value.
- **Known exclusions or exceptions:** No exclusions. Expected exceptions: Professional Fees spike every February (annual audit and tax prep), so label that recurring. Retained Earnings differs between years because of year-end close. Accumulated Depreciation grows every month by design.
- **New or discontinued accounts:** None. If the two account lists ever differ, stop and tell the preparer.
- **Reclassifications:** None known.
- **Required tie-outs:** Each trial balance must balance every month: assets net of Accumulated Depreciation equal liabilities plus equity net of Owner Draws plus year-to-date net income. 32 rows in, 32 out. Account lists identical. Recompute a sample of variances by hand.
- **Situations requiring professional judgment:** The cause of any flag. Whether a spike is a miscoding, such as an expense that should have been capitalized. Whether a recurring pattern is still acceptable. Any account where it is unclear whether it is balance sheet or P&L: ask.

## Execution Plan (ONBOARD: Obtain)

*Approved for the controlled test and the full run. Controller review pending.*

- **Required inputs:** `data/raw/trial_balance_2025.csv` and `data/raw/trial_balance_2026.csv`.
- **Expected fields:** Account Code, Account, Type, Jan, Feb, Mar, Apr. Every amount numeric and not blank.
- **Data-preparation steps:** Confirm 32 rows each and identical account codes. Classify each account from its Type as balance sheet or P&L. Save a tidy copy to `data/processed/`.
- **Calculations:** Never total an account's monthly columns. Year over year compares the same month, 2026 against 2025. Month over month compares each month with the previous month within 2026 only. Balance-sheet accounts use the month-end balance. P&L accounts use that month's activity. Variance is current minus prior. Percent is variance divided by the absolute earlier value.
- **Materiality logic:** Flag an account only when both the dollar and the percent bar are cleared, using `yoy_threshold` for year over year and `mom_threshold` for month over month. The bars are read from the `plan.md` front matter, not typed into scripts. Materiality is the reviewer's decision.
- **Mapping procedures:** Join the two years on Account Code. Stop if the account lists differ.
- **Validation checks:** Row counts 32 in, 32 out. Reconcile both files for every month with the two contra accounts subtracted. Recompute a sample of variances.
- **Exception handling:** Flags go to the reviewer. Month-over-month flags are checked against the same months in 2025 and labeled recurring if they match. No explanation of causes.
- **Output files:** `outputs/yoy_flags.csv`, `outputs/mom_flags.csv`, `outputs/flag_summary.md`. Controlled test: `outputs/2026-04-yoy-flags.csv`.
- **Evidence to preserve:** `evidence/reconciliation.md` and a run log.
- **Stop conditions:** A trial balance does not balance, the account lists differ, a field is missing, or an account type is unclear.
- **Open questions / assumptions:** Assumptions: amounts are in dollars with no rounding applied; the percent bars apply to the absolute percent change; both files cover January to April only. Open: what if the prior-year value is zero? The percent cannot be computed, so the account is not flagged. Deferred to `backlog.md`.

---

## Approval log

| Date | What | Approved by |
|---|---|---|
| 2026-12-16 | Execution plan, for the controlled test (April YoY) | Preparer |
| 2026-12-16 | Full run (YoY Jan to Apr, MoM within 2026) | Preparer |
| 2026-12-16 | Dollar bar raised from $2,500 to $5,000 for both passes (percent bars unchanged at 15% and 20%). Controller's materiality decision | Controller |
| Pending | Review of results and flags | Controller |

