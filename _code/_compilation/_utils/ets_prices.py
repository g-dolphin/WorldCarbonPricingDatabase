#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loads ETS price data for use in the World Carbon Pricing Database.
"""

import os
import pandas as pd
import logging
from typing import Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set relative default path
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

DEFAULT_PRICE_PATH = os.path.normpath(os.path.join(BASE_DIR, "_raw/price"))

def process_ets_prices(price_dir: str = DEFAULT_PRICE_PATH) -> Dict[str, pd.DataFrame]:
    """
    Load all known ETS prices from CSV files.

    Args:
        price_dir (str): Path to directory containing ETS price CSVs.

    Returns:
        dict: Dictionary of jurisdiction codes mapped to their ETS price DataFrames.
    """

    files = {
        "aut_ets": "aut_ets_prices.csv",
        "can_obps": "can_obps_prices.csv",
        "kaz_ets": "kaz_ets_prices.csv",
        "idn_ets": "idn_ets_prices.csv",
        "mex_ets": "mex_ets_prices.csv",
        "mne_ets": "mne_ets_prices.csv",
        "che_ets": "che_ets_prices.csv",
        "usa_rggi": "usa_rggi_prices.csv",
        "usa_ma_ets": "usa_ma_ets_prices.csv",
        "usa_or_ets": "usa_or_ets_prices.csv",
        "can_qc_cat": "can_qc_cat_prices.csv",
        "usa_ca_ets": "usa_ca_ets_prices.csv",
        "usa_wa_ets": "usa_wa_ets_prices.csv",
        "can_ab_ets": "can_ab_ets_prices.csv",
        "can_bc_ets": "can_bc_ets_prices.csv",
        "can_sk_ets": "can_sk_ets_prices.csv",
        "can_nb_ets": "can_nb_ets_prices.csv",
        "can_ns_ets": "can_ns_ets_prices.csv",
        "can_ns_ets_II": "can_ns_ets_II_prices.csv",
        "can_nl_ets": "can_nl_ets_prices.csv"    
        }

    data = {}
    for code, filename in files.items():
        path = os.path.join(price_dir, filename)
        if os.path.exists(path):
            data[code] = pd.read_csv(path)
            if code == "usa_rggi":
                data[code]["allowance_price"] = data[code]["allowance_price"] / 0.907185
            logging.info(f"Loaded ETS price data for {code}")
        else:
            logging.warning(f"Missing price file: {filename}")

    return data


def process_icap_prices(price_dir: str) -> pd.DataFrame:
    """
    Processes ICAP ETS price data and returns a tidy DataFrame with yearly averages.

    Args:
        price_path (str): Path to the price data directory.
        icap_file (str): Filename of the ICAP CSV.

    Returns:
        pd.DataFrame: Yearly average allowance prices with scheme ID and metadata.
    """

    # Define mapping of substrings to scheme IDs
    column_map = {
        "Nova Scotia": "can_ns_ets", "European Union": "eu_ets", "Quebec": "can_qc_cat",
        "Québec": "can_qc_cat", "QuÃ©bec": "can_qc_cat",
        "Ontario": "can_on_ets", "Switzerland": "che_ets", "United Kingdom": "gbr_ets",
        "China": "chn_ets", "German": "deu_ets", "Shenzhen": "chn_sz_ets", "Shanghai": "chn_sh_ets",
        "Beijing": "chn_bj_ets", "Guangdong": "chn_gd_ets", "Tianjin": "chn_tj_ets",
        "Hubei": "chn_hb_ets", "Chongqing": "chn_cq_ets", "Fujian": "chn_fj_ets",
        "New Zealand": "nzl_ets", "Regional Greenhouse": "usa_rggi", "California": "usa_ca_ets",
        "Korean": "kor_ets", "Washington": "usa_wa_ets"
    }

    # Define currencies for valid schemes
    curr_codes = {
        "eu_ets": "EUR", "nzl_ets": "NZD", "kor_ets": "KRW", "gbr_ets": "GBP", "chn_ets": "CNY",
        "deu_ets": "EUR", "chn_sz_ets": "CNY", "chn_sh_ets": "CNY", "chn_bj_ets": "CNY",
        "chn_gd_ets": "CNY", "chn_tj_ets": "CNY", "chn_hb_ets": "CNY", "chn_cq_ets": "CNY", "chn_fj_ets": "CNY"
    }

    drop_schemes = {"usa_rggi", "can_on_ets", "che_ets", "usa_ca_ets", "can_qc_cat", "can_ns_ets", "usa_wa_ets"}

    icap_dir = os.path.join(price_dir, "_icap")
    preferred_path = os.path.join(icap_dir, "_ICAP_allowance_prices.csv")
    if os.path.exists(preferred_path):
        icap_csv_path = preferred_path
    else:
        icap_files = [
            os.path.join(icap_dir, filename)
            for filename in os.listdir(icap_dir)
            if filename.startswith("icap_prices") and filename.endswith(".csv")
        ]
        if not icap_files:
            raise FileNotFoundError(
                f"No ICAP price files found in {icap_dir}. Expected files like "
                "'icap_pricesYYYYMMDD_HHMMSS.csv'."
            )
        icap_csv_path = max(icap_files, key=os.path.getmtime)

    # Read header row for column filtering
    columns = pd.read_csv(icap_csv_path, encoding="latin-1", nrows=0).columns
    target_cols = [col for col in columns if any(key in col for key in column_map)]

    # Read actual data (header=1 skips redundant top row)
    df = pd.read_csv(icap_csv_path, encoding="latin-1", header=1, low_memory=False)
    primary_cols = df.columns[df.columns.str.startswith("Primary Market")]
    secondary_cols = df.columns[df.columns.str.startswith("Secondary Market")]
    if len(primary_cols) == 0 and len(secondary_cols) == 0:
        raise ValueError(
            f"No 'Primary Market' or 'Secondary Market' columns found in {icap_csv_path}. "
            "The ICAP download format may have changed."
        )
    if len(primary_cols) == 0:
        logging.warning("No 'Primary Market' columns found in %s.", icap_csv_path)
    if len(secondary_cols) == 0:
        logging.warning("No 'Secondary Market' columns found in %s.", icap_csv_path)

    if (
        len(primary_cols) != len(target_cols)
        or len(secondary_cols) != len(target_cols)
    ):
        logging.warning(
            "Mismatch between scheme headers and market columns in %s. "
            "Found %s scheme columns, %s primary columns, %s secondary columns. "
            "Aligning by position using the shorter length.",
            icap_csv_path,
            len(target_cols),
            len(primary_cols),
            len(secondary_cols),
        )
        n = min(
            len(target_cols),
            len(primary_cols) if len(primary_cols) > 0 else len(target_cols),
            len(secondary_cols) if len(secondary_cols) > 0 else len(target_cols),
        )
        target_cols = target_cols[:n]
        primary_cols = primary_cols[:n]
        secondary_cols = secondary_cols[:n]

    # Resolve target scheme IDs in order
    scheme_ids: list[str] = []
    use_idx: list[int] = []
    for idx, col in enumerate(target_cols):
        mapped = ""
        for key, new_name in column_map.items():
            if key in col:
                mapped = new_name
                break
        if mapped:
            scheme_ids.append(mapped)
            use_idx.append(idx)

    target_cols = [target_cols[i] for i in use_idx]
    primary_cols = [primary_cols[i] for i in use_idx]
    secondary_cols = [secondary_cols[i] for i in use_idx]

    def _build_market_df(market_cols: list[str]) -> pd.DataFrame:
        if not market_cols:
            return pd.DataFrame(columns=["Date"] + scheme_ids)
        out = pd.concat([df.loc[:, ["Date"]], df.loc[:, market_cols]], axis=1)
        out.columns = ["Date"] + scheme_ids
        return out

    primary_df = _build_market_df(primary_cols)
    secondary_df = _build_market_df(secondary_cols)

    # Remove trailing rows with summary text
    if len(primary_df) >= 4:
        primary_df = primary_df.iloc[:-4].copy()
    if len(secondary_df) >= 4:
        secondary_df = secondary_df.iloc[:-4].copy()

    def _yearly_avg(market_df: pd.DataFrame) -> pd.DataFrame:
        if market_df.empty:
            return pd.DataFrame(columns=["year"])
        market_df = market_df.copy()
        market_df["year"] = market_df["Date"].str.extract(r"(\d{4})").astype(int)
        for col in market_df.columns:
            if col in ("Date", "year"):
                continue
            market_df[col] = pd.to_numeric(market_df[col], errors="coerce")
        yearly = market_df.drop(columns="Date").groupby("year", as_index=False).mean()
        yearly.drop(columns=drop_schemes & set(yearly.columns), errors="ignore", inplace=True)
        return yearly

    yearly_primary = _yearly_avg(primary_df)
    yearly_secondary = _yearly_avg(secondary_df)

    tidy_primary = yearly_primary.melt(
        id_vars=["year"], var_name="scheme_id", value_name="allowance_price_primary"
    )
    tidy_secondary = yearly_secondary.melt(
        id_vars=["year"], var_name="scheme_id", value_name="allowance_price_secondary"
    )

    merged = tidy_secondary.merge(tidy_primary, on=["year", "scheme_id"], how="outer")

    # Prefer secondary prices when available; fall back to primary.
    merged["allowance_price"] = merged["allowance_price_secondary"]
    primary_fill = merged["allowance_price"].isna()
    merged.loc[primary_fill, "allowance_price"] = merged.loc[
        primary_fill, "allowance_price_primary"
    ]

    # Flag large differences (>5% of secondary) when both are available.
    both = merged["allowance_price_secondary"].notna() & merged[
        "allowance_price_primary"
    ].notna()
    secondary_abs = merged["allowance_price_secondary"].abs()
    diff = (merged["allowance_price_primary"] - merged["allowance_price_secondary"]).abs()
    merged["primary_secondary_diff_flag"] = False
    merged.loc[both & (secondary_abs == 0), "primary_secondary_diff_flag"] = (
        diff[both & (secondary_abs == 0)] > 0
    )
    merged.loc[both & (secondary_abs > 0), "primary_secondary_diff_flag"] = (
        diff[both & (secondary_abs > 0)] > (0.05 * secondary_abs[both & (secondary_abs > 0)])
    )

    tidy = merged.loc[:, ["scheme_id", "year", "allowance_price", "primary_secondary_diff_flag"]]

    # Add metadata
    tidy["currency_code"] = tidy["scheme_id"].map(curr_codes).fillna("")
    tidy["source"] = "db(ICAP-ETS[2024])"
    tidy["comment"] = "yearly average of (daily) prices provided by ICAP"

    logging.info(f"Processed ICAP ETS prices: {tidy.shape[0]} records")

    return tidy



#-------------------------------------------------------------------

def load_ets_prices(price_dir: str = DEFAULT_PRICE_PATH):
    # Aggregate data from all the sources
    df = pd.concat(
        process_ets_prices(price_dir), 
        ignore_index=True
    )
    df = pd.concat([df, process_icap_prices(price_dir)])
    
    df["allowance_price"] =  df["allowance_price"].round(2)

    return df
