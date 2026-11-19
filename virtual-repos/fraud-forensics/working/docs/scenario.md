# Scenario background — CodeCritters Inc.

All data in this repo is synthetic. This page gives just enough background to make the scenario legible; it does not reproduce PythonMuse's full internal story bible, which covers other characters, videos, and scenarios not used here.

## The fictional company

**CodeCritters Inc.** sells premium AI-themed desk fidgets across three product lines, including the TensorTurtle line referenced in `instructions/business-rules.md`. The vendor-cost-inflation detail behind SiliconSerpent Supply Co, QuantumCoil Materials, and NeuralNest Components continues a real finding from a published PythonMuse article rather than inventing an unrelated story — see [Article 01: AI Co-Pilot for Accounting](https://github.com/PythonMuse/ai-ledger/tree/main/articles/01-ai-copilot-for-accounting) on [ai-ledger](https://github.com/PythonMuse/ai-ledger).

## The fictional review

**Harvey & Jenz CPAs** — a fictional outsourced-accounting/advisory firm — is performing the AP disbursement triage in this repo on CodeCritters' behalf. **Devraj Bose** (manager) and **Maya Ortiz** reviewed and dispositioned every exception (see `reviewer-notes/exception-disposition.md`).

## Why this matters for how you use this repo

CodeCritters is cast as **the client** of the fictional firm doing the review, not as the learner's own employer. That framing is deliberate: CodeCritters' data is the kind of client information that would need protecting in a real engagement (never pasted into an unapproved AI tool, etc.), even though here it's entirely fictional and safe to use freely.

**If you adapt this workflow to real client or company data:** mask sensitive fields first, state materiality and the review period explicitly, and don't let an AI assistant silently assume thresholds, GL mappings, or vendor relationships the way `instructions/business-rules.md` deliberately spells them out here. See `CLAUDE.md` for the rules this repo itself follows.

## Source material

- [PythonMuse AI Ledger](https://github.com/PythonMuse/ai-ledger) — the articles this scenario draws from
- [PythonMuse AI Accounting Framework](https://github.com/PythonMuse/pythonmuse-ai-accounting-framework) — the broader framework ONBOARD extends
- [PythonMuse Workflow Kit](https://github.com/PythonMuse/pythonmuse-workflow-kit) — the project scaffolding this repo is built on
