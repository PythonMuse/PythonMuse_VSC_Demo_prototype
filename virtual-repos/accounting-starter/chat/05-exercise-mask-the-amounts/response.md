Not as they are. Under `AGENTS.md` section 3, unmasked financial data does not go to a cloud tool. That includes me reading the file into this chat. I ran the four options locally with `scripts/mask_options.py`. It read `data/raw/` on your machine and printed only counts.

| Masking option | Months out of balance (of 8) | YoY flags | MoM flags |
|---|---|---|---|
| No masking | 0 | 21 | 7 |
| Halve every amount, keep the $2,500 bar | 0 | 14 | 3 |
| Halve every amount and the bar ($1,250) | 0 | 21 | 7 |
| Round to the nearest $1,000 | 6 | 21 | 8 |

## What each option does to the analysis

| Option | Keeps the analysis useful? | Why |
|---|---|---|
| Rename product lines (PyPal to Product A) | Yes | Names do not drive any calculation. |
| Halve every amount, keep the $2,500 bar | No | Percentages survive but dollar tests change: 14 YoY flags instead of 21, and 3 MoM instead of 7. |
| Halve every amount and the bar | Yes | Identical result, 21 and 7. Scaling is only safe if the threshold scales with it. |
| Round to the nearest $1,000 | No | The trial balance stops balancing in 6 of 8 months, so the workflow must stop. The MoM count also changes, 8 instead of 7. |
| Drop the account codes | No | The two years can no longer be joined on a key. The next exercise shows why that matters. |
| Keep it local: a script reads the data and the AI sees only results | Yes | The raw ledger never enters the AI's context. This is also the strongest control. |

Masking is a control decision, not formatting. Whether a masked file is safe depends on what the analysis needs to stay true. Note that a halved file is still a client's data at half size. Check whether your policy treats scaled amounts as masked.

I saved the halved copies for the exercise. They are derived data, so they are in `data/processed/masked/`. `data/raw/` is untouched.

**Changes**

- `scripts/mask_options.py` — new. Local comparison, counts only.
- `data/processed/masked/trial_balance_2025_halved.csv`, `trial_balance_2026_halved.csv` — new.
- `status_update.md` — log updated.
