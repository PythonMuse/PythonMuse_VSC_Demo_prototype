# Backlog

Recommended controls, open questions, and follow-ups surfaced during ONBOARD's Organize, Review, and Document steps. Written instructions in `AGENTS.md` are a starting point, not enforcement — this is where the gap between the two gets tracked until someone closes it.

## Recommended Technical Controls

*(masking scripts, validation hooks, restricted permissions, approved-tool lists, logging — proposed but not yet built)*

- [ ] **Block edits to `data/raw/`.** AGENTS.md section 3 says "do not alter raw files." Today that works only if the AI remembers it and you notice. A permission setting or hook should refuse writes to `data/raw/`.
- [ ] **Keep the raw ledger out of the chat.** The sensitive-data hook scans text for patterns such as SSNs and card numbers. It does not stop the AI from reading a whole CSV into the conversation. A script should read the data locally so the AI sees only results.
- [ ] **Check ingested files for instruction-like text.** Section 4 relies on the AI noticing. A small scan of cell comments and text fields before analysis would make it a check.
- [ ] **Make the balance check a script, not a promise.** "Stop when reconciliation fails" should be code that exits, not an instruction.

## Open Questions

*(ambiguous rules, undocumented mappings, thresholds still awaiting an answer)*

- [ ] "Sensitive" in section 3 is not defined. Decide whether account balances count as sensitive for the approved AI tool.
- [ ] Materiality thresholds are not yet defined. They come from the assignment step and belong in `plan.md`.

## Deferred Scope

*(things intentionally cut from the current run — a department, a period, an account — with the reason why)*

- [ ]
