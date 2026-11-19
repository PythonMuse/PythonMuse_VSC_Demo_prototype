# Review Package — Controlled Test: Prepaid Amortization Check

**Entity:** CodeCritters Inc. (fictional)
**Period tested:** October 2026 (month ending 2026-10-31)
**Data:** Synthetic sample, `data/raw/prepaid_schedule_sample.csv`
**Status:** DRAFT for human review. This package does not state that the work is complete or approved.

## 1. Record counts

| Measure | Count | Notes |
|---|---|---|
| Source records | 8 | Rows in the sample CSV. |
| Processed records | 8 | Rows in `outputs/amortization_check.csv`. |
| Excluded records | 0 | No rows excluded. |

## 2. Control totals and reconciliation

| Measure | Amount |
|---|---|
| Source total cost (`total_amount`) | 21,460.00 |
| Source recorded ending balance | 13,210.01 |
| Processed recorded ending balance | 13,210.01 |
| GL control total used in the test | 13,210.01 |
| Schedule vs GL difference | 0.00 |
| Recorded vs recomputed balance, amortizable items only (7 items) | 200.00 |

The GL control total is hard-coded in the script and equals the schedule total. It is not an independent figure from the GL. See item H1 below.

## 3. Data quality checks

| Check | Result |
|---|---|
| Missing fields | `term_months` is blank for PP-006. No other blanks. |
| Duplicate `item_id` | None found. |
| Unmapped accounts or departments | Not tested. No category-to-GL-account mapping is documented in `plan.md` or `docs/`. |

## 4. Assumptions used

1. Straight-line amortization, with the start month counted as month 1.
2. Monthly amortization is rounded to cents before multiplying by months elapsed.
3. The $1.00 threshold applies per item.
4. The GL control total is supplied by a human. In this test it was typed into the script.

None of these assumptions has been confirmed by the Controller.

## 5. Traceability

Each output row maps to the source row with the same `item_id`. Columns are `monthly_amortization = total_amount / term_months`, `expected_ending_balance = total_amount − monthly_amortization × months_elapsed`, `variance = recorded − expected`.

| item_id | Source row | Recorded | Expected | Variance | Status |
|---|---|---|---|---|---|
| PP-001 | 1 | 4,800.00 | 4,800.00 | 0.00 | OK |
| PP-002 | 2 | 1,200.00 | 1,200.00 | 0.00 | OK |
| PP-003 | 3 | 1,400.00 | 1,200.00 | 200.00 | REVIEW - variance |
| PP-004 | 4 | 1,650.00 | 1,650.00 | 0.00 | OK |
| PP-005 | 5 | 200.00 | 200.00 | 0.00 | OK |
| PP-006 | 6 | 3,000.00 | n/a | n/a | REVIEW - no amortization term |
| PP-007 | 7 | 210.00 | 210.00 | 0.00 | OK |
| PP-008 | 8 | 750.01 | 750.01 | 0.00 | OK |

## 6. Exceptions requiring judgment

- **PP-003 (software):** recorded balance is 200.00 higher than the recompute. The cause is unknown. No explanation has been assumed.
- **PP-006 (rent deposit):** no amortization term. Whether the deposit should be amortized, held as a deposit or reclassified is an accounting judgment.

## 7. Conformance to the plan and `AGENTS.md`

| Requirement | Observed |
|---|---|
| Raw file not modified | The script only reads `data/raw/`. Confirm with a file comparison. |
| Only the approved sample processed | Yes, 8 synthetic rows. |
| Stop on missing fields and tie-out failure | Both stops are coded. Neither was triggered. |
| Write prepared data to `data/processed/` | Not done. The script writes only to `outputs/`. |
| Preserve evidence in `evidence/` | Not done. Only terminal output exists. |
| Wait for approval before executing | A smoke test on synthetic data ran before Step 2 approval. |

## 8. Items requiring human review

- **H1:** Replace the hard-coded GL control total with a figure supplied from the GL.
- **H2:** Investigate the 200.00 variance on PP-003.
- **H3:** Decide the treatment of the PP-006 rent deposit.
- **H4:** Confirm the straight-line method, the start-month convention and the rounding convention.
- **H5:** Confirm the $1.00 threshold.
- **H6:** Decide whether the missing `data/processed/` and `evidence/` outputs should be added to the script.
- **H7:** Recalculate a few rows by hand against the CSV.
