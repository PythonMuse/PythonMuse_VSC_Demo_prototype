---
title: 07 · Allow — Design the smallest test
---
I reviewed the execution plan and the assignment. Before the test, correct `plan.md`:

- Materiality means both bars, as I said in the interview. Replace "or" with "and" in the Assignment section and in the Execution Plan.
- Materiality is mine and the controller's call, not yours. Remove the line about determining materiality from context, and say the thresholds are read from the `plan.md` front matter.
- Do not total the monthly columns of any account. Compare balance-sheet accounts at the same month-end, and P&L accounts month by month.

Then mark the plan as approved by me for the controlled test only.

Review the approved plan and propose the smallest controlled test that can demonstrate whether the workflow logic works correctly.

The test must:

- Use synthetic, masked, or otherwise approved data
- Cover one limited portion of the workflow
- Produce one sample output
- Include validation evidence
- Stop if required fields are missing
- Stop if control totals do not reconcile

Before executing, confirm that the test does not require unmasked sensitive data to be passed to a cloud-based service.

Show me the test design and wait for approval.
