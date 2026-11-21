I changed the bar in `plan.md` only. I did not touch the script, and I reran the full comparison. In Source Control, open the diff of `plan.md` to see exactly what moved.

## 1. What changed

```
- yoy_threshold: { dollars: 2500, percent: 15 }
- mom_threshold: { dollars: 2500, percent: 20 }
+ yoy_threshold: { dollars: 5000, percent: 15 }
+ mom_threshold: { dollars: 5000, percent: 20 }
```

Only the dollar bars changed, in both passes. The percent bars are the same. The Assignment and Execution Plan paragraphs repeated the old dollar amounts, so I pointed them at the front matter instead of editing the numbers again. A threshold now exists in one place. I also added a line to the approval log.

## 2. What happens to the flags

| Pass | At $2,500 | At $5,000 |
|---|---|---|
| Year over year | 21 | 14 |
| Month over month | 7 | 3 |

**Dropped, year over year (7):** Loan Payable - Equipment in all four months, Sales - PyPal in April, COGS - Materials in March and April.

**Dropped, month over month (4):** Sales - PyPal (Mar to Apr), COGS - Materials (Feb to Mar), and Professional Fees (both moves).

**Still flagged:** Checking in all four months, Accounts Receivable in April, Accumulated Depreciation in all four months, Retained Earnings in all four months and Marketing in March. Month over month: Accounts Receivable (Mar to Apr) and Marketing (Feb to Mar and Mar to Apr).

A higher bar means fewer questions. It also means the reviewer no longer sees the dropped movements at all. That is a materiality decision, which is why it belongs to the controller.

`outputs/yoy_flags.csv`, `outputs/mom_flags.csv` and `outputs/flag_summary.md` were regenerated. `outputs/2026-04-yoy-flags.csv` is from the earlier April test and was not rerun.

## 3. Is the script that ran the one that was approved?

Compare the version recorded in the run log with the version that was approved. `evidence/run_log.md` has an entry for each run with the script's version fingerprint (sha256 `dcd7a0213b3d` in runs 3 and 4), the `plan.md` fingerprint, and the thresholds used. Run 3 and run 4 used the same script, and only the plan changed. If the fingerprint in a run differs from the one on the approval line, the run is not the approved procedure. In a Git repository the commit plays the same role.

## 4. Where is the record of who approved this?

In the commit history and in the `plan.md` approval log: who, when and why. A chat answer is not a record. The log line reads "Controller's materiality decision". Please confirm the date and have the controller confirm the entry.

**Changes**

- `plan.md` — dollar bars changed, two prose lines now point at the front matter, approval log entry added.
- `outputs/yoy_flags.csv`, `outputs/mom_flags.csv`, `outputs/flag_summary.md` — regenerated.
- `evidence/run_log.md` — run 4 added.
- `status_update.md` — log updated.
