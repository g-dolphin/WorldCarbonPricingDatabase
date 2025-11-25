# Usage Guide

This guide explains how to run the WCPD build pipeline with the current codebase and how these docs can be integrated with Sphinx later.

## 1. Repository layout and prerequisites

Expected top-level structure:

- `_code/`
- `_raw/`
- `_dataset/` (can be empty initially)

You will need:

- Python (3.x) with `pandas`, `numpy`, `logging`, etc.
- Access to the ECP repository and coverage modules referenced via absolute paths in:
  - `_code/_compilation/db_build.py`
  - `_code/_compilation/_preprocessing/_overlap.py`
  - `_code/_aux_scripts/sumstat.py`, etc.

> **Recommendation:** refactor absolute paths to configuration variables or environment variables for portability.

## 2. Configure gas and structure

Open `_code/_compilation/db_build.py` and ensure:

```python
GAS = "CO2"  # or "CH4", "F-GASES", "SF6"
WCPD_STRUCTURE_PATH = "_raw/_aux_files/wcpd_structure/wcpd_structure_CO2.csv"
```

Also verify that:

- `_raw/price/` contains ETS and tax rate input files.
- `_raw/scope/` contains ETS and tax scope modules/files.
- `_raw/_aux_files/wcpd_structure/` contains the structure CSV(s) for the gas you are building.

## 3. Run the build and write outputs

From a Python shell or notebook, with the working directory somewhere inside the repo:

```python
from _code._compilation import db_build  # runs the build pipeline on import
from _code._compilation import db_write  # writes files using globals from db_build
```

What happens:

1. Importing `db_build`:

   - Discovers `ROOT_DIR`.
   - Loads jurisdictions, ETS prices, and tax rates.
   - Loads scope information for ETS and taxes.
   - Builds `wcpd_all_jur` (core WCPD data) and `wcpd_all_jur_sources` (metadata).
   - Constructs coverage factors `cf` and overlap corrections `overlap`.
   - Runs `validate_output(...)` and prints warnings.

2. Importing `db_write`:

   - Uses the objects defined by `db_build` (e.g. `wcpd_all_jur`, `cf`, `overlap`, `GAS`).
   - Writes jurisdiction-level CSVs under, for example:

     - `_dataset/data/CO2/national/`
     - `_dataset/data/CO2/subnational/`

   - Writes parallel source files under `_dataset/sources/...`.
   - Writes coverage-factor CSVs under `_raw/coverageFactor/`.
   - Writes overlap CSV under `_raw/overlap/`.

If you prefer to control the timing of writes, you can:

- Comment out top-level writing code in `db_write.py`, and
- Call `save_jurisdiction_files(...)` and the coverage / overlap writing logic manually.

## 4. Inspecting and analysing outputs

A typical workflow after building:

```python
import pandas as pd
from _code._aux_scripts import db_concat

# Concatenate all national CO2 WCPD files
df = db_concat.concatenate("_dataset/data/CO2/national")

# Look at a few rows
print(df.head())
```

For summary statistics:

```python
from _code._aux_scripts import sumstat

sumstat_jur, sumstat_sec = sumstat.summaryStatistics(2021)
```

You can then export or plot these results as needed.

## 5. Using these docs with Sphinx

These Markdown files are designed to be Sphinx-friendly (especially with `myst-parser`) or usable directly with MkDocs.

### Minimal Sphinx setup (with MyST)

In your `conf.py`:

```python
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
]
```

Create `index.md` (or `index.rst`) with something like:

```md
# World Carbon Pricing Database

```{toctree}
:maxdepth: 2

overview
architecture_compilation
aux_scripts
industry_mapping
api_reference
usage
```
```

Once docstrings are added to the modules, you can extend the docs with autodoc, for example in a Markdown file:

```md
# Compilation module reference

```{autodoc} _code._compilation.db_build
:members:
:undoc-members:
:show-inheritance:
```
```

The current files give you the human-readable structure; later, autodoc will fill in function-level details directly from the code.
