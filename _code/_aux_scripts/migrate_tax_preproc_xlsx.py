#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate tax rate change calculations from legacy XLSX files into a
normalized CSV for pro-rata processing.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import pandas as pd

SRC_ROOT = Path(
    "/Users/geoffroydolphin/Library/CloudStorage/OneDrive-rff/Documents/Research/projects/ecp/wcpd_dataset/source_data/price_preproc"
)
DST_ROOT = Path("_raw/price/_preproc")
OUT_PATH = DST_ROOT / "rate_changes.csv"
REPORT_PATH = DST_ROOT / "migrate_report.txt"

DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _norm(s: object) -> str:
    return str(s).strip().lower()


def _guess_scheme_id(path: Path, scheme_ids: set[str]) -> str:
    parts = [path.stem] + [p for p in path.parts]
    candidates = []
    for part in parts:
        token = re.sub(r"[^a-z0-9_]+", "_", part.lower())
        if "tax" in token:
            candidates.append(token)
    for cand in candidates:
        if cand in scheme_ids:
            return cand
    return candidates[0] if candidates else path.stem.lower()


def _clean_product(label: str) -> str:
    if not label:
        return ""
    # remove parenthetical units and currency
    label = re.sub(r"\([^)]*\)", "", label).strip()
    label = re.sub(r"\s+", " ", label)
    return label


def _header_row(df: pd.DataFrame, required: set[str]) -> Optional[int]:
    for idx, row in df.iterrows():
        values = {_norm(v) for v in row.tolist()}
        if required.issubset(values):
            return idx
    return None


def _extract_from_to(df: pd.DataFrame, scheme_id: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header_idx = _header_row(df, {"from", "to"})
    if header_idx is None:
        return rows
    header = df.iloc[header_idx].tolist()
    data = df.iloc[header_idx + 1 :].copy()
    data.columns = header

    col_from = "from"
    col_to = "to"
    source_col = None
    currency_col = None
    for col in data.columns:
        col_norm = _norm(col)
        if col_norm == "source":
            source_col = col
        if col_norm in {"currency", "currency_code"}:
            currency_col = col

    product_cols = [
        c
        for c in data.columns
        if _norm(c) not in {"from", "to", "source", "currency", "currency_code", "comment"}
    ]

    for _, r in data.iterrows():
        start = r.get(col_from)
        end = r.get(col_to)
        if pd.isna(start):
            continue
        start_str = str(start)[:10]
        end_str = str(end)[:10] if pd.notna(end) else ""
        source = str(r.get(source_col, "")).strip() if source_col else ""
        currency = str(r.get(currency_col, "")).strip() if currency_col else ""
        for col in product_cols:
            val = r.get(col)
            if pd.isna(val) or str(val).strip() == "":
                continue
            product = _clean_product(str(col))
            rows.append(
                {
                    "scheme_id": scheme_id,
                    "product": product,
                    "effective_date": start_str,
                    "end_date": end_str,
                    "rate": str(val).strip(),
                    "currency_code": currency,
                    "source": source,
                    "comment": "",
                }
            )
    return rows


def _extract_periods(df: pd.DataFrame, scheme_id: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header_idx = _header_row(df, {"period_start", "period_end"})
    if header_idx is None:
        return rows
    header = df.iloc[header_idx].tolist()
    data = df.iloc[header_idx + 1 :].copy()
    data.columns = header
    rate_col = None
    for col in data.columns:
        if "price" in _norm(col) or "rate" in _norm(col):
            rate_col = col
            break
    if not rate_col:
        return rows
    for _, r in data.iterrows():
        start = r.get("period_start")
        end = r.get("period_end")
        if pd.isna(start):
            continue
        rows.append(
            {
                "scheme_id": str(r.get("scheme_id", scheme_id)).strip() or scheme_id,
                "product": "",
                "effective_date": str(start)[:10],
                "end_date": str(end)[:10] if pd.notna(end) else "",
                "rate": str(r.get(rate_col, "")).strip(),
                "currency_code": str(r.get("currency_code", "")).strip(),
                "source": str(r.get("source", "")).strip(),
                "comment": str(r.get("comment", "")).strip(),
            }
        )
    return rows


def _extract_rate_from(df: pd.DataFrame, scheme_id: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    header_idx = _header_row(df, {"rate from"})
    if header_idx is None:
        return rows
    header = df.iloc[header_idx].tolist()
    data = df.iloc[header_idx + 1 :].copy()
    data.columns = header
    date_col = "Rate from"
    for _, r in data.iterrows():
        start = r.get(date_col)
        if pd.isna(start):
            continue
        start_str = str(start)[:10]
        for col in data.columns:
            if col == date_col:
                continue
            val = r.get(col)
            if pd.isna(val) or str(val).strip() == "":
                continue
            product = _clean_product(str(col))
            rows.append(
                {
                    "scheme_id": scheme_id,
                    "product": product,
                    "effective_date": start_str,
                    "end_date": "",
                    "rate": str(val).strip(),
                    "currency_code": "",
                    "source": "",
                    "comment": "",
                }
            )
    return rows


def _extract_simple_dates(df: pd.DataFrame, scheme_id: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    # detect if first two columns are dates
    if df.shape[1] < 3:
        return rows
    col0 = df.iloc[:, 0]
    col1 = df.iloc[:, 1]
    col2 = df.iloc[:, 2]
    for i in range(len(df)):
        a = str(col0.iloc[i])
        b = str(col1.iloc[i])
        if DATE_RE.search(a) and DATE_RE.search(b):
            rate = col2.iloc[i]
            if pd.isna(rate):
                continue
            rows.append(
                {
                    "scheme_id": scheme_id,
                    "product": "",
                    "effective_date": a[:10],
                    "end_date": b[:10],
                    "rate": str(rate).strip(),
                    "currency_code": "",
                    "source": "",
                    "comment": "",
                }
            )
    return rows


def main() -> None:
    DST_ROOT.mkdir(parents=True, exist_ok=True)

    scheme_ids = set()
    scheme_path = Path("_raw/_aux_files/scheme_description.csv")
    if scheme_path.exists():
        try:
            df = pd.read_csv(scheme_path, dtype=str)
            scheme_ids = set(df.get("scheme_id", []).dropna().astype(str).tolist())
        except Exception:
            pass

    rows: list[dict[str, str]] = []
    report_lines: list[str] = []

    for path in SRC_ROOT.rglob("*.xlsx"):
        scheme_id = _guess_scheme_id(path, scheme_ids)
        try:
            xl = pd.ExcelFile(path)
        except Exception as exc:
            report_lines.append(f"FAILED to read {path}: {exc}")
            continue
        extracted = False
        for sheet in xl.sheet_names:
            try:
                raw = xl.parse(sheet, header=None)
            except Exception:
                continue
            for extractor in (
                _extract_periods,
                _extract_from_to,
                _extract_rate_from,
                _extract_simple_dates,
            ):
                found = extractor(raw, scheme_id)
                if found:
                    rows.extend(found)
                    report_lines.append(f"{path}::{sheet} -> {len(found)} rows")
                    extracted = True
                    break
            if extracted:
                break
        if not extracted:
            report_lines.append(f"NO MATCH {path}")

    if rows:
        out_df = pd.DataFrame(rows)
        out_df.to_csv(OUT_PATH, index=False)

    REPORT_PATH.write_text("\n".join(report_lines))
    print(f"wrote {OUT_PATH} ({len(rows)} rows)")
    print(f"report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
