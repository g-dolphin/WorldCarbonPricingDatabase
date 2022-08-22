#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:57:58 2022

@author: gd
"""

# This script creates the files recording the tax exemption/rebate data
# Current records have been manually constructed by encoding entries in raw csv files.
# The next update of this file will code these exemptions in the dedicated section below

import pandas as pd
import numpy as np


stream = open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/jurisdictions.py")
read_file = stream.read()
exec(read_file)

#ctry_list = ctries
#subnat_list = subnat_mex + subnat_jpn #subnat_can + subnat_chn + subnat_usa #+ 
#all_jur_list = ctry_list + subnat_list

# Add scope indicator variable to determine "NA" v. non "NA" values
wcpd_all_jur["tax_ex_rate"] = np.nan
wcpd_all_jur_sources["tax_ex_rate_sources"] = np.nan

wcpd_all_jur_sources.rename(columns={"tax_ex_rate_sources":"tax_ex_rate"}, inplace=True)


## Filling "tax_ex_rate" column with "NA" if no tax scheme
wcpd_all_jur.loc[wcpd_all_jur.tax!=1, "tax_ex_rate"] = "NA"
wcpd_all_jur_sources.loc[wcpd_all_jur.tax!=1, "tax_ex_rate"] = "NA"
#all_jur.loc[(all_jur.tax==1) & (all_jur.tax_ex_rate==""), :] #checking whether we've missed any exemptions

# Set default non-"NA" values to 0
wcpd_all_jur.loc[wcpd_all_jur.tax.isna(), "tax_ex_rate"] = 0
wcpd_all_jur_sources.loc[wcpd_all_jur.tax.isna(), "tax_ex_rate"] = 0


#--------------------------------Exemption/rebate coding-----------------------------

# 'Argentina'

# 'Australia' - no exemptions

# 'Colombia' - no exemptions

# 'Chile' - no exemptions

# 'Denmark' 

# 'Estonia' - no exemptions

# 'Finland' - no exemptions

# 'France' - no exemptions

# 'Iceland' - no exemptions

# 'Ireland' - no exemptions

# 'Japan' - no exemptions

# 'Liechtenstein' - no exemptions

# 'Mexico' - no exemptions

# 'Norway' - no exemptions

# 'Poland' - no exemptions

# 'Portugal'

# 'Slovenia'

# 'Sweden'

# 'Switzerland' - no exemptions

# 'United Kingdom' - no exemptions


#-------------------------------------------------------------------------------------


std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))

for jur in countries_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price_exemptions/tax/national/tax_ex_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price_exemptions/tax/subnat/tax_ex_"+subnat_dic[jur]+".csv", index=None)

    