from __future__ import annotations

import datetime
import re
from typing import Dict
import pandas as pd

def host(url: str) -> str:
    url = str(url or "")
    return re.sub(r"^https?://([^/]+)/.*$", r"\1", url) if url.startswith("http") else ""

def build_sources_register(acts: pd.DataFrame, retrieved_date: str | None = None, retrieval_method: str = "web (candidate review)") -> pd.DataFrame:
    if retrieved_date is None:
        retrieved_date = datetime.date.today().isoformat()
    out = acts.copy()
    out["source_host"] = out["source_url"].fillna("").apply(host)
    out["retrieved_date"] = retrieved_date
    out["retrieval_method"] = retrieval_method
    out["content_hash_sha256"] = ""
    out["local_artifact"] = ""
    out["notes"] = "Populate hash + local artifact after storing authoritative snapshot."
    cols = ["jurisdiction","act_id","instrument_name","instrument_type","citation","source_url",
            "source_host","retrieved_date","retrieval_method","content_hash_sha256","local_artifact","notes"]
    return out[cols]

def merge_artifact_hashes(sources: pd.DataFrame, artifact_map: pd.DataFrame) -> pd.DataFrame:
    """Merge content_hash_sha256/local_artifact into sources by act_id, with fallback matching on source_url."""
    if artifact_map is None or artifact_map.empty:
        return sources
    out = sources.copy()
    # primary merge by act_id where act_id is provided
    m = artifact_map[artifact_map["act_id"].astype(str).str.len() > 0].drop_duplicates("act_id", keep="last")
    out = out.merge(m[["act_id","local_artifact","content_hash_sha256"]], on="act_id", how="left", suffixes=("","_new"))
    for col in ["local_artifact","content_hash_sha256"]:
        out[col] = out[f"{col}_new"].combine_first(out[col])
        out.drop(columns=[f"{col}_new"], inplace=True)
    # secondary merge by source_url
    u = artifact_map.drop_duplicates("source_url", keep="last")
    out = out.merge(u[["source_url","local_artifact","content_hash_sha256"]], on="source_url", how="left", suffixes=("","_url"))
    for col in ["local_artifact","content_hash_sha256"]:
        out[col] = out[f"{col}_url"].combine_first(out[col])
        out.drop(columns=[f"{col}_url"], inplace=True)
    return out

def write_seed_bundle(out_dir, tables: Dict[str, pd.DataFrame], prefix: str) -> None:
    from pathlib import Path
    tables = _enrich_coverage_tables(tables, prefix)
    tables = _enrich_rate_tables(tables)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    required = [
        ("acts", f"acts_{prefix}_seed.csv"),
        ("provisions", f"provisions_{prefix}_seed.csv"),
        ("rates", f"rates_{prefix}_seed.csv"),
        ("coverage", f"coverage_{prefix}_seed.csv"),
        ("exemptions", f"exemptions_{prefix}_seed.csv"),
        ("sources", f"sources_{prefix}.csv"),
    ]
    for key, fname in required:
        df = tables.get(key)
        if df is None:
            raise ValueError(f"Missing required table: {key}")
        df.to_csv(out_dir/fname, index=False)

    for key, df in tables.items():
        if key in {"acts","provisions","rates","coverage","exemptions","sources"}:
            continue
        df.to_csv(out_dir/f"{key}_{prefix}_seed.csv", index=False)


def _enrich_coverage_tables(tables: Dict[str, pd.DataFrame], prefix: str) -> Dict[str, pd.DataFrame]:
    coverage = tables.get("coverage")
    rates = tables.get("rates")
    if coverage is None or rates is None:
        return tables
    if coverage.empty and rates.empty:
        return tables
    cov = coverage.copy()

    cov = _add_sector_rows_from_ipcc(cov, prefix)
    cov = _add_fuel_rows_from_rates(cov, rates, prefix)

    tables = dict(tables)
    tables["coverage"] = cov.reset_index(drop=True)
    return tables


