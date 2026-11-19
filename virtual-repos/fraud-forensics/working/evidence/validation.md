# Validation Record

Checks each requirement in `instructions/validation-requirements.md` against the actual run of `scripts/forensic_review.py`.

| Requirement | Result |
|---|---|
| Source row count and total dollars | 34 rows, $346,300.00 — see `population-reconciliation.md` |
| Analyzed row count equals source row count | Yes — 34 analyzed, 0 excluded (assignment excludes nothing) |
| Every exception traceable to source row(s) | Yes — `outputs/exception-report.csv` carries `invoice_number` and `vendor_id` for every flagged row |
| Duplicate-detection logic documented | Yes — exact match on (`vendor_id`, `invoice_number`, `payment_amount`); near-duplicate match on the same fields after stripping whitespace/punctuation from `invoice_number` |
| Threshold logic documented | Yes — $10,000 approval threshold, "near" defined as within $500, both stated in `instructions/assignment.md` and implemented as named constants in the script, not hardcoded inline |
| GL-classification check documented | Yes — flags only rows whose note discloses a banking relationship with another vendor (`related_party_note` containing "bank account"), specifically to avoid conflating this test with the unrelated free-text notes on other rows (weekend explanation, credit-memo reference) |
| Every flagged exception carries a disposition | Yes — all 20 exception rows dispositioned in `reviewer-notes/exception-disposition.md`; 2 vendor groups remain explicitly open pending outside information |
| Exception-report totals reconcile to script output | Yes — 20 rows, $286,450.00, matches `outputs/summary.md` |

## One documented limitation

`test_vendor_volume_change()` compares each vendor's first-half-of-period vs. second-half-of-period totals, split at the population's date midpoint (2026-04-06). A vendor with **zero** first-half activity produces an undefined ratio and is excluded from this test by construction — such vendors are covered instead by `test_new_vendor_activity()` if their `vendor_creation_date` falls inside the review period. This is a deliberate design choice (documented here so it isn't mistaken for a gap during review), not an oversight: it avoids double-counting a brand-new vendor as a "volume increase" when the more precise fact is simply "new vendor."
