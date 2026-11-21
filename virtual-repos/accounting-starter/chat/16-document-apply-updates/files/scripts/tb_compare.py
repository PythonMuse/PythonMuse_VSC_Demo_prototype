"""Trial balance comparison for CodeCritters Inc.: year over year (YoY) and month over month (MoM).

Reads  data/raw/        (read-only)
Writes data/processed/, outputs/, evidence/

Usage
  python scripts/tb_compare.py --month Apr   approved controlled test: reconcile both files, YoY for April only
  python scripts/tb_compare.py --full        full run: YoY for Jan-Apr, MoM for Jan->Feb, Feb->Mar, Mar->Apr

Method (see plan.md)
  1. Check that both files have the same accounts, then reconcile every month. Stop if not.
  2. Classify each account: balance sheet (month-end balance) or P&L (that month's activity).
     Balance-sheet columns are never added across months.
  3. Variance = current minus prior. Percent = variance / |prior|.
  4. Flag only when the dollar change AND the percent change both clear the bar.
     The bars are read from the plan.md front matter. They are not typed in this file.
"""
import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
OUTPUTS = Path("outputs")
EVIDENCE = Path("evidence")
PLAN = Path("plan.md")
FILE_2025 = RAW / "trial_balance_2025.csv"
FILE_2026 = RAW / "trial_balance_2026.csv"

MONTHS = ["Jan", "Feb", "Mar", "Apr"]
COLUMNS = ["Account Code", "Account", "Type"] + MONTHS
FLOW_TYPES = {"Revenue", "COGS", "Expense"}          # P&L: monthly activity
CONTRAS = {"Accumulated Depreciation", "Owner Draws"}  # stored positive, subtracted


# ---------------------------------------------------------------- load / check
def read_thresholds(path=PLAN):
    """Read yoy_threshold and mom_threshold from the plan.md front matter.

    Returns ((yoy_dollars, yoy_pct), (mom_dollars, mom_pct)), with pct as a fraction.
    """
    text = path.read_text(encoding="utf-8")
    parts = text.split("---")
    if not text.startswith("---") or len(parts) < 3:
        sys.exit("STOP: plan.md has no front matter, so the thresholds cannot be read.")
    found = []
    for key in ("yoy_threshold", "mom_threshold"):
        m = re.search(rf"^{key}:\s*\{{\s*dollars:\s*([\d.]+)\s*,\s*percent:\s*([\d.]+)\s*\}}",
                      parts[1], re.M)
        if not m:
            sys.exit(f"STOP: {key} is missing from the plan.md front matter.")
        found.append((float(m.group(1)), float(m.group(2)) / 100))
    return found[0], found[1]


def bar_text(bar):
    return f"> ${bar[0]:,.0f} and > {bar[1] * 100:g}%"


def load_tb(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            sys.exit(f"STOP: {path.name} headers are {reader.fieldnames}, expected {COLUMNS}")
        rows = []
        for r in reader:
            for m in MONTHS:
                if r[m].strip() == "":
                    sys.exit(f"STOP: {path.name} has a blank {m} amount for account {r['Account Code']}")
            rows.append({
                "code": r["Account Code"], "account": r["Account"], "type": r["Type"],
                "basis": "activity" if r["Type"] in FLOW_TYPES else "balance",
                "vals": {m: float(r[m]) for m in MONTHS},
            })
    return rows


def check_same_accounts(prior, curr):
    if [r["code"] for r in prior] != [r["code"] for r in curr]:
        sys.exit("STOP: Account lists differ between the two files - cannot compare row-by-row.")


def reconcile(rows):
    """Assets (less contra) = Liabilities + Equity (less contra) + YTD net income, per month."""
    out = []
    for i, m in enumerate(MONTHS):
        def amt(r):
            return -r["vals"][m] if r["account"] in CONTRAS else r["vals"][m]
        assets = sum(amt(r) for r in rows if r["type"] == "Asset")
        liab_eq = sum(amt(r) for r in rows if r["type"] in ("Liability", "Equity"))
        ytd_ni = 0.0
        for mm in MONTHS[: i + 1]:
            ytd_ni += sum(r["vals"][mm] for r in rows if r["type"] == "Revenue")
            ytd_ni -= sum(r["vals"][mm] for r in rows if r["type"] in ("COGS", "Expense"))
        out.append({"month": m, "assets": assets, "liab_eq": liab_eq, "ytd_ni": ytd_ni,
                    "diff": assets - (liab_eq + ytd_ni)})
    return out


# ---------------------------------------------------------------- comparisons
def pct_change(prior, current):
    return None if prior == 0 else (current - prior) / abs(prior)


def yoy_pass(prior, curr, months, bar):
    dollars, pct_bar = bar
    flags = []
    for p, c in zip(prior, curr):
        for m in months:
            a, b = p["vals"][m], c["vals"][m]
            var = b - a
            pct = pct_change(a, b)
            if pct is None:
                continue  # no prior-year value: percent cannot be computed, so not flagged
            if abs(var) > dollars and abs(pct) > pct_bar:
                flags.append({"code": c["code"], "account": c["account"], "type": c["type"],
                              "basis": c["basis"], "month": m, "prior": a, "current": b,
                              "var": var, "pct": pct})
    return flags


def mom_pass(prior, curr, bar):
    dollars, pct_bar = bar
    flags = []
    for p, c in zip(prior, curr):
        for m1, m2 in zip(MONTHS[:-1], MONTHS[1:]):
            a, b = c["vals"][m1], c["vals"][m2]
            var = b - a
            pct = pct_change(a, b)
            if pct is None:
                continue
            if abs(var) > dollars and abs(pct) > pct_bar:
                # Same months last year: did the account move the same way by a flaggable amount?
                pa, pb = p["vals"][m1], p["vals"][m2]
                pvar, ppct = pb - pa, pct_change(pa, pb)
                recurring = (ppct is not None and abs(pvar) > dollars and abs(ppct) > pct_bar
                             and (pvar > 0) == (var > 0))
                flags.append({"code": c["code"], "account": c["account"], "type": c["type"],
                              "basis": c["basis"], "from": m1, "to": m2, "from_value": a,
                              "to_value": b, "var": var, "pct": pct,
                              "recurring": f"yes ({pvar:+,.0f} in 2025)" if recurring else "no"})
    return flags


# ---------------------------------------------------------------- writers
def fmt(x):
    return f"{x:,.0f}"


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="\n", encoding="utf-8") as f:
        f.write(text)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def yoy_rows(flags):
    return [[f["code"], f["account"], f["type"], f["basis"], f["month"], f"{f['prior']:.1f}",
             f"{f['current']:.1f}", f"{f['var']:.1f}", f"{f['pct'] * 100:.1f}"] for f in flags]


