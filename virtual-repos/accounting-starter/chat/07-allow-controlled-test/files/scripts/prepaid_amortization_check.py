"""Controlled test: recompute prepaid amortization and tie to the GL control total.

Synthetic sample data only. Reads data/raw/ (never modified), writes outputs/.
Stops (non-zero exit) if required fields are missing or the schedule does not
tie to the GL control total.
"""
import sys
import pandas as pd

PERIOD_END = "2026-10"          # month being reviewed (YYYY-MM)
GL_CONTROL_TOTAL = 13210.01     # synthetic GL prepaid balance for the test
TOLERANCE = 1.00                # ASSUMPTION: illustrative, pending approval
REQUIRED = ["item_id", "description", "category", "start_month",
            "term_months", "total_amount", "recorded_ending_balance"]

df = pd.read_csv("data/raw/prepaid_schedule_sample.csv")

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    sys.exit(f"STOP: missing required columns: {missing}")

period = pd.Period(PERIOD_END, freq="M")
start = pd.PeriodIndex(df["start_month"], freq="M")
df["months_elapsed"] = [(period - s).n + 1 for s in start]

amortizable = df["term_months"].notna()
df["monthly_amortization"] = (df["total_amount"] / df["term_months"]).round(2)
elapsed = df["months_elapsed"].clip(upper=df["term_months"])
df["expected_ending_balance"] = (
    df["total_amount"] - df["monthly_amortization"] * elapsed
).round(2).where(amortizable)
df["variance"] = (df["recorded_ending_balance"] - df["expected_ending_balance"]).round(2)

def status(row):
    if pd.isna(row["term_months"]):
        return "REVIEW - no amortization term"
    return "REVIEW - variance" if abs(row["variance"]) > TOLERANCE else "OK"

df["status"] = df.apply(status, axis=1)

out_cols = ["item_id", "months_elapsed", "monthly_amortization",
            "recorded_ending_balance", "expected_ending_balance", "variance", "status"]
df[out_cols].to_csv("outputs/amortization_check.csv", index=False)

recorded_total = round(df["recorded_ending_balance"].sum(), 2)
print(f"Rows read: {len(df)}")
print(f"Schedule recorded total: {recorded_total:,.2f}")
print(f"GL control total:        {GL_CONTROL_TOTAL:,.2f}")
print(f"Schedule vs GL difference: {recorded_total - GL_CONTROL_TOTAL:,.2f}")
print(df["status"].value_counts().to_string())
if abs(recorded_total - GL_CONTROL_TOTAL) > 0.005:
    sys.exit("STOP: schedule does not tie to GL control total")
print("Wrote outputs/amortization_check.csv")
