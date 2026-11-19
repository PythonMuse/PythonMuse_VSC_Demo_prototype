# Validation Requirements

What the **Review** step must check before anyone relies on the exception report (`plan.md` §10 R-step). This list is fixed in advance, at Brief/Obtain time — Review is not the moment to decide what counts as validated.

- Source row count and total dollars (34 rows; sum of `payment_amount`, including the one negative credit-memo row).
- Analyzed row count equals source row count (no rows silently dropped — this assignment excludes nothing, see `instructions/assignment.md`).
- Every exception traceable back to specific source row(s) by `invoice_number` and `vendor_id`.
- Duplicate-detection logic documented as exact-match vs. normalized near-duplicate, with the normalization rule stated (strip whitespace and punctuation from `invoice_number` before comparing).
- Threshold logic documented: the $10,000 approval threshold and the "within $500" near-threshold definition, both stated in `instructions/assignment.md`, not implicit in the script.
- GL-classification check documented: which GL account each vendor's payments were coded to, and whether that's consistent across payments to related vendors.
- Every flagged exception carries a disposition in `reviewer-notes/exception-disposition.md` — false positive (with explanation), or open/requires further investigation. No exception is left unaddressed.
- Total dollars and row count in `outputs/exception-report.csv` reconcile to the sum of all rows the script actually flagged — see `evidence/population-reconciliation.md`.
