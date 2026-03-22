#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download the ICAP allowance price CSV and normalize it for process_icap_prices.

Quarterly cron example:
0 3 1 */3 * /usr/bin/env python3 /path/to/icap_download.py
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import unicodedata
from datetime import datetime
import urllib.request
import ssl
import json
import ssl

ICAP_BASE_URL = "https://allowancepriceexplorer.icapcarbonaction.com"
ICAP_SYSTEMS_API = f"{ICAP_BASE_URL}/api/systems"
ICAP_REPORT_URL = f"{ICAP_BASE_URL}/systems/reports/price/download"

DEFAULT_SYSTEM_IDS = [
    6, 33, 28, 29, 14, 8, 16, 30, 32, 15, 35, 4, 7, 11, 18, 19, 20, 21, 23, 24, 25, 26
]


def _default_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    try:
        import certifi  # type: ignore

        context.load_verify_locations(certifi.where())
    except Exception:
        # Fall back to system CAs; if they are missing, urllib will raise SSL error.
        pass
    return context


def _read_icap_systems(context: ssl.SSLContext) -> list[dict]:
    request = urllib.request.Request(
        ICAP_SYSTEMS_API,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, context=context) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def _canonical_scheme_name(name: str | None) -> str:
    if name is None:
        return ""
    collapsed = " ".join(str(name).split())
    if collapsed == "":
        return ""
    collapsed = unicodedata.normalize("NFKD", collapsed).encode("ascii", "ignore").decode("ascii")

    aliases = {
        "European Union Emissions Trading System (until 2018)": "European Union Emissions Trading System",
        "European Union Emissions Trading System (from 2019)": "European Union Emissions Trading System",
        "European Union Emissions Trading System (from 2019, download)": "European Union Emissions Trading System",
        "New Zealand Emissions Trading System (Up to 2023)": "New Zealand Emissions Trading System",
        "New Zealand Emissions Trading System (From 2024)": "New Zealand Emissions Trading System",
        "California Cap-and-Trade Program (download)": "California Cap-and-Trade Program",
        "Washington Cap-and-Invest Program (download)": "Washington Cap-and-Invest Program",
        "United Kingdom Emissions Trading Scheme (download)": "United Kingdom Emissions Trading Scheme",
    }
    return aliases.get(collapsed, collapsed)


def _build_report_url(system_ids: list[int]) -> str:
    ids = "-".join(str(x) for x in system_ids)
    # Start date corresponds to 2005-03-09; end date far in future
    return f"{ICAP_REPORT_URL}?systemIds={ids}&startDate=1110326400000&endDate=1768848182186"


def _discover_system_ids(template_path: str, context: ssl.SSLContext) -> list[int]:
    try:
        systems = _read_icap_systems(context)
    except Exception:
        return DEFAULT_SYSTEM_IDS

    # Collect canonical scheme names from template
    template_encoding = _detect_encoding(template_path)
    template_top, template_header = _read_headers(template_path, template_encoding)
    template_keys = _build_keys(template_top, template_header, canonicalize=True)
    template_schemes = sorted({k[0] for k in template_keys if k[0]})

    ids: list[int] = []
    for sys in systems:
        name = _canonical_scheme_name(sys.get("name"))
        if name in template_schemes:
            ids.append(int(sys.get("id")))
    if not ids:
        return DEFAULT_SYSTEM_IDS
    return sorted(set(ids))


