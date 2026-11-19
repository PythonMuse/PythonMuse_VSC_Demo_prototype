---
name: clean-orders
description: >-
  Clean raw point-of-sale order exports into analysis-ready CSVs with pandas.
  Use when asked to clean, fix, tidy, or re-process files in data/raw, or when
  orders look duplicated or malformed.
---

# Clean orders

Turn a messy POS export in `data/raw/` into tidy files in `data/processed/`.

## Steps

1. Read [cleaning-rules.md](references/cleaning-rules.md). The rules there are
   the source of truth.
2. Run the cleaner from the repo root:
   `python .github/skills/clean-orders/scripts/clean_orders.py data/raw/orders.csv`
3. Roll the result up by month and store:
   `python .github/skills/clean-orders/scripts/summarize_orders.py`
4. Compare the row counts the scripts print with the raw file and report them.

## When a rule is missing

Do not patch a CSV by hand. Add the rule to `cleaning-rules.md`, implement it
in `clean_orders.py`, and re-run both scripts so every output is reproducible.

## References

- [cleaning-rules.md](references/cleaning-rules.md): every rule, in order
- [data-dictionary.md](references/data-dictionary.md): columns in each file
