from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import yaml

from common.schema import build_sources_register, merge_artifact_hashes, write_seed_bundle
from common.artifacts import download_artifacts
from common.sources_seed import build_acts_seed_from_sources
from tax_schemes.swe_tax.parsers.parse_rates import extract_skatteverket_rates
from tax_schemes.swe_tax.parsers.parse_6akap import extract_6akap_from_sfs_pdf, apply_overrides

SCHEME_ID = "swe_tax"

def _base_acts(cfg: dict) -> pd.DataFrame:
    acts = [
        {
            "act_id":"SE_LSE_1994_1776",
            "jurisdiction":"Sweden",
            "instrument_name":"Lag (1994:1776) om skatt på energi (LSE)",
            "instrument_type":"Act",
            "citation":"SFS 1994:1776",
            "adoption_date":"",
            "publication_date":"",
            "entry_into_force":"1995-01-01",
            "source_url": cfg["artifacts"]["lse_consolidated_html"]["url"],
        },
        {
            "act_id":"SE_SKV_HIST_TOM_2024_12_31",
            "jurisdiction":"Sweden",
            "instrument_name":"Skatteverket – Skattesatser t.o.m. 2024-12-31",
            "instrument_type":"Administrative PDF",
            "citation":"Skatteverket rate tables (energiskatt/koldioxidskatt by fuel & effective date)",
            "adoption_date":"",
            "publication_date":"",
            "entry_into_force":"",
            "source_url": cfg["artifacts"]["skatteverket_rates_pdf"]["url"],
        },
    ]
    for a in cfg.get("amending_acts", []) or []:
        acts.append({
            "act_id": a["act_id"],
            "jurisdiction":"Sweden",
            "instrument_name": f"LSE amendment ({a['act_id']})",
            "instrument_type":"Amending act (SFS)",
            "citation": a["act_id"],
            "adoption_date":"",
            "publication_date":"",
            "entry_into_force": a.get("entry_into_force",""),
            "source_url": a["url"],
        })
    return pd.DataFrame(acts)

def _provisions() -> pd.DataFrame:
    return pd.DataFrame([
        {"provision_id":"SE_LSE_2KAP_CO2","act_id":"SE_LSE_1994_1776","provision_ref":"2 kap.","chapter_ref":"2 kap.","title":"CO2 tax on fuels (fuel-unit schedules)","change_type":"baseline","change_note":"Numeric rates extracted from Skatteverket tables."},
        {"provision_id":"SE_LSE_6AKAP","act_id":"SE_LSE_1994_1776","provision_ref":"6 a kap.","chapter_ref":"6 a kap.","title":"Use-based exemptions/reductions","change_type":"baseline","change_note":"Extract as time series from SFS amending acts (best-effort + overrides)."},
        {"provision_id":"SE_LSE_7KAP","act_id":"SE_LSE_1994_1776","provision_ref":"7 kap.","chapter_ref":"7 kap.","title":"Deductions/repayments mechanics","change_type":"baseline","change_note":"Mechanism for applying exemptions."},
        {"provision_id":"SE_SKV_RATE_TABLES","act_id":"SE_SKV_HIST_TOM_2024_12_31","provision_ref":"Skatteverket tables","chapter_ref":"","title":"Fuel rate tables by effective date","change_type":"rate_series","change_note":"Authoritative numeric source for fuel-unit CO2 tax values."},
    ])

def build_fuel_unit_rates(rates_df: pd.DataFrame) -> pd.DataFrame:
    df = rates_df.copy()
    df["fuel_key"] = (df["category"].fillna("") + " | " + df["subcat"].fillna("") + " | " + df["fuel_name"].fillna("")).str.strip()
    df["effective_from_dt"] = pd.to_datetime(df["effective_from"], errors="coerce")
    df = df.sort_values(["fuel_key","effective_from_dt"]).reset_index(drop=True)
    df["effective_to_dt"] = df.groupby("fuel_key")["effective_from_dt"].shift(-1) - pd.Timedelta(days=1)
    df["effective_to"] = df["effective_to_dt"].dt.strftime("%Y-%m-%d")
    df.loc[df["effective_to_dt"].isna(), "effective_to"] = ""

    import re
    def fuel_id(s: str) -> str:
        fid = re.sub(r"[^A-Z0-9]+","_", s.upper()).strip("_")
        return fid[:64]

    out = pd.DataFrame({
        "fuel_id": df["fuel_key"].apply(fuel_id),
        "category": df["category"],
        "subcat": df["subcat"],
        "fuel_variant": df["fuel_name"],
        "co2_tax_value": df["co2_tax"].astype(float),
        "energy_tax_value": df["energy_tax"].astype(float),
        "rate_unit": df["unit"],
        "effective_from": df["effective_from"],
        "effective_to": df["effective_to"],
        "source_act_id": "SE_SKV_HIST_TOM_2024_12_31",
        "source_page": df.get("page", ""),
        "notes": "Extracted from Skatteverket PDF; CO2 tax component is koldioxidskatt."
    })
    out = out.drop_duplicates(subset=["fuel_id","effective_from","rate_unit","co2_tax_value","energy_tax_value"])
    return out