def download_icap_csv(output_dir: str, template_path: str | None = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    output_filename = f"icap_prices_{timestamp}.csv"
    output_path = os.path.join(output_dir, output_filename)
    if template_path is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_path = os.path.join(
            repo_root, "_raw", "price", "_icap", "_ICAP_allowance_prices.csv"
        )
    context = _default_ssl_context()
    system_ids = _discover_system_ids(template_path, context)
    report_url = _build_report_url(system_ids)
    request = urllib.request.Request(
        report_url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, context=context) as response:
        with open(output_path, "wb") as outfile:
            shutil.copyfileobj(response, outfile)
    return output_path


def _read_headers(path: str, encoding: str) -> tuple[list[str], list[str]]:
    with open(path, "r", encoding=encoding, newline="") as infile:
        reader = csv.reader(infile)
        header_top = next(reader, None)
        header = next(reader, None)
    if not header_top or not header:
        raise ValueError(f"ICAP file {path} is missing the expected two header rows.")
    return header_top, header


def _detect_encoding(path: str) -> str:
    try:
        _read_headers(path, "utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def _normalize_scheme_name(name: str | None) -> str:
    if name is None:
        return ""
    if name == " ":
        return " "
    collapsed = " ".join(name.split())
    if collapsed == "":
        return ""
    return unicodedata.normalize("NFKD", collapsed).encode("ascii", "ignore").decode("ascii")


def _normalize_label(label: str | None) -> str:
    if label is None:
        return ""
    if label == " ":
        return " "
    return label.strip()


def _build_keys(
    header_top: list[str],
    header: list[str],
    canonicalize: bool = False,
) -> list[tuple[str, str]]:
    keys = []
    current_scheme = ""
    for top_value, label in zip(header_top, header):
        top_value = top_value if top_value is not None else ""
        if top_value != "":
            current_scheme = top_value
        scheme_name = _normalize_scheme_name(current_scheme)
        if canonicalize:
            scheme_name = _canonical_scheme_name(scheme_name)
        keys.append((scheme_name, _normalize_label(label)))
    return keys


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d")
    except Exception:
        return None


def _read_rows_mapped_to_template(
    path: str,
    template_keys: list[tuple[str, str]],
) -> list[tuple[datetime | None, str, list[str]]]:
    encoding = _detect_encoding(path)
    with open(path, "r", encoding=encoding, newline="") as infile:
        reader = csv.reader(infile)
        input_top = next(reader, None)
        input_header = next(reader, None)
        if not input_top or not input_header:
            raise ValueError(f"ICAP file {path} is missing the expected two header rows.")

        input_keys = _build_keys(input_top, input_header, canonicalize=True)
        input_key_map: dict[tuple[str, str], list[int]] = {}
        for idx, key in enumerate(input_keys):
            input_key_map.setdefault(key, []).append(idx)

        date_key = ("", "Date")
        if date_key not in template_keys:
            raise ValueError("Template keys do not include a Date column.")
        template_date_idx = template_keys.index(date_key)

        rows: list[tuple[datetime | None, str, list[str]]] = []
        for row in reader:
            output_row = []
            for key in template_keys:
                idxs = input_key_map.get(key, [])
                value = ""
                for idx in idxs:
                    if idx < len(row) and row[idx] not in ("", None):
                        value = row[idx]
                        break
                output_row.append(value)
            date_value = output_row[template_date_idx] if template_date_idx < len(output_row) else ""
            rows.append((_parse_date(date_value), date_value, output_row))
    return rows


def normalize_icap_file(
    input_path: str,
    output_path: str | None = None,
    template_path: str | None = None,
) -> str:
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}-normalized{ext}"

    if template_path is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_path = os.path.join(
            repo_root, "_raw", "price", "_icap", "_ICAP_allowance_prices.csv"
        )

    template_encoding = _detect_encoding(template_path)
    template_top, template_header = _read_headers(template_path, template_encoding)
    template_keys = _build_keys(template_top, template_header, canonicalize=True)
    date_key = ("", "Date")
    date_idx = template_keys.index(date_key)
    eu_scheme_name = _canonical_scheme_name("European Union Emissions Trading System")
    eu_column_indexes = [idx for idx, key in enumerate(template_keys) if key[0] == eu_scheme_name]

    legacy_rows = _read_rows_mapped_to_template(template_path, template_keys)
    input_rows = _read_rows_mapped_to_template(input_path, template_keys)

    legacy_by_date = {date_value: (parsed_date, row) for parsed_date, date_value, row in legacy_rows}
    combined_by_date: dict[str, tuple[datetime | None, list[str]]] = {}

    # Start from the newly downloaded rows and backfill only EU ETS cells from legacy.
    for parsed_date, date_value, row in input_rows:
        merged_row = list(row)
        if date_value in legacy_by_date:
            legacy_parsed_date, legacy_row = legacy_by_date[date_value]
            for idx in eu_column_indexes:
                if merged_row[idx] in ("", None):
                    merged_row[idx] = legacy_row[idx]
            combined_by_date[date_value] = (parsed_date or legacy_parsed_date, merged_row)
        else:
            combined_by_date[date_value] = (parsed_date, merged_row)

    # Add legacy-only dates, but populate only the EU ETS columns.
    for date_value, (parsed_date, legacy_row) in legacy_by_date.items():
        if date_value in combined_by_date:
            continue
        blank_row = [""] * len(template_keys)
        blank_row[date_idx] = date_value
        for idx in eu_column_indexes:
            blank_row[idx] = legacy_row[idx]
        combined_by_date[date_value] = (parsed_date, blank_row)

    rows_with_dates = sorted(
        combined_by_date.values(),
        key=lambda item: (item[0] is None, item[0] or datetime.max),
    )

    with open(output_path, "w", encoding="latin-1", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(template_top)
        writer.writerow(template_header)
        for _, output_row in rows_with_dates:
            writer.writerow(output_row)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and normalize ICAP price data.")
    parser.add_argument(
        "--output-dir",
        default=os.path.join(os.getcwd(), "_raw", "price", "_icap"),
        help="Directory to save the downloaded and normalized files.",
    )
    parser.add_argument(
        "--template-path",
        default=None,
        help="Template CSV used to normalize columns (defaults to the repo canvas file).",
    )
    args = parser.parse_args()

    raw_path = download_icap_csv(args.output_dir, template_path=args.template_path)
    normalized_path = normalize_icap_file(raw_path, template_path=args.template_path)

    print(f"Downloaded: {raw_path}")
    print(f"Normalized: {normalized_path}")


if __name__ == "__main__":
    main()
