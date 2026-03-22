import argparse
import logging
import os
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np
import pandas as pd


def find_project_root(
    markers=("pyproject.toml", "setup.cfg", "requirements.txt", ".git", ".project-root")
):
    p = Path.cwd().resolve()
    for parent in (p, *p.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent
    return p


ROOT_DIR = find_project_root()
CODE_DIR = ROOT_DIR / "_code/_compilation/_utils"
RAW_DIR = ROOT_DIR / "_raw"
DEFAULT_GAS = os.environ.get("WCPD_GAS", "CO2").upper()
GAS = DEFAULT_GAS

OUTPUT_COLUMNS = [
    "tax",
    "ets",
    "ets_2",
    "tax_2",
    "tax_id",
    "tax_2_id",
    "ets_id",
    "ets_2_id",
    "tax_rate_excl_ex_clcu",
    "tax_2_rate_excl_ex_clcu",
    "tax_curr_code",
    "tax_2_curr_code",
    "tax_ex_rate",
    "tax_rate_incl_ex_clcu",
    "ets_price",
    "ets_curr_code",
    "ets_2_price",
    "ets_2_curr_code",
]

SOURCE_COLUMNS = [
    "tax",
    "ets",
    "ets_2",
    "tax_2",
    "tax_rate_excl_ex_clcu",
    "tax_2_rate_excl_ex_clcu",
    "tax_ex_rate",
    "ets_price",
    "ets_2_price",
]

FINAL_COLUMNS = [
    "jurisdiction",
    "year",
    "ipcc_code",
    "Product",
    "tax",
    "ets",
    "tax_id",
    "tax_rate_excl_ex_clcu",
    "tax_ex_rate",
    "tax_rate_incl_ex_clcu",
    "tax_curr_code",
    "ets_id",
    "ets_price",
    "ets_curr_code",
    "ets_2_id",
    "ets_2_price",
    "ets_2_curr_code",
]

FINAL_SOURCE_COLUMNS = [
    "jurisdiction",
    "year",
    "ipcc_code",
    "Product",
    "tax",
    "ets",
    "tax_rate_excl_ex_clcu",
    "tax_ex_rate",
    "ets_price",
    "ets_2_price",
]


def load_module(name, relative_path):
    path = Path(relative_path)
    if not path.is_absolute():
        path = ROOT_DIR / path
    if not path.exists():
        logging.error("Module not found: %s", path)
        raise FileNotFoundError(path)
    return SourceFileLoader(name, str(path)).load_module()


def structure_path_for_gas(gas: str) -> Path:
    suffix = "CO2" if gas == "CO2" else "nonCO2"
    return RAW_DIR / "_aux_files" / "wcpd_structure" / f"wcpd_structure_{suffix}.csv"


def load_structure(gas: str) -> pd.DataFrame:
    return pd.read_csv(structure_path_for_gas(gas))


def create_jurisdiction_frame(wcpd_structure: pd.DataFrame, jurisdictions: list[str]) -> pd.DataFrame:
    records = []
    for jurisdiction in jurisdictions:
        temp = wcpd_structure.copy()
        temp["jurisdiction"] = jurisdiction
        records.append(temp)
    return pd.concat(records, axis=0, ignore_index=True)


def initialize_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        if column not in df.columns:
            df[column] = pd.NA
    return df


def assign_price_and_currency(df, selection, scheme_df, scheme, year, columns, fuel=None, source_df=None):
    row_sel = (
        (scheme_df.scheme_id == scheme) & (scheme_df.year == year)
        if any(x in scheme for x in ["ets", "obps", "cat", "rggi"])
        else (scheme_df.scheme_id == scheme) & (scheme_df.year == year) & (scheme_df.em_type == fuel)
    )
    try:
        row = scheme_df.loc[row_sel].squeeze()
        price_col = "price" if any(x in scheme for x in ["ets", "obps", "cat", "rggi"]) else "rate"
        df.loc[selection, columns[price_col]] = row["rate"] if "rate" in row else row["allowance_price"]
        df.loc[selection, columns["curr_code"]] = row["currency_code"]
        if source_df is not None:
            source = f"{row['source']}; {row['comment']}"
            source_df.loc[selection, columns[price_col]] = source
    except Exception as exc:
        print(f"{scheme} {year}: {exc}")


def year_source(source_dict, scheme, year):
    scheme_sources = source_dict.get(scheme, {})
    if year in scheme_sources:
        return scheme_sources[year]
    return "NA"


def scope_block(scope_config, primary_key, *aliases):
    for key in (primary_key, *aliases):
        if key in scope_config:
            return scope_config[key]
    return {}


def apply_ets_scope_exceptions(ets_scope_data, ets_scope_sources, gas: str):
    exceptions_module = load_module(
        "ets_scope_exceptions",
        RAW_DIR / "scope/ets/ets_scope_exceptions.py",
    )
    records = getattr(exceptions_module, "ETS_SCOPE_EXCEPTIONS", [])
    gas = gas.upper()

    for record in records:
        record_gas = str(record.get("gas", "")).upper()
        if record_gas and record_gas != gas:
            continue

        scheme_id = record.get("scheme_id")
        if scheme_id not in ets_scope_data:
            continue

        year_from = int(record["year_from"])
        year_to = int(record["year_to"])
        jurisdictions_to_add = list(record.get("jurisdictions", []))
        add_sectors = list(record.get("add_sectors", []))
        remove_sectors = set(record.get("remove_sectors", []))
        source_suffix = record.get("source")

        scheme_data = ets_scope_data[scheme_id]
        scheme_jurisdictions = scope_block(scheme_data, "jurisdictions")
        scheme_sectors = scope_block(scheme_data, "sectors")

        for year in range(year_from, year_to + 1):
            year_jurisdictions = list(scheme_jurisdictions.get(year, []))
            for jurisdiction in jurisdictions_to_add:
                if jurisdiction not in year_jurisdictions:
                    year_jurisdictions.append(jurisdiction)
            scheme_jurisdictions[year] = year_jurisdictions

            year_sectors = list(scheme_sectors.get(year, []))
            for sector in add_sectors:
                if sector not in year_sectors:
                    year_sectors.append(sector)
            if remove_sectors:
                year_sectors = [sector for sector in year_sectors if sector not in remove_sectors]
            scheme_sectors[year] = year_sectors

            if source_suffix:
                base_source = year_source(ets_scope_sources, scheme_id, year)
                ets_scope_sources.setdefault(scheme_id, {})
                ets_scope_sources[scheme_id][year] = (
                    source_suffix if base_source == "NA" else f"{base_source}; {source_suffix}"
                )

    return ets_scope_data, ets_scope_sources


def run_tax_exemptions(gas: str, wcpd_all_jur: pd.DataFrame, wcpd_all_jur_sources: pd.DataFrame):
    rebate_module = load_module(
        f"tax_rebates_{gas}",
        RAW_DIR / f"priceRebates/tax/_price_exemptions_tax_{gas}.py",
    )

    records = getattr(rebate_module, "tax_exemptions_records", None)
    legacy = getattr(rebate_module, "tax_exemptions", None)
    legacy_sources = getattr(rebate_module, "tax_exemptions_sources", None)

    if records:
        for rec in records:
            year_from = rec.get("year_from")
            year_to = rec.get("year_to")
            if year_from is None or year_to is None:
                continue
            value_by_year = rec.get("value_by_year", {})
            source_by_year = rec.get("source_by_year", {})
            default_value = rec.get("value")
            default_source = rec.get("source", "NA")

            for year in range(int(year_from), int(year_to) + 1):
                value = value_by_year.get(year, default_value)
                if value is None:
                    continue
                source = source_by_year.get(year, default_source)
                row_selection = (
                    wcpd_all_jur.jurisdiction.isin(rec.get("jurisdiction", []))
                    & (wcpd_all_jur.year == year)
                    & (wcpd_all_jur.ipcc_code.isin(rec.get("ipcc", [])))
                    & (wcpd_all_jur.Product.isin(rec.get("fuel", [])))
                )
                wcpd_all_jur.loc[row_selection, "tax_ex_rate"] = value
                wcpd_all_jur_sources.loc[row_selection, "tax_ex_rate"] = source
    elif legacy and legacy != [""]:
        for idx, exemption in enumerate(legacy):
            for year in exemption["jurisdiction"].keys():
                row_selection = (
                    wcpd_all_jur.jurisdiction.isin(exemption["jurisdiction"][year])
                    & (wcpd_all_jur.year == year)
                    & (wcpd_all_jur.ipcc_code.isin(exemption["ipcc"][year]))
                    & (wcpd_all_jur.Product.isin(exemption["fuel"][year]))
                )
                wcpd_all_jur.loc[row_selection, "tax_ex_rate"] = exemption["value"][year]
                if legacy_sources:
                    wcpd_all_jur_sources.loc[row_selection, "tax_ex_rate"] = legacy_sources[idx][year]

    wcpd_all_jur["tax_rate_incl_ex_clcu"] = (
        wcpd_all_jur["tax_rate_excl_ex_clcu"] * (1 - wcpd_all_jur["tax_ex_rate"])
    )


def finalize_output(wcpd_all_jur: pd.DataFrame, wcpd_all_jur_sources: pd.DataFrame):
    wcpd_all_jur.loc[wcpd_all_jur.tax != 1, "tax"] = 0
    wcpd_all_jur.loc[wcpd_all_jur.ets != 1, "ets"] = 0
    wcpd_all_jur.loc[wcpd_all_jur.ets_2 != 1, "ets_2"] = 0
    wcpd_all_jur.loc[wcpd_all_jur.tax_2 != 1, "tax_2"] = 0

    wcpd_all_jur.loc[wcpd_all_jur.tax != 1, "tax_ex_rate"] = np.nan
    wcpd_all_jur_sources.loc[wcpd_all_jur.tax != 1, "tax_ex_rate"] = np.nan

    tax_mask = wcpd_all_jur.tax == 1
    tax_ex_rate = pd.to_numeric(wcpd_all_jur.loc[tax_mask, "tax_ex_rate"], errors="coerce")
    wcpd_all_jur.loc[tax_mask, "tax_ex_rate"] = tax_ex_rate.fillna(0)
    wcpd_all_jur_sources.loc[wcpd_all_jur.tax == 1, "tax_ex_rate"] = (
        wcpd_all_jur_sources.loc[wcpd_all_jur.tax == 1, "tax_ex_rate"].fillna("NA")
    )

    wcpd_all_jur["Product"] = wcpd_all_jur["Product"].fillna("NA")
    wcpd_all_jur_sources["Product"] = wcpd_all_jur_sources["Product"].fillna("NA")

    tax_cols = [
        "tax_id",
        "tax_rate_excl_ex_clcu",
        "tax_curr_code",
        "tax_ex_rate",
        "tax_rate_incl_ex_clcu",
    ]
    ets_1_cols = ["ets_id", "ets_price", "ets_curr_code"]
    ets_2_cols = ["ets_2_id", "ets_2_price", "ets_2_curr_code"]

    wcpd_all_jur.loc[wcpd_all_jur.tax != 1, tax_cols] = "NA"
    wcpd_all_jur.loc[wcpd_all_jur.ets != 1, ets_1_cols] = "NA"
    wcpd_all_jur.loc[wcpd_all_jur.ets_2 != 1, ets_2_cols] = "NA"
    wcpd_all_jur_sources.fillna("NA", inplace=True)
    wcpd_all_jur.fillna("NA", inplace=True)

    return wcpd_all_jur[FINAL_COLUMNS].copy(), wcpd_all_jur_sources[FINAL_SOURCE_COLUMNS].copy()


def validate_output(df):
    print("\nRunning validation checks...")

    missing_prices = df[(df["ets"] == 1) & (df["ets_price"] == "NA")]
    if not missing_prices.empty:
        print(f"Warning: {len(missing_prices)} ETS-covered rows have missing prices.")

    missing_tax_rates = df[(df["tax"] == 1) & (df["tax_rate_excl_ex_clcu"] == "NA")]
    if not missing_tax_rates.empty:
        print(f"Warning: {len(missing_tax_rates)} tax-covered rows have missing tax rates.")

    if "ets_2" in df.columns:
        overlapping_schemes = df[(df["ets"] == 1) & (df["ets_2"] == 1)]
        if not overlapping_schemes.empty:
            print(f"Note: {len(overlapping_schemes)} rows have overlapping ETS schemes.")

    print("Validation checks complete.\n")


def build(gas: str = DEFAULT_GAS, verbose: bool = False):
    gas = gas.upper()
    logging.info("Starting WCPD build for GHG: %s", gas)
    status = print if verbose else (lambda *args, **kwargs: None)

    jurisdictions_module = load_module("jurisdictions", CODE_DIR / "jurisdictions.py")
    ets_prices_module = load_module("ets_prices", CODE_DIR / "ets_prices.py")
    tax_rates_module = load_module("tax_rates", CODE_DIR / "tax_rates.py")
    ets_scope_module = load_module("ets_scope", RAW_DIR / f"scope/ets/ets_scope_{gas}.py")
    tax_scope_module = load_module("taxes_scope", RAW_DIR / f"scope/tax/taxes_scope_{gas}.py")
    coverage_module = load_module(
        "coverage_factors",
        ROOT_DIR / "_code/_compilation/_preprocessing/_coverageFactors.py",
    )
    overlap_module = load_module(
        "overlap",
        ROOT_DIR / "_code/_compilation/_preprocessing/_overlap.py",
    )

    wcpd_structure = load_structure(gas)
    ctries = jurisdictions_module.jurisdictions["countries"]
    subnats = (
        jurisdictions_module.jurisdictions["subnationals"]["Canada"]
        + jurisdictions_module.jurisdictions["subnationals"]["China"]
        + jurisdictions_module.jurisdictions["subnationals"]["Japan"]
        + jurisdictions_module.jurisdictions["subnationals"]["United States"]
        + jurisdictions_module.jurisdictions["subnationals"]["Mexico"]
    )
    all_jurisdictions = ctries + subnats

    wcpd_all_jur = initialize_columns(
        create_jurisdiction_frame(wcpd_structure, all_jurisdictions), OUTPUT_COLUMNS
    )
    wcpd_all_jur_sources = initialize_columns(
        create_jurisdiction_frame(wcpd_structure, all_jurisdictions), SOURCE_COLUMNS
    )

    logging.info("Constructed base data for %s jurisdictions", len(all_jurisdictions))

    ets_prices = ets_prices_module.load_ets_prices(RAW_DIR / "price")
    tax_rates = tax_rates_module.load_tax_rates(RAW_DIR / "price", gas=gas)
    if "product" in tax_rates.columns:
        tax_rates = tax_rates.rename(columns={"product": "em_type"})

    ets_scope = ets_scope_module.scope()
    ets_scope_data, ets_scope_sources = ets_scope["data"], ets_scope["sources"]
    ets_scope_data, ets_scope_sources = apply_ets_scope_exceptions(
        ets_scope_data, ets_scope_sources, gas
    )
    taxes_scope = tax_scope_module.scope()
    taxes_scope_data, taxes_scope_sources = taxes_scope["data"], taxes_scope["sources"]

    def ets_db_values(schemes, scheme_no):
        columns = {
            "scheme_1": {
                "id": "ets_id",
                "binary": "ets",
                "price": "ets_price",
                "curr_code": "ets_curr_code",
            },
            "scheme_2": {
                "id": "ets_2_id",
                "binary": "ets_2",
                "price": "ets_2_price",
                "curr_code": "ets_2_curr_code",
            },
        }[scheme_no]

        for scheme in schemes:
            scheme_cfg = ets_scope_data[scheme]
            scheme_jurisdictions = scope_block(scheme_cfg, "jurisdictions")
            scheme_sectors = scope_block(scheme_cfg, "sectors")

            if not scheme_jurisdictions or not scheme_sectors:
                status(f"Warning: skipping {scheme} due to incomplete ETS scope configuration.")
                continue

            status(scheme)
            status("Available years for scheme:", list(scheme_jurisdictions.keys()))
            for year in scheme_jurisdictions:
                if year not in scheme_sectors:
                    status(f"Warning: skipping {scheme} {year} due to missing ETS sector scope.")
                    continue
                status("Processing year:", year)
                selection = (
                    (wcpd_all_jur.year == year)
                    & (wcpd_all_jur.jurisdiction.isin(scheme_jurisdictions[year]))
                    & (wcpd_all_jur.ipcc_code.isin(scheme_sectors[year]))
                )
                selection_src = (
                    (wcpd_all_jur_sources.year == year)
                    & (wcpd_all_jur_sources.jurisdiction.isin(scheme_jurisdictions[year]))
                    & (wcpd_all_jur_sources.ipcc_code.isin(scheme_sectors[year]))
                )
                wcpd_all_jur.loc[selection, columns["binary"]] = 1
                wcpd_all_jur.loc[selection, columns["id"]] = scheme
                wcpd_all_jur_sources.loc[selection_src, columns["binary"]] = year_source(
                    ets_scope_sources, scheme, year
                )
                assign_price_and_currency(
                    wcpd_all_jur,
                    selection,
                    ets_prices,
                    scheme,
                    year,
                    columns,
                    source_df=wcpd_all_jur_sources,
                )

    def tax_db_values(schemes, scheme_no):
        columns = {
            "scheme_1": {
                "id": "tax_id",
                "binary": "tax",
                "rate": "tax_rate_excl_ex_clcu",
                "curr_code": "tax_curr_code",
            },
            "scheme_2": {
                "id": "tax_2_id",
                "binary": "tax_2",
                "rate": "tax_2_rate_excl_ex_clcu",
                "curr_code": "tax_2_curr_code",
            },
        }[scheme_no]

        for scheme in schemes:
            scheme_cfg = taxes_scope_data[scheme]
            scheme_jurisdictions = scope_block(scheme_cfg, "jurisdictions", "juristicons")
            scheme_sectors = scope_block(scheme_cfg, "sectors")
            scheme_fuels = scope_block(scheme_cfg, "fuels")

            if not scheme_jurisdictions or not scheme_sectors:
                status(f"Warning: skipping {scheme} due to incomplete tax scope configuration.")
                continue

            status(scheme)
            status("Available years for scheme:", list(scheme_jurisdictions.keys()))
            for year in scheme_jurisdictions:
                if year not in scheme_sectors:
                    status(f"Warning: skipping {scheme} {year} due to missing tax sector scope.")
                    continue
                status("Processing year:", year)
                jurisdictions = scheme_jurisdictions[year]
                sectors = scheme_sectors[year]
                fuels = scheme_fuels.get(year, [None])

                for fuel in fuels:
                    selection = (
                        (wcpd_all_jur.year == year)
                        & (wcpd_all_jur.jurisdiction.isin(jurisdictions))
                        & (wcpd_all_jur.ipcc_code.isin(sectors))
                    )
                    selection_src = (
                        (wcpd_all_jur_sources.year == year)
                        & (wcpd_all_jur_sources.jurisdiction.isin(jurisdictions))
                        & (wcpd_all_jur_sources.ipcc_code.isin(sectors))
                    )
                    if gas == "CO2" and fuel is not None:
                        selection &= wcpd_all_jur.Product == fuel
                        selection_src &= wcpd_all_jur_sources.Product == fuel
                    wcpd_all_jur.loc[selection, columns["binary"]] = 1
                    wcpd_all_jur.loc[selection, columns["id"]] = scheme
                    wcpd_all_jur_sources.loc[selection_src, columns["binary"]] = year_source(
                        taxes_scope_sources, scheme, year
                    )
                    assign_price_and_currency(
                        wcpd_all_jur,
                        selection,
                        tax_rates,
                        scheme,
                        year,
                        columns,
                        fuel,
                        wcpd_all_jur_sources,
                    )

    if gas == "CO2":
        ets_1_list = list(ets_scope_data.keys())
        if "usa_ma_ets" in ets_1_list:
            ets_1_list.remove("usa_ma_ets")
        ets_2_list = ["usa_ma_ets"]
        taxes_1_list = list(taxes_scope_data.keys())
        tax_2_list = []

        ets_db_values(ets_1_list, "scheme_1")
        tax_db_values(taxes_1_list, "scheme_1")
        ets_db_values(ets_2_list, "scheme_2")
        tax_db_values(tax_2_list, "scheme_2")
    elif gas == "N2O":
        ets_1_list = list(ets_scope_data.keys())
        ets_2_list = []
        taxes_1_list = list(taxes_scope_data.keys())
        if "nld_tax_II" in taxes_1_list:
            taxes_1_list.remove("nld_tax_II")
        tax_2_list = ["nld_tax_II"]

        ets_db_values(ets_1_list, "scheme_1")
        tax_db_values(taxes_1_list, "scheme_1")
        ets_db_values(ets_2_list, "scheme_2")
        tax_db_values(tax_2_list, "scheme_2")
    else:
        ets_1_list = list(ets_scope_data.keys())
        ets_2_list = []
        taxes_1_list = list(taxes_scope_data.keys())
        tax_2_list = []

        ets_db_values(ets_1_list, "scheme_1")
        tax_db_values(taxes_1_list, "scheme_1")
        ets_db_values(ets_2_list, "scheme_2")
        tax_db_values(tax_2_list, "scheme_2")

    run_tax_exemptions(gas, wcpd_all_jur, wcpd_all_jur_sources)
    wcpd_all_jur, wcpd_all_jur_sources = finalize_output(wcpd_all_jur, wcpd_all_jur_sources)

    cf = coverage_module.generate_coverage_factors(
        gas=gas,
        wcpd_all_jur=wcpd_all_jur,
        raw_dir=RAW_DIR,
        taxes_1_list=taxes_1_list + tax_2_list,
        taxes_scope_data=taxes_scope_data,
        ets_1_list=ets_1_list + ets_2_list,
        ets_scope_data=ets_scope_data,
    )
    overlap = overlap_module.compute_overlap(
        wcpd_all_jur=wcpd_all_jur,
        gas=gas,
        raw_dir=RAW_DIR,
        coverage_factors=cf,
    )

    validate_output(wcpd_all_jur)

    return {
        "gas": gas,
        "ctries": ctries,
        "subnats": subnats,
        "wcpd_all_jur": wcpd_all_jur,
        "wcpd_all_jur_sources": wcpd_all_jur_sources,
        "taxes_1_list": taxes_1_list,
        "tax_2_list": tax_2_list,
        "ets_1_list": ets_1_list,
        "ets_2_list": ets_2_list,
        "cf": cf,
        "overlap": overlap,
    }


def _populate_module_globals(build_result):
    globals().update(build_result)
    globals()["GAS"] = build_result["gas"]


def main():
    parser = argparse.ArgumentParser(description="Build WCPD compilation tables for a single gas.")
    parser.add_argument("--gas", default=DEFAULT_GAS, help="Gas to build: CO2, CH4, N2O, etc.")
    parser.add_argument("--verbose", action="store_true", help="Print per-scheme progress details.")
    args = parser.parse_args()
    _populate_module_globals(build(args.gas, verbose=args.verbose))


if __name__ == "__main__":
    main()
