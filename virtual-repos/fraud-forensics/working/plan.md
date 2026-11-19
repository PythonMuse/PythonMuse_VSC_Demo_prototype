# Project Plan — AP Disbursement Fraud Triage (ONBOARD Demo)

## Objective

Demonstrate the **ONBOARD framework** — a workflow-level control layer for AI-assisted accounting and forensic work — end to end, using one worked example: an accounts-payable disbursement triage over a synthetic H1 2026 population for CodeCritters Inc. (see `docs/scenario.md`).

ONBOARD sits *below* entity-level controls (e.g. "which libraries a script may import" is a policy decision made above this framework, not by it) and answers a narrower question: for one AI-assisted task, how do you go from a vague request to a controlled, reviewable, reproducible workflow?

## The seven steps

| Step | Folder / file | What it demonstrates |
|---|---|---|
| **O — Organize** the workspace | This repo's structure (`raw-data/`, `instructions/`, `plans/`, `scripts/`, `outputs/`, `evidence/`, `reviewer-notes/`) | Source preservation, read/write access boundaries, separation of source data from generated outputs |
| **N — Name** the assignment | [`instructions/assignment.md`](instructions/assignment.md) | Replacing "find fraud" with a scoped, defensible assignment: population, period, objective, specific tests, thresholds, output format, exclusions, stopping points, required validations |
| **B — Brief** the AI | [`instructions/business-rules.md`](instructions/business-rules.md) | Categorical institutional context given *before* execution — deliberately not row-level answers, so the exercise still requires investigation |
| **O — Obtain** and approve the plan | [`plans/approved-plan.md`](plans/approved-plan.md) | The AI proposes a procedure; a human pauses to approve, add, remove, or change it before anything runs |
| **A — Allow** controlled execution | [`scripts/forensic_review.py`](scripts/forensic_review.py), [`evidence/execution-log.md`](evidence/execution-log.md) | What the workflow was permitted to do vs. what it actually did. Read-only against the source; writes only to `outputs/` and `evidence/`; no network access; no fraud characterization |
| **R — Review** the work and evidence | [`outputs/`](outputs/), [`evidence/`](evidence/), [`reviewer-notes/exception-disposition.md`](reviewer-notes/exception-disposition.md) | Reconciliation, inspection of every exception, investigation of false positives, identification of genuinely open matters |
| **D — Document** what was learned | This file + `status_update.md` + everything retained in this repo | If investigation reveals a rule should change: **review → approve change → update the controlled instruction → rerun.** The workflow does not silently "learn." |

**Capability is not authority.** `execution-log.md` makes this explicit: the script contains no code path that writes to `raw-data/`, reaches the network, or emits a fraud label — but none of that is *enforced* (no OS-level permission, no sandbox, no network block). For a script this size, code review is the control. A larger or higher-risk workflow needs an actually enforced mechanism, not just a well-written script.

## Source population

- `raw-data/ap-disbursements-h1-2026.csv` — 34 rows, every disbursement processed against a CodeCritters vendor between 2026-01-01 and 2026-06-30, presumed complete for the period (an assumption, not a verified fact — see `instructions/assignment.md`).
- Nine named tests run against it (exact/near-duplicate invoices, near-threshold payments, recurring round-dollar amounts, weekend/holiday timing, new-vendor activity, material volume change, disclosed related-party banking, missing credit-memo reference).
- Result: 20 of 34 rows flagged ($286,450.00 of $346,300.00), across 8 of the 9 tests (the credit-memo reference check runs clean on this population — see `reviewer-notes/exception-disposition.md`'s "reviewed but never flagged" note).

## The before/after contrast

`docs/ad-hoc-response-synthetic-example.md` is a labeled, constructed illustration of what an *uncontrolled* prompt ("Review these disbursements for potential fraud and tell me what looks suspicious") produces against this same population — deliberately outside the seven ONBOARD workspace folders, because that absence is itself the point. It gets several individual facts right and is still unusable as evidence: no stated population, an invented threshold basis, a fabricated motive, a self-authorized exclusion, and a summary total that doesn't reconcile to its own line items. Read it alongside `reviewer-notes/exception-disposition.md` to see the same facts handled with a stated population, named tests, and a reconciled, human-dispositioned result.

## What this workflow explicitly will not do

- It will not label any transaction, vendor, or person as fraudulent — the output is a triage list for investigator review, not a conclusion.
- It will not resolve ambiguous exceptions inside the script. The NeuralNest near-duplicate invoices and the BrightPath/Meridian related-vendor pair are handed to `reviewer-notes/exception-disposition.md` for human disposition, and both remain **open**, pending information (vendor confirmation, vendor-master change log) this population alone cannot supply.

## Status

See `status_update.md` for the current state of this repo. The underlying scenario (dataset, tests, evidence, and reviewer disposition) is complete and reproducible; this repo packages it as a standalone, cloneable demo.
