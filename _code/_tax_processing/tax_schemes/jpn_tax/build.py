from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import yaml

from common.schema import build_sources_register, merge_artifact_hashes, write_seed_bundle
from common.manual_series import build_rate_series
from common.artifacts import download_artifacts
from common.sources_seed import build_acts_seed_from_sources

SCHEME_ID = "jpn_tax"

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

    coverage = pd.DataFrame(cfg.get("coverage", []))
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
