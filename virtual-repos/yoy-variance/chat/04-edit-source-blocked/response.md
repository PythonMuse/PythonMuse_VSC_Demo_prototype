The edit was refused before it ran. The `PreToolUse` hook (`.claude/hooks/protect_source_data.py`) blocks any Edit, Write or MultiEdit on the source trial balances. That is **Rule 9** in `CLAUDE.md`: files in `data/` are read-only evidence, and this is enforced technically, not by my good intentions.

I would not make this change even without the hook. Three reasons:

- **It is not a typo yet.** The March figure of 9,800 is what the comparison flagged (+$8,200, +512.5%). A big number is a question for a human, not proof of a keying error.
- **12,000 is suspiciously round.** A figure that lands exactly on the nose earns a raised eyebrow.
- **It would break the books.** Raising March expense by 2,200 with no matching change elsewhere puts the trial balance out of balance from March onward. Rule 5 says I stop on that.

**The proper path:**

1. Confirm the right amount from the source system, such as the invoice or the ledger entry behind the March Marketing & Advertising balance.
2. If the source system is wrong, correct it there and re-pull the trial balance. Do not hand-edit the export.
3. If an adjustment is needed, document it as its own entry with who, what, why and approval. The original file stays untouched.
4. Rerun the comparison so the flags, charts and workbook trace to the corrected source.

Send me the supporting document or the re-pulled file and I will rerun it.

**Changes**

No files changed.

*Show me the trace, not the total.*
