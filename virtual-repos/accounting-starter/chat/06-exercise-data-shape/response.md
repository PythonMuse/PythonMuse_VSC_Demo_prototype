Several things break, and the worst one fails silently. I tested them with `scripts/join_shape_check.py`. It uses account codes and names only, no amounts.

| Case | Result |
|---|---|
| Join on the export's first column as it is (`1000 · Checking` against `1000`) | 0 of 32 match. Every account looks new or deleted. |
| Split the code from the name, then join on code | 32 of 32 match. |
| Compare by row position when 2026 gains 6095 Software - AI tools mid-list | 10 of 32 rows pair with the wrong prior-year account. No error is raised. |
| Join on code when 2026 gains 6095 | Code 6095 is reported as unmatched, so a human sees it. |

## What the script should do

1. **Stop rather than guess.** If the two files do not have identical account lists, stop with a clear message: "Account lists differ between the two files - cannot compare row-by-row."
2. **Join on account code,** never on row position or on a combined label.
3. **Split code from name** before joining, whatever the export format.
4. **Report unmatched accounts as exceptions** for the reviewer instead of dropping them.

The wrong-pairing case is the dangerous one. A comparison by position still produces numbers, and each looks plausible.

## How ready is your source?

| Source | Readiness |
|---|---|
| Database | Typed and keyed, ready on arrival |
| CSV | Close, but check headers, codes and types |
| Excel | Hidden rows, merged cells, codes stored as text. Needs a skill or a cleanup step |
| PDF | Must be extracted and then proved complete |

I added one item to `backlog.md` so these four rules are built into the comparison script when it is written. I did not build anything beyond the check.

**Changes**

- `scripts/join_shape_check.py` — new.
- `backlog.md` — data-shape items added.
- `status_update.md` — log updated.
