# Auxiliary Scripts (`_code/_aux_scripts`)

The `_aux_scripts` folder contains scripts that support maintenance, updating raw data, and producing summary statistics. They are mainly for internal use rather than a public API.

## `scope_jurisdiction.py`

**Purpose:**  
Maintain and manipulate **scope / coverage files** at sector–jurisdiction level.

Typical behaviour (from the code structure):

- `concatenate(indir)`:
  - Scans `indir` (often a `_raw/scope` subfolder) for scope-related CSV files.
  - Reads them, standardises structure, and concatenates into one DataFrame.

Additional logic in the script:

- **Extends coverage information** where appropriate:
  - If a scheme continues beyond the last year with an explicit scope file, it may create rows for later years with structure copied forward and coverage factor left blank (`NA`) for manual filling.
- Sorts and overwrites the underlying CSV files with the updated structure.

This script is useful when adding new years or schemes to the scope.

## `ipcc_isic_mapping.py`

**Purpose:**  
Support construction and maintenance of mappings between IPCC emission categories and ISIC/NACE industry codes.

Characteristics:

- Designed as a helper or one-off script; not structured as a reusable module.
- Likely used in conjunction with `_industryMapping/estat_nace_prices.py`.

## `sumstat.py`

**Purpose:**  
Compute summary statistics of WCPD coverage for a given year.

Key function:

- `summaryStatistics(year) -> (sumstat_jurisdictions, sumstat_sectors)`:

  - Loads jurisdiction-level WCPD files (typically from `_dataset/data/CO2/...`).
  - Concatenates them into a national and subnational DataFrame.
  - Constructs binary indicators for each jurisdiction (e.g. tax present, ETS present, any pricing).
  - Aggregates coverage statistics:
    - By jurisdiction.
    - By sector.

The script currently depends on ECP helper functions and may contain **hard-coded paths** that should be adapted for portability.

At the bottom of the file there is a simple test call, e.g.:

```python
test = summaryStatistics(2021)
```

## `db_concat.py`

**Purpose:**  
Concatenate jurisdiction-level WCPD CSVs into a single DataFrame.

Key pattern:

- `concatenate(indir)`:

  - Recursively scans `indir` for WCPD output CSVs.
  - Reads and concatenates them into one DataFrame.
  - Optionally writes the combined file back to disk.

Useful for:

- Exploratory analysis.
- Cross-jurisdiction validation and plotting.

## `rawFilesUpdate/` scripts

These scripts help update and harmonise raw data when new releases become available.

### `_updateScanningPrice.py`

- Contains helper logic (e.g. `get_price_column(...)`) to handle variations in column names or formats in newly scanned price files.
- Intended to be imported by other update scripts.

### `rawFilesUpdatePrice.py`

- Compares existing raw price CSVs with new ones.
- Uses helpers from `_updateScanningPrice.py` to robustly identify price columns.
- Merges or replaces series as needed.
- Writes updated raw price files back under `_raw/price/`.

### `rawFilesUpdateCFactor.py`

- Performs similar tasks for coverage-factor files:
  - Reads existing coverage-factor CSVs (`_raw/coverageFactor/*.csv`).
  - Applies updates or adds new years.
  - Writes revised files while keeping the structure consistent with WCPD scope and `cf` construction.
