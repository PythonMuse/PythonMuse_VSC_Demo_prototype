I will not open the files, and nothing will be printed. To confirm they are present and the headers match, I wrote a small script, `scripts/check_inputs.py`. It prints only file names, row counts and a header check. It never prints an account name or an amount, so nothing from the ledger enters this conversation.

Result:

| File | Data rows | Columns | Headers |
|---|---|---|---|
| `data/raw/trial_balance_2025.csv` | 32 | 7 | As described |
| `data/raw/trial_balance_2026.csv` | 32 | 7 | As described |

Both files are in `data/raw/`, which stays read-only. Nothing was copied, changed or processed.

**Before any of this data goes to a cloud AI tool, decide whether it may.** The next exercise covers masking.

**Changes**

- `data/raw/trial_balance_2025.csv`, `data/raw/trial_balance_2026.csv` — added by you.
- `scripts/check_inputs.py` — new. Row counts and header check only.
- `status_update.md` — log updated.
