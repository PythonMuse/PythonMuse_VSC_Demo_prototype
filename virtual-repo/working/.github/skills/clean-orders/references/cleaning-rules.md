# Cleaning rules for POS order exports

`scripts/clean_orders.py` applies these in order. Change a rule here first,
then change the script to match.

| Rule | Column          | Problem in the raw file         | Fix                        |
|------|-----------------|---------------------------------|----------------------------|
| R1   | store, category | stray spaces, mixed case        | trim, then Title Case      |
| R2   | order_date      | three different date formats    | parse, write `YYYY-MM-DD`  |
| R3   | unit_price      | some values carry a `$`         | strip it, store a number   |
| R4   | qty             | blank on single-item orders     | fill with `1`              |
| R5   | store           | no region on the order          | join `data/raw/stores.csv` |
| R6   | order_id        | POS can export an order twice   | keep the first copy        |

## Rejected rows

Rows removed by R6 are never dropped silently. They are written to
`data/processed/rejected_rows.csv` with a `reason` column for a person to audit.

## Not handled yet

- Refunds (negative `qty`). None seen so far; stop and ask before guessing.
- Currencies other than USD.
