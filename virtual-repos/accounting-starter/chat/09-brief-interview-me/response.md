I asked one question at a time, as a new intern would. I did not execute the workflow or open any data. Below is what I understood, then where each item should live. You approved the placements at the end, so I applied them to `plan.md`.

## What I understood

| I asked about | You told me |
|---|---|
| Source reports | QuickBooks-style trial balances: one column per month, one row per account. |
| Activity or balance | Assets, liabilities and equity are month-end balances and are never added across months. Revenue, COGS and expenses are that month's activity. |
| Mappings | None needed. Same chart of accounts and order both years. Join on Account Code. |
| Signs | Everything is stored positive on its normal side. Accumulated Depreciation is subtracted from assets. Owner Draws is subtracted from equity. Variance is current minus prior. |
| Materiality | Already in `plan.md`. |
| Exclusions, new accounts, reclassifications | None. If the account lists differ, stop and tell you. |
| Expected exceptions | Professional Fees spike every February. Retained Earnings differs between years because of year-end close. Accumulated Depreciation grows every month. |
| Tie-outs | Assets net of Accumulated Depreciation equal liabilities plus equity net of Owner Draws plus year-to-date net income, every month. 32 rows in, 32 out. Identical account lists. Recompute a sample of variances. |
| Judgment calls | The cause of any flag, whether a spike is a miscoding, whether a recurring pattern is acceptable, and any account whose type is unclear. |

## Where each item goes, and why

| Item | Location | Why |
|---|---|---|
| Thresholds | `plan.md` front matter and Materiality section (already there) | One home. A person and a script both read it. |
| Contras, signs, balance versus activity | `plan.md` Business Context | Accumulated Depreciation is typed Asset and stored positive, so the data cannot tell me to subtract it. |
| Expected exceptions | `plan.md` Business Context | They are context for the reviewer, specific to this workflow. |
| Tie-outs | `plan.md` Business Context | The execution plan will turn them into validation checks. |
| Judgment calls | `plan.md` Business Context | They tell me when to stop and ask. |

I did not create a mapping file because you said none is needed. I did not repeat any rule that already has a home.

**Changes**

- `plan.md` — Business Context section filled in.
- `status_update.md` — log updated.
