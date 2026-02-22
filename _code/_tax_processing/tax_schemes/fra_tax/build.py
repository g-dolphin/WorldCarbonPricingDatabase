from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import yaml

from common.schema import build_sources_register, merge_artifact_hashes, write_seed_bundle
from common.manual_series import build_rate_series
from common.artifacts import download_artifacts
from common.sources_seed import build_acts_seed_from_sources

SCHEME_ID = "fra_tax"
IPCC_PATH = "/Users/geoffroydolphin/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv"

def _ipcc_codes(prefix: str) -> list[str]:
    try:
        df = pd.read_csv(IPCC_PATH)
    except Exception:
        return []
    return df[(df["ipcc_code"].str.startswith(prefix)) & (df["lowest_level"] == 1)]["ipcc_code"].tolist()

def _coverage_from_rates(rates: pd.DataFrame) -> pd.DataFrame:
    cols = ["coverage_id","provision_id","scope_type","scope_subject","condition_text","effective_from","effective_to","notes"]
    if rates.empty:
        return pd.DataFrame(columns=cols)
    periods = (
        rates[["effective_from","effective_to"]]
        .drop_duplicates()
        .fillna("")
        .to_records(index=False)
        .tolist()
    )
    ipcc_power = _ipcc_codes("1A1A")
    ipcc_industry = _ipcc_codes("1A2")
    ipcc_transport = _ipcc_codes("1A3")
    ipcc_other = _ipcc_codes("1A4")
    rows = []
    for eff_from, eff_to in periods:
        for code in ipcc_power + ipcc_industry + ipcc_transport + ipcc_other:
            rows.append({
                "coverage_id": f"FRA_COV_{code}_{eff_from}",
                "provision_id": "FR_CCE_VALUE",
                "scope_type": "ipcc_code",
                "scope_subject": code,
                "condition_text": "Carbon component applies to fossil energy products; ETS installations are exempt.",
                "effective_from": eff_from,
                "effective_to": eff_to,
                "notes": "Mapped to lowest-level IPCC energy categories (1A1A/1A2/1A3/1A4).",
            })
        for sector in ["power", "industry", "transport", "buildings"]:
            rows.append({
                "coverage_id": f"FRA_COV_SECTOR_{sector}_{eff_from}",
                "provision_id": "FR_CCE_VALUE",
                "scope_type": "sector",
                "scope_subject": sector,
                "condition_text": "Carbon component applies to fossil energy products; ETS installations are exempt.",
                "effective_from": eff_from,
                "effective_to": eff_to,
                "notes": "Broad sector tag.",
            })
    return pd.DataFrame(rows, columns=cols)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", default=str(Path(__file__).resolve().parent / "config" / "sources.yml"))
    ap.add_argument("--download-artifacts", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))

    acts = build_acts_seed_from_sources(
        Path(__file__).resolve().parent / "acts_sources_map.csv",
        fallback=pd.DataFrame(cfg.get("acts", [])),
    )
    provisions = pd.DataFrame(cfg["provisions"])
    meta = cfg["rate_series_meta"]
    rates = build_rate_series(cfg.get("rate_series", []), provision_id=meta["provision_id"],
                              pollutant=meta["pollutant"], unit=meta["unit"],
                              basis=meta["basis"], method=meta["method"])

    coverage_cfg = cfg.get("coverage", []) or []
    coverage = pd.DataFrame(coverage_cfg) if coverage_cfg else _coverage_from_rates(rates)
    exemptions = pd.DataFrame(cfg.get("exemptions", []))
    sources = build_sources_register(acts)

    artifact_map = pd.DataFrame()
    if args.download_artifacts:
        artifact_map = download_artifacts(cfg, Path(args.out) / "artifacts")
        sources = merge_artifact_hashes(sources, artifact_map)

    tables = {
        "acts": acts,
        "provisions": provisions,
        "rates": rates,
        "coverage": coverage,
        "exemptions": exemptions,
        "sources": sources,
    }

    for k, v in (cfg.get("extras", {}) or {}).items():
        tables[k] = pd.DataFrame(v)

    write_seed_bundle(args.out, tables, prefix=SCHEME_ID)

if __name__ == "__main__":
    main()
