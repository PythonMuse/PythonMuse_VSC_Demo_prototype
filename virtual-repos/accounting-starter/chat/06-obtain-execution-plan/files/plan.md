# Project Plan

> Fill this in using `prompts/04-name-the-assignment.md` and `prompts/05-brief-interview-me.md` — don't write it from scratch by hand. Let AI interview you one question at a time, then review its draft before it edits this file.

## Assignment (ONBOARD: Name)

- **Business objective:** Confirm the prepaid balance is correctly amortized and ties to the GL prepaid account.
- **Reporting period:** October 2026 (month ending 2026-10-31).
- **Included entities / departments:** CodeCritters Inc. (fictional), all departments combined.
- **Included accounts:** Prepaid insurance, prepaid software subscriptions, prepaid rent deposit.
- **Excluded accounts:** Items under $500 (expensed at purchase, not on the schedule).
- **Materiality thresholds:** Flag any item variance over $1.00. Any schedule-to-GL difference stops the work.
- **Expected output:** Amortization check file and review package.
- **Intended users:** Controller, staff accountant.
- **Reviewer / approver:** Staff accountant prepares; Controller reviews and approves.
- **Out of scope:** Posting entries, setting amortization policy, vendor payments.

## Business Context (ONBOARD: Brief)

- **What each source report means:** [ ]
- **Period activity vs. ending balances:** [ ]
- **Account / department mappings:** [ ]
- **Sign conventions:** [ ]
- **Known exclusions or exceptions:** [ ]
- **New or discontinued accounts:** [ ]
- **Reclassifications:** [ ]
- **Required tie-outs:** Prepaid schedule ending balance to the GL prepaid account.

## Execution Plan (ONBOARD: Obtain)

*Proposed by AI. Not approved until the signature line below is completed.*

- **Required inputs:** (1) Prepaid schedule export for October 2026. (2) GL prepaid account balance at 2026-10-31 as a single control total.
- **Expected fields:** `item_id`, `description`, `category`, `start_month`, `term_months`, `total_amount`, `recorded_ending_balance`.
- **Data-preparation steps:**
  1. Copy the schedule to a working file. Never edit `data/raw/`.
  2. Check that all expected fields are present.
  3. Check for duplicate `item_id` values and blank required fields.
  4. Write the prepared data to `data/processed/`.
- **Calculations:**
  1. Monthly amortization = `total_amount` / `term_months`, rounded to cents.
  2. Months elapsed = number of months from `start_month` through the period end, counting the start month as month 1.
  3. Expected ending balance = `total_amount` − (monthly amortization × months elapsed, capped at the term).
  4. Variance = `recorded_ending_balance` − expected ending balance.
- **Materiality logic:** Flag an item when the absolute variance exceeds $1.00. Items at or below $1.00 are treated as rounding and reported as OK.
- **Mapping procedures:** Group items by `category` (insurance, software, deposit). The category-to-GL-account mapping is not yet documented, so AI will not map items to accounts.
- **Validation checks:**
  1. Required fields present.
  2. No duplicate `item_id`.
  3. Schedule ending-balance total equals the GL control total.
  4. Row counts agree between source and output.
  5. No negative expected balances.
- **Exception handling:** Items with no `term_months`, items with a variance over $1.00, and any failed validation are listed for human review. AI does not decide the cause or propose entries.
- **Output files:** `data/processed/` for the prepared data, `outputs/amortization_check.csv`, and `outputs/review-package.md`.
- **Evidence to preserve:** The tie-out of schedule total to GL control total, the validation log, the script version used, and row counts, all in `evidence/`.
- **Stop conditions:** Any condition in `AGENTS.md` Section 5, in particular a missing required field or a schedule-to-GL difference.
- **Open questions / assumptions:**
  1. ASSUMPTION: Amortization is straight-line, starting in the month of the start date. Needs Controller confirmation.
  2. ASSUMPTION: The $1.00 threshold is a rounding tolerance for each item, not an escalation threshold.
  3. ASSUMPTION: The GL control total is supplied by a human. AI does not read the GL.
  4. QUESTION: How should the rent deposit be treated? It has no amortization term, so it will be flagged for review.
  5. QUESTION: Which GL account does each category map to?
  6. QUESTION: What is the expected sign convention for balances?

---

*Approved by: [ ] on [date]*
