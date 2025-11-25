# Compilation Architecture (`_code/_compilation`)

This document describes how the WCPD build pipeline is structured.

## Modules

- `db_build.py` – orchestrates construction of the WCPD core tables from raw inputs.
- `db_write.py` – writes compiled data and metadata to disk.
- `_utils/`
  - `ets_prices.py` – loads and harmonises ETS price series.
  - `tax_rates.py` – loads and harmonises carbon tax rates.
  - `jurisdictions.py` – loads the list/dict of WCPD jurisdictions from a JSON file.
  - `sector_agg_scope.py` – small helpers for sector aggregation / scope logic.
- `_preprocessing/`
  - `_coverageFactors.py` – builds coverage-factor DataFrames.
  - `_overlap.py` – defines overlap corrections between schemes.

### Project root discovery

`db_build.find_project_root(...)` searches upwards from `Path.cwd()` for typical project markers:

- `pyproject.toml`, `setup.cfg`, `requirements.txt`, `.git`, `.project-root`

The first matching directory is used as `ROOT_DIR`. This allows running the build from different working directories as long as you are somewhere inside the repo.

### Paths and constants (in `db_build.py`)

Key variables defined near the top:

- `ROOT_DIR` – project root (see above).
- `CODE_DIR = ROOT_DIR / "_code/_compilation/_utils"`
- `RAW_DIR  = ROOT_DIR / "_raw"`

And gas / structure configuration, e.g.:

- `GAS = "CO2"` (or `"CH4"`, `"F-GASES"`, `"SF6"`).
- `WCPD_STRUCTURE_PATH = "_raw/_aux_files/wcpd_structure/wcpd_structure_CO2.csv"`

> **Note:** `WCPD_STRUCTURE_PATH` is currently a string path; it is resolved relative to `ROOT_DIR` at runtime.

### Dynamic loading

The function:

```python
load_module(name: str, relative_path)
```

uses `importlib.machinery.SourceFileLoader` to load modules by path. It is used to bring in:

- ECP dependencies (general helper functions and coverage machinery), via **absolute paths**.
- WCPD utilities: `jurisdictions`, `ets_prices`, `tax_rates`.
- Scope modules located under `_raw/scope/` (ETS, taxes).

You will need to adapt these paths if running on a different machine.

### Structural frame (WCPD skeleton)

The `load_structure(path)` function reads the structure CSV, which defines the “skeleton” of WCPD rows:

- Columns typically include: year, IPCC code, some structural flags, etc.
- Jurisdiction is *added later*.

`create_jurisdiction_frame(wcpd_structure, jurisdictions)`:

- Takes the base structure DataFrame and a list/dict of jurisdictions.
- For each jurisdiction, clones the structure and adds a `jurisdiction` column.
- Concatenates all clones into a single DataFrame `wcpd_all_jur`.

This `wcpd_all_jur` is the master table that gets populated with prices, rates, coverage flags, and coverage factors.

### Loading price data

Two utility modules handle price data:

- `_utils/ets_prices.py`
- `_utils/tax_rates.py`

#### ETS prices (`ets_prices.py`)

Key functions:

- `process_ets_prices(price_dir)`  
  Processes “internal” ETS price files in `price_dir` (a `_raw/price` subfolder), normalising columns and turning them into a long format with scheme IDs, years, and prices.

- `process_icap_prices(price_dir)`  
  Reads ICAP price data (a separate CSV), selects relevant columns for ETS schemes, and reshapes them to match the internal format.

- `load_ets_prices(price_dir=DEFAULT_PRICE_PATH)`  
  Combines the internal and ICAP sources using `pd.concat`, rounds prices, and returns a DataFrame with at least:

  - `scheme_id`
  - `year`
  - `allowance_price`
  - `currency_code`
  - `source`, `comment` (where available).

`db_build.py` calls `load_ets_prices(RAW_DIR / "price")`.

#### Carbon tax rates (`tax_rates.py`)

Main function:

- `load_tax_rates(price_path, gas)`  

  Loads tax rate CSVs from `price_path` (usually `_raw/price`):

  - Uses `glob` to find relevant files.
  - Filters or groups by `gas` (CO₂, CH₄, F-gases, etc.).
  - Harmonises column names across files.
  - Concatenates them into a single DataFrame.

The output typically includes:

- `scheme_id`
- `year`
- `product` / `em_type`
- `rate`
- `currency_code`
- `source`, `comment`

`db_build.py` then renames `product` to `em_type` so it can filter by gas type more easily.

### Jurisdictions (`jurisdictions.py`)

This module loads the jurisdiction list/dict from a JSON file:

- Currently the path is **hard-coded** to a user directory.
- The loaded value is exposed as a top-level `jurisdictions` variable.

