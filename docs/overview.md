# Overview

This repository contains the World Carbon Pricing Database (WCPD) pipeline, from upstream source discovery and extraction through curated raw inputs and compiled dataset outputs.

## High-level flow
1. **Discover sources (optional)**: generate candidate URLs with `_code/_sources_extraction/discover.py` and review in the **Manage sources** view. Results are stored in `_raw/sources/discovery_candidates.csv`.
2. **Fetch & extract**: fetch artifacts from `sources.csv`, parse them, and extract candidates into `_raw/sources/cp_candidates.csv`.
3. **Review**: confirm candidates in the Streamlit app and apply decisions to write `upstream_*.csv` outputs.
4. **Encode raw inputs**: update the curated `_raw/` price, scope, rebate, and coverage inputs.
5. **Compile**: build final datasets under `_dataset/` using `_code/_compilation/`.

## Key locations
- Upstream extraction + review: `_code/_sources_extraction/`
- Discovery outputs: `_raw/sources/discovery_candidates.csv`
- Source registry: `_raw/sources/sources.csv`
- Candidate review: `_raw/sources/cp_candidates.csv` and `_raw/sources/cp_review_state.csv`
- Curated raw inputs: `_raw/price`, `_raw/scope`, `_raw/coverageFactor`, `_raw/overlap`
- Dataset outputs: `_dataset/`

## Diagram
The full pipeline diagram is maintained in `_raw/_aux_files/wcpd_architecture.mmd`.
