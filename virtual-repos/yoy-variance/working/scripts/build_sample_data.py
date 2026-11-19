"""
build_sample_data.py - CodeCritters Inc. sample trial balance generator

Regenerates the two synthetic trial balance CSVs used by
skills/trial-balance-comparison/scripts/generate_visuals.py. Not part of the
analysis skill itself (see CLAUDE.md, Data Locations). Run this only if the
sample data needs to be rebuilt from scratch - the checked-in CSVs in data/
are the read-only source of truth for the demo.

Usage:
    python3 scripts/build_sample_data.py
"""

import csv
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

HEADER = ["Account Code", "Account", "Type", "Jan", "Feb", "Mar", "Apr"]

# (Account Code, Account, Type, prior-year Jan-Apr, current-year Jan-Apr)
ACCOUNTS = [
    ("1000", "Checking",                    "Asset",     [7600, 11270, 18855, 27430],   [42870, 47175, 41325, 41385]),
    ("1010", "Savings",                     "Asset",     [20000, 20000, 20000, 20000],  [20000, 20000, 20000, 20000]),
    ("1200", "Accounts Receivable",         "Asset",     [14000, 14500, 15000, 15200],  [15400, 15700, 16100, 24800]),
    ("1300", "Inventory - Raw Materials",   "Asset",     [8000, 8200, 8400, 8600],      [8700, 8850, 9200, 9500]),
    ("1310", "Inventory - Finished Goods",  "Asset",     [11000, 11200, 11400, 11600],  [11700, 11900, 12100, 12300]),
    ("1400", "Prepaid Insurance",           "Asset",     [2400, 2200, 2000, 1800],      [1600, 1400, 1200, 1000]),
    ("1500", "Equipment",                   "Asset",     [45000, 45000, 45000, 45000],  [45000, 45000, 46800, 46800]),
    ("1510", "Accumulated Depreciation",    "Asset",     [9800, 10600, 11400, 12200],   [13000, 13800, 14600, 15400]),
    ("2000", "Accounts Payable",            "Liability", [7000, 7200, 7400, 7600],      [7700, 7900, 8100, 8300]),
    ("2100", "Credit Card Payable",         "Liability", [3200, 3300, 3100, 3400],      [3500, 3600, 3450, 4700]),
    ("2200", "Sales Tax Payable",           "Liability", [1800, 1850, 1900, 1950],      [1980, 2020, 2060, 2100]),
    ("2300", "Payroll Liabilities",         "Liability", [2200, 2200, 2300, 2300],      [2350, 2350, 2400, 2400]),
    ("2400", "Loan Payable - Equipment",    "Liability", [18000, 17600, 17200, 16800],  [16400, 16000, 15600, 15200]),
    ("3000", "Common Stock",                "Equity",    [10000, 10000, 10000, 10000],  [10000, 10000, 10000, 10000]),
    ("3100", "Retained Earnings",           "Equity",    [50000, 50000, 50000, 50000],  [83380, 83380, 83380, 83380]),
    ("3200", "Owner Draws",                 "Equity",    [2000, 4000, 6000, 8000],      [2200, 4400, 6600, 8800]),
    ("4000", "Sales - PyPal",               "Revenue",   [15000, 15500, 16000, 16200],  [16000, 16300, 17000, 21000]),
    ("4010", "Sales - ByteBot",             "Revenue",   [18000, 18500, 19000, 19200],  [19000, 19500, 19800, 20200]),
    ("4020", "Sales - TensorTurtle",        "Revenue",   [9000, 9200, 9500, 9700],      [9700, 9900, 10100, 10400]),
    ("4900", "Shipping Income",             "Revenue",   [1200, 1250, 1300, 1320],      [1320, 1350, 1400, 1450]),
    ("5000", "COGS - Materials",            "COGS",      [9000, 9200, 9400, 9600],      [9500, 9700, 13500, 14200]),
    ("5010", "COGS - Labor",                "COGS",      [6000, 6100, 6200, 6300],      [6300, 6400, 6500, 6600]),
    ("6000", "Rent Expense",                "Expense",   [3500, 3500, 3500, 3500],      [3600, 3600, 3600, 3600]),
    ("6010", "Utilities",                   "Expense",   [450, 480, 420, 400],          [460, 490, 430, 410]),
    ("6020", "Payroll Expense",             "Expense",   [12000, 12000, 12200, 12200],  [12500, 12500, 12500, 12500]),
    ("6030", "Marketing & Advertising",     "Expense",   [1500, 1500, 1600, 1600],      [1600, 1600, 9800, 3200]),
    ("6040", "Software Subscriptions",      "Expense",   [380, 380, 395, 395],          [400, 400, 410, 410]),
    ("6050", "Insurance Expense",           "Expense",   [600, 600, 600, 600],          [620, 620, 620, 620]),
    ("6060", "Professional Fees",           "Expense",   [500, 3800, 450, 500],         [550, 4200, 500, 550]),
    ("6070", "Depreciation Expense",        "Expense",   [800, 800, 800, 800],          [820, 820, 820, 820]),
    ("6080", "Bank Fees & Merchant Charges", "Expense",  [320, 330, 340, 345],          [350, 355, 360, 600]),
    ("6090", "Office Supplies",             "Expense",   [150, 140, 160, 155],          [160, 150, 900, 170]),
]