YOY_HEADER = ["account_code", "account", "type", "basis", "month", "prior_2025", "current_2026",
              "dollar_change", "pct_change"]


def write_reconciliation(rec25, rec26, n25, n26):
    lines = ["# Reconciliation evidence", "",
             "Check: Assets (less Accumulated Depreciation) = Liabilities + Equity (less Owner Draws) + YTD net income.",
             "Accumulated Depreciation and Owner Draws are stored positive and are subtracted.", "",
             f"Rows read: {n25} (2025) + {n26} (2026). Account codes identical and in the same order.", ""]
    for label, rec in (("trial_balance_2025.csv", rec25), ("trial_balance_2026.csv", rec26)):
        lines += [f"## {label}", "",
                  "| Month | Assets, net | Liabilities + Equity, net | YTD net income | Difference |",
                  "|---|---|---|---|---|"]
        for r in rec:
            lines.append(f"| {r['month']} | {fmt(r['assets'])} | {fmt(r['liab_eq'])} | "
                         f"{fmt(r['ytd_ni'])} | {r['diff']:.2f} |")
        lines.append("")
    write_text(EVIDENCE / "reconciliation.md", "\n".join(lines))


def write_processed_long(prior, curr):
    rows = []
    for year, tb in (("2025", prior), ("2026", curr)):
        for r in tb:
            for m in MONTHS:
                rows.append([year, r["code"], r["account"], r["type"], r["basis"], m,
                             f"{r['vals'][m]:.1f}"])
    write_csv(PROCESSED / "tb_long.csv",
              ["year", "account_code", "account", "type", "basis", "month", "amount"], rows)


