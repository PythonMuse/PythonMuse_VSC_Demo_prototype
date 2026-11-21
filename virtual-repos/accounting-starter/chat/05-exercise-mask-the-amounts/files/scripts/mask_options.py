"""Masking what-if: which masking choices keep the comparison useful?

Reads data/raw/ locally and prints counts only. The AI sees the results,
never the ledger. Writes the halved copies to data/processed/masked/.

The flag counts use the same rule as the plan: flag only when the dollar
change AND the percent change both clear their bars (percent measured
against the earlier value).
"""
import csv
import math
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed/masked")
MONTHS = ["Jan", "Feb", "Mar", "Apr"]
CONTRAS = {"Accumulated Depreciation", "Owner Draws"}


def load(name):
    with (RAW / name).open(newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def transform(rows, fn):
    out = []
    for r in rows:
        r = dict(r)
        for m in MONTHS:
            r[m] = fn(float(r[m]))
        out.append(r)
    return out


def flags(prior, curr, dollars_yoy, dollars_mom):
    yoy = mom = 0
    for p, c in zip(prior, curr):
        for m in MONTHS:
            a, b = float(p[m]), float(c[m])
            var = b - a
            if a != 0 and abs(var) > dollars_yoy and abs(var / a) > 0.15:
                yoy += 1
        for m1, m2 in zip(MONTHS[:-1], MONTHS[1:]):
            a, b = float(c[m1]), float(c[m2])
            var = b - a
            if a != 0 and abs(var) > dollars_mom and abs(var / a) > 0.20:
                mom += 1
    return yoy, mom


def unbalanced_months(rows):
    bad = 0
    for i, m in enumerate(MONTHS):
        def amt(r, mm):
            v = float(r[mm])
            return -v if r["Account"] in CONTRAS else v
        assets = sum(amt(r, m) for r in rows if r["Type"] == "Asset")
        le = sum(amt(r, m) for r in rows if r["Type"] in ("Liability", "Equity"))
        ni = 0.0
        for mm in MONTHS[: i + 1]:
            ni += sum(float(r[mm]) for r in rows if r["Type"] == "Revenue")
            ni -= sum(float(r[mm]) for r in rows if r["Type"] in ("COGS", "Expense"))
        if abs(assets - (le + ni)) > 0.005:
            bad += 1
    return bad


def round_1000(x):
    return math.floor(x / 1000 + 0.5) * 1000


def write(rows, name):
    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["Account Code", "Account", "Type"] + MONTHS
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] if c not in MONTHS else f"{float(r[c]):.1f}" for c in cols])


p25, p26 = load("trial_balance_2025.csv"), load("trial_balance_2026.csv")
half25 = transform(p25, lambda v: v / 2)
half26 = transform(p26, lambda v: v / 2)
rnd25 = transform(p25, round_1000)
rnd26 = transform(p26, round_1000)

print(f"{'Masking option':<46}{'Months out of balance':>22}{'YoY flags':>11}{'MoM flags':>11}")
cases = [
    ("As received (no masking)", p25, p26, 2500, 2500),
    ("Halve every amount, keep the $2,500 bar", half25, half26, 2500, 2500),
    ("Halve every amount and the bar ($1,250)", half25, half26, 1250, 1250),
    ("Round to the nearest $1,000", rnd25, rnd26, 2500, 2500),
]
for label, a, b, dy, dm in cases:
    yoy, mom = flags(a, b, dy, dm)
    bad = unbalanced_months(a) + unbalanced_months(b)
    print(f"{label:<46}{bad:>14} of 8{yoy:>11}{mom:>11}")

write(half25, "trial_balance_2025_halved.csv")
write(half26, "trial_balance_2026_halved.csv")
print("Wrote data/processed/masked/trial_balance_2025_halved.csv and trial_balance_2026_halved.csv")
