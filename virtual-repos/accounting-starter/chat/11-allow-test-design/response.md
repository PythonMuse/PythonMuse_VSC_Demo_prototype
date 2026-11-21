I made the three corrections in `plan.md` and marked it approved for the controlled test only. I have not run anything.

## Corrections applied

| Section | Change |
|---|---|
| Assignment, Materiality thresholds | "or" replaced with "and" for both passes. |
| Execution Plan, Materiality logic | "and" for both passes. The line about determining materiality from context is removed. Thresholds are read from the `plan.md` front matter. |
| Execution Plan, Calculations | No account's monthly columns are totaled. Year over year compares the same month. Balance-sheet accounts use the month-end balance. P&L accounts use that month's activity. |

## Proposed test: reconcile both files, then year over year for April only

| Test requirement | Design |
|---|---|
| Approved data | Both files are synthetic CodeCritters data. The script runs locally. Nothing is sent to a cloud service. |
| One limited portion | The reconciliation of both files for all months, then the YoY pass for April only. No MoM pass. |
| One sample output | `outputs/2026-04-yoy-flags.csv`. |
| Validation evidence | `evidence/reconciliation.md` and a run entry in `evidence/run_log.md`. |
| Stops if a field is missing | Headers are checked and a blank amount stops the run. |
| Stops if totals do not reconcile | Each month must balance with Accumulated Depreciation and Owner Draws subtracted. |

## What to expect

- Both files report a difference of 0 for every month.
- Rows read: 32 and 32, with identical account lists.
- April flags appear only on accounts whose April change clears both bars.
- Check one result by hand against the CSV before moving on.

**Files the test will write.** `scripts/tb_compare.py`, `data/processed/tb_apr_pairs.csv`, `outputs/2026-04-yoy-flags.csv`, `evidence/reconciliation.md`, `evidence/run_log.md`. It reads `data/raw/` and never writes there.

Do you approve this test?

**Changes**

- `plan.md` — corrections applied. Approval line filled in for the controlled test only.
- `status_update.md` — log updated.
