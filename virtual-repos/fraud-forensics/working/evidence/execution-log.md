# Execution Log

**A — Allow controlled execution.** What the workflow was permitted to do, and what it actually did.

## Permissions granted (per `plans/approved-plan.md`)

- Read `raw-data/ap-disbursements-h1-2026.csv`. Read-only — no permission to modify the source file.
- Write to `outputs/` and `evidence/` only.
- No network access, no access to any system other than the local workspace files listed above.
- No permission to characterize any transaction, vendor, or person as fraudulent — output is limited to "flagged for investigation."

**What kind of boundary this is — added 2026-09-03, per GPT's readiness review.** All four of the above are *authorized behavior*: `scripts/forensic_review.py` simply contains no code path that writes to `raw-data/`, reaches the network, or emits a fraud label. None of it is *enforced* — there is no OS-level file permission, no sandbox, and no network block in this workspace. A differently-written script could violate every boundary above and nothing here would stop it. For a script this size, reviewing the code is the control. A larger or higher-risk workflow would need an enforced mechanism (a real read-only file permission, a network-denied sandbox), not just a well-written script — see `plan.md` §10's "capability is not authority" for why that distinction matters.

## What actually ran

| Step | Detail |
|---|---|
| Script | `scripts/forensic_review.py` |
| Input read | `raw-data/ap-disbursements-h1-2026.csv` (34 rows) — not modified |
| Outputs written | `outputs/exception-report.csv`, `outputs/summary.md`, `evidence/population-reconciliation.md` |
| Result | 34 rows analyzed, 20 flagged across 8 tests (see `outputs/summary.md`) |
| Characterizations made | None — every flagged row carries only its triggered test name(s), never a conclusion |

## Reproducibility

Re-running `python scripts/forensic_review.py` from the `scripts/` directory against the unmodified source CSV reproduces the same exception count and dollar totals every time — the script contains no randomness and no external calls. This is the reproducibility check called for in `plan.md` §20 Phase 3.