def _enrich_rate_tables(tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    rates = tables.get("rates")
    if rates is None or rates.empty:
        return tables

    rates = rates.copy()
    for col in ["rate_value_tco2e", "rate_unit_tco2e", "tco2e_method", "tco2e_notes"]:
        if col not in rates.columns:
            rates[col] = ""

    def _currency_from_unit(unit: str) -> str:
        unit = str(unit or "").strip()
        if "/" in unit:
            return unit.split("/", 1)[0].strip()
        if " per " in unit:
            return unit.split(" per ", 1)[0].strip()
        return unit

    def _text_blob(row: pd.Series) -> str:
        parts = []
        for c in ["pollutant", "rate_basis", "notes"]:
            if c in row and pd.notna(row[c]):
                parts.append(str(row[c]))
        return " ".join(parts).lower()

    fuel_factors = {
        # IPCC 2006 GL factors via EU ETS Annex VI (tCO2/TJ, TJ/Gg)
        "motor_gasoline": {"ef_tco2_tj": 69.3, "ncv_tj_gg": 44.3, "density_kg_l": 0.7407},
        "gas_diesel_oil": {"ef_tco2_tj": 74.1, "ncv_tj_gg": 43.0, "density_kg_l": 0.8439},
        "residual_fuel_oil": {"ef_tco2_tj": 77.4, "ncv_tj_gg": 40.4, "density_kg_l": 0.99},
        "lpg": {"ef_tco2_tj": 63.1, "ncv_tj_gg": 47.3, "density_kg_l": None},
        # IPCC 2006 default mass-based factor (kg CO2/kg)
        "natural_gas": {"kgco2_per_kg": 2.6928, "density_kg_l": None},
        # IPCC 2006 default factors for solid fuels (EU ETS Annex VI)
        "coal": {"ef_tco2_tj": 94.6, "ncv_tj_gg": 25.8, "density_kg_l": None},
        "petroleum_coke": {"ef_tco2_tj": 97.5, "ncv_tj_gg": 32.5, "density_kg_l": None},
    }

    fuel_keywords = [
        ("motor_gasoline", [r"gasoline", r"petrol", r"bens[ií]n", r"benz[ií]n[ëe]"]),
        ("gas_diesel_oil", [r"diesel", r"gasoil", r"gazoil", r"gazoilin", r"d[ií]sel", r"gas- og d[ií]silol[ií]a", r"solarin", r"\bsolar\b"]),
        ("residual_fuel_oil", [r"residual fuel", r"heavy fuel", r"fuel oil", r"brennsluol[ií]u", r"raskas polttoöljy", r"mazut"]),
        ("gas_diesel_oil", [r"kerosene", r"vajgur"]),
        ("lpg", [r"lpg", r"liquefied petroleum", r"jar[ðd]ol[ií]ugas"]),
        ("natural_gas", [r"natural gas", r"gaz naturel", r"loftkennt kolvatnsefni"]),
        ("coal", [r"coal", r"qymyr"]),
        ("petroleum_coke", [r"petroleum coke", r"koks nafte"]),
    ]

    def _infer_fuel_key(text: str) -> str | None:
        for key, pats in fuel_keywords:
            if any(re.search(pat, text) for pat in pats):
                return key
        return None

    for idx, row in rates.iterrows():
        unit = str(row.get("rate_unit", "")).lower()
        if "tco2" in unit:
            rates.at[idx, "rate_value_tco2e"] = row.get("rate_value", "")
            cur = _currency_from_unit(row.get("rate_unit", ""))
            rates.at[idx, "rate_unit_tco2e"] = f"{cur}/tCO2e" if cur else "tCO2e"
            rates.at[idx, "tco2e_method"] = "direct"
            rates.at[idx, "tco2e_notes"] = "Rate already expressed per tCO2e."
            continue

        text = _text_blob(row)
        fuel_key = _infer_fuel_key(text)
        if not fuel_key:
            code = str(row.get("pollutant", "")).strip().upper()
            code_map = {
                "K2": "gas_diesel_oil",
                "K3": "motor_gasoline",
                "K5": "residual_fuel_oil",
                "K6": "natural_gas",
            }
            fuel_key = code_map.get(code)
        if not fuel_key:
            continue
        factor = fuel_factors.get(fuel_key, {})
        kgco2_per_kg = factor.get("kgco2_per_kg")
        if kgco2_per_kg is None:
            ef = factor.get("ef_tco2_tj")
            ncv = factor.get("ncv_tj_gg")
            if ef and ncv:
                kgco2_per_kg = (ef * ncv) / 1000.0
        if kgco2_per_kg is None:
            continue

        cur = _currency_from_unit(row.get("rate_unit", ""))
        if unit.endswith("/kg") or unit.endswith("per kg"):
            val = row.get("rate_value")
            if pd.notna(val):
                rates.at[idx, "rate_value_tco2e"] = float(val) / kgco2_per_kg * 1000.0
                rates.at[idx, "rate_unit_tco2e"] = f"{cur}/tCO2e" if cur else "tCO2e"
                rates.at[idx, "tco2e_method"] = "ipcc_default_mass"
                rates.at[idx, "tco2e_notes"] = f"Converted using IPCC 2006 default factors for {fuel_key}."
            continue

        if unit.endswith("/l") or unit.endswith("/liter") or unit.endswith("/litre") or unit.endswith("/lítra"):
            density = factor.get("density_kg_l")
            if density is None:
                continue
            val = row.get("rate_value")
            if pd.notna(val):
                kgco2_per_l = kgco2_per_kg * density
                rates.at[idx, "rate_value_tco2e"] = float(val) / kgco2_per_l * 1000.0
                rates.at[idx, "rate_unit_tco2e"] = f"{cur}/tCO2e" if cur else "tCO2e"
                rates.at[idx, "tco2e_method"] = "ipcc_default_mass_density"
                rates.at[idx, "tco2e_notes"] = f"Converted using IPCC 2006 default factors for {fuel_key} with default density."

    tables = dict(tables)
    tables["rates"] = rates
    return tables


def _add_sector_rows_from_ipcc(cov: pd.DataFrame, prefix: str) -> pd.DataFrame:
    if cov.empty:
        return cov
    if "scope_type" not in cov.columns or "scope_subject" not in cov.columns:
        return cov

    def ipcc_to_sector(code: str) -> str | None:
        code = str(code or "")
        if code.startswith("1A1"):
            return "power"
        if code.startswith("1A2") or code.startswith("2"):
            return "industry"
        if code.startswith("1A3"):
            return "transport"
        if code.startswith("1A4"):
            return "buildings"
        if code.startswith("1A5"):
            return "other_energy"
        if code.startswith("1B"):
            return "energy"
        if code.startswith("3"):
            return "afolu"
        if code.startswith("4"):
            return "waste"
        return None

    ipcc_rows = cov[cov["scope_type"] == "ipcc_code"].copy()
    if ipcc_rows.empty:
        return cov

    rows = []
    seen = set()
    for _, row in ipcc_rows.iterrows():
        sector = ipcc_to_sector(row.get("scope_subject", ""))
        if not sector:
            continue
        eff_from = row.get("effective_from", "")
        eff_to = row.get("effective_to", "")
        eff_from = "" if pd.isna(eff_from) else eff_from
        eff_to = "" if pd.isna(eff_to) else eff_to
        key = (row.get("provision_id", ""), sector, eff_from, eff_to)
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "coverage_id": f"{prefix.upper()}_COV_SECTOR_{sector}_{eff_from}_{eff_to or 'open'}",
            "provision_id": row.get("provision_id", ""),
            "scope_type": "sector",
            "scope_subject": sector,
            "condition_text": "Sector inferred from IPCC category coverage.",
            "effective_from": eff_from,
            "effective_to": eff_to,
            "notes": "Derived sector tag from IPCC code coverage.",
        })

    if not rows:
        return cov

    new = pd.DataFrame(rows)
    key_cols = ["provision_id","scope_type","scope_subject","effective_from","effective_to"]
    existing = cov[key_cols].fillna("").astype(str)
    new = new[~new[key_cols].fillna("").astype(str).apply(tuple, axis=1).isin(existing.apply(tuple, axis=1))]
    if new.empty:
        return cov
    return pd.concat([cov, new], ignore_index=True)


