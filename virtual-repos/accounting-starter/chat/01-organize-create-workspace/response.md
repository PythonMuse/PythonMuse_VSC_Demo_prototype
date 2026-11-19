I read `README.md`, `AGENTS.md`, `plan.md`, `status_update.md`, `backlog.md` and the README in each folder. The workspace structure from the starter template is already in place, so I did not recreate anything. I only logged the setup in `status_update.md`. No accounting data was read or processed, and I added no business rules.

## Folders

| Folder | Purpose |
|---|---|
| `data/raw/` | Original exports for the prepaid review. Read-only for AI. |
| `data/processed/` | Cleaned or intermediate data, reproducible from `data/raw/` plus `scripts/`. |
| `outputs/` | Draft deliverables. Nothing here goes out before human review. |
| `evidence/` | Tie-outs, control totals and validation logs a reviewer can trace back to source. |
| `scripts/` | Reviewed, reusable processing logic. Empty until a test is approved. |
| `skills/` | Reusable procedures, added only once a process proves reusable. |
| `docs/` | Mapping tables, glossaries and longer business-rule notes. |
| `prompts/` | The nine ONBOARD prompts. |

## Files

| File | Purpose |
|---|---|
| `AGENTS.md` | Single source of truth for AI instructions. Still generic. |
| `plan.md` | Assignment, business context and execution plan. Still blank. |
| `status_update.md` | Session log for reconstructing what happened. |
| `backlog.md` | Recommended controls, open questions and deferred scope. |

`CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` are short pointers back to `AGENTS.md`. I left them alone.

A tidy folder structure is not a security control. Keep source data out of `data/raw/` until the agent instructions are approved.

**Changes**

- `status_update.md` — logged this session's workspace review and next steps.
