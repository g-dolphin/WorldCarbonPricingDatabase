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

ICAP_URL = (
    "https://allowancepriceexplorer.icapcarbonaction.com/systems/reports/price/"
    "download?systemIds=6-33-28-29-14-8-16-30-32-15-35-4-7-11-18-19-20-21-23-24-25-26"
    "&startDate=1110326400000&endDate=1768848182186"
)


def download_icap_csv(output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    output_filename = f"icap_prices_{timestamp}.csv"
    output_path = os.path.join(output_dir, output_filename)
    request = urllib.request.Request(
        ICAP_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request) as response:
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


def _build_keys(header_top: list[str], header: list[str]) -> list[tuple[str, str]]:
    keys = []
    current_scheme = ""
    for top_value, label in zip(header_top, header):
        top_value = top_value if top_value is not None else ""
        if top_value != "":
            current_scheme = top_value
        keys.append((_normalize_scheme_name(current_scheme), _normalize_label(label)))
    return keys


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
            repo_root, "_raw", "price", "_icap", "_icap-graph-price-data-2008-04-01-2025-04-15.csv"
        )

    template_encoding = _detect_encoding(template_path)
    template_top, template_header = _read_headers(template_path, template_encoding)
    template_keys = _build_keys(template_top, template_header)

    input_encoding = _detect_encoding(input_path)
    with open(input_path, "r", encoding=input_encoding, newline="") as infile:
        reader = csv.reader(infile)
        input_top = next(reader, None)
        input_header = next(reader, None)

        if not input_top or not input_header:
            raise ValueError("ICAP file is missing the expected two header rows.")

        input_keys = _build_keys(input_top, input_header)
        input_key_map = {}
        for idx, key in enumerate(input_keys):
            input_key_map.setdefault(key, idx)

        with open(output_path, "w", encoding="latin-1", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(template_top)
            writer.writerow(template_header)

            for row in reader:
                output_row = []
                for key in template_keys:
                    idx = input_key_map.get(key)
                    output_row.append(row[idx] if idx is not None and idx < len(row) else "")
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

    raw_path = download_icap_csv(args.output_dir)
    normalized_path = normalize_icap_file(raw_path, template_path=args.template_path)

    print(f"Downloaded: {raw_path}")
    print(f"Normalized: {normalized_path}")


if __name__ == "__main__":
    main()
