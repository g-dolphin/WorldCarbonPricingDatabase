from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


SOURCES_PATH = Path("_raw/sources/sources.csv")


REQUIRED_ACT_COLS = [
    "act_id",
    "jurisdiction",
    "instrument_name",
    "instrument_type",
    "citation",
    "adoption_date",
    "publication_date",
    "entry_into_force",
    "source_url",
    "source_id",
]


def _ensure_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            out[col] = ""
    return out


def _load_sources() -> pd.DataFrame:
    if not SOURCES_PATH.exists():
        raise FileNotFoundError(f"Missing sources file: {SOURCES_PATH}")
    return pd.read_csv(SOURCES_PATH, dtype=str)


def build_acts_seed_from_sources(
    mapping_path: Path,
    fallback: Optional[pd.DataFrame] = None,
) -> pd.DataFrame:
    if not mapping_path.exists():
        if fallback is None:
            raise FileNotFoundError(f"Missing acts mapping: {mapping_path}")
        return _ensure_columns(fallback, REQUIRED_ACT_COLS)

    mapping = pd.read_csv(mapping_path, dtype=str)
    if mapping.empty:
        if fallback is None:
            raise ValueError(f"Acts mapping is empty: {mapping_path}")
        return _ensure_columns(fallback, REQUIRED_ACT_COLS)
    if "act_id" not in mapping.columns or "source_id" not in mapping.columns:
        raise ValueError(
            f"{mapping_path} must include act_id and source_id columns."
        )

    sources = _load_sources()
    merged = mapping.merge(
        sources,
        on="source_id",
        how="left",
        suffixes=("", "_src"),
    )

    # Fill in key act fields from sources when absent
    if "source_url" not in merged.columns:
        merged["source_url"] = ""
    merged["source_url"] = merged["source_url"].fillna("")
    merged.loc[merged["source_url"].astype(str).str.strip() == "", "source_url"] = (
        merged.get("url", "").fillna("")
    )

    if "instrument_name" not in merged.columns:
        merged["instrument_name"] = ""
    merged["instrument_name"] = merged["instrument_name"].fillna("")
    merged.loc[
        merged["instrument_name"].astype(str).str.strip() == "", "instrument_name"
    ] = merged.get("title", "").fillna("")

    if "citation" not in merged.columns:
        merged["citation"] = ""
    merged["citation"] = merged["citation"].fillna("")
    merged.loc[merged["citation"].astype(str).str.strip() == "", "citation"] = (
        merged.get("citation_key", "").fillna("")
    )

    if "jurisdiction" not in merged.columns:
        merged["jurisdiction"] = ""
    merged["jurisdiction"] = merged["jurisdiction"].fillna("")
    merged.loc[
        merged["jurisdiction"].astype(str).str.strip() == "", "jurisdiction"
    ] = merged.get("jurisdiction_src", merged.get("jurisdiction", "")).fillna("")

    merged = _ensure_columns(merged, REQUIRED_ACT_COLS)
    _warn_missing_act_fields(merged, mapping_path)
    return merged[REQUIRED_ACT_COLS]


def _warn_missing_act_fields(df: pd.DataFrame, mapping_path: Path) -> None:
    required = ["act_id", "source_id", "jurisdiction", "instrument_name", "instrument_type"]
    for col in required:
        missing = df[col].astype(str).str.strip() == ""
        if missing.any():
            count = int(missing.sum())
            print(f"WARNING: {mapping_path.name} has {count} row(s) with missing {col}.")
