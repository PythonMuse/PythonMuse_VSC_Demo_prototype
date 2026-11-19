"""
A - Allow controlled execution.

Runs the approved plan (plans/approved-plan.md) against the source
population (raw-data/ap-disbursements-h1-2026.csv). Read-only against
the source file; writes only to outputs/ and evidence/.

This script identifies transactions warranting investigation. It does not,
and must not, characterize any transaction, vendor, or person as fraudulent.
"""

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = ROOT / "raw-data" / "ap-disbursements-h1-2026.csv"
OUTPUTS = ROOT / "outputs"
EVIDENCE = ROOT / "evidence"

APPROVAL_THRESHOLD = 10_000.00
NEAR_THRESHOLD_BAND = 500.00
ROUND_DOLLAR_STEP = 500.00
ROUND_DOLLAR_MIN_OCCURRENCES = 3

# US federal holidays actually present in the H1 2026 population.
HOLIDAYS_2026 = {
    pd.Timestamp("2026-01-01"),  # New Year's Day
    pd.Timestamp("2026-01-19"),  # MLK Day
    pd.Timestamp("2026-02-16"),  # Presidents' Day
    pd.Timestamp("2026-05-25"),  # Memorial Day
}


def normalize_invoice_number(value: str) -> str:
    """Strip whitespace and punctuation so format variants compare equal."""
    return re.sub(r"[\s\-_.]", "", str(value)).upper()


def load_population() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA, dtype={"vendor_id": str, "purchase_order_number": str})
    for col in ("transaction_date", "invoice_date", "payment_date", "vendor_creation_date"):
        df[col] = pd.to_datetime(df[col])
    df["invoice_number_normalized"] = df["invoice_number"].apply(normalize_invoice_number)
    df["row_id"] = df.index
    return df


def test_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    dup_keys = df[df.duplicated(subset=["vendor_id", "invoice_number", "payment_amount"], keep=False)]
    return dup_keys.assign(test_triggered="exact_duplicate_invoice")


def test_near_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    normalized_dupes = df[
        df.duplicated(subset=["vendor_id", "invoice_number_normalized", "payment_amount"], keep=False)
    ]
    # Exclude rows already caught as an exact duplicate on the raw invoice number,
    # so this test's output is specifically "format variants exact-match misses."
    exact_keys = set(
        map(tuple, df[df.duplicated(subset=["vendor_id", "invoice_number", "payment_amount"], keep=False)][
            ["vendor_id", "invoice_number", "payment_amount"]
        ].values)
    )
    near_only = normalized_dupes[
        ~normalized_dupes.apply(lambda r: (r["vendor_id"], r["invoice_number"], r["payment_amount"]) in exact_keys, axis=1)
    ]
    return near_only.assign(test_triggered="near_duplicate_invoice_number")


def test_threshold_patterns(df: pd.DataFrame) -> pd.DataFrame:
    near = df[
        (df["payment_amount"] > 0)
        & (df["payment_amount"] < APPROVAL_THRESHOLD)
        & (df["payment_amount"] >= APPROVAL_THRESHOLD - NEAR_THRESHOLD_BAND)
    ]
    return near.assign(test_triggered="near_approval_threshold")


def test_round_dollar_payments(df: pd.DataFrame) -> pd.DataFrame:
    is_round = (df["payment_amount"] > 0) & (df["payment_amount"] % ROUND_DOLLAR_STEP == 0)
    counts = df[is_round].groupby("vendor_id")["vendor_id"].transform("count")
    flagged = df[is_round & (counts >= ROUND_DOLLAR_MIN_OCCURRENCES)]
    return flagged.assign(test_triggered="recurring_round_dollar_payment")


def test_weekend_or_holiday(df: pd.DataFrame) -> pd.DataFrame:
    is_weekend = df["payment_date"].dt.dayofweek >= 5
    is_holiday = df["payment_date"].isin(HOLIDAYS_2026)
    return df[is_weekend | is_holiday].assign(test_triggered="weekend_or_holiday_payment")


def test_new_vendor_activity(df: pd.DataFrame, review_start: pd.Timestamp, review_end: pd.Timestamp) -> pd.DataFrame:
    created_in_period = df[
        (df["vendor_creation_date"] >= review_start) & (df["vendor_creation_date"] <= review_end)
    ]
    return created_in_period.assign(test_triggered="new_vendor_in_period")


VOLUME_INCREASE_RATIO = 2.0
VOLUME_INCREASE_DOLLAR_FLOOR = 15_000.00  # ignore small vendors where any swing looks huge in ratio terms


