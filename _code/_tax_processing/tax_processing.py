from __future__ import annotations

import os
import re
from datetime import date, timedelta
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

DEFAULT_SEED_DIR = Path("_raw/_preproc/_preproc_tax/seeds")
DEFAULT_OUT_DIR = Path("_raw/_preproc/_preproc_tax/out")
SCHEME_DESC_PATH = Path("_raw/_aux_files/scheme_description.csv")

EU_SCHEMES = {
    "and_tax",
    "dnk_tax",
    "est_tax",
    "fin_tax",
    "fra_tax",
    "hun_tax",
    "irl_tax",
    "isl_tax",
    "lie_tax",
    "lux_tax",
    "lva_tax",
    "nld_tax",
    "pol_tax",
    "prt_tax",
    "slo_tax",
    "esp_tax",
}


def _scheme_start_date(scheme_id: Optional[str]) -> Optional[date]:
    if not scheme_id:
        return None
    if not SCHEME_DESC_PATH.exists():
        return None
    try:
        desc = pd.read_csv(SCHEME_DESC_PATH)
    except Exception:
        return None
    row = desc[desc["scheme_id"] == scheme_id]
    if row.empty:
        return None
    year = row["implementation_year"].iloc[0]
    try:
        year_int = int(year)
    except Exception:
        return None
    if year_int <= 0:
        return None
    return date(year_int, 1, 1)


def _normalize_periods(
    df: pd.DataFrame,
    group_cols: list[str],
    scheme_id: Optional[str],
    table_name: str,
    start_date: Optional[date],
) -> pd.DataFrame:
    if df.empty or "effective_from" not in df.columns:
        return df
    out = df.copy()
    out = _coerce_dates(out)
    if "effective_to" not in out.columns:
        return out
    today = date.today()
    for keys, g in out.groupby(group_cols, dropna=False):
        g = g.sort_values("effective_from")
        if start_date is not None:
            first = g["effective_from"].dropna().min()
            if pd.notna(first) and first.date() > start_date:
                print(
                    f"WARNING: {scheme_id} {table_name} {keys} starts at {first.date()} "
                    f"after scheme_start_date {start_date}"
                )
        # fill effective_to using next effective_from
        idxs = g.index.tolist()
        for i, idx in enumerate(idxs):
            curr_from = g.loc[idx, "effective_from"]
            curr_to = g.loc[idx, "effective_to"]
            next_from = None
            if i + 1 < len(idxs):
                next_from = g.loc[idxs[i + 1], "effective_from"]
            if pd.isna(curr_from):
                continue
            if pd.isna(curr_to) and pd.notna(next_from):
                out.loc[idx, "effective_to"] = next_from - pd.Timedelta(days=1)
            if pd.notna(curr_to) and pd.notna(next_from):
                if next_from <= curr_to:
                    print(
                        f"WARNING: {scheme_id} {table_name} {keys} overlap: "
                        f"{next_from.date()} <= {curr_to.date()}"
                    )
                elif next_from > curr_to + pd.Timedelta(days=1):
                    print(
                        f"WARNING: {scheme_id} {table_name} {keys} gap: "
                        f"{curr_to.date()} -> {next_from.date()}"
                    )
        last_to = g["effective_to"].dropna().max()
        if pd.notna(last_to) and last_to.date() < today:
            print(
                f"WARNING: {scheme_id} {table_name} {keys} ends {last_to.date()} "
                f"before today {today}"
            )
    # back to ISO date strings
    for c in ["effective_from", "effective_to"]:
        if c in out.columns:
            out[c] = out[c].dt.date.astype("object")
    return out


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
    scheme_id = prefix
    if scheme_id in EU_SCHEMES:
        start_date = _scheme_start_date(scheme_id)
        dfs["rates"] = _normalize_periods(
            dfs["rates"],
            ["provision_id", "pollutant"],
            scheme_id,
            "rates",
            start_date,
        )
        dfs["coverage_rules"] = _normalize_periods(
            dfs["coverage_rules"],
            ["provision_id", "scope_type", "scope_subject"],
            scheme_id,
            "coverage",
            start_date,
        )
        dfs["exemptions"] = _normalize_periods(
            dfs["exemptions"],
            ["provision_id", "exemption_type", "description_text"],
            scheme_id,
            "exemptions",
            start_date,
        )

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
