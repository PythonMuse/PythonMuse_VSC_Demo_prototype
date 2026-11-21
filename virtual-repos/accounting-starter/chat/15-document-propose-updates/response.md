I reviewed the session and propose seven items. I have not edited any file. Each has one home, so no rule is repeated.

## Proposed updates

| # | Learned | Why the current instructions were not enough | File | Proposed wording or logic | Skill or project only | Written rule enough? |
|---|---|---|---|---|---|---|
| 1 | Thresholds were typed in the script | `plan.md` says the bars live in the front matter, but nothing made the script read them | `scripts/tb_compare.py` | Read `yoy_threshold` and `mom_threshold` from the `plan.md` front matter. Stop if they are missing. | Project | No. See item 5. |
| 2 | Same lesson as 1, as a rule | AGENTS.md has no rule about where thresholds live | `AGENTS.md` section 7 | "Thresholds live in `plan.md`. Never type them into a script or a one-off answer." | Project | Partly. A check in the backlog makes it enforceable. |
| 3 | A prior-year value of zero is never flagged | The plan names it as an open question | `backlog.md` | "Flag any account with no prior-year balance." | Project | No. It needs a script rule. |
| 4 | Nothing stops edits or raw reads of `data/raw/` | "Do not alter raw files" is guidance only | `backlog.md` | Block edits and raw reads of `data/raw/` with a hook, as in the finished YOY repo. | Reusable | No. This needs a technical control. |
| 5 | A check could catch typed thresholds | One typed bar went unnoticed until the checklist | `backlog.md` | "Fail the run if a script types a threshold." | Reusable | No. |
| 6 | Books may not carry over from last year | The balance check proves each month balances, not that last year's closing balances open this year | `backlog.md` | "Roll-forward check: closing balances roll into the next opening balances." | Reusable | No. |
| 7 | The whole procedure | The steps live in chat history | `skills/trial-balance-comparison/SKILL.md` | A skill with front matter, when to use and not to use, inputs, steps, output format and a review checklist. | Reusable | Yes, once the script holds the logic. |

## Already recorded, so no change

- **The contras must be subtracted.** Already in `plan.md` Business Context. The run confirmed it. Repeating it would duplicate the rule.
- **Professional Fees' February spike is recurring.** Already in `plan.md` expected exceptions. The script now labels it.

## For the controller

Checking and Loan Payable flagged in all four months and are not in the expected-exceptions list. I will not add them. That is the controller's decision. I will note the question in `backlog.md`.

Which of these do you approve?
