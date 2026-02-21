from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd
import pdfplumber
import yaml
from bs4 import BeautifulSoup

DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

def _norm_pct(s: str) -> Optional[int]:
    s = (s or "").strip()
    if not s:
        return None
    s = s.replace("%","").strip()
    try:
        return int(s)
    except ValueError:
        return None

def extract_6akap_from_sfs_pdf(pdf_path: Path, act_id: str, effective_from: str) -> pd.DataFrame:
    """
    Best-effort extraction of the 6 a kap. tables from an SFS amending-act PDF.

    The parser looks for blocks around '6 a kap.' and tries to extract:
    - section (e.g., 1 §, 2 a §)
    - item numbers (1 a, 2, 5 b, etc.)
    - exemption percentages columns

    Because formatting varies, this is intended to be followed by candidate review.
    """
    records: List[Dict[str, object]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for pno, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if "6 a kap" not in text:
                continue

            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            current_section = None

            for ln in lines:
                msec = re.search(r"(6 a kap\.)\s*(\d+\s*[a-z]?\s*§)", ln)
                if msec:
                    current_section = msec.group(2).replace(" ", "")
                    continue

                # Match table-like rows beginning with item ref like "1 a" or "5 b"
                mitem = re.match(r"^(\d+\s*[a-z]?)\b(.*)$", ln)
                if current_section and mitem:
                    item_ref = mitem.group(1).strip()
                    rest = mitem.group(2).strip()

                    # Try to capture last 1-3 percentage columns at end
                    # Example: "... 100 100 100"
                    mpct = re.search(r"(\b\d{1,3}\b)\s+(\b\d{1,3}\b)(?:\s+(\b\d{1,3}\b))?\s*$", rest)
                    if mpct:
                        en = _norm_pct(mpct.group(1))
                        co2 = _norm_pct(mpct.group(2))
                        so2 = _norm_pct(mpct.group(3)) if mpct.group(3) else None
                        desc = rest[:mpct.start()].strip(" -")
                        records.append({
                            "record_id": f"{act_id}_{current_section}_{item_ref}".replace("§","par").replace(" ", "_"),
                            "chapter_ref":"6 a kap.",
                            "section_ref": current_section.replace("§"," §"),
                            "item_ref": item_ref,
                            "item_id": f"6a:{current_section}:{item_ref}".replace(" ", ""),
                            "exemption_energy_pct": en,
                            "exemption_co2_pct": co2,
                            "exemption_sulfur_pct": so2,
                            "fuel_no_relief": "",
                            "description_text": desc,
                            "effective_from": effective_from,
                            "effective_to": "",
                            "source_act_id": act_id,
                            "source_page": pno,
                            "notes": "Extracted from SFS PDF (best-effort). Review formatting/meaning."
                        })

    return pd.DataFrame(records)

def extract_6akap_from_consolidated_html(html_path: Path) -> pd.DataFrame:
    """
    Optional: extract current consolidated 6 a kap text from a saved HTML snapshot.
    This does NOT give historical periods; it gives the latest text for cross-checking.
    """
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")
    # crude split around '6 a kap.'
    if "6 a kap" not in text:
        return pd.DataFrame()
    chunk = text.split("6 a kap", 1)[1]
    chunk = "6 a kap" + chunk
    lines = [ln.strip() for ln in chunk.splitlines() if ln.strip()]
    # return as one big record for manual diffing
    return pd.DataFrame([{
        "record_id":"CONSOLIDATED_6AKAP",
        "chapter_ref":"6 a kap.",
        "section_ref":"",
        "item_ref":"",
        "item_id":"",
        "exemption_energy_pct":"",
        "exemption_co2_pct":"",
        "exemption_sulfur_pct":"",
        "fuel_no_relief":"",
        "description_text":"\n".join(lines[:5000]),
        "effective_from":"",
        "effective_to":"",
        "source_act_id":"SE_LSE_1994_1776",
        "source_page":"",
        "notes":"Extracted consolidated 6 a kap text for cross-checking (not a time series)."
    }])

def apply_overrides(df: pd.DataFrame, overrides_path: Path) -> pd.DataFrame:
    if not overrides_path.exists():
        return df
    data = yaml.safe_load(overrides_path.read_text(encoding="utf-8")) or {}
    recs = data.get("records", [])
    if not recs:
        return df
    odf = pd.DataFrame(recs)
    # overrides are appended; de-dup by record_id
    out = pd.concat([df, odf], ignore_index=True)
    out = out.drop_duplicates(subset=["record_id"], keep="last")
    return out
