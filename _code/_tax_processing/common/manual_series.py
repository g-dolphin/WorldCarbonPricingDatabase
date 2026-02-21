from __future__ import annotations
from typing import Any, Dict, List
import pandas as pd

def build_rate_series(rows: List[Dict[str, Any]], provision_id: str, pollutant: str, unit: str, basis: str, method: str) -> pd.DataFrame:
    out = []
    for i, r in enumerate(rows, start=1):
        out.append({
            "rate_id": r.get("rate_id") or f"{provision_id}_{i}",
            "provision_id": provision_id,
            "pollutant": pollutant,
            "rate_value": r["rate_value"],
            "rate_unit": unit,
            "effective_from": r["effective_from"],
            "effective_to": r.get("effective_to",""),
            "rate_basis": basis,
            "method": method,
            "notes": r.get("notes",""),
        })
    return pd.DataFrame(out)
