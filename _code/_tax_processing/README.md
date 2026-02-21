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
  - `python _code/_tax_processing/run_pipeline.py --out-root _raw/_preproc_tax`

Generated: 2026-02-21
