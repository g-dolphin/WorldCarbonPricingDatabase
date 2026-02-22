# WCPD extractors (unified)

This repo includes:
- Manual-series seed generators for: Canada, Japan, South Africa, France CCE, Spain F-gas.
- A parser-based extractor for Sweden (Skatteverket PDF + SFS 6 a kap best-effort).

New feature:
- `--download-artifacts` downloads declared artifacts and automatically fills:
  - sources_<country>.csv: local_artifact, content_hash_sha256

Integration notes:
- Each scheme can define an explicit `acts_sources_map.csv` under `tax_schemes/<scheme_id>/`.
- That mapping is merged with `_raw/sources/sources.csv` to populate `acts_<scheme_id>_seed.csv`
  with a `source_id` column (and `source_url` filled from sources when missing).
- Run the standalone pipeline with:
- `python _code/_tax_processing/run_pipeline.py --out-root _raw/_preproc/_preproc_tax`

Rate normalization (LCU/tCO2e):
- The seed writer now adds derived columns to all `rates_*_seed.csv` files:
  - `rate_value_tco2e`, `rate_unit_tco2e`, `tco2e_method`, `tco2e_notes`
- If a rate is already expressed per tCO2e, it is copied directly.
- If a rate is expressed per physical unit (e.g., `LCU/l`, `LCU/kg`), it is converted using
  IPCC 2006 default emission factors. The conversion layer is global and applies to all schemes.
- Conversions use IPCC 2006 default CO2 emission factors (via EU ETS Annex VI table) and default
  densities for gasoline/diesel when needed for `per liter` rates.

Generated: 2026-02-21
