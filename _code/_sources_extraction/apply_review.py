# _code/upstream/apply_review.py

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd


RAW_ROOT = Path("_raw/sources")
CAND_PATH = RAW_ROOT / "cp_candidates.csv"
REVIEW_PATH = RAW_ROOT / "cp_review_state.csv"

OUT_PRICES = RAW_ROOT / "upstream_prices.csv"
OUT_START = RAW_ROOT / "upstream_start_dates.csv"
OUT_IPCC = RAW_ROOT / "upstream_coverage_ipcc.csv"


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    if not CAND_PATH.exists():
        raise FileNotFoundError(f"Missing candidates file: {CAND_PATH}")
    if not REVIEW_PATH.exists():
        raise FileNotFoundError(f"Missing review state file: {REVIEW_PATH}")

    cand = pd.read_csv(CAND_PATH, dtype=str)
    review = pd.read_csv(REVIEW_PATH, dtype=str)

    return cand, review


def build_final_table() -> pd.DataFrame:
    cand, review = load_data()

    # Keep only candidates that have a review row
    merged = cand.merge(review, on="candidate_id", how="inner", suffixes=("", "_rev"))

    # Only accepted
    merged = merged[merged["decision"] == "accepted"].copy()
    if merged.empty:
        return merged

    if "instrument_id" not in merged.columns and "scheme_id" in merged.columns:
        merged["instrument_id"] = merged["scheme_id"]

    # Fill NaNs with empty strings for convenience
    for col in ["edited_value", "edited_numeric_value", "edited_currency", "edited_unit"]:
        if col not in merged.columns:
            merged[col] = ""
        merged[col] = merged[col].fillna("")

    for col in ["value", "numeric_value", "currency", "unit"]:
        if col not in merged.columns:
            merged[col] = ""
        merged[col] = merged[col].fillna("")

    for col in ["edited_ghg", "edited_product", "edited_ipcc"]:
        if col not in merged.columns:
            merged[col] = ""
        merged[col] = merged[col].fillna("")

    # Compute final values
    merged["final_value"] = merged.apply(
        lambda r: r["edited_value"] if r["edited_value"] else r["value"],
        axis=1,
    )
    merged["final_numeric_value"] = merged.apply(
        lambda r: r["edited_numeric_value"] if r["edited_numeric_value"] else r["numeric_value"],
        axis=1,
    )
    merged["final_currency"] = merged.apply(
        lambda r: r["edited_currency"] if r["edited_currency"] else r["currency"],
        axis=1,
    )
    merged["final_unit"] = merged.apply(
        lambda r: r["edited_unit"] if r["edited_unit"] else r["unit"],
        axis=1,
    )

    merged["final_ghg"] = merged["edited_ghg"]
    merged["final_product"] = merged["edited_product"]
    merged["final_ipcc"] = merged["edited_ipcc"]

    # Standardise some key columns (ensure they exist)
    for col in [
        "review_entry_id",
        "instrument_id",
        "jurisdiction_code",
        "source_id",
        "artifact_id",
        "field_name",
        "method",
        "confidence",
        "reviewer",
        "reviewed_at",
        "comment",
        "final_ghg",
        "final_product",
        "final_ipcc",
    ]:
        if col not in merged.columns:
            merged[col] = ""

    return merged


def write_prices(df: pd.DataFrame) -> None:
    prices = df[df["field_name"] == "rate"].copy()
    if prices.empty:
        OUT_PRICES.unlink(missing_ok=True)
        return

    cols = [
        "review_entry_id",
        "instrument_id",
        "jurisdiction_code",
        "source_id",
        "artifact_id",
        "candidate_id",
        "final_numeric_value",
        "final_currency",
        "final_unit",
        "final_ghg",
        "final_product",
        "final_ipcc",
        "final_value",  # human-readable string
        "method",
        "confidence",
        "reviewer",
        "reviewed_at",
        "comment",
    ]

    prices_out = prices[cols]
    prices_out.to_csv(OUT_PRICES, index=False)


def write_start_dates(df: pd.DataFrame) -> None:
    starts = df[df["field_name"] == "start_date"].copy()
    if starts.empty:
        OUT_START.unlink(missing_ok=True)
        return

    cols = [
        "review_entry_id",
        "instrument_id",
        "jurisdiction_code",
        "source_id",
        "artifact_id",
        "candidate_id",
        "final_value",  # start date as reviewed text (e.g. "1 January 2025")
        "final_ghg",
        "final_product",
        "final_ipcc",
        "method",
        "confidence",
        "reviewer",
        "reviewed_at",
        "comment",
    ]

    starts_out = starts[cols]
    starts_out.to_csv(OUT_START, index=False)


def write_ipcc(df: pd.DataFrame) -> None:
    ipcc = df[df["field_name"] == "ipcc_category"].copy()
    if ipcc.empty:
        OUT_IPCC.unlink(missing_ok=True)
        return

    cols = [
        "review_entry_id",
        "instrument_id",
        "jurisdiction_code",
        "source_id",
        "artifact_id",
        "candidate_id",
        "final_value",  # IPCC code
        "final_ghg",
        "final_product",
        "final_ipcc",
        "method",
        "confidence",
        "reviewer",
        "reviewed_at",
        "comment",
    ]

    ipcc_out = ipcc[cols]
    ipcc_out.to_csv(OUT_IPCC, index=False)


def main() -> None:
    df = build_final_table()
    if df.empty:
        print("No accepted candidates found – nothing to write.")
        return

    write_prices(df)
    write_start_dates(df)
    write_ipcc(df)

    print(f"Wrote {OUT_PRICES} (prices/tax rates)")
    print(f"Wrote {OUT_START} (start dates)")
    print(f"Wrote {OUT_IPCC} (IPCC coverage)")


if __name__ == "__main__":
    main()