def build_fuel_map(fuel_unit_rates: pd.DataFrame) -> pd.DataFrame:
    m = (fuel_unit_rates[["fuel_id","category","subcat","fuel_variant","rate_unit"]]
         .drop_duplicates()
         .rename(columns={"rate_unit":"unit"}))
    m["kn_numbers"] = ""
    m["tco2_per_unit"] = ""
    m["notes"] = "Populate KN numbers and emission factors if needed; numeric fuel-unit CO2 tax is in fuel_unit_rates."
    return m[["fuel_id","category","subcat","fuel_variant","unit","kn_numbers","tco2_per_unit","notes"]]

def build_6akap_timeseries(cfg: dict, artifacts_dir: Path) -> pd.DataFrame:
    recs = []
    for act in cfg.get("amending_acts", []) or []:
        url = act["url"]
        act_id = act["act_id"]
        eff = act.get("entry_into_force","")
        # only PDFs parsed here; HTML handled via overrides/manual
        if url.lower().endswith(".pdf"):
            pdf_path = artifacts_dir / f"{act_id}.pdf"
            df = extract_6akap_from_sfs_pdf(pdf_path, act_id=act_id, effective_from=eff)
            recs.append(df)
    out = pd.concat(recs, ignore_index=True) if recs else pd.DataFrame()

    # Optional overrides inside jurisdiction folder
    overrides = Path(__file__).resolve().parent / "config" / "six_a_kap_overrides.yml"
    out = apply_overrides(out, overrides)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", default=str(Path(__file__).resolve().parent / "config" / "sources.yml"))
    ap.add_argument("--download-artifacts", action="store_true")
    ap.add_argument("--with-6akap", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    acts = build_acts_seed_from_sources(
        Path(__file__).resolve().parent / "acts_sources_map.csv",
        fallback=_base_acts(cfg),
    )
    provisions = _provisions()

    out_dir = Path(args.out)
    artifacts_dir = out_dir / "artifacts"
    artifact_map = pd.DataFrame()
    if args.download_artifacts:
        artifact_map = download_artifacts(cfg, artifacts_dir)

    # rates extraction
    pdf_path = artifacts_dir / cfg["artifacts"]["skatteverket_rates_pdf"]["filename"]
    parsed = extract_skatteverket_rates(pdf_path)
    fuel_unit_rates = build_fuel_unit_rates(parsed)
    fuel_map = build_fuel_map(fuel_unit_rates)

    # Minimal core tables
    rates = pd.DataFrame([])  # optional headline anchors can be added as needed
    coverage = pd.DataFrame([
        {"coverage_id":"SE_COV_FUELS_GENERAL","provision_id":"SE_LSE_2KAP_CO2","scope_type":"fuel_use","scope_subject":"Most fuels used for propulsion/heating",
         "condition_text":"Energiskatt and koldioxidskatt apply to most taxable fuels unless exempt/reduced under 6 a kap.","effective_from":"1991-01-01","effective_to":"","notes":"See Skatteverket guidance."}
    ])
    exemptions = pd.DataFrame([
        {"exemption_id":"SE_EX_6AKAP_RULESET","provision_id":"SE_LSE_6AKAP","exemption_type":"rule_catalog",
         "description_text":"Use-based exemptions/reductions are defined in 6 a kap. and applied via deductions/repayments.",
         "condition_text":"See six_a_kap_timeseries_sweden_seed.csv (if generated) and/or manual encoding.","effective_from":"1995-01-01","effective_to":"","notes":"Populate detailed items from SFS PDFs + consolidated text."}
    ])

    sources = build_sources_register(acts)
    sources = merge_artifact_hashes(sources, artifact_map)

    tables = {
        "acts": acts,
        "provisions": provisions,
        "rates": rates,
        "coverage": coverage,
        "exemptions": exemptions,
        "sources": sources,
        "fuel_unit_rates": fuel_unit_rates,
        "fuel_map": fuel_map,
    }

    if args.with_6akap:
        sixakap = build_6akap_timeseries(cfg, artifacts_dir)
        tables["six_a_kap_timeseries"] = sixakap

    write_seed_bundle(out_dir, tables, prefix=SCHEME_ID)

if __name__ == "__main__":
    main()
