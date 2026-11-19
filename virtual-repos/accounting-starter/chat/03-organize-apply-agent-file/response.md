I read `AGENTS.md`, `backlog.md` and the draft you approved. I applied it to `AGENTS.md`, keeping the six-section structure, the safety rules, the prompt-injection section and the stop conditions. Then I reviewed the result.

## Review findings

| Area | Finding | Action |
|---|---|---|
| Ambiguous language | "Sensitive data" is not defined. | Added to `backlog.md` as an open question. |
| Conflicting instructions | None found. | None. |
| Missing stop conditions | No stop for a failed GL tie-out or a prepaid item with no term. | Added both to Section 5. |
| Prompt injection | Free-text fields such as descriptions were not named as ingested content. | Added a line to Section 4. |
| Compliance-only rules | Raw-file protection, masking, tie-out enforcement and injection scanning depend on AI behavior alone. | Listed as controls in `backlog.md`. |

The Section 6 canary is still the template placeholder. I did not invent a string for you.

I did not build any technical controls. No accounting data was read or processed.

**Changes**

- `AGENTS.md` — filled in the role for the prepaid review, added the two stop conditions and the free-text-field line.
- `backlog.md` — added six recommended controls and two open questions for your review.

Please review the backlog items and tell me which ones to keep, change or drop.
