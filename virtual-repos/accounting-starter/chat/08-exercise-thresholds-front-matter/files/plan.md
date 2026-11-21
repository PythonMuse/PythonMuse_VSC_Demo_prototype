---
workflow: codecritters-tb-comparison
period: 2026-01 to 2026-04
compare_to: 2025-01 to 2025-04
yoy_threshold: { dollars: 2500, percent: 15 }
mom_threshold: { dollars: 2500, percent: 20 }
reviewer: Controller
---
# Project Plan

> Fill this in using `prompts/04-name-the-assignment.md` and `prompts/05-brief-interview-me.md` — don't write it from scratch by hand. Let AI interview you one question at a time, then review its draft before it edits this file.

## Materiality

Flag only when **both** the dollar and the percent bar are cleared.

## Assignment (ONBOARD: Name)

- **Business objective:** Identify which CodeCritters accounts moved enough, year over year and month over month, to need a reviewer's question. Flag and trace only.
- **Reporting period:** January to April 2026 against January to April 2025, month by month. Month over month within 2026 only (Jan to Feb, Feb to Mar, Mar to Apr).
- **Included entities / departments:** CodeCritters Inc. only. No departments or classes.
- **Included accounts:** All 32 accounts in both files.
- **Excluded accounts:** None.
- **Materiality thresholds:** Flag an account when the year-over-year change is more than $2,500 or more than 15%. For month over month, flag when the change is more than $2,500 or more than 20%. Percent change is measured against the earlier value.
- **Expected output:** A flagged-accounts file in `outputs/`, a reconciliation and tie-out note in `evidence/`, and a short summary giving each flag's dollar and percent change together and naming the accounts with no flags.
- **Intended users:** The controller and the CFO, for the monthly flux review.
- **Reviewer / approver:** The preparer prepares. The controller reviews and approves.
- **Out of scope:** Explaining causes, deciding whether a variance is acceptable, journal entries, budget versus actual, months after April, any change to the source files.

## Business Context (ONBOARD: Brief)

- **What each source report means:** [ ]
- **Period activity vs. ending balances:** [ ]
- **Account / department mappings:** [ ]
- **Sign conventions:** [ ]
- **Known exclusions or exceptions:** [ ]
- **New or discontinued accounts:** [ ]
- **Reclassifications:** [ ]
- **Required tie-outs:** [ ]

## Execution Plan (ONBOARD: Obtain)

- **Required inputs:** [ ]
- **Expected fields:** [ ]
- **Data-preparation steps:** [ ]
- **Calculations:** [ ]
- **Materiality logic:** [ ]
- **Mapping procedures:** [ ]
- **Validation checks:** [ ]
- **Exception handling:** [ ]
- **Output files:** [ ]
- **Evidence to preserve:** [ ]
- **Stop conditions:** [ ]
- **Open questions / assumptions:** [ ]

---

*Approved by: [ ] on [date]*