def _add_fuel_rows_from_rates(cov: pd.DataFrame, rates: pd.DataFrame, prefix: str) -> pd.DataFrame:
    if rates.empty:
        return cov
    text_cols = [c for c in ["pollutant", "rate_basis", "notes"] if c in rates.columns]
    if not text_cols:
        return cov
    tmp = rates.copy()
    tmp["_text"] = (
        tmp[text_cols]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )

    fuel_map = {
        "oil": [
            r"\\boil\\b",
            r"petrol",
            r"gasoline",
            r"diesel",
            r"gasoil",
            r"fuel oil",
            r"kerosene",
            r"jet fuel",
            r"fioul",
            r"gazole",
            r"essence",
            r"bens[ií]n",
            r"d[ií]sil",
            r"brennsluol[ií]u",
            r"liquid fuels?",
            r"lpg",
        ],
        "natural_gas": [
            r"natural gas",
            r"gaz naturel",
            r"lng",
            r"cng",
            r"jar[ðd]ol[ií]ugas",
            r"loftkennt kolvatnsefni",
        ],
        "coal": [
            r"\\bcoal\\b",
            r"lignite",
            r"coke",
            r"anthracite",
            r"peat",
            r"briquette",
            r"solid fuels?",
            r"charbon",
        ],
    }

    rows = []
    for (prov_id, eff_from, eff_to), group in tmp.groupby(["provision_id","effective_from","effective_to"], dropna=False):
        text = " ".join(group["_text"].tolist())
        detected = []
        for fuel, patterns in fuel_map.items():
            if any(re.search(pat, text) for pat in patterns):
                detected.append(fuel)
        if not detected:
            continue
        eff_from = "" if pd.isna(eff_from) else eff_from
        eff_to = "" if pd.isna(eff_to) else eff_to
        suffix = eff_to if eff_to else "open"
        for fuel in sorted(set(detected)):
            rows.append({
                "coverage_id": f"{prefix.upper()}_COV_FUEL_{fuel}_{eff_from}_{suffix}",
                "provision_id": prov_id,
                "scope_type": "fuel_type",
                "scope_subject": fuel,
                "condition_text": "Fuel coverage inferred from rate descriptions.",
                "effective_from": eff_from,
                "effective_to": eff_to,
                "notes": "Derived from rate text (pollutant/rate_basis/notes) via keyword matching.",
            })

    if not rows:
        return cov

    new = pd.DataFrame(rows)
    key_cols = ["provision_id","scope_type","scope_subject","effective_from","effective_to"]
    existing = cov[key_cols].fillna("").astype(str)
    new = new[~new[key_cols].fillna("").astype(str).apply(tuple, axis=1).isin(existing.apply(tuple, axis=1))]
    if new.empty:
        return cov
    return pd.concat([cov, new], ignore_index=True)
