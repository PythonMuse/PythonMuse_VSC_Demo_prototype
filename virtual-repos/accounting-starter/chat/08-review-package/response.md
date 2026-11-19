I read `AGENTS.md`, `plan.md`, `scripts/prepaid_amortization_check.py`, `data/raw/prepaid_schedule_sample.csv` and `outputs/amortization_check.csv`. I prepared the package in `outputs/review-package.md`. It is a draft for your review, not a conclusion.

## Headline figures (synthetic sample)

| Item | Result |
|---|---|
| Source records | 8 |
| Processed records | 8 |
| Excluded records | 0 |
| Schedule recorded balance total | 13,210.01 |
| GL control total used in the test | 13,210.01 |
| Schedule-to-GL difference | 0.00 |
| Items marked OK | 6 |
| Items needing review | 2 (PP-003 and PP-006) |

## Things you should look at yourself

- **The GL tie-out is weak evidence.** The control total is typed into the script and was set equal to the schedule total, so a zero difference proves nothing independent. A real run needs a control total from the GL.
- **PP-003 has a variance of 200.00.** The numbers show it, but I do not know the cause, and I have not assumed one.
- **PP-006 has no amortization term.** The rent-deposit treatment is still an open question.
- **Rounding.** PP-008 is recorded at 750.01 against a straight-line recompute of 750.01 after rounding the monthly amount to cents. An unrounded calculation would give 750.00. Which convention applies is not documented.
- **Plan deviations.** The script writes only `outputs/amortization_check.csv`. It did not write `data/processed/` or `evidence/` files as the plan describes. I also ran a smoke test on synthetic data before you approved Step 2.

I cannot confirm that every step followed the plan and `AGENTS.md`. The package lists the deviations above. The "validations passed" line in the terminal is not sufficient evidence by itself, so please check the calculations in the CSV.

**Changes**

- `outputs/review-package.md` — new review package draft with a traceability table and a list of items for human review.

Which items would you like me to investigate further, and who should receive this package for review?
