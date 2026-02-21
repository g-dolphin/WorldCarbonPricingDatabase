from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, Tuple, Optional

import pandas as pd


DATE_COLS = [
    "adoption_date",
    "publication_date",
    "entry_into_force",
    "effective_from",
    "effective_to",
]

DEFAULT_SEED_DIR = Path("_raw/_preproc_tax/seeds")
DEFAULT_OUT_DIR = Path("_raw/_preproc_tax/out")


def _find_seed(seed_dir: Path, stem: str, prefix: Optional[str]) -> Path:
    if prefix:
        path = seed_dir / f"{stem}_{prefix}_seed.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing seed CSV: {path}")
        return path
    matches = list(seed_dir.glob(f"{stem}_*_seed.csv"))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise FileNotFoundError(f"Missing seed CSV(s): {stem}_*_seed.csv in {seed_dir}")
    raise FileNotFoundError(
        f"Multiple {stem}_*_seed.csv files in {seed_dir}; pass a prefix."
    )


def _read_seed_csvs(seed_dir: Path, prefix: Optional[str]) -> Dict[str, pd.DataFrame]:
    """Reads all required seed CSVs from a folder."""
    required = {
        "acts": _find_seed(seed_dir, "acts", prefix),
        "provisions": _find_seed(seed_dir, "provisions", prefix),
        "rates": _find_seed(seed_dir, "rates", prefix),
        "coverage_rules": _find_seed(seed_dir, "coverage", prefix),
        "exemptions": _find_seed(seed_dir, "exemptions", prefix),
    }
    expected_cols = {
        "acts": [
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
        ],
        "provisions": [
            "provision_id",
            "act_id",
            "provision_ref",
            "chapter_ref",
            "title",
            "change_type",
            "change_note",
        ],
        "rates": [
            "rate_id",
            "provision_id",
            "pollutant",
            "rate_value",
            "rate_unit",
            "effective_from",
            "effective_to",
            "rate_basis",
            "method",
            "notes",
        ],
        "coverage_rules": [
            "coverage_id",
            "provision_id",
            "scope_type",
            "scope_subject",
            "condition_text",
            "effective_from",
            "effective_to",
            "notes",
        ],
        "exemptions": [
            "exemption_id",
            "provision_id",
            "exemption_type",
            "description_text",
            "condition_text",
            "effective_from",
            "effective_to",
            "notes",
        ],
    }
    dfs: Dict[str, pd.DataFrame] = {}
    for key, path in required.items():
        try:
            dfs[key] = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            dfs[key] = pd.DataFrame(columns=expected_cols.get(key, []))
    return dfs


