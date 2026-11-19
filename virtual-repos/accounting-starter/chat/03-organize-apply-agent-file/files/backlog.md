# Backlog

Recommended controls, open questions, and follow-ups surfaced during ONBOARD's Organize, Review, and Document steps. Written instructions in `AGENTS.md` are a starting point, not enforcement — this is where the gap between the two gets tracked until someone closes it.

## Recommended Technical Controls

*(masking scripts, validation hooks, restricted permissions, approved-tool lists, logging — proposed but not yet built)*

- [ ] Make `data/raw/` read-only (file permissions or a pre-commit check) so "do not alter raw files" is enforced, not just instructed.
- [ ] Add a masking script that removes or hashes vendor and bank-related fields before any file is shared with a cloud AI tool.
- [ ] Add a validation script that fails the run if the schedule does not tie to the GL control total, so "do not continue when a tie-out fails" does not depend on AI compliance.
- [ ] Add a pre-run scan of free-text fields (descriptions, notes) for instruction-like language, to support the prompt-injection rule.
- [ ] Keep the sensitive-data hook enabled and test it with a made-up value before each new data set.
- [ ] Log every file AI reads and writes during a run, for reviewer traceability.

## Open Questions

*(ambiguous rules, undocumented mappings, thresholds still awaiting an answer)*

- [ ] Which values count as "sensitive" for this workflow? The instructions currently rely on judgment.
- [ ] Is there a unique canary string to put in `AGENTS.md` Section 6 once real business details are added?

## Deferred Scope

*(things intentionally cut from the current run — a department, a period, an account — with the reason why)*

- [ ]
