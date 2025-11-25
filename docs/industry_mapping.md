# Industry Mapping (`_code/_industryMapping`)

The `_industryMapping` folder contains scripts aimed at mapping WCPD prices from emission categories to economic industries.

## `estat_nace_prices.py`

This script is currently a **design skeleton** rather than a complete implementation. It outlines a workflow to compute **emissions-weighted industry-level carbon prices**.

Planned steps (from comments and structure):

1. **Load air emissions by industry**  
   - Use Eurostat environmental accounts, with emissions reported by NACE industry.

2. **Load national accounts**  
   - Use Eurostat national accounts data (e.g. value added or output by NACE).

3. **Define mapping between IEA/IPCC and NACE**  
   - Establish 1–1 and 1–N mappings from IEA/IPCC energy/emission categories to NACE industries.
   - For 1–N splits, use an allocation rule inspired by FIGARO (multi-regional input-output) methodology.

4. **Compute distribution keys**  
   - For each IEA/IPCC category, compute weights across NACE industries using indicators such as:
     - Sectoral energy use,
     - Sectoral emissions,
     - Sectoral value added.

5. **Attach WCPD emissions prices to IEA/IPCC categories**  
   - Link WCPD prices by sector and jurisdiction to the IEA/IPCC categories used above.

6. **Allocate to industries and aggregate**  
   - Use the distribution keys to allocate emissions and prices to NACE industries.
   - Compute emissions-weighted average prices by NACE code.
   - Fall back to more aggregate prices where detailed splits are not available.

Because the implementation is mostly comments at present, this module mainly documents the intended methodology and data dependencies for future work.