def write_csv(path, year_index):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for code, name, acct_type, prior, current in ACCOUNTS:
            values = prior if year_index == 0 else current
            writer.writerow([code, name, acct_type] + [float(v) for v in values])


# Contra accounts carry a natural balance opposite their parent category and
# must be SUBTRACTED, not summed in, when reconciling (Accumulated Depreciation
# is a contra-asset; Owner Draws is a contra-equity account).
CONTRA_ASSETS = {"Accumulated Depreciation"}
CONTRA_EQUITY = {"Owner Draws"}


# ---------------------------------------------------------------------------
# YEAR-END ROLL-FORWARD (Apr 2025 -> Jan 2026)
#
# The two files are not two isolated samples: Jan 2026 opens where Dec 2025
# closed, and the data has to carry that gap (May-Dec 2025, 8 months). The
# hard-coded 2026 lists above are placeholders for the accounts rebuilt here;
# this step overwrites them. Assumptions (synthetic, stated so a reviewer can
# challenge them):
#   - P&L activity for May-Dec 2025 holds at the April 2025 run rate.
#   - Accumulated Depreciation, Loan Payable and Owner Draws keep their 2025
#     monthly step through Dec 2025.
#   - Prepaid Insurance is NOT rolled forward on the 2025 slope: the policy is
#     assumed renewed during 2025, leaving $1,800 at Dec 2025 (Jan 2026: $1,600
#     after one more month of $200 amortization). It would otherwise hit zero.
#   - Retained Earnings (2026 opening) = Apr 2025 opening RE + full-year 2025
#     net income - full-year 2025 owner draws (draws are closed to RE at
#     year-end, which is why Owner Draws restarts in 2026).
#   - Accumulated Depreciation in 2026 rises by Depreciation Expense each month.
#   - Checking is the balancing account: it is solved each month so that
#     Assets = Liabilities + Equity + YTD Net Income.
# ---------------------------------------------------------------------------
GAP_MONTHS = 8  # May-Dec 2025


