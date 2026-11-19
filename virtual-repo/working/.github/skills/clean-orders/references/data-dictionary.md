# Data dictionary

## data/raw/orders.csv

One row per order, straight from the point-of-sale system.

| Column     | Example            | Notes                           |
|------------|--------------------|---------------------------------|
| order_id   | 1019               | should be unique                |
| order_date | 03/02/2026         | ISO, US, or `Mar 18 2026`       |
| store      | UPTOWN             | free text typed at the register |
| product    | Espresso Roast 2lb |                                 |
| category   | beans              | Beans, Gear, or Merch           |
| qty        |                    | blank means 1                   |
| unit_price | $34.00             | USD, sometimes with the symbol  |

## data/processed/orders_clean.csv

The same columns, cleaned, plus two more.

| Column  | Example | Notes                      |
|---------|---------|----------------------------|
| region  | North   | from `data/raw/stores.csv` |
| revenue | 408.00  | `qty * unit_price`         |

## data/processed/monthly_summary.csv

One row per month and store: `orders`, `units`, `revenue`, `avg_order`.
