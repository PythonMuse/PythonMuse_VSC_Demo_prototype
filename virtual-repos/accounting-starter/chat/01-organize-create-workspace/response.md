I checked the open folder before creating anything. The starter kit already contains the recommended folders and all four starter files, so I did not create or overwrite any of them. I recorded the workflow name, `codecritters-tb-comparison`, at the top of `status_update.md`. I did not read or create any accounting data, and I did not write any business rules.

## Folders

| Folder | Purpose |
|---|---|
| `data/raw/` | Original source files exactly as received. Read-only. |
| `data/processed/` | Anything AI derives from the raw files. It must be reproducible from `data/raw/` plus a script. |
| `outputs/` | Reports and schedules for the reviewer. Nothing here is distributed before a human reviews it. |
| `evidence/` | Tie-outs and validation logs that prove an output is correct. |
| `scripts/` | Reviewed, reusable processing logic. Empty for now. |
| `skills/` | Reusable procedures, one `SKILL.md` per subfolder. Empty for now. |
| `docs/` | Supporting documentation that does not belong in `plan.md`. |
| `prompts/` | The nine starter-kit prompts used in this session. |

## Files

| File | Purpose |
|---|---|
| `AGENTS.md` | The single source of truth for AI instructions: role, allowed and prohibited actions, stop conditions. |
| `CLAUDE.md`, `GEMINI.md` | One-line pointers to `AGENTS.md`, because some tools look for their own filename. |
| `plan.md` | The assignment, the business context and the approved execution plan. Still blank. |
| `status_update.md` | A running log of what was asked, done and left open. |
| `backlog.md` | Recommended technical controls, open questions and deferred scope. |

## What to check

A neat folder structure is not a security control. It makes evidence findable. The agent file and your approvals do the controlling. Confirm that raw and processed data have separate folders and that nothing has been processed yet.

**Changes**

- `status_update.md` — added the session header and the workflow name.
