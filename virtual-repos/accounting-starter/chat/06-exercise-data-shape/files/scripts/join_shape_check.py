"""Data-shape what-if: what breaks if the export's first column is '1000 · Checking'?

Uses account codes and names only (no amounts). Compares three ways of
lining up the two years' accounts when the 2026 export arrives as
'<code> · <name>' in one column.
"""
import csv
from pathlib import Path

RAW = Path("data/raw")


def load(name):
    with (RAW / name).open(newline="", encoding="utf-8") as f:
        return [(r["Account Code"], r["Account"]) for r in csv.DictReader(f)]


prior = load("trial_balance_2025.csv")
current = load("trial_balance_2026.csv")

# Simulated QuickBooks-style export: code and name in one column.
export = [f"{code} · {name}" for code, name in current]
print(f"Simulated 2026 export, first column, first 3 rows: {export[:3]}")

prior_codes = {code for code, _ in prior}

print("\n1. Join on the export's first column as-is")
matched = sum(1 for key in export if key in prior_codes)
print(f"   Matches: {matched} of {len(export)}   (every account looks new or deleted)")

print("\n2. Split the code from the name, then join on code")
split = [key.split(" · ", 1)[0] for key in export]
matched = sum(1 for code in split if code in prior_codes)
print(f"   Matches: {matched} of {len(export)}")

print("\n3. Compare by row position when 2026 gains one account (6095 Software - AI tools, inserted mid-list)")
shifted = list(current)
shifted.insert(22, ("6095", "Software - AI tools"))
pairs = list(zip(prior, shifted))
wrong = sum(1 for (pc, _), (cc, _) in pairs if pc != cc)
print(f"   Rows paired with the wrong prior-year account: {wrong} of {len(pairs)}   (silent, no error)")
unmatched = sorted(code for code, _ in shifted if code not in prior_codes)
print(f"   Joining on code instead: unmatched accounts to report as exceptions: {unmatched}")

print("\n4. The guard the script needs")
if [c for c, _ in prior] != [c for c, _ in shifted]:
    print("   STOP: Account lists differ between the two files - cannot compare row-by-row.")
