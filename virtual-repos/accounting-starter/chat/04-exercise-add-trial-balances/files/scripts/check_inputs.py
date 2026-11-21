"""Confirm the input files exist and have the expected headers.

Prints file names, row counts and header status only. It never prints
account names or amounts, so nothing sensitive reaches the chat.
"""
import csv
from pathlib import Path

RAW = Path("data/raw")
EXPECTED = ["Account Code", "Account", "Type", "Jan", "Feb", "Mar", "Apr"]
FILES = ["trial_balance_2025.csv", "trial_balance_2026.csv"]

for name in FILES:
    path = RAW / name
    if not path.exists():
        raise SystemExit(f"STOP: {path} is missing.")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = sum(1 for _ in reader)
    status = "headers OK" if header == EXPECTED else "HEADERS DIFFER: " + ", ".join(header)
    print(f"{path.as_posix()}: {rows} data rows, {len(header)} columns, {status}")
