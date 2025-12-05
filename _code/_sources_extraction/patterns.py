from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class MatchResult:
    field_name: str          # e.g. 'start_date', 'rate', 'ipcc_category'
    value: str               # human-readable value (string)
    numeric_value: Optional[float]  # for prices/rates where applicable
    currency: Optional[str]  # e.g. 'EUR', 'CAD', etc.
    unit: Optional[str]      # e.g. 'tCO2e'
    span: Tuple[int, int]    # character span in the text
    method: str              # e.g. 'regex_rate_v1'
    confidence: float        # 0–1

# --- Date and rate patterns (simple MVP) ---

DATE_PATTERN = re.compile(
    r"\b(?:from|as of|effective|enter(?:s)? into force(?: on)?)\s+"
    r"(\d{1,2}\s+\w+\s+\d{4})",
    flags=re.IGNORECASE,
)

# Strict pattern: number + currency + per tonne
RATE_PATTERN_STRICT = re.compile(
    r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)\s*"          # numeric value
    r"(EUR|€|EURO|CAD|C\$|USD|\$|SEK|DKK|NOK|GBP)\s*"  # currency
    r"(?:per|/)?\s*(?:tonne|ton|t)\s*(CO2e?|CO₂e?|CO2eq)?",
    flags=re.IGNORECASE,
)

# Loose pattern: number + "per tonne/tCO2" but currency may be elsewhere
RATE_PATTERN_LOOSE = re.compile(
    r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)"         # numeric value
    r"\s*(?:per|/)\s*(?:tonne|ton|t)\s*(CO2e?|CO₂e?|CO2eq)?",
    flags=re.IGNORECASE,
)

# --- IPCC sector mapping via keywords (very approximate) ---

IPCC_KEYWORD_MAP = {
    # Power & heat
    "electricity": ["1A1A1"],
    "power generation": ["1A1A1", "1A1A2", "1A1A3"],
    "heat plant": ["1A1A3"],
    "district heating": ["1A1A3"],
    # Refineries & fuels
    "refinery": ["1A1B"],
    "refining": ["1A1B"],
    "petroleum refining": ["1A1B"],
    # Industry
    "iron and steel": ["1A2A", "2C1"],
    "steelworks": ["1A2A", "2C1"],
    "cement": ["2A1"],
    "clinker": ["2A1"],
    "lime": ["2A2"],
    "chemicals": ["1A2C", "2B"],
    "pulp and paper": ["1A2D"],
    "paper mill": ["1A2D"],
    "mining": ["1A2I"],
    "quarrying": ["1A2I"],
    "aluminium": ["2C3"],
    # Transport
    "road transport": ["1A3B"],
    "motor gasoline": ["1A3B"],
    "diesel vehicles": ["1A3B"],
    "aviation": ["1A3A"],
    "shipping": ["1A3D"],
    "marine transport": ["1A3D"],
    # Buildings
    "residential": ["1A4B"],
    "household": ["1A4B"],
    "commercial": ["1A4A"],
    "service sector": ["1A4A"],
}

def _norm_number(s: str) -> float | None:
    try:
        if "," in s and "." in s:
            s2 = s.replace(".", "").replace(",", ".")
        elif "," in s and "." not in s:
            s2 = s.replace(",", ".")
        else:
            s2 = s
        return float(s2)
    except Exception:
        return None

def extract_basic_matches(text: str) -> List[MatchResult]:
    results: List[MatchResult] = []

    # (keep your DATE_PATTERN logic here as before…)

    # Strict rate matches
    for m in RATE_PATTERN_STRICT.finditer(text):
        value_raw = m.group(1)
        currency_raw = m.group(2)
        gas_unit = m.group(3)
        numeric = _norm_number(value_raw)

        c = currency_raw.upper()
        if c in {"€", "EURO"}:
            c_norm = "EUR"
        elif c in {"C$"}:
            c_norm = "CAD"
        elif c == "$":
            c_norm = "USD"  # naive default
        else:
            c_norm = c

        unit = "tCO2e" if gas_unit else "tCO2"
        pretty = f"{value_raw} {c_norm}/{unit}"

        results.append(
            MatchResult(
                field_name="rate",
                value=pretty,
                numeric_value=numeric,
                currency=c_norm,
                unit=unit,
                span=m.span(0),
                method="regex_rate_strict_v1",
                confidence=0.8,
            )
        )

    # Loose rate matches (no explicit currency close by)
    for m in RATE_PATTERN_LOOSE.finditer(text):
        value_raw = m.group(1)
        gas_unit = m.group(2)
        numeric = _norm_number(value_raw)

        unit = "tCO2e" if gas_unit else "tCO2"
        pretty = f"{value_raw} /{unit}"

        results.append(
            MatchResult(
                field_name="rate",
                value=pretty,
                numeric_value=numeric,
                currency=None,      # unknown here
                unit=unit,
                span=m.span(0),
                method="regex_rate_loose_v1",
                confidence=0.5,     # lower, needs human check
            )
        )

    return results

def extract_ipcc_matches(text: str) -> List[MatchResult]:
    results: List[MatchResult] = []
    lower = text.lower()
    seen: set[str] = set()

    for kw, codes in IPCC_KEYWORD_MAP.items():
        idx = lower.find(kw)
        if idx == -1:
            continue
        span = (idx, idx + len(kw))
        for code in codes:
            if code in seen:
                continue
            seen.add(code)
            results.append(
                MatchResult(
                    field_name="ipcc_category",
                    value=code,
                    numeric_value=None,
                    currency=None,
                    unit=None,
                    span=span,
                    method="keyword_ipcc_v1",
                    confidence=0.3,
                )
            )

    return results

def extract_all_matches(text: str) -> List[MatchResult]:
    out: List[MatchResult] = []
    out.extend(extract_basic_matches(text))
    out.extend(extract_ipcc_matches(text))
    return out
