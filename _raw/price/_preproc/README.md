# Tax Rate Preprocessing (Pro Rata)

This folder stores inputs used to compute **pro‑rated annual average** carbon tax rates when rates change within a year.

## Inputs
- `rate_changes.csv` — normalized rate‑change events (one row per period).
- `_source_xlsx/` — legacy spreadsheets migrated for reference.

## `rate_changes.csv` schema
Required columns:
- `scheme_id`
- `effective_date` (YYYY‑MM‑DD)
- `end_date` (YYYY‑MM‑DD, optional)
- `rate`
- `currency_code`
- `source`

Optional columns:
- `product`
- `comment`

Notes:
- If `end_date` is blank, it will be inferred from the next `effective_date` for the same `scheme_id` + `product`.
- If the last period has no `end_date`, it is assumed to end on Dec 31 of the `effective_date` year.

## Outputs
- `annual_rates.csv` (generated) — annual rates in `_raw/price/*_tax*_prices.csv` format:
  `[scheme_id, year, ghg, product, rate, currency_code, source, comment]`

## Generate annual rates
```
python3 -m _code._compilation._utils.tax_rate_pro_rata \
  --preproc-dir _raw/price/_preproc \
  --out _raw/price/_preproc/annual_rates.csv
```

The resulting `annual_rates.csv` can be used to update `_raw/price/*_tax*_prices.csv`.
