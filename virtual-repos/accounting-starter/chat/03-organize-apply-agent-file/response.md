I saved the approved draft to `AGENTS.md`, then reviewed the saved file. I did not build any technical controls.

## Review findings

| Check | Finding |
|---|---|
| Ambiguous language | Section 3 says "sensitive" without defining it. I did not guess. It is logged as an open question in `backlog.md`. |
| Conflicting instructions | None found. Section 2 lets AI save to `outputs/`. Section 3 forbids distributing without review. These do not conflict. |
| Missing stop conditions | Two were missing and are now in Section 5: a trial balance that does not balance, and an unclear account type. |
| Prompt injection | Section 4 covers it. It relies on the AI noticing. See controls below. |
| Rules that rely only on AI compliance | Four, listed below. |

## Recommended controls (added to `backlog.md`, not built)

1. Block edits to `data/raw/`. Today "do not alter raw files" holds only if the AI remembers it and you notice.
2. Keep the raw ledger out of the chat. The kit's hook scans text for SSN, EIN, card and bank-account patterns. It does not stop the AI from reading or editing `data/raw/`.
3. Scan ingested files for instruction-like text.
4. Make the balance check a script that exits, not an instruction.

Controls 1 and 2 are the gap between written guidance and an enforced control. Until they exist, your "Allow" approval is the only thing standing between the AI and `data/raw/`.

No financial data has been added or processed. The project structure exists, raw and processed data have separate folders, and `AGENTS.md` states the role, allowed actions, prohibited actions and stop conditions.

**Changes**

- `AGENTS.md` — role set, trial-balance rules added as Section 7, two stop conditions added.
- `backlog.md` — four recommended controls and two open questions.
- `status_update.md` — log updated.
