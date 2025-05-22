#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 1 2023
"""

import numpy as np
import pandas as pd

from importlib.machinery import SourceFileLoader

# Load coverage factor computation module
ecp_cov_fac = SourceFileLoader(
    'coverage_factors',
    '/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp/ecp_v3_coverageFactors.py'
).load_module()

# -------------------------------------------------------------------------
# Compute overlap between schemes (tax, ETS, ETS2) using coverage factors
# -------------------------------------------------------------------------

# Compute coverage factors
overlap = ecp_cov_fac.coverageFactors(wcpd_all_jur.copy(), gas)

# Retain relevant columns
overlap = overlap[[
    "jurisdiction", "year", "ipcc_code", "Product",
    "tax_id", "ets_id", "ets_2_id",
    "tax_cf", "ets_cf", "ets_2_cf"
]]

# Binarize scheme presence
for scheme in ["tax_id", "ets_id", "ets_2_id"]:
    overlap[scheme + "_bin"] = np.where(overlap[scheme] != "NA", 1, 0)

# Count active mechanisms and sum coverage factors
overlap["inForce"] = overlap[["tax_id_bin", "ets_id_bin", "ets_2_id_bin"]].sum(axis=1)
overlap["cf_sum"] = overlap[["tax_cf", "ets_cf", "ets_2_cf"]].sum(axis=1)

# Identify overlaps: more than one scheme in force and combined CF > 1
overlap["overlap"] = np.where((overlap["inForce"] > 1) & (overlap["cf_sum"] > 1), 1, 0)