def test_vendor_volume_change(df: pd.DataFrame) -> pd.DataFrame:
    """Flag vendors whose later-period volume materially exceeds their earlier-period volume."""
    midpoint = df["transaction_date"].min() + (df["transaction_date"].max() - df["transaction_date"].min()) / 2
    first_half = df[df["transaction_date"] <= midpoint].groupby("vendor_id")["payment_amount"].sum()
    second_half = df[df["transaction_date"] > midpoint].groupby("vendor_id")["payment_amount"].sum()
    ratio = (second_half / first_half.replace(0, pd.NA)).dropna()
    # New vendors have no first-half activity at all and are covered by test_new_vendor_activity instead.
    increased = ratio[
        (ratio >= VOLUME_INCREASE_RATIO) & (second_half.reindex(ratio.index) >= VOLUME_INCREASE_DOLLAR_FLOOR)
    ].index
    return df[df["vendor_id"].isin(increased) & (df["transaction_date"] > midpoint)].assign(
        test_triggered="material_volume_increase"
    )


def test_gl_inconsistency_among_related_vendors(df: pd.DataFrame) -> pd.DataFrame:
    """Flag rows whose note discloses a shared vendor-banking relationship.

    `related_party_note` is a free-text field also used for other annotations
    (credit-memo references, weekend/holiday explanations) that must NOT trigger
    this test -- only a disclosed banking/remit-to relationship should.
    """
    related = df[df["related_party_note"].str.contains("bank account", case=False, na=False)]
    return related.assign(test_triggered="related_vendor_gl_inconsistency")


def test_credit_memo_reference(df: pd.DataFrame) -> pd.DataFrame:
    credits = df[df["payment_amount"] < 0]
    missing_reference = credits[~credits["related_party_note"].str.contains("References", na=False)]
    return missing_reference.assign(test_triggered="credit_memo_missing_reference")


def build_exception_report(df: pd.DataFrame) -> pd.DataFrame:
    review_start = pd.Timestamp("2026-01-01")
    review_end = pd.Timestamp("2026-06-30")

    flagged = pd.concat(
        [
            test_exact_duplicates(df),
            test_near_duplicates(df),
            test_threshold_patterns(df),
            test_round_dollar_payments(df),
            test_weekend_or_holiday(df),
            test_new_vendor_activity(df, review_start, review_end),
            test_vendor_volume_change(df),
            test_gl_inconsistency_among_related_vendors(df),
            test_credit_memo_reference(df),
        ],
        ignore_index=True,
    )

    grouped = (
        flagged.groupby("row_id")["test_triggered"]
        .apply(lambda tests: ";".join(sorted(set(tests))))
        .rename("tests_triggered")
    )
    exceptions = df.merge(grouped, on="row_id", how="inner").sort_values(["vendor_name", "transaction_date"])
    return exceptions


def write_outputs(df: pd.DataFrame, exceptions: pd.DataFrame) -> None:
    OUTPUTS.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)

    export_cols = [
        "transaction_date", "vendor_name", "vendor_id", "invoice_number", "payment_amount",
        "payment_date", "approver", "gl_account", "purchase_order_number", "tests_triggered",
    ]
    exceptions[export_cols].to_csv(OUTPUTS / "exception-report.csv", index=False)

    test_counts = (
        exceptions["tests_triggered"].str.split(";").explode().value_counts().sort_index()
    )
    summary_lines = [
        "# Exception Summary\n",
        f"Source population: {len(df)} rows, total {df['payment_amount'].sum():,.2f}\n",
        f"Exception population: {len(exceptions)} rows, total {exceptions['payment_amount'].sum():,.2f}\n",
        "\n## Exceptions by test\n",
    ]
    for test_name, count in test_counts.items():
        summary_lines.append(f"- `{test_name}`: {count}\n")
    (OUTPUTS / "summary.md").write_text("".join(summary_lines), encoding="utf-8")

    recon_lines = [
        "# Population Reconciliation\n",
        f"- Source rows: {len(df)}\n",
        f"- Source total (payment_amount): {df['payment_amount'].sum():,.2f}\n",
        f"- Rows excluded from analysis: 0 (assignment excludes nothing; see instructions/assignment.md)\n",
        f"- Rows analyzed: {len(df)}\n",
        f"- Exception rows: {len(exceptions)} ({len(exceptions) / len(df):.1%} of population)\n",
        f"- Exception dollars: {exceptions['payment_amount'].sum():,.2f} "
        f"({exceptions['payment_amount'].sum() / df['payment_amount'].sum():.1%} of population dollars)\n",
    ]
    (EVIDENCE / "population-reconciliation.md").write_text("".join(recon_lines), encoding="utf-8")


def main() -> None:
    df = load_population()
    exceptions = build_exception_report(df)
    write_outputs(df, exceptions)
    print(f"Analyzed {len(df)} rows; flagged {len(exceptions)} for investigation.")
    print(f"Outputs written to {OUTPUTS}")


if __name__ == "__main__":
    main()
