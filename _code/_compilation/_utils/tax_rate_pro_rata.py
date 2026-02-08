#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute pro‑rated annual average carbon tax rates from rate change periods.
"""
from __future__ import annotations

import argparse
import calendar
from pathlib import Path
from typing import Optional

import pandas as pd


DEFAULT_PREPROC_DIR = Path("_raw/price/_preproc")
DEFAULT_INPUT = DEFAULT_PREPROC_DIR / "rate_changes.csv"


def _parse_date(value: object) -> Optional[pd.Timestamp]:
    if value is None:
        return None
    s = str(value).strip()
    if not s or s.lower() in {"nan", "na"}:
        return None
    try:
        return pd.to_datetime(s, errors="coerce")
    except Exception:
        return None


def _infer_end_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["effective_date"] = df["effective_date"].apply(_parse_date)
    df["end_date"] = df["end_date"].apply(_parse_date)

    df = df.sort_values(by=["scheme_id", "product", "effective_date"])

    def _fill_group(group: pd.DataFrame) -> pd.DataFrame:
        group = group.copy()
        dates = group["effective_date"].tolist()
        for i in range(len(group)):
            if pd.isna(group.iloc[i]["effective_date"]):
                continue
            if pd.isna(group.iloc[i]["end_date"]):
                if i + 1 < len(group) and pd.notna(dates[i + 1]):
                    group.iloc[i, group.columns.get_loc("end_date")] = dates[i + 1] - pd.Timedelta(days=1)
                else:
                    year = int(group.iloc[i]["effective_date"].year)
                    group.iloc[i, group.columns.get_loc("end_date")] = pd.Timestamp(year=year, month=12, day=31)
        return group

    df = df.groupby(["scheme_id", "product"], dropna=False, sort=False).apply(_fill_group)
    df = df.reset_index(drop=True)
    return df


def compute_annual_rates(rate_changes: pd.DataFrame) -> pd.DataFrame:
    if rate_changes.empty:
        return rate_changes

    df = rate_changes.copy()
    for col in ["scheme_id", "product", "currency_code", "source", "comment"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("")

    df = _infer_end_dates(df)

    rows = []
    for _, r in df.iterrows():
        if pd.isna(r["effective_date"]) or pd.isna(r["end_date"]):
            continue
        try:
            rate = float(r.get("rate"))
        except Exception:
            continue
        start = r["effective_date"].normalize()
        end = r["end_date"].normalize()
        if end < start:
            continue
        for year in range(start.year, end.year + 1):
            year_start = pd.Timestamp(year=year, month=1, day=1)
            year_end = pd.Timestamp(year=year, month=12, day=31)
            overlap_start = max(start, year_start)
            overlap_end = min(end, year_end)
            if overlap_end < overlap_start:
                continue
            days = (overlap_end - overlap_start).days + 1
            days_in_year = 366 if calendar.isleap(year) else 365
            rows.append(
                {
                    "scheme_id": r["scheme_id"],
                    "product": r["product"],
                    "year": year,
                    "rate_days": rate * days,
                    "days_in_year": days_in_year,
                    "currency_code": r["currency_code"],
                    "source": r["source"],
                    "comment": r["comment"],
                }
            )

    if not rows:
        return pd.DataFrame()

    tmp = pd.DataFrame(rows)
    grouped = tmp.groupby(["scheme_id", "product", "year"], dropna=False)

    out = grouped.agg(
        rate_days=("rate_days", "sum"),
        days_in_year=("days_in_year", "max"),
    ).reset_index()
    out["rate"] = out["rate_days"] / out["days_in_year"]

    # merge currency/source/comment as simple concatenations
    meta = grouped.agg(
        currency_code=("currency_code", lambda s: ";".join(sorted({x for x in s if x}))),
        source=("source", lambda s: ";".join(sorted({x for x in s if x}))),
        comment=("comment", lambda s: ";".join(sorted({x for x in s if x}))),
    ).reset_index()

    out = out.merge(meta, on=["scheme_id", "product", "year"], how="left")
    out = out[["scheme_id", "year", "product", "rate", "currency_code", "source", "comment"]]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preproc-dir", default=str(DEFAULT_PREPROC_DIR))
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--out", default=str(DEFAULT_PREPROC_DIR / "annual_rates.csv"))
    parser.add_argument("--out-tax", default="")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    df = pd.read_csv(input_path, dtype=str)
    out = compute_annual_rates(df)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)

    print(f"Wrote {len(out)} rows to {out_path}")


if __name__ == "__main__":
    main()