def _rebuild_2026_rollforward(accounts):
    by_name = {n: (c, n, t, p, cur) for c, n, t, p, cur in accounts}

    def prior(name):
        return by_name[name][3]

    # Full-year 2025 net income: Jan-Apr actuals + 8 months at April's run rate.
    jan_apr_ni = apr_ni = 0
    for _, _, t, p, _ in accounts:
        sign = 1 if t == "Revenue" else -1 if t in ("COGS", "Expense") else 0
        jan_apr_ni += sign * sum(p)
        apr_ni += sign * p[3]
    fy2025_ni = jan_apr_ni + GAP_MONTHS * apr_ni

    draws = prior("Owner Draws")
    draws_step = draws[3] - draws[2]
    fy2025_draws = draws[3] + GAP_MONTHS * draws_step
    re_open_2026 = prior("Retained Earnings")[3] + fy2025_ni - fy2025_draws

    ad = prior("Accumulated Depreciation")
    ad_dec2025 = ad[3] + GAP_MONTHS * (ad[3] - ad[2])
    dep_expense = by_name["Depreciation Expense"][4]
    ad_2026, running = [], ad_dec2025
    for i in range(4):
        running += dep_expense[i]
        ad_2026.append(running)

    loan = prior("Loan Payable - Equipment")
    loan_step = loan[3] - loan[2]  # negative: balance falls each month
    loan_dec2025 = loan[3] + GAP_MONTHS * loan_step
    loan_2026 = [loan_dec2025 + loan_step * (i + 1) for i in range(4)]

    overrides = {
        "Accumulated Depreciation": ad_2026,
        "Loan Payable - Equipment": loan_2026,
        "Retained Earnings": [re_open_2026] * 4,
    }
    rebuilt = [
        (c, n, t, p, overrides.get(n, cur)) for c, n, t, p, cur in accounts
    ]

    # Solve Checking so 2026 reconciles each month.
    ytd_ni = 0
    checking = []
    for i in range(4):
        for _, _, t, _, cur in rebuilt:
            ytd_ni += cur[i] if t == "Revenue" else -cur[i] if t in ("COGS", "Expense") else 0
        other_assets = liab = equity = 0
        for _, n, t, _, cur in rebuilt:
            if t == "Asset" and n != "Checking":
                other_assets += -cur[i] if n in CONTRA_ASSETS else cur[i]
            elif t == "Liability":
                liab += cur[i]
            elif t == "Equity":
                equity += -cur[i] if n in CONTRA_EQUITY else cur[i]
        checking.append(liab + equity + ytd_ni - other_assets)
    return [
        (c, n, t, p, checking if n == "Checking" else cur) for c, n, t, p, cur in rebuilt
    ]


ACCOUNTS = _rebuild_2026_rollforward(ACCOUNTS)

def reconciles(values_by_type, months):
    """Assets should equal Liabilities + Equity + YTD net income for every month, net of contras.

    This is a pre-closing trial balance: Retained Earnings is the opening
    balance and the P&L accounts are still open, so current-year earnings
    (Revenue - COGS - Expense, cumulative from Jan) belongs on the equity side.
    """
    ok = True
    ytd_net_income = 0
    for i, m in enumerate(months):
        ytd_net_income += sum(v[i] for _, n, t, v in values_by_type if t == "Revenue")
        ytd_net_income -= sum(v[i] for _, n, t, v in values_by_type if t in ("COGS", "Expense"))
        assets = sum(v[i] for _, n, t, v in values_by_type if t == "Asset" and n not in CONTRA_ASSETS)
        assets -= sum(v[i] for _, n, t, v in values_by_type if n in CONTRA_ASSETS)
        equity = sum(v[i] for _, n, t, v in values_by_type if t == "Equity" and n not in CONTRA_EQUITY)
        equity -= sum(v[i] for _, n, t, v in values_by_type if n in CONTRA_EQUITY)
        liab = sum(v[i] for _, n, t, v in values_by_type if t == "Liability")
        liab_eq = liab + equity + ytd_net_income
        if round(assets - liab_eq, 2) != 0:
            print(f"[WARN] {m}: Assets {assets} != Liabilities + Equity + YTD Net Income {liab_eq}")
            ok = False
    return ok


if __name__ == "__main__":
    months = ["Jan", "Feb", "Mar", "Apr"]

    prior_rows = [(c, n, t, p) for c, n, t, p, cur in ACCOUNTS]
    curr_rows = [(c, n, t, cur) for c, n, t, p, cur in ACCOUNTS]

    print("Checking prior-year (2025) reconciliation...")
    ok_2025 = reconciles(prior_rows, months)
    print("Checking current-year (2026) reconciliation...")
    ok_2026 = reconciles(curr_rows, months)

    if not (ok_2025 and ok_2026):
        raise SystemExit("Trial balance does not reconcile - fix source data before writing CSVs.")

    write_csv(os.path.join(DATA_DIR, "trial_balance_2025.csv"), year_index=0)
    write_csv(os.path.join(DATA_DIR, "trial_balance_2026.csv"), year_index=1)
    print("\n[OK] Both trial balances reconcile (Assets = Liabilities + Equity + YTD Net Income, every month).")
    print("Wrote data/trial_balance_2025.csv and data/trial_balance_2026.csv")
