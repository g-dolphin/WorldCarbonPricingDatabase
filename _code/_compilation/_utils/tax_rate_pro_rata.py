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


DEFAULT_OUT_DIR = Path("_raw/_preproc/_preproc_tax/out")
DEFAULT_RATE_CHANGES_DIR = Path("_raw/price/_preproc")
DEFAULT_INPUT = DEFAULT_RATE_CHANGES_DIR / "rate_changes.csv"


def _extract_currency(unit: object) -> str:
    s = str(unit or "").strip()
    if not s:
        return ""
    if "/" in s:
        return s.split("/", 1)[0].strip()
    if " per " in s:
        return s.split(" per ", 1)[0].strip()
    return s


def _is_ghg_label(label: str) -> bool:
    s = str(label or "").strip().lower()
    if not s:
        return False
    return bool(pd.Series([s]).str.contains(r"(?:^|\\b)(co2e?|ch4|n2o|sf6|nf3|hfcs?|pfcs?)\\b|greenhouse", regex=True).iloc[0])


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

    df = df.sort_values(by=["scheme_id", "product", "ghg", "effective_date"])

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

    df = df.groupby(["scheme_id", "product", "ghg"], dropna=False, sort=False).apply(_fill_group)
    df = df.reset_index(drop=True)
    return df


def compute_annual_rates(rate_changes: pd.DataFrame) -> pd.DataFrame:
    if rate_changes.empty:
        return rate_changes

    df = rate_changes.copy()
    for col in ["scheme_id", "product", "currency_code", "source", "comment", "ghg"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("")
    if (df["ghg"] == "").all():
        df["ghg"] = "CO2"

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
                    "ghg": r["ghg"],
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
    grouped = tmp.groupby(["scheme_id", "product", "ghg", "year"], dropna=False)

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

    out = out.merge(meta, on=["scheme_id", "product", "ghg", "year"], how="left")
    out = out[
        ["scheme_id", "year", "ghg", "product", "rate", "currency_code", "source", "comment"]
    ]
    return out


def _load_final_rates(out_dir: Path) -> pd.DataFrame:
    rows = []
    out_dir = Path(out_dir)
    if not out_dir.exists():
        return pd.DataFrame()
    for scheme_dir in sorted(out_dir.iterdir()):
        if not scheme_dir.is_dir():
            continue
        path = scheme_dir / "final_rates.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path, dtype=str)
        if df.empty:
            continue
        df["scheme_id"] = scheme_dir.name
        rows.append(df)
    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)


def build_rate_changes_from_final_rates(final_rates: pd.DataFrame) -> pd.DataFrame:
    if final_rates.empty:
        return final_rates

    df = final_rates.copy()
    for col in [
        "scheme_id",
        "pollutant",
        "rate_value",
        "rate_unit",
        "rate_value_tco2e",
        "rate_unit_tco2e",
        "effective_from",
        "effective_to",
        "source_id",
        "source_url",
        "method",
        "notes",
    ]:
        if col not in df.columns:
            df[col] = ""

    rv_tco2e = pd.to_numeric(df["rate_value_tco2e"], errors="coerce")
    rv = pd.to_numeric(df["rate_value"], errors="coerce")
    use_tco2e = rv_tco2e.notna()
    rate = rv.where(~use_tco2e, rv_tco2e)
    unit = df["rate_unit"].where(~use_tco2e, df["rate_unit_tco2e"])

    pollutant = df["pollutant"].fillna("").astype(str).str.strip()
    is_ghg = pollutant.apply(_is_ghg_label)
    ghg = pollutant.where(is_ghg, "CO2")
    ghg = ghg.replace({"co2": "CO2", "co2e": "CO2e"})
    product = pollutant.where(~is_ghg, "")

    source = df["source_id"].fillna("").astype(str).str.strip()
    source = source.where(source != "", df["source_url"].fillna("").astype(str).str.strip())
    comment = df["method"].fillna("").astype(str).str.strip()
    comment = comment.where(comment != "", df["notes"].fillna("").astype(str).str.strip())

    out = pd.DataFrame(
        {
            "scheme_id": df["scheme_id"].fillna("").astype(str).str.strip(),
            "product": product,
            "ghg": ghg,
            "rate": rate,
            "currency_code": unit.apply(_extract_currency),
            "source": source,
            "comment": comment,
            "effective_date": df["effective_from"],
            "end_date": df["effective_to"],
        }
    )
    return out


def apply_annual_rates_to_tax_files(annual_rates: pd.DataFrame, price_dir: Path) -> int:
    if annual_rates.empty:
        return 0
    price_dir = Path(price_dir)
    price_dir.mkdir(parents=True, exist_ok=True)

    required = ["scheme_id", "year", "ghg", "product", "rate", "currency_code", "source", "comment"]
    for col in required:
        if col not in annual_rates.columns:
            annual_rates[col] = ""

    updated = 0
    for scheme_id, block in annual_rates.groupby("scheme_id"):
        if not scheme_id:
            continue
        path = price_dir / f"{scheme_id}_prices.csv"
        if path.exists():
            df = pd.read_csv(path, dtype=str)
        else:
            df = pd.DataFrame(columns=required)

        for col in required:
            if col not in df.columns:
                df[col] = ""

        def _key(frame: pd.DataFrame) -> pd.Series:
            return (
                frame["scheme_id"].astype(str).str.strip()
                + "|"
                + frame["year"].astype(str).str.strip()
                + "|"
                + frame["ghg"].astype(str).str.strip()
                + "|"
                + frame["product"].astype(str).str.strip()
            )

        existing_key = _key(df)
        incoming_key = _key(block)
        df = df.copy()
        block = block.copy()

        for _, row in block.iterrows():
            key = (
                f"{str(row.get('scheme_id','')).strip()}|"
                f"{str(row.get('year','')).strip()}|"
                f"{str(row.get('ghg','')).strip()}|"
                f"{str(row.get('product','')).strip()}"
            )
            mask = existing_key == key
            if mask.any():
                for col in required:
                    df.loc[mask, col] = row.get(col, "")
            else:
                df = pd.concat([df, pd.DataFrame([row[required]])], ignore_index=True)

        df = df[required]
        df = df.sort_values(by=["year", "ghg", "product"])
        df.to_csv(path, index=False)
        updated += 1

    return updated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preproc-dir", default=str(DEFAULT_RATE_CHANGES_DIR))
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--rates-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--out", default=str(DEFAULT_OUT_DIR / "annual_rates.csv"))
    parser.add_argument("--out-tax", default="")
    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.exists():
        df = pd.read_csv(input_path, dtype=str)
        out = compute_annual_rates(df)
    else:
        final_rates = _load_final_rates(Path(args.rates_dir))
        rate_changes = build_rate_changes_from_final_rates(final_rates)
        out = compute_annual_rates(rate_changes)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False)

    print(f"Wrote {len(out)} rows to {out_path}")

    if args.out_tax:
        updated = apply_annual_rates_to_tax_files(out, Path(args.out_tax))
        print(f"Updated {updated} tax price file(s) in {args.out_tax}")


if __name__ == "__main__":
    main()
