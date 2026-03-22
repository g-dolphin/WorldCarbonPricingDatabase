#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute overlap between pricing mechanisms using gas-specific coverage-factor files.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _load_coverage_factors(gas: str, raw_dir: Path) -> pd.DataFrame:
    gas_dir = Path(raw_dir) / "coverageFactor" / gas
    pattern = f"*_*_{gas}_cf.csv"
    paths = sorted(gas_dir.glob(pattern))
    if not paths:
        raise FileNotFoundError(f"No coverage-factor files found in {gas_dir} matching {pattern}")

    frames: list[pd.DataFrame] = []
    cf_col = f"cf_{gas}"
    for path in paths:
        df = pd.read_csv(path)
        keep = ["scheme_id", "jurisdiction", "year", "ipcc_code", cf_col]
        missing = [col for col in keep if col not in df.columns]
        if missing:
            raise KeyError(f"{path} is missing coverage-factor columns: {missing}")
        frames.append(df.loc[:, keep].copy())

    coverage = pd.concat(frames, ignore_index=True)
    duplicates = coverage.duplicated(["scheme_id", "jurisdiction", "year", "ipcc_code"], keep=False)
    if duplicates.any():
        dup_count = int(duplicates.sum())
        raise ValueError(
            f"Coverage-factor duplicates detected in {gas_dir} for {dup_count} rows. "
            "Use only one file per scheme/jurisdiction/year/ipcc combination."
        )
    return coverage


def _attach_cf(
    df: pd.DataFrame,
    coverage: pd.DataFrame,
    id_col: str,
    cf_col: str,
    gas: str,
) -> pd.DataFrame:
    if id_col not in df.columns:
        df[cf_col] = np.nan
        return df

    merge_cols = ["jurisdiction", "year", "ipcc_code", id_col]
    right_cols = ["jurisdiction", "year", "ipcc_code", "scheme_id", f"cf_{gas}"]
    merged = df.merge(
        coverage.loc[:, right_cols],
        left_on=merge_cols,
        right_on=["jurisdiction", "year", "ipcc_code", "scheme_id"],
        how="left",
    )
    merged.drop(columns=["scheme_id"], inplace=True)
    merged.rename(columns={f"cf_{gas}": cf_col}, inplace=True)
    return merged


def compute_overlap(
    wcpd_all_jur: pd.DataFrame,
    gas: str,
    raw_dir: str | Path,
    coverage_factors: pd.DataFrame | None = None,
) -> pd.DataFrame:
    gas = gas.upper()
    coverage = coverage_factors.copy() if coverage_factors is not None else _load_coverage_factors(gas, Path(raw_dir))
    if coverage_factors is not None:
        cf_col = f"cf_{gas}"
        keep = ["scheme_id", "jurisdiction", "year", "ipcc_code", cf_col]
        coverage = coverage.loc[:, keep].copy()
        duplicates = coverage.duplicated(["scheme_id", "jurisdiction", "year", "ipcc_code"], keep=False)
        if duplicates.any():
            dup_count = int(duplicates.sum())
            raise ValueError(f"In-memory coverage-factor dataframe contains {dup_count} duplicate rows.")

    overlap = wcpd_all_jur.copy()
    overlap = _attach_cf(overlap, coverage, "tax_id", "tax_cf", gas)
    overlap = _attach_cf(overlap, coverage, "ets_id", "ets_cf", gas)
    overlap = _attach_cf(overlap, coverage, "ets_2_id", "ets_2_cf", gas)

    for cf_col in ["tax_cf", "ets_cf", "ets_2_cf"]:
        if cf_col not in overlap.columns:
            overlap[cf_col] = np.nan
        overlap[cf_col] = pd.to_numeric(overlap[cf_col], errors="coerce").fillna(0)

    overlap = overlap[
        [
            "jurisdiction",
            "year",
            "ipcc_code",
            "Product",
            "tax_id",
            "ets_id",
            "ets_2_id",
            "tax_cf",
            "ets_cf",
            "ets_2_cf",
        ]
    ].copy()

    for scheme in ["tax_id", "ets_id", "ets_2_id"]:
        overlap[scheme + "_bin"] = np.where(overlap[scheme] != "NA", 1, 0)

    overlap["inForce"] = overlap[["tax_id_bin", "ets_id_bin", "ets_2_id_bin"]].sum(axis=1)
    overlap["cf_sum"] = overlap[["tax_cf", "ets_cf", "ets_2_cf"]].sum(axis=1)
    overlap["overlap"] = np.where((overlap["inForce"] > 1) & (overlap["cf_sum"] > 1), 1, 0)

    return overlap