For a more portable setup, update the path to something like:

```python
json_path = os.path.join(os.path.dirname(__file__), "jurisdictions.json")
```

and place `jurisdictions.json` alongside the module.

### Populating prices and coverage

`db_build.py` contains several helper functions that operate on `wcpd_all_jur`:

- `assign_price_and_currency(df, selection, scheme_df, scheme, yr, columns, fuel=None, source_df=None)`

  Core routine that:

  - For a given `scheme` and `yr`, finds the corresponding row in `scheme_df` (ETS prices or tax rates).
  - Picks either a **price** column (for ETS) or a **rate** column (for taxes).
  - Assigns the numeric value and `currency_code` to rows of `df` selected by `selection`.
  - Optionally writes a combined textual source into a parallel `source_df`.

- `ets_db_values(ets_1_list, label)`
- `tax_db_values(taxes_1_list, label)`

  These functions loop over lists of ETS / tax schemes and:

  - Read scope information from loaded scope modules.
  - Mark coverage in `wcpd_all_jur` (e.g. `ets`, `ets_2`, `tax` flags).
  - Call `assign_price_and_currency` to populate prices / rates and currencies.
  - Log warnings about covered rows with missing numeric values.

- `tax_exemptions(wcpd_all_jur, gas)`

  Applies specific rules for tax exemptions and interactions with ETS coverage.  
  This may adjust:

  - Coverage flags (e.g. set tax coverage to 0 if ETS already covers a segment).
  - Effective tax rates.

### Coverage factors and overlap (preprocessing)

`_preprocessing/_coverageFactors.py` and `_preprocessing/_overlap.py` are used to compute:

- Coverage-factor DataFrame `cf`.
- Overlap corrections DataFrame `overlap`.

#### Coverage factors (`_coverageFactors.py`)

The key idea is:

- Coverage factors should be defined **only where a scheme is actually present** in `wcpd_all_jur`.
- Default coverage factor is 1, with scheme-specific modifications.

The main entry point is:

- `build_cf_df(schemes, scope_dict, gas, wcpd_all_jur, RAW_DIR)`

  It:

  - For each scheme in `schemes`, uses the scope dictionary to determine which sectors / jurisdictions / years are covered.
  - Constructs a DataFrame with index over `(scheme_id, jurisdiction, year, ipcc_code)`.
  - Sets `cf_<gas> = 1` where covered, `NaN` (or `"NA"`) otherwise.
  - Adds metadata columns such as `cf_<gas>_source` and `cf_<gas>_comment`.

Manual corrections for particular schemes (e.g. UK ETS aviation) are also applied in this module.

#### Overlap (`_overlap.py`)

This module:

- Defines overlapping coverage between schemes (typically ETS vs taxes, or overlapping ETS).
- Uses helper functions from ECP coverage tools (loaded via `SourceFileLoader`).
- Produces a DataFrame (often named `overlap`) with:

  - `scheme_id`
  - `jurisdiction`
  - `year` / year range
  - `ipcc_code`
  - overlap information and comments.

`db_write.py` later writes this to `_raw/overlap/overlap_<GAS>.csv`.

### Validation

`validate_output(df)` in `db_build.py` performs simple checks:

- ETS-covered rows with missing prices.
- Tax-covered rows with missing tax rates.
- Rows with overlapping ETS schemes (e.g. `ets == 1` and `ets_2 == 1`).

It summarises any issues via `print` calls.

### Writing outputs (`db_write.py`)

Key helper:

- `standardize_name(name)` – strips `"."` and `","`, replaces spaces with `"_"`.  
  Used to create filenames like `wcpd_co2_United_States.csv`.

- `save_jurisdiction_files(df, jurisdictions, std_names, gas, level, base_dir)`

  For each `jur` in `jurisdictions`:

  - Filters `df[df.jurisdiction == jur]`.
  - Builds a filename `wcpd_<gas_lower>_<std_name>.csv`.
  - Writes it under `base_dir/gas/level/`.

At module level, `db_write.py` uses global variables populated in `db_build.py` (e.g. `wcpd_all_jur`, `wcpd_all_jur_sources`, `cf`, `overlap`, `GAS`, lists of jurisdictions) to:

- Write **data files** to `_dataset/data/<GAS>/national/` and `/subnational/`.
- Write **source files** (parallel structure) to `_dataset/sources/<GAS>/...`.
- Write **coverage factors** to `_raw/coverageFactor/<scheme>_cf.csv`.
- Write **overlap** data to `_raw/overlap/overlap_<GAS>.csv`.

> **Important:** Because `db_write.py` depends on variables created in `db_build.py`, you must import / run `db_build` first in the same Python process.
