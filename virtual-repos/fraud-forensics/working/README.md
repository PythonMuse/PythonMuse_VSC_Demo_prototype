# Fraud & Forensics Review Training — AP Disbursement Triage Demo

A ready-to-run demo workspace built for PythonMuse's **"AI-Assisted Accounting Workflows: From Prompt to Controlled Process"** session (Fraud & Forensics Seminar, 2026-11-13). It walks the **ONBOARD framework** — Organize, Name, Brief, Obtain, Allow, Review, Document — end to end against a synthetic accounts-payable disbursement population, contrasting one uncontrolled ("ad hoc") prompt against the full controlled workflow.

Built on the [PythonMuse](https://github.com/PythonMuse/ai-ledger) methodology for controlled, repeatable, and audit-ready AI workflows, scaffolded from the [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit).

**Data is entirely synthetic.** CodeCritters Inc. is PythonMuse's standing fictional company (see [`docs/scenario.md`](docs/scenario.md)) — no real client, firm, or vendor data appears anywhere in this repo.

---

## What is inside

This repo layers the Workflow Kit's project-memory conventions (`CLAUDE.md` / `plan.md` / `status_update.md`, `.vscode/`, `docs/`, `skills/`) on top of the **exact ONBOARD workspace folder names used on screen in the session** — `raw-data/`, `instructions/`, `plans/`, `scripts/`, `outputs/`, `evidence/`, `reviewer-notes/`. Those seven folders are not renamed to the kit's generic `data/raw`, `src/`, etc., because matching the names shown live in the seminar is the point of this repo.

```text
fraud_and_forensics_review_training_repo/
  CLAUDE.md                 instructions for AI (rules, data locations, tone, boundaries)
  plan.md                   project blueprint — the ONBOARD demo, step by step
  status_update.md          rolling progress tracker
  requirements.txt          Python dependencies (pandas)

  raw-data/
    ap-disbursements-h1-2026.csv   the 34-row H1 2026 population. Read-only source.

  instructions/              N + B steps
    assignment.md             the scoped assignment (N — Name)
    business-rules.md         context briefed in advance (B — Brief)
    validation-requirements.md  fixed in advance, checked at Review

  plans/
    approved-plan.md          O — Obtain: the proposed procedure, with the live pause point

  scripts/
    forensic_review.py        A — Allow: the controlled execution. Reads raw-data/ read-only;
                               writes only to outputs/ and evidence/.

  outputs/
    exception-report.csv      20 of 34 rows flagged, tagged with every test triggered
    summary.md                exception counts by test

  evidence/
    population-reconciliation.md   population ties out: 34 rows / $346,300.00 in, 20 / $286,450.00 flagged
    validation.md                   every validation-requirements.md item checked against the run
    execution-log.md                R — what the workflow was permitted to do vs. what it actually did
    run-logs/                       (empty by default) drop your own reproduction run's logs here

  reviewer-notes/
    exception-disposition.md  R — Review: the actual disposition of every exception —
                               closed false positive, closed genuine exception, or open pending
                               outside information

  docs/
    scenario.md                       CodeCritters Inc. / Harvey & Jenz CPAs background, source links
    ad-hoc-response-synthetic-example.md   the "before" contrast — a constructed, labeled example of
                                            what an uncontrolled prompt produces against this same
                                            population (see the banner inside for its labeling rules)

  skills/
    ap-disbursement-fraud-triage/
      SKILL.md                 the workflow above, promoted to a reusable, prompt-driven skill
```

**Not included:** an instructor-only answer key exists for this scenario (planted-condition map, expected test/result per condition, scoring rubric) but is deliberately **excluded from this repo**. It's marked "instructor/presenter use only — do not distribute to participants or post publicly," and this repo's remote points at a GitHub org. It stays in PythonMuse's internal working repo.

---

## Requirements

- Python 3.10+

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

## Run the demo

```bash
python scripts/forensic_review.py
```

Reproduces `outputs/exception-report.csv`, `outputs/summary.md`, and `evidence/population-reconciliation.md` from the unmodified source population every time — no randomness, no external calls. Then read `reviewer-notes/exception-disposition.md` to see how a human reviewer actually dispositioned every flagged row.

**Walk the ONBOARD steps in order:** `plan.md` → `instructions/assignment.md` → `instructions/business-rules.md` → `plans/approved-plan.md` (the pause-for-approval point) → `scripts/forensic_review.py` → `outputs/` + `evidence/` → `reviewer-notes/exception-disposition.md`. For the "why does this matter" contrast, read `docs/ad-hoc-response-synthetic-example.md` first.

## Using this with an AI assistant

Point your assistant at `CLAUDE.md` and `plan.md` to start:

> "Read CLAUDE.md and plan.md. Summarize the ONBOARD workflow this repo demonstrates and confirm what's read-only vs. writable."

> "Read skills/ap-disbursement-fraud-triage/SKILL.md and apply it to raw-data/ap-disbursements-h1-2026.csv."

---

## Licensing

This repo follows PythonMuse's standard split license (same as [ai-ledger](https://github.com/PythonMuse/ai-ledger) and the [Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit)):

- **Written content** (docs, instructions, evidence, reviewer notes, scenario material) — [Creative Commons Attribution-NonCommercial-ShareAlike 4.0](LICENSE)
- **Python source code** (`.py` files) — [MIT License](LICENSE-CODE)

## Learn more

- [PythonMuse AI Ledger](https://github.com/PythonMuse/ai-ledger) — practical Python, AI, and automation for accounting and finance teams; source of the underlying methodology
- [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit) — the project template this repo is scaffolded from
- [PythonMuse AI Accounting Framework](https://github.com/PythonMuse/pythonmuse-ai-accounting-framework) — the full learning framework ONBOARD extends
- [Article 19 — When One Agent Is Not Enough](https://github.com/PythonMuse/ai-ledger/tree/main/articles/19-multi-agent-orchestration/) and [Article 11 — From One-Time to Repeatable Workflows](https://github.com/PythonMuse/ai-ledger/tree/main/articles/11-one-time-to-repeatable-workflows/) — related methodology

---

*From [PythonMuse](https://github.com/PythonMuse/ai-ledger) — Practical Python, AI, and automation for accounting and finance teams.*
