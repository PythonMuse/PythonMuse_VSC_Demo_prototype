"""Clean a raw POS export. Rules: ../references/cleaning-rules.md"""
import sys
from pathlib import Path

import pandas as pd

raw = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw/orders.csv")
out = Path("data/processed")
out.mkdir(parents=True, exist_ok=True)
orders = pd.read_csv(raw, dtype=str)
stores = pd.read_csv("data/raw/stores.csv")

# R1  trim whitespace and fix casing: " UPTOWN" -> "Uptown"
for col in ["store", "category"]:
    orders[col] = orders[col].str.strip().str.title()
# R2  mixed date formats -> ISO dates
dates = pd.to_datetime(orders["order_date"], format="mixed")
orders["order_date"] = dates.dt.date
# R3  "$34.00" -> 34.0
orders["unit_price"] = orders["unit_price"].str.lstrip("$").astype(float)
# R4  a blank qty means a single item
orders["qty"] = orders["qty"].fillna("1").astype(int)
# R5  look up each store's region
clean = orders.merge(stores[["store", "region"]], on="store")

clean["revenue"] = clean["qty"] * clean["unit_price"]
clean.to_csv(out / "orders_clean.csv", index=False, float_format="%.2f")
print(f"{len(orders)} raw rows -> {len(clean)} clean rows")