def append_run_log(mode, n, rec_ok, yoy_n, mom_n, yoy_bar, mom_bar):
    path = EVIDENCE / "run_log.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Run log\n\n"
    run = text.count("## Run ") + 1
    entry = [f"## Run {run} - {mode}", "",
             f"- Script: scripts/tb_compare.py (sha256 {sha(Path(__file__))})",
             f"- Plan: plan.md (sha256 {sha(Path('plan.md'))})",
             f"- Thresholds: YoY {bar_text(yoy_bar)}; MoM {bar_text(mom_bar)}. Source: plan.md front matter",
             f"- Inputs: {FILE_2025.as_posix()} (sha256 {sha(FILE_2025)}), "
             f"{FILE_2026.as_posix()} (sha256 {sha(FILE_2026)})",
             f"- Rows read {n} + {n}; used {n} + {n}; excluded 0",
             f"- Reconciliation: {rec_ok} of 8 months balance, difference 0.00",
             f"- YoY flags: {yoy_n}" + (f". MoM flags: {mom_n}" if mom_n is not None else ". MoM not run"), ""]
    write_text(path, text + "\n".join(entry) + "\n")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--month", choices=MONTHS, help="controlled test: YoY for one month")
    g.add_argument("--full", action="store_true", help="full run: YoY and MoM")
    args = ap.parse_args()

    yoy_bar, mom_bar = read_thresholds()
    prior, curr = load_tb(FILE_2025), load_tb(FILE_2026)
    check_same_accounts(prior, curr)
    rec25, rec26 = reconcile(prior), reconcile(curr)
    for label, rec in (("trial_balance_2025.csv", rec25), ("trial_balance_2026.csv", rec26)):
        bad = [r["month"] for r in rec if abs(r["diff"]) > 0.005]
        if bad:
            sys.exit(f"STOP: {label} does not reconcile in {', '.join(bad)}. No analysis run.")
        print(f"{label} reconciles: every month, difference 0")
    print(f"Rows read: {len(prior)} + {len(curr)}, account lists identical")
    write_reconciliation(rec25, rec26, len(prior), len(curr))

    if args.month:
        m = args.month
        flags = yoy_pass(prior, curr, [m], yoy_bar)
        print(f"{m} YoY flags ({bar_text(yoy_bar).replace(' and ', ' AND ')}): {len(flags)}")
        for f in flags:
            print(f"  {f['code']} {f['account']:<27}{f['var']:>+10,.0f}  {f['pct'] * 100:>6.1f}%")
        pairs = [[p["code"], p["account"], p["type"], p["basis"], f"{p['vals'][m]:.1f}",
                  f"{c['vals'][m]:.1f}"] for p, c in zip(prior, curr)]
        write_csv(PROCESSED / f"tb_{m.lower()}_pairs.csv",
                  ["account_code", "account", "type", "basis", f"{m.lower()}_2025", f"{m.lower()}_2026"], pairs)
        out = OUTPUTS / f"2026-{MONTHS.index(m) + 1:02d}-yoy-flags.csv"
        write_csv(out, YOY_HEADER, yoy_rows(flags))
        append_run_log(f"controlled test, {m} YoY only", len(prior), 8, len(flags), None, yoy_bar, mom_bar)
        print(f"Saved: {out.as_posix()}, evidence/reconciliation.md, evidence/run_log.md")
        return

    yoy = yoy_pass(prior, curr, MONTHS, yoy_bar)
    mom = mom_pass(prior, curr, mom_bar)
    yoy_accts = sorted({f["code"] for f in yoy})
    print(f"YoY flags ({bar_text(yoy_bar).replace(' and ', ' AND ')}): {len(yoy)} across {len(yoy_accts)} accounts")
    print(f"MoM flags ({bar_text(mom_bar).replace(' and ', ' AND ')}): {len(mom)}")
    print("YoY by account:")
    for code in yoy_accts:
        items = [f for f in yoy if f["code"] == code]
        months = ", ".join(f["month"] for f in items)
        print(f"  {code} {items[0]['account']:<27}{len(items)} flag(s): {months}")
    print("MoM flags:")
    for f in mom:
        print(f"  {f['code']} {f['account']:<27}{f['from']}->{f['to']}{f['var']:>+10,.0f}  "
              f"{f['pct'] * 100:>7.1f}%  recurring: {f['recurring']}")

    write_processed_long(prior, curr)
    write_csv(OUTPUTS / "yoy_flags.csv", YOY_HEADER, yoy_rows(yoy))
    write_csv(OUTPUTS / "mom_flags.csv",
              ["account_code", "account", "type", "basis", "from_month", "to_month", "from_value",
               "to_value", "dollar_change", "pct_change", "recurring_in_2025"],
              [[f["code"], f["account"], f["type"], f["basis"], f["from"], f["to"],
                f"{f['from_value']:.1f}", f"{f['to_value']:.1f}", f"{f['var']:.1f}",
                f"{f['pct'] * 100:.1f}", f["recurring"]] for f in mom])

    flagged_codes = {f["code"] for f in yoy} | {f["code"] for f in mom}
    unflagged = [r["account"] for r in prior if r["code"] not in flagged_codes]
    s = ["# Flag summary: Jan-Apr 2026 vs Jan-Apr 2025", "",
         "Flags only. Each one is a question for the reviewer, not a conclusion.", "",
         f"Thresholds, read from plan.md: YoY {bar_text(yoy_bar)}; MoM {bar_text(mom_bar)}.", "",
         "## Year over year (same month, 2026 vs 2025)", "",
         "| Account | Month | 2025 | 2026 | Change | % change |", "|---|---|---|---|---|---|"]
    for f in yoy:
        s.append(f"| {f['code']} {f['account']} | {f['month']} | {fmt(f['prior'])} | {fmt(f['current'])} | "
                 f"{f['var']:+,.0f} | {f['pct'] * 100:+.1f}% |")
    s += ["", "## Month over month (2026)", "",
          "| Account | Months | From | To | Change | % change | Recurring in 2025? |",
          "|---|---|---|---|---|---|---|"]
    for f in mom:
        s.append(f"| {f['code']} {f['account']} | {f['from']} to {f['to']} | {fmt(f['from_value'])} | "
                 f"{fmt(f['to_value'])} | {f['var']:+,.0f} | {f['pct'] * 100:+.1f}% | {f['recurring']} |")
    s += ["", f"## Accounts with no flags ({len(unflagged)} of {len(prior)})", "", ", ".join(unflagged), ""]
    write_text(OUTPUTS / "flag_summary.md", "\n".join(s))
    append_run_log("full run", len(prior), 8, len(yoy), len(mom), yoy_bar, mom_bar)
    print("Saved: data/processed/tb_long.csv, outputs/yoy_flags.csv, outputs/mom_flags.csv, "
          "outputs/flag_summary.md, evidence/run_log.md")


if __name__ == "__main__":
    main()
