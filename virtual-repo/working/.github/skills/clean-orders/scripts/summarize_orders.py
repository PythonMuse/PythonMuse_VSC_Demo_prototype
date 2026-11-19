"""Roll the clean orders up to one row per month and store."""
import pandas as pd

clean = pd.read_csv("data/processed/orders_clean.csv", parse_dates=["order_date"])
clean["month"] = clean["order_date"].dt.strftime("%Y-%m")

summary = clean.groupby(["month", "store"], as_index=False).agg(
    orders=("order_id", "count"),
    units=("qty", "sum"),
    revenue=("revenue", "sum"),
)
summary["avg_order"] = summary["revenue"] / summary["orders"]

summary.to_csv(
    "data/processed/monthly_summary.csv", index=False, float_format="%.2f"
)
print(summary.round(2).to_string(index=False))
