I applied only the seven approved items, then reran the full comparison. The flags did not change.

## What changed

| File | What changed | Why | Effect on the next run |
|---|---|---|---|
| `scripts/tb_compare.py` | Reads `yoy_threshold` and `mom_threshold` from the `plan.md` front matter. Stops if either is missing. The run log now records the source. | The bars were typed in the code, so a change to `plan.md` would have been ignored. | A threshold change in `plan.md` takes effect on the next run. |
| `AGENTS.md` | Section 7, rule 5: thresholds live in `plan.md` and are never typed into a script or a one-off answer. | One written home for the rule. | Future scripts follow it. |
| `backlog.md` | Added: no prior-year balance, typed thresholds check, roll-forward check, and the raw read and edit block. Marked the balance check done. Added the Checking and Loan Payable question for the controller. | Each needs a technical control, not a written rule. | None until built. |
| `skills/trial-balance-comparison/SKILL.md` | New skill with front matter, when to use and not use, inputs, steps, output format and a review checklist. | The procedure no longer depends on chat history. | The comparison can be rerun the same way. |
| `plan.md` | Approval log added. The zero prior-year question is marked as deferred to the backlog. | Records who approved what and when. | None. |

I did not touch the contra and Professional Fees notes in `plan.md`.

## Rerun

| Check | Before | After |
|---|---|---|
| Both files reconcile | Every month, difference 0 | Every month, difference 0 |
| YoY flags | 21 on 8 accounts | 21 on 8 accounts |
| MoM flags | 7 | 7 |
| `outputs/yoy_flags.csv`, `outputs/mom_flags.csv` | | Unchanged |
| Thresholds source in the run log | Typed in the script | `plan.md` front matter |

The only output that changed is `outputs/flag_summary.md`, which now prints the thresholds it used. The run log has a third entry with new script and plan versions. The input hashes are the same as the earlier runs, so `data/raw/` is unchanged.

## Controls still open in `backlog.md`

- Block edits and raw reads of `data/raw/`.
- Scan ingested files for instruction-like text.
- Fail the run if a script types a threshold.
- Flag any account with no prior-year balance.
- Roll-forward check.

**Changes**

- `scripts/tb_compare.py`, `AGENTS.md`, `plan.md`, `backlog.md` — updated.
- `skills/trial-balance-comparison/SKILL.md` — new.
- `outputs/flag_summary.md`, `evidence/run_log.md` — regenerated.
- `status_update.md` — log updated.
