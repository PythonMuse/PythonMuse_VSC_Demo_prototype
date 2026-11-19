# Skill: AP Disbursement Fraud Triage

**Use case:** Screen an accounts-payable disbursement population for defined fraud indicators and produce a reviewer-ready exception report — without characterizing anything as fraudulent.

This is the `scripts/forensic_review.py` workflow in this repo, promoted to a reusable skill per the ONBOARD **D — Document** step: once a workflow is validated, it graduates from a one-off script into something a future session can invoke by name.

## When to use this skill

- You have a transaction-level disbursement (or similar payment) export in CSV form.
- You need a **triage list for human investigation**, not a conclusion.
- You want the result to reconcile: every exception traceable back to source rows, population totals tying out, nothing silently excluded.

## Inputs required

1. **The population** — a CSV with, at minimum: transaction date, vendor identifier, invoice number, payment amount, payment date, approver, GL account, purchase order number, vendor creation date. See `raw-data/ap-disbursements-h1-2026.csv` for the reference shape.
2. **Business rules** — categorical context (approval thresholds, known vendor relationships, payment-method conventions, credit-memo policy) briefed *before* execution. See `instructions/business-rules.md` for the reference shape. Do not brief row-level answers — that defeats the point of a review.
3. **An approved plan** — the specific tests, thresholds, and stopping points, agreed before anything runs. See `plans/approved-plan.md`.

## The nine tests (reference implementation)

1. Exact-duplicate invoices (same vendor, invoice number, amount, paid more than once)
2. Near-duplicate invoices (same vendor/amount, invoice number normalized — whitespace/punctuation stripped)
3. Payments within a defined band of the approval threshold
4. Round-dollar payments recurring 3+ times to the same vendor
5. Weekend/holiday payment timing
6. Vendors created inside the review period, cross-referenced against volume
7. Material volume change between the first and second half of the period (own history only, not external/prior-year)
8. Vendors whose notes disclose a shared banking/remit-to relationship (flags the disclosure for GL-coding review — does not itself confirm anything)
9. Credit-memo rows missing a stated invoice reference

Full logic: `scripts/forensic_review.py`. Adapt thresholds and test definitions to your own population's approved plan — don't reuse these numbers as if they were universal.

## What this skill will not do

- Label any transaction, vendor, or person as fraudulent. Output stops at "flagged for investigation."
- Resolve ambiguous exceptions. Those go to a human reviewer (see `reviewer-notes/exception-disposition.md` for the reference disposition format: closed false positive / closed genuine exception / open pending outside information).
- Assume facts the population doesn't contain (vendor-master history, bank-account fields, etc.) — flag them as open instead.

## How to run it

```bash
python scripts/forensic_review.py
```

Reads the source population read-only; writes only to `outputs/` and `evidence/`. Reproduces identical totals on every run (no randomness, no network calls) — see `evidence/execution-log.md` for the reproducibility check.

## After running

1. Reconcile: does the analyzed row count equal the source row count? Do the exception population's rows and dollars reconcile to what the script actually flagged? (`evidence/population-reconciliation.md`)
2. Disposition every exception — false positive, genuine exception, or open pending outside information. No exception left unaddressed. (`reviewer-notes/exception-disposition.md`)
3. If a test or threshold turns out to need changing, don't edit it silently: review → approve the change → update the controlled instruction (`instructions/` or `plans/`) → rerun.
