#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:57:58 2022

@author: gd
"""

import pandas as pd
import numpy as np


stream = open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/dependencies/jurisdictions.py")
read_file = stream.read()
exec(read_file)


wcpd_structure = pd.read_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/_aux_files/wcpd_structure.csv")

ctry_list = ctries
subnat_list = subnat_mex + subnat_jpn #subnat_can + subnat_chn + subnat_usa #+ 
all_jur_list = ctry_list + subnat_list

wcpd_all_jur = pd.DataFrame()

for jur in all_jur_list:
    wcpd_structure["jurisdiction"] = jur
    
    if wcpd_all_jur.empty == True:
        wcpd_all_jur = wcpd_structure
    else:
        wcpd_all_jur = pd.concat([wcpd_all_jur, wcpd_structure], axis=0)

wcpd_all_jur["tax_ex_rate"] = np.nan
wcpd_all_jur["tax_ex_rate_sources"] = np.nan

std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))

for jur in countries_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price_exemptions/national/tax_ex_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price_exemptions/subnat/tax_ex_"+subnat_dic[jur]+".csv", index=None)

    