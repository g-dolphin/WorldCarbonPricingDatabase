# API Reference (Draft)

This file sketches an **informal API** for the most relevant functions in this repo.  
It is intended as a starting point for later Sphinx `autodoc` integration, once proper docstrings are added.

## `_code/_compilation/db_build.py`

### `find_project_root(markers=("pyproject.toml", "setup.cfg", "requirements.txt", ".git", ".project-root")) -> Path`

Search upwards from the current working directory for a directory containing any of the `markers`.  
Returns the first match, or the current directory if none are found.

---

### `load_module(name: str, relative_path) -> module`

Dynamically load a module from a file path:

- If `relative_path` is absolute, it is used directly.
- Otherwise it is joined to `ROOT_DIR`.

Used to load:

- ECP helper modules.
- WCPD utility modules.
- Scope modules.

---

### `load_structure(path) -> pd.DataFrame`

Read the WCPD structural template CSV:

- Input: path to the structure file (e.g. `_raw/_aux_files/wcpd_structure/wcpd_structure_CO2.csv`).
- Output: base DataFrame without jurisdiction column.

---

### `create_jurisdiction_frame(wcpd_structure: pd.DataFrame, jurisdictions) -> pd.DataFrame`

Given the base `wcpd_structure` and a collection of jurisdiction names:

- Clones the structure once per jurisdiction.
- Adds a `jurisdiction` column.
- Concatenates all clones into a single DataFrame.

---

### `assign_price_and_currency(df, selection, scheme_df, scheme, yr, columns, fuel=None, source_df=None)`

Populate price / rate and currency columns in `df` for a given scheme and year.

Parameters (inferred from usage):

- `df`: WCPD core DataFrame (`wcpd_all_jur`).
- `selection`: boolean mask or index for rows to be updated.
- `scheme_df`: ETS or tax DataFrame (from `ets_prices` or `tax_rates`).
- `scheme`: scheme identifier.
- `yr`: year.
- `columns`: mapping from logical names (e.g. `"price"`, `"rate"`, `"curr_code"`) to actual column names in `df`.
- `fuel` (optional): restricts to a specific emissions type (when relevant).
- `source_df` (optional): parallel DataFrame to hold textual source metadata.

---

### `ets_db_values(ets_1_list: list[str], label: str) -> None`

Populate ETS coverage and price columns in `wcpd_all_jur`:

- Iterates over ETS schemes in `ets_1_list`.
- Uses scope dictionaries to identify covered rows.
- Calls `assign_price_and_currency` to fill prices and currencies.
- Logs warnings for ETS-covered rows with missing prices.

---

### `tax_db_values(taxes_1_list: list[str], label: str) -> None`

Populate tax coverage and rate columns in `wcpd_all_jur`:

- Iterates over tax schemes in `taxes_1_list`.
- Uses scope dictionaries to identify covered rows.
- Calls `assign_price_and_currency` to fill rates and currencies.
- Logs warnings for tax-covered rows with missing rates.

---

### `tax_exemptions(wcpd_all_jur: pd.DataFrame, gas: str) -> pd.DataFrame`

Apply gas-specific tax exemptions and adjustments, possibly accounting for overlap with ETS:

- May modify coverage flags and effective tax rates.
- Returns the adjusted `wcpd_all_jur`.

---

### `validate_output(df: pd.DataFrame) -> None`

Perform basic quality checks on the compiled dataset:

- Reports ETS-covered rows with missing prices.
- Reports tax-covered rows with missing tax rates.
- Reports rows with overlapping ETS schemes.

Prints warnings and a final status message to stdout.

---

## `_code/_compilation/db_write.py`

### `standardize_name(name: str) -> str`

Return a filesystem-friendly version of `name`:

- Remove `"."` and `","`.
- Replace spaces with `"_"`.

Used to construct file names like `wcpd_co2_United_Kingdom.csv`.

---

### `save_jurisdiction_files(df: pd.DataFrame, jurisdictions, std_names, gas: str, level: str, base_dir) -> None`

Write one CSV per jurisdiction for a given gas and level:

- Filters `df` by `jurisdiction`.
- Builds paths like:  
  `<base_dir>/<gas>/<level>/wcpd_<gas_lower>_<std_name>.csv`
- Ensures parent directories exist.
- Writes CSVs without index.

---

## `_code/_compilation/_utils/tax_rates.py`

### `load_tax_rates(price_path, gas) -> pd.DataFrame`

Load and harmonise carbon tax rate data:

- Scans `price_path` for tax rate CSVs.
- Filters / aggregates them for the specified `gas`.
- Harmonises column names.
- Returns a combined DataFrame with scheme IDs, years, emission types, rates, and metadata.

---

## `_code/_compilation/_utils/ets_prices.py`

### `process_ets_prices(price_dir) -> pd.DataFrame`

Process internal ETS price files:

- Reads ETS price CSVs in `price_dir`.
- Standardises and reshapes them into a long format.

---

### `process_icap_prices(price_dir) -> pd.DataFrame`

Process ICAP price data:

- Reads the ICAP CSV.
- Selects and reshapes columns for ETS schemes tracked in WCPD.

---

### `load_ets_prices(price_dir=DEFAULT_PRICE_PATH) -> pd.DataFrame`

Combine internal and ICAP ETS price sources:

- Concatenates processed data.
- Rounds allowance prices to two decimals.
- Returns the combined DataFrame.

---

## `_code/_compilation/_utils/jurisdictions.py`

### `jurisdictions`

Top-level variable:

- Loaded from `jurisdictions.json`.
- Represents the list or mapping of WCPD jurisdictions used by `db_build.py`.

---

## `_code/_compilation/_utils/sector_agg_scope.py`

### `Extract(lst, i)`

Small helper function for working with lists in the context of sector aggregation and scope.

---

## `_code/_compilation/_preprocessing/_coverageFactors.py`

### `build_cf_df(schemes, scope_dict, gas, wcpd_all_jur, RAW_DIR) -> pd.DataFrame`

Construct the coverage-factor DataFrame `cf`:

- Index: `(scheme_id, jurisdiction, year, ipcc_code)`.
- Coverage factor column: `cf_<gas>`.
- Additional metadata columns (e.g. `cf_<gas>_source`, `cf_<gas>_comment`).

---

## `_code/_aux_scripts/sumstat.py`

### `summaryStatistics(year: int) -> tuple[dict, dict]`

Compute summary statistics:

- Builds national and subnational WCPD DataFrames for the chosen `year`.
- Returns:
  - `sumstat_jurisdictions` – coverage metrics by jurisdiction.
  - `sumstat_sectors` – coverage metrics by sector.

---

## `_code/_aux_scripts/db_concat.py`

### `concatenate(indir) -> pd.DataFrame`

Concatenate WCPD jurisdiction-level output files:

- Reads all CSVs beneath `indir`.
- Returns a single concatenated DataFrame.

---

## `_code/_aux_scripts/scope_jurisdiction.py`

### `concatenate(indir) -> pd.DataFrame`

Concatenate and clean scope / coverage files at sector–jurisdiction level for maintenance and updates.
