I read [assignment.md](instructions/assignment.md) and [business-rules.md](instructions/business-rules.md). Nothing has been run. Here is the procedure I propose, which matches [approved-plan.md](plans/approved-plan.md).

**Proposed procedure (13 steps)**

1. Validate and profile the population: row count, date range, total dollars, distinct vendors.
2. Normalize `invoice_number` (strip whitespace and punctuation) as a working column, without altering the source.
3. Test for exact-duplicate invoices (same vendor, invoice number and amount, paid more than once).
4. Test for near-duplicate invoices using the normalized invoice number.
5. Test for payments within $500 of the $10,000 approval threshold.
6. Test for round-dollar amounts (divisible by $500) recurring three or more times to the same vendor.
7. Test for payments dated on a weekend or U.S. bank holiday.
8. Test for vendors created inside the review period, cross-referenced to payment volume.
9. Test for material volume change between the first and second half, measured against the vendor's own first-half activity only.
10. Test for vendors whose `related_party_note` discloses a shared banking relationship. This flags the disclosure; it does not compare GL accounts.
11. Test credit-memo rows for a stated invoice reference.
12. Generate the exception population: one row per flagged transaction, tagged with every test triggered.
13. Reconcile the analyzed population to the source, and separately report the exception subset's own rows and dollars.

**What this plan will not do**

- Label any transaction, vendor or person as fraudulent.
- Resolve ambiguous exceptions, such as the NeuralNest near-duplicate invoices or the BrightPath/Meridian pair. Those go to a human reviewer.
- Exclude any rows. The assignment says "Exclusions: None".
- Use facts the export does not contain, such as bank-account fields or vendor-master history.

**Stop points**

- Before execution, for plan approval.
- Before any exception is characterized. Output ends at "flagged for investigation".

**Writes** would be limited to `outputs/` and `evidence/`. `raw-data/` stays read-only.

Would you approve this plan? What would you add, remove, or change?
