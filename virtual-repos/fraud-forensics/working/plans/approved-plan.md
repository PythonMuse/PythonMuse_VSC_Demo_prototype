# Approved Analysis Plan

**O — Obtain and approve the plan.** This is what the AI proposes before any execution is permitted (`plan.md` §10 O-step). The live-session pause point sits right here: *"Would you approve this plan? What would you add, remove, or change?"*

## Proposed procedure

1. Validate and profile the population — row count, date range, total dollars, distinct vendors.
2. Normalize `invoice_number` (strip whitespace and punctuation) as a working column, without altering the source data.
3. Test for exact-duplicate invoices (same vendor, same invoice number, same amount, paid more than once).
4. Test for near-duplicate invoices using the normalized invoice number (catches formatting variants exact-match misses).
5. Test for payments within $500 of the $10,000 approval threshold.
6. Test for round-dollar payment amounts (evenly divisible by $500) recurring three or more times to the same vendor.
7. Test for payments dated on a weekend or a recognized U.S. bank holiday.
8. Test for vendors with a `vendor_creation_date` inside the review period, cross-referenced against their total payment volume.
9. Test for vendors whose volume changes materially between the first and second half of this population, measured against their own first-half activity — not against any external or prior-year history, which this export does not contain. Flagged regardless of whether the vendor is new or established.
10. Test for vendors sharing a `related_party_note` that discloses a connection (such as shared banking details) — flags the disclosure for reviewer follow-up; does not itself compare GL accounts.
11. Test credit-memo rows for a stated invoice reference, and flag any without one.
12. Generate the exception population — one row per flagged transaction, tagged with every test it triggered.
13. Reconcile the *analyzed* population's row count and dollar total back to the source population. Separately report the exception subset's own row count and dollar total — the exception subset will not, and should not, equal the source or analyzed totals.

## What this plan explicitly will not do

- It will not label any transaction, vendor, or person as fraudulent.
- It will not resolve ambiguous exceptions (e.g., the NeuralNest near-duplicate invoices, or the BrightPath/Meridian vendor pair) — those are handed to `reviewer-notes/exception-disposition.md` for human disposition, not decided in the script.

## Approval

Pause point for live discussion: ask the room what they'd add, remove, or change before this plan runs. Two prompts already built into `plan.md` §15's engagement questions: *"Which procedure would you require before approving the forensic analysis plan?"* and (at the Allow step that follows) *"Which change most significantly alters the risk of this workflow?"*
