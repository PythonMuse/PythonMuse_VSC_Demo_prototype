# Backlog

Recommended controls, open questions, and follow-ups surfaced during ONBOARD's Organize, Review, and Document steps. Written instructions in `AGENTS.md` are a starting point, not enforcement — this is where the gap between the two gets tracked until someone closes it.

## Recommended Technical Controls

*(masking scripts, validation hooks, restricted permissions, approved-tool lists, logging — proposed but not yet built)*

- [ ] **Block edits and raw reads of `data/raw/`.** Written rules hold only if the AI remembers them. A hook or permission setting should refuse edits to the raw CSVs and refuse reading them into the chat, so scripts read locally and the AI sees only results. The kit's hook scans for SSN-type patterns and does not do this. The finished YOY repo's hook is the example to copy.
- [ ] **Check ingested files for instruction-like text.** Section 4 relies on the AI noticing. A small scan of cell comments and text fields before analysis would make it a check.
- [x] **Make the balance check a script, not a promise.** Done: `scripts/tb_compare.py` reconciles every month and exits if a month does not balance.
- [ ] **Fail the run if a script types a threshold.** `plan.md` is the only home for the bars. A check should flag any dollar or percent bar written into code.
- [ ] **Flag any account with no prior-year balance.** A prior value of zero makes the percent incalculable, so a brand-new account would never be flagged.
- [ ] **Roll-forward check.** The balance check proves each month balances. It does not prove last year's closing balances carry into this year's opening balances. Add a check that does.

## Open Questions

*(ambiguous rules, undocumented mappings, thresholds still awaiting an answer)*

- [ ] "Sensitive" in section 3 is not defined. Decide whether account balances count as sensitive for the approved AI tool.
- [x] Materiality thresholds are defined in the `plan.md` front matter.
- [x] Data shape: the script stops if the account lists differ.
- [ ] Data shape: report unmatched accounts as exceptions, for the case where the lists legitimately differ.
- [ ] Checking and Loan Payable are flagged in all four months and are not listed as expected in `plan.md`. Ask the controller whether they are expected.

## Deferred Scope

*(things intentionally cut from the current run — a department, a period, an account — with the reason why)*

- [ ]
