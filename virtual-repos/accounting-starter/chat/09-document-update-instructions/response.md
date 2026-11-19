I read `AGENTS.md`, `plan.md`, `backlog.md`, `status_update.md` and `outputs/review-package.md`. I applied only the updates you approved. Each rule lives in one place, `AGENTS.md`, so it is not duplicated elsewhere.

## What changed and why

| File | Change | Why | Effect on next run |
|---|---|---|---|
| `AGENTS.md` Section 2 | The GL control total must be human-supplied and recorded in `evidence/`. | The test's control total was typed into the script, so the tie-out was not independent. | AI must ask for the total instead of embedding it. |
| `AGENTS.md` Section 2 | Every run writes prepared data and evidence files. | The script wrote only to `outputs/`. | A reviewer gets files, not terminal text. |
| `AGENTS.md` Section 3 | Do not amortize items with no documented term. Flag them. | The rent deposit had no term. | The deposit stays flagged until you decide. |
| `AGENTS.md` Section 5 | Two new stops: a non-independent control total, and an undocumented rounding or start-month convention. | Both surfaced in review. | AI stops and asks, not assumes. |
| `AGENTS.md`, new project section | Working conventions: straight-line, start month is month 1, round monthly to cents, $1.00 threshold. | They were assumptions. | Marked pending Controller confirmation. |
| `status_update.md` | Logged the session, the learnings and next steps. | A reviewer can reconstruct what happened. | None. |

## What did not change

- `plan.md` is unchanged. The approval line stays blank until you sign it.
- No script was updated. Fixing the script to write `data/processed/` and `evidence/` is a technical control, so it stays in `backlog.md`.

## Controls still in `backlog.md`

- Read-only `data/raw/`.
- Masking script for vendor and bank-related fields.
- A validation script that fails when the tie-out fails.
- A pre-run scan of free-text fields for instruction-like language.
- Logging of every file read and written.

The written rules guide behavior but are not enforcement. The validation script is the most useful next control.

**Changes**

- `AGENTS.md` — five instruction updates and a project-specific section.
- `status_update.md` — session log with learnings and next steps.

Once the Controller confirms the conventions, expand one step at a time, for example one more period, and review again.
