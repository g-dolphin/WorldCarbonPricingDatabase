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
                data[code].iloc[:, "allowance_price"] = data[code].iloc[:, "allowance_price"] / 0.907185
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

    icap_csv_path = os.path.join(price_dir, "_icap-graph-price-data-2008-04-01-2025-04-15.csv")

    # Read header row for column filtering
    columns = pd.read_csv(icap_csv_path, encoding="latin-1", nrows=0).columns
    target_cols = [col for col in columns if any(key in col for key in column_map)]

    # Read actual data (header=1 skips redundant top row)
    df = pd.read_csv(icap_csv_path, encoding="latin-1", header=1, low_memory=False)
    df = pd.concat([df.loc[:, ["Date"]], df.loc[:, df.columns.str.startswith('Reference Market')]],
                         axis=1)
    df.columns = ["Date"]+target_cols

    # Rename columns using first match
    renamed_cols = {"Date": "Date"}
    for col in target_cols:
        for key, new_name in column_map.items():
            if key in col:
                renamed_cols[col] = new_name
                break

    df.rename(columns=renamed_cols, inplace=True)

    # Remove trailing rows with summary text
    df = df.iloc[:-4].copy()

    # Extract year from date string
    df["year"] = df["Date"].str.extract(r"(\d{4})").astype(int)

    # Ensure numeric prices
    for col in df.columns:
        if col not in ("Date", "year"):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Compute yearly averages
    yearly_avg = df.drop(columns="Date").groupby("year", as_index=False).mean()

    # Drop unneeded schemes
    yearly_avg.drop(columns=drop_schemes & set(yearly_avg.columns), errors="ignore", inplace=True)

    # Melt into long format
    tidy = yearly_avg.melt(id_vars=["year"], var_name="scheme_id", value_name="allowance_price")

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
