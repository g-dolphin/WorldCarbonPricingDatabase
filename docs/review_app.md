# WCPD Review App (Streamlit) – User Guide

This document describes the Streamlit review app used to manage upstream sources and edit raw data files safely.

## Location
- App: `_code/_sources_extraction/review_app.py`
- Launch (local): `streamlit run _code/_sources_extraction/review_app.py`

## What the app does
The app is split into five main areas:
1. **Gap dashboard**: identify missing data by scheme/year/variable and jump to Review candidates with filters applied.
2. **Scheme intake**: review existing schemes and run SerpAPI searches for newly launched schemes.
3. **Review candidates**: review extracted candidates from fetched sources.
4. **Manage sources**: edit the upstream sources registry for the fetcher and promote discovery candidates.
5. **Raw editor**: write updates directly into raw data files (prices, scope, rebates) using timestamped output files for safety.

**How Review Candidates connects to Raw Editor**  
Reviewed values are saved to `_raw/sources/cp_review_state.csv`. To turn those decisions into structured outputs, run `_code/_sources_extraction/apply_review.py`, which writes:
- `_raw/sources/upstream_prices.csv`
- `_raw/sources/upstream_start_dates.csv`
- `_raw/sources/upstream_coverage_ipcc.csv`

These outputs include the reviewed **GHG**, **fuel/product**, and **IPCC** selections (when provided). They are **inputs for manual encoding** in the Raw editor (prices/scope/rebates). The app does not auto-write to `_raw/price` or `_raw/scope` from review decisions.

## Data paths used by the app
**Upstream extraction** (`_raw/sources/`)
- `cp_candidates.csv`: extracted candidates for review.
- `cp_review_state.csv`: review decisions and edits.
- `sources.csv`: upstream source registry.
- `discovery_candidates.csv`: candidate URLs found by discovery (optional).
- `meta/raw_artifacts.csv`: log of fetched artifacts.

**Source discovery inputs (optional)**
- `_raw/sources/discovery_seeds.csv`: extra seed URLs for discovery.
- `_raw/sources/discovery_queries.csv`: search queries for SerpAPI (if enabled).
 - `SERPAPI_KEY` (env var): SerpAPI key used by Scheme intake and discovery search channel.

**Scheme metadata**
- `_raw/_aux_files/scheme_description.csv`: scheme list and metadata.

**Raw data files edited by the app**
- Prices: `_raw/price/*.csv`
- Scope (ETS): `_raw/scope/ets/ets_scope_<GAS>.py`
- Scope (Taxes): `_raw/scope/tax/taxes_scope_<GAS>.py`
- Price rebates: `_raw/priceRebates/tax/_price_exemptions_tax_<GAS>.py`

**Tax rate preprocessing (pro rata)**
- `_raw/price/_preproc/rate_changes.csv`: rate change periods
- `_raw/price/_preproc/annual_rates.csv`: annual rates in tax price format

**Review-only**
- Coverage factors: `_raw/coverageFactor/<GAS>/*.csv`
- Overlaps: `_raw/overlap/overlap_mechanisms_<GAS>.csv`

## How to use the app
### 1) Gap dashboard
- Check missing raw inputs (price, scope, coverageFactor) for a target year and gas.
- Click **Open in Review candidates** on a missing row to pre-fill filters.

### 2) Scheme intake
- Review the scheme list and whether each scheme appears in the dataset.
- Run fixed SerpAPI query templates to identify new schemes (manual action only).
- Generate a targeted `discovery_queries.csv` tied to scheme names and keywords.

### 3) Review candidates
- **Input**: `_raw/sources/cp_candidates.csv`
- **Output**: `_raw/sources/cp_review_state.csv`
- Use filters for jurisdiction, scheme, field, and confidence.
- Save decisions as accepted/rejected/skipped. Edits are stored per candidate.
- Use the **Applies to** selectors (GHG, fuel/product, IPCC category) to scope each accepted value.
- For **tax rate** entries, you can optionally record **Effective date** and **End date** to support pro‑rata annual averages.

### 4) Manage sources
- **Input/Output**: `_raw/sources/sources.csv`
- Add or edit upstream sources used by the fetcher.
- URL validation is optional.
- **Discovery candidates**: review `_raw/sources/discovery_candidates.csv` and promote rows into `sources.csv`.
  - The table is row-selectable and searchable.
  - A **promoted** flag indicates if the candidate URL already exists in `sources.csv`.
  - The promote form uses controlled pickers for **Jurisdiction** and **Instrument ID** (with a **New instrument** toggle).

### 4a) Source discovery (optional, upstream of Manage sources)
Run discovery to generate `discovery_candidates.csv`:
- `python3 -m _code._sources_extraction.discover --years 2025,2026`
- With SerpAPI (optional): `--search-provider serpapi` (uses `SERPAPI_KEY`)
You can also generate `discovery_queries.csv` from **Scheme intake** to make discovery more targeted.

### 5) Raw editor
The raw editor writes new files with timestamped names (YYYYMMDD) and provides a **promote** flow to replace the canonical file.

#### Prices
- **Edits**: `_raw/price/<scheme_id>_prices.csv`
- **Key fields**: `scheme_id`, `year`, `ghg`, `product`, `rate`, `currency_code`, `source`, `comment`
- The app warns only when a **non-empty** existing entry conflicts with the new value.

#### Scope (ETS and Taxes)
- **Edits**:
  - ETS: `_raw/scope/ets/ets_scope_<GAS>.py`
  - Taxes: `_raw/scope/tax/taxes_scope_<GAS>.py`
- Per-year UI with multi-select **IPCC codes** and **fuels** (fuels only for taxes).
- **Scheme type** is determined by where the `scheme_id` exists (ETS or tax scope file).

#### Price rebates / exemptions
- **Edits**: `_raw/priceRebates/tax/_price_exemptions_tax_<GAS>.py`
- Per-year UI for jurisdiction, IPCC, fuels, and rebate value.
- New entries are appended as new exemption blocks; a warning appears on conflicts.

#### Coverage factors (review-only)
- Displays the current CSV contents from `_raw/coverageFactor/<GAS>`.

#### Overlaps (review-only)
- Displays `_raw/overlap/overlap_mechanisms_<GAS>.csv` for validation.

## Promote workflow (safe writes)
When you write from the Raw editor:
1. The app generates a **timestamped** file (e.g., `ets_scope_CO2_20250308.py`).
2. The canonical file is unchanged.
3. Use the **Promote timestamped file** section to replace the canonical file.
4. A **diff preview** is shown before promotion.

## Overwrite warnings
Warnings appear only if the existing value is **non-empty** and differs from the new value. A confirmation checkbox is required before overwriting.

## Notes
- Jurisdiction lists are treated as user-reviewed: they are editable, but expected to change less frequently than other parameters.
- Overlap files are derived from scope/coverage factors; edits should be done upstream in scope/coverage factor inputs, not by editing overlap CSVs directly.
