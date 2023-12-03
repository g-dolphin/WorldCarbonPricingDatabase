#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Dec 1 2023

@author: gd
"""

from importlib.machinery import SourceFileLoader

ecp_cov_fac = SourceFileLoader('coverage_factors', '/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp/ecp_v3_coverageFactors.py').load_module()

# for each scheme-sect, check whether there is overlap

# a tricky issue is that two schemes may apply to the same sector-fuel but not cover the same emissions. 
# Hence overlap cannot be determined solely based on scheme-jurisdiction-fuel-entries

# Take final dataset files, sum over all mechanisms fields.
# If sum > 1, extract scheme_id entries (for that particular row)
# If sum of coverage factors > 1, overlap = 1; else overlap = 0.
    
overlap = wcpd_all_jur.copy()

overlap = ecp_cov_fac.coverageFactors(overlap, gas)

overlap = overlap[["jurisdiction", "year", "ipcc_code", "Product", 
                   "tax_id", "ets_id", "ets_2_id", 
                   "tax_cf", "ets_cf", "ets_2_cf"]]  

for col in ["tax_id", "ets_id", "ets_2_id"]:
    overlap.loc[overlap[col]!="NA", col+"_bin"] = 1
    overlap.loc[overlap[col]=="NA", col+"_bin"] = 0

overlap["inForce"] = overlap[["tax_id_bin", "ets_id_bin", "ets_2_id_bin"]].sum(axis=1) 
overlap["cf_sum"] = overlap[["tax_cf", "ets_cf", "ets_2_cf"]].sum(axis=1)

overlap["overlap"] = 0
overlap.loc[(overlap.inForce>1) & (overlap.cf_sum>1), "overlap"] = 1
