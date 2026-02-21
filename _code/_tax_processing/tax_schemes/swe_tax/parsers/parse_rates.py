from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import pandas as pd
import pdfplumber

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

@dataclass
class RateRow:
    effective_from: str
    category: str
    subcat: str
    fuel_name: str
    unit: str
    energy_tax: float
    co2_tax: float
    page: int

def _parse_effective_from(line: str) -> Optional[str]:
    m = DATE_RE.search(line)
    if not m:
        return None
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

def extract_skatteverket_rates(pdf_path: Path) -> pd.DataFrame:
    """
    Extracts energiskatt + koldioxidskatt from Skatteverket historical rates PDF.

    The PDF is structured in blocks by fuel category with repeated headings and
    date-effective rows. We do *not* OCR; we use text extraction and robust regex.

    Returns a dataframe with:
      effective_from, category, subcat, fuel_name, unit, energy_tax, co2_tax, page
    """
    rows: List[RateRow] = []
    current_category = ""
    current_subcat = ""

    # Regex patterns for numeric fields:
    # - Swedish uses spaces as thousand separators sometimes
    # - decimals can be comma or dot
    def to_num(s: str) -> float:
        s = s.strip()
        s = s.replace("\u00a0", " ")
        s = s.replace(" ", "")
        s = s.replace(",", ".")
        return float(s)

    # Typical line structure examples (varies):
    # "2024-01-01  ...  Energiskatt  1260  Koldioxidskatt  3720  SEK/m3"
    # Some tables are "öre/liter" for petrol.
    num_re = re.compile(r"(?P<energy>[-\d\s.,]+)\s+(?P<co2>[-\d\s.,]+)\s+(?P<unit>SEK/m3|SEK/1000m3|öre/liter)", re.IGNORECASE)

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            # Update category/subcategory from headings
            for ln in lines:
                if ln.lower() in {"bensin", "olja", "naturgas", "metan"}:
                    current_category = ln.strip()
                    current_subcat = ""
                # Some PDFs have subheadings like "Bensin - Mk1" etc.
                if ln.lower().startswith("bensin") and ln.lower() != "bensin":
                    current_subcat = ln.strip()

            # Parse date rows
            for ln in lines:
                eff = _parse_effective_from(ln)
                if not eff:
                    continue
                m = num_re.search(ln)
                if not m:
                    continue
                energy = to_num(m.group("energy"))
                co2 = to_num(m.group("co2"))
                unit = m.group("unit")
                # Best-effort fuel name: strip the date and numeric tail
                fuel_name = re.sub(DATE_RE, "", ln).strip()
                fuel_name = num_re.sub("", fuel_name).strip(" -\t")

                rows.append(RateRow(
                    effective_from=eff,
                    category=current_category or "",
                    subcat=current_subcat or "",
                    fuel_name=fuel_name or "",
                    unit=unit,
                    energy_tax=energy,
                    co2_tax=co2,
                    page=i
                ))

    df = pd.DataFrame([r.__dict__ for r in rows])
    # Clean obvious empties
    df = df[df["co2_tax"].notna()].copy()
    # De-dupe identical parses
    df = df.drop_duplicates(subset=["effective_from","category","subcat","fuel_name","unit","energy_tax","co2_tax","page"])
    return df
