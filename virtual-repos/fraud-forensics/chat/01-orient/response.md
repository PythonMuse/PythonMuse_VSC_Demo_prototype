I read [CLAUDE.md](CLAUDE.md) and [plan.md](plan.md). This repo walks the **ONBOARD** framework against a synthetic 34-row H1 2026 AP disbursement population for CodeCritters Inc. Each step maps to a specific artifact:

| Step | Artifact | What it does |
|---|---|---|
| **O**rganize | Folder structure (`raw-data/`, `instructions/`, `plans/`, `scripts/`, `outputs/`, `evidence/`, `reviewer-notes/`) | Separates source data from generated outputs and sets access boundaries |
| **N**ame | [assignment.md](instructions/assignment.md) | Replaces "find fraud" with a scoped assignment: population, period, nine tests, thresholds, stopping points |
| **B**rief | [business-rules.md](instructions/business-rules.md) | Categorical context given before execution, not row-level answers |
| **O**btain | [approved-plan.md](plans/approved-plan.md) | The proposed procedure, with a human approval pause before anything runs |
| **A**llow | [forensic_review.py](scripts/forensic_review.py) and [execution-log.md](evidence/execution-log.md) | Controlled execution: what the workflow was permitted to do vs. what it did |
| **R**eview | [outputs/](outputs/), [evidence/](evidence/), [exception-disposition.md](reviewer-notes/exception-disposition.md) | Reconciliation and a human disposition of every exception |
| **D**ocument | `plan.md`, `status_update.md` | Rule changes go review, approve, update the instruction, rerun. The workflow does not silently "learn". |

**Read-only:** `raw-data/ap-disbursements-h1-2026.csv`.

**Writable:** `outputs/`, `evidence/`, `evidence/run-logs/` and `status_update.md`.

**Reference only** (do not script against or silently edit): `instructions/`, `plans/`, `reviewer-notes/`, `docs/`.

**Rules I will follow from CLAUDE.md:**

- Never characterize a transaction, vendor or person as fraudulent. Output stops at "flagged for investigation".
- Do not invent facts the population does not contain, such as vendor-master history or bank-account fields.
- Do not change test logic or thresholds silently. Propose changes explicitly.
- Any script change must still reconcile: analyzed rows equal source rows, and `evidence/population-reconciliation.md` is regenerated.
- Treat `docs/ad-hoc-response-synthetic-example.md` as a labeled teaching artifact, not a real AI output.

One caveat from [execution-log.md](evidence/execution-log.md): the read-only and no-network boundaries are authorized behavior, not enforced by the OS. For a script this size, code review is the control.

No files were changed.