def _coerce_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce ISO date columns to pandas datetime (nullable)."""
    out = df.copy()
    for c in DATE_COLS:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors="coerce")
    return out


def validate_seeds(dfs: Dict[str, pd.DataFrame]) -> None:
    """Basic relational integrity checks on the seed tables."""
    acts = dfs["acts"]
    prov = dfs["provisions"]
    rates = dfs["rates"]
    cov = dfs["coverage_rules"]
    exm = dfs["exemptions"]

    # Primary keys unique
    for name, pk in [
        ("acts", "act_id"),
        ("provisions", "provision_id"),
        ("rates", "rate_id"),
        ("coverage_rules", "coverage_id"),
        ("exemptions", "exemption_id"),
    ]:
        if pk not in dfs[name].columns:
            raise ValueError(f"{name} missing PK column {pk}")
        if dfs[name][pk].duplicated().any():
            dups = dfs[name].loc[dfs[name][pk].duplicated(), pk].tolist()
            raise ValueError(f"{name}: duplicated {pk}: {dups[:10]}")

    # FK integrity
    act_ids = set(acts["act_id"])
    if not set(prov["act_id"]).issubset(act_ids):
        bad = sorted(set(prov["act_id"]) - act_ids)
        raise ValueError(f"provisions.act_id has unknown ids: {bad}")

    prov_ids = set(prov["provision_id"])
    for tbl, col in [
        ("rates", "provision_id"),
        ("coverage_rules", "provision_id"),
        ("exemptions", "provision_id"),
    ]:
        bad = sorted(set(dfs[tbl][col]) - prov_ids)
        if bad:
            raise ValueError(f"{tbl}.{col} has unknown provision_id(s): {bad}")

    # Rate period sanity: effective_from <= effective_to
    rates_dt = _coerce_dates(rates)
    if "effective_to" in rates_dt.columns:
        bad = rates_dt.dropna(subset=["effective_from", "effective_to"])
        bad = bad[bad["effective_from"] > bad["effective_to"]]
        if len(bad):
            raise ValueError(
                f"rates has {len(bad)} rows where effective_from > effective_to"
            )

    # Optional: overlapping periods for same pollutant within same provision
    if {"provision_id", "pollutant", "effective_from"}.issubset(rates.columns):
        r = rates_dt.sort_values(["provision_id", "pollutant", "effective_from"])
        overlaps = []
        for (pid, pol), g in r.groupby(["provision_id", "pollutant"], dropna=False):
            g = g.copy()
            g["prev_to"] = g["effective_to"].shift(1)
            g["prev_from"] = g["effective_from"].shift(1)
            mask = (
                g["prev_to"].notna()
                & g["effective_from"].notna()
                & (g["effective_from"] <= g["prev_to"])
            )
            if mask.any():
                overlaps.append((pid, pol, int(mask.sum())))
        if overlaps:
            print("WARNING: potential overlapping rate periods:", overlaps)


def build_final_tables(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    acts = _coerce_dates(dfs["acts"])
    prov = _coerce_dates(dfs["provisions"])
    rates = _coerce_dates(dfs["rates"])
    cov = _coerce_dates(dfs["coverage_rules"])
    exm = _coerce_dates(dfs["exemptions"])

    final_rates = (
        rates.merge(
            prov, on="provision_id", how="left", validate="many_to_one", suffixes=("", "_prov")
        ).merge(
            acts, on="act_id", how="left", validate="many_to_one", suffixes=("", "_act")
        )
    )

    final_rates = final_rates.sort_values(
        ["jurisdiction", "pollutant", "effective_from", "rate_value"]
    )
    for c in [
        "effective_from",
        "effective_to",
        "entry_into_force",
        "publication_date",
        "adoption_date",
    ]:
        if c in final_rates.columns:
            final_rates[c] = final_rates[c].dt.strftime("%Y-%m-%d")

    final_coverage = (
        cov.merge(prov, on="provision_id", how="left", validate="many_to_one")
        .merge(acts, on="act_id", how="left", validate="many_to_one")
        .sort_values(["jurisdiction", "scope_type", "scope_subject"])
    )
    for c in [
        "effective_from",
        "effective_to",
        "entry_into_force",
        "publication_date",
        "adoption_date",
    ]:
        if c in final_coverage.columns:
            final_coverage[c] = (
                pd.to_datetime(final_coverage[c], errors="coerce").dt.strftime("%Y-%m-%d")
            )

    final_exemptions = (
        exm.merge(prov, on="provision_id", how="left", validate="many_to_one")
        .merge(acts, on="act_id", how="left", validate="many_to_one")
        .sort_values(["jurisdiction", "exemption_type", "effective_from"])
    )
    for c in [
        "effective_from",
        "effective_to",
        "entry_into_force",
        "publication_date",
        "adoption_date",
    ]:
        if c in final_exemptions.columns:
            final_exemptions[c] = (
                pd.to_datetime(final_exemptions[c], errors="coerce").dt.strftime("%Y-%m-%d")
            )

    timeline = (
        final_rates[
            [
                "jurisdiction",
                "pollutant",
                "effective_from",
                "rate_value",
                "rate_unit",
                "instrument_name",
                "instrument_type",
                "citation",
                "source_url",
                "provision_ref",
                "change_type",
                "change_note",
            ]
        ]
        .drop_duplicates()
        .sort_values(["jurisdiction", "pollutant", "effective_from"])
        .reset_index(drop=True)
    )

    return {
        "final_rates": final_rates,
        "final_coverage": final_coverage,
        "final_exemptions": final_exemptions,
        "final_policy_timeline": timeline,
    }


def main(seed_dir: str, out_dir: str, prefix: Optional[str] = None) -> None:
    seed_dir_p = Path(seed_dir)
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)

    dfs = _read_seed_csvs(seed_dir_p, prefix)
    validate_seeds(dfs)

    finals = build_final_tables(dfs)

    for name, df in finals.items():
        df.to_csv(out_dir_p / f"{name}.csv", index=False)

    print(f"Wrote: {', '.join([f'{k}.csv' for k in finals.keys()])} to {out_dir_p}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        main(str(DEFAULT_SEED_DIR), str(DEFAULT_OUT_DIR))
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(
            "Usage: python build_final_tables.py <seed_dir> <out_dir> [prefix]\n"
            f"Defaults: {DEFAULT_SEED_DIR} -> {DEFAULT_OUT_DIR}"
        )
