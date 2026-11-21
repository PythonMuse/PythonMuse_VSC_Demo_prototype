---
title: 05 · Brief — Let AI interview you
---
Act as a new accounting intern preparing to perform this assignment.

Ask me one question at a time to identify the business and accounting context needed to complete it correctly.

Cover:

- The meaning of each source report
- Period activity versus ending balances
- Account and department mappings
- Sign conventions
- Materiality rules
- Known exclusions
- New or discontinued accounts
- Reclassifications
- Expected exceptions
- Required tie-outs
- Situations requiring professional judgment

Do not execute the workflow.

Use my answers to propose updates to `plan.md`, `docs/`, a mapping file, or another appropriate project file.

Explain why each item belongs in the recommended location and wait for my approval.

My answers, in the order you will ask (this data is synthetic, so I can be specific):

1. QuickBooks-style trial balance exports, one column per month, one row per account.
2. Asset, liability and equity columns are month-end balances. Never add them across months. Revenue, COGS and expense columns are that month's activity, not year to date.
3. None needed. Same chart of accounts both years, same order. Join on Account Code.
4. Everything is stored positive on its normal side. Type tells you which side. Two contras are stored positive and must be subtracted: Accumulated Depreciation from assets, Owner Draws from equity. Variance is current minus prior.
5. Same as the assignment. Keep it in one place, `plan.md`.
6. None.
7. None. If the account lists ever differ, stop and tell me.
8. None known.
9. Professional Fees spike every February for the annual audit and tax prep, so label that recurring. Retained Earnings changes between years because of year-end close. Accumulated Depreciation grows every month by design.
10. Each trial balance must balance every month: assets net of Accumulated Depreciation equal liabilities plus equity net of Owner Draws plus year-to-date net income. Thirty-two rows in, thirty-two out. Account lists identical. Recompute a sample of variances.
11. The cause of any flag. Whether a spike is a miscoding, such as an expense that should have been capitalized. Whether a recurring pattern is still acceptable. Any account where it is unclear whether it is balance sheet or P&L: ask.
