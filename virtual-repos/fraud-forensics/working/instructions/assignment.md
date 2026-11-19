# Assignment — AP Disbursement Fraud Triage, H1 2026

**N — Name the assignment.** This is the ONBOARD demo's naming artifact, replacing the vague request "find fraud" with a scoped, defensible assignment (`plan.md` §10 N-step).

## The assignment

> Analyze the January 1 – June 30, 2026 CodeCritters Inc. accounts-payable disbursement population for defined fraud indicators, and produce an exception population for investigator review. **Do not characterize any transaction, vendor, or individual as fraudulent.** The output is a triage list requiring human investigation, not a conclusion.

## Population

- **Source:** `assets/raw-data/ap-disbursements-h1-2026.csv`, 34 rows — every disbursement processed against a CodeCritters vendor between 2026-01-01 and 2026-06-30, exported directly from the AP subledger. Treated as read-only.
- **Completeness:** The population is presumed complete for the period defined above. This is an assumption, not a verified fact — see Validation, below.

## Objective

Identify transactions or patterns that warrant investigator attention, using the nine specific tests listed below — not open-ended anomaly detection.

## Specific tests (see `plans/approved-plan.md` for the full, approved procedure)

1. Exact duplicate invoices
2. Near-duplicate invoice numbers (normalized)
3. Payments clustered near the approval threshold
4. Round-dollar payment frequency
5. Weekend/holiday payment timing
6. New vendors created inside the review period
7. Material volume change between the first and second half of the period
8. Vendors whose `related_party_note` **discloses** a shared banking relationship — flagged for a reviewer to check GL coding consistency
9. Credit memo rows carrying a stated invoice reference

**What tests 8 and 9 do and do not establish.** Both are rule-based checks against fields that exist in this export, and both stop short of confirmation:

- **Test 8 reads a disclosure, it does not compare GL accounts.** This population contains no bank-account or remit-to address fields. What it contains is a narrative `related_party_note` in which a shared banking relationship was already disclosed by whoever prepared the export. The automated test finds that disclosure — nothing more. Whether the vendors involved are actually coded to different GL accounts is something a human reviewer checks by looking at the flagged rows, the same way test 9's reference is checked for correct application. **Independently confirming that two vendors share a payment destination requires vendor-master evidence this population does not include.**
- **Test 9 confirms a reference is present, not that it is correct.** It checks whether a credit memo row states an invoice reference. It does not verify that the referenced invoice exists, or that the credit was applied to it. Both of those are confirmed in human review — see `reviewer-notes/exception-disposition.md`.

## Materiality / thresholds

- **Approval threshold:** $10,000 per disbursement (see `business-rules.md`). "Near threshold" is defined as within $500 of this limit.
- No dollar-materiality floor is applied below which a row is excluded from testing — this is a triage exercise, not a financial-statement materiality review, so small-dollar rows are tested on the same basis as large ones.

## Output format

- `outputs/exception-report.csv` — one row per flagged transaction, with the specific test(s) it triggered.
- `outputs/summary.md` — population counts, exception counts by test, and a plain-language description of each flagged group (not a conclusion).

## Exclusions

None. Every row in the source population is in scope for every applicable test.

## Stopping points

The workflow **stops and requires human approval before execution** at the plan-approval step (`plans/approved-plan.md`) — see the **Obtain** step. It also stops before any exception is characterized: the workflow's output ends at "flagged for investigation," never at "fraud" or "not fraud."

## Required validations

- Source row count and total dollars reconcile to the analyzed population (see `evidence/population-reconciliation.md`).
- Every exception is traceable back to its source row(s).
- Test logic (especially invoice-number normalization) is documented, not just executed.

## Matters requiring human judgment

- Whether any flagged item rises from "red flag" to "finding."
- Disposition of the two vendors whose note discloses a shared banking relationship and which are coded to different GL accounts (BrightPath Fulfillment Services / Meridian Pack & Fulfillment LLC). The population alone cannot establish who created these vendor records, nor independently confirm the shared payment destination — both require the vendor-master change log and vendor-master banking detail, which are outside this export.
- Whether the near-duplicate NeuralNest Components invoices represent a duplicate payment, a legitimate resubmission, or something else.
- Whether each credit memo was applied to the invoice it names. Test 9 confirms only that a reference is stated.
