# WCPD update workflow (any year)

This is a short, year-agnostic checklist for updating the dataset. It focuses on the files you edit under `_raw/`.

## 0) Discover potential sources (optional, human-in-the-loop)
- `_code/_sources_extraction/discover.py` (sitemap/page-link/search API discovery)
- `_raw/_sources/discovery_candidates.csv` (candidate URLs for review)
- `_raw/_sources/discovery_seeds.csv` (optional extra seed URLs)
- `_raw/_sources/discovery_queries.csv` (optional search queries for SerpAPI)
- Review and promote discovery candidates in **Manage sources** (adds to `sources.csv`)

## 1) Update upstream sources (registry + artifacts)
- `_raw/_sources/sources.csv` (source registry for fetcher/app)
- `_raw/_sources/sources_bibliography.csv` (references for the sources)
- `_raw/_sources/sources_schema.csv` (schema/fields for the sources file)
- `_raw/_sources/html/` and `_raw/_sources/pdf/` (fetched artifacts)
- `_raw/_sources/text/` (parsed text from artifacts)
- `_raw/_sources/meta/raw_artifacts.csv` (artifact log)

## 2) Run extraction + review (candidate pipeline)
- `_raw/_sources/cp_candidates.csv` (extracted candidates)
- `_raw/_sources/cp_review_state.csv` (review decisions)
- `_raw/_sources/upstream_prices.csv` (accepted price candidates)
- `_raw/_sources/upstream_start_dates.csv` (accepted start-date candidates)
- `_raw/_sources/upstream_coverage_ipcc.csv` (accepted IPCC coverage candidates)

## 2b) Candidate-to-seed mapping (new, optional)
These files are seed-aligned candidates produced after review. They are not used by builds until promoted into `/seeds`.

Tax candidates
- `_raw/_preproc/_preproc_tax/candidates/<scheme_id>/rates_<scheme_id>_candidate.csv`
- `_raw/_preproc/_preproc_tax/candidates/<scheme_id>/coverage_<scheme_id>_candidate.csv`
- `_raw/_preproc/_preproc_tax/candidates/<scheme_id>/provisions_<scheme_id>_candidate.csv`

ETS candidates
- `_raw/_preproc/_preproc_ets/candidates/<scheme_id>/auctions_<scheme_id>_candidate.csv`
- `_raw/_preproc/_preproc_ets/candidates/<scheme_id>/coverage_<scheme_id>_candidate.csv`
- `_raw/_preproc/_preproc_ets/candidates/<scheme_id>/provisions_<scheme_id>_candidate.csv`

Seed and output relationship
- `/seeds` are the approved, structured inputs for each scheme.
- `/out` are the compiled outputs derived from `/seeds`.
- `/candidates` are draft rows awaiting review and promotion into `/seeds`.

## 3) Encode updates into the raw data files
These are the files you ultimately update to move the dataset forward for the target year.

Prices and tax rates
- `_raw/price/*.csv` (per-instrument price time series, incl. taxes and ETS prices)
- `_raw/price/_preproc/rate_changes.csv` (optional, tax rate change periods for pro‑rata averages)
- `_raw/price/_preproc/annual_rates.csv` (optional, computed annual averages)

Coverage / scope (what is covered)
- `_raw/scope/ets/ets_scope_CO2.py`
- `_raw/scope/ets/ets_scope_CH4.py`
- `_raw/scope/ets/ets_scope_N2O.py`
- `_raw/scope/ets/ets_scope_Fgases.py`
- `_raw/scope/ets/ets_scope_exceptions.py`

Coverage factors (if partial coverage or exemptions require it)
- `_raw/coverageFactor/CO2/*.csv`
- `_raw/coverageFactor/CH4/*.csv`
- `_raw/coverageFactor/N2O/*.csv`

Price rebates / exemptions
- `_raw/priceRebates/tax/_price_exemptions_tax_CO2.py`
- `_raw/priceRebates/tax/_price_exemptions_tax_CH4.py`
- `_raw/priceRebates/tax/_price_exemptions_tax_N2O.py`

Overlaps between mechanisms (if new overlaps emerge)
- `_raw/overlap/overlap_mechanisms_CO2.csv`
- `_raw/overlap/overlap_mechanisms_CH4.csv`
- `_raw/overlap/overlap_mechanisms_N2O.csv`
- `_raw/overlap/overlap_mechanisms_F-GASES.csv`

Auxiliary scheme metadata (only if adding or renaming schemes)
- `_raw/_aux_files/scheme_description.csv`
