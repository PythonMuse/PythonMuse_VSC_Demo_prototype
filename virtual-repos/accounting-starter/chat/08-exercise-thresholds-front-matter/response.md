Done. I added the block exactly as written. The front matter is at the very top of `plan.md`, and the Materiality section sits below the page title.

## Why this matters

- A person reads the sentence: "Flag only when **both** the dollar and the percent bar are cleared."
- A script reads the front matter: `yoy_threshold` and `mom_threshold`.

It is one file with one source for each threshold. That way the threshold is not typed into a script, where a reviewer would never see it.

## How the front matter reads

| Key | Value |
|---|---|
| `workflow` | `codecritters-tb-comparison` |
| `period` | 2026-01 to 2026-04 |
| `compare_to` | 2025-01 to 2025-04 |
| `yoy_threshold` | $2,500 and 15% |
| `mom_threshold` | $2,500 and 20% |
| `reviewer` | Controller |

I did not change anything else in the file and did not read any data.

**Changes**

- `plan.md` — front matter and Materiality section added.
- `status_update.md` — log updated.
