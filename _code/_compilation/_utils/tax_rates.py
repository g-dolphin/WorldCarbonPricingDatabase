#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load and aggregate carbon tax rate data by gas type.
"""

import os
import glob
import logging
import pandas as pd
import numpy as np
from typing import Optional

# ------------------------ Logging ------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ------------------------ Default Path Handling ------------------------

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

DEFAULT_TAX_PATH = os.path.normpath(os.path.join(BASE_DIR, "_raw/price"))

# ------------------------ Core Function ------------------------

def load_tax_rates(
    price_path,
    gas: str
) -> pd.DataFrame:
    """
    Load and aggregate tax price data for a given GHG.

    Args:
        gas (str): Greenhouse gas (e.g., "CO2", "CH4")
        price_path (str, optional): Directory path to tax CSVs

    Returns:
        pd.DataFrame: Combined and cleaned carbon tax data
    """
    price_path = price_path or DEFAULT_TAX_PATH
    pattern = os.path.join(price_path, "*_tax*_prices.csv")
    file_list = glob.glob(pattern)

    df_list = []

    for file in file_list:
        try:
            df = pd.read_csv(file, keep_default_na=False, header=0, encoding="latin-1", dtype={"product": str})
            df = df[df["ghg"] == gas]
            df["rate"] = pd.to_numeric(df["rate"].replace(["NA", ""], np.nan), errors="coerce")
            df_list.append(df)
            logging.info(f"Loaded tax data from: {os.path.basename(file)}")
        except Exception as e:
            logging.warning(f"Failed to process file {file}: {e}")

    if not df_list:
        logging.warning(f"No valid tax data found for GHG: {gas}")
        return pd.DataFrame()

    combined_df = pd.concat(df_list, ignore_index=True)
    logging.info(f"Compiled tax data: {combined_df.shape[0]} records")

    return combined_df



