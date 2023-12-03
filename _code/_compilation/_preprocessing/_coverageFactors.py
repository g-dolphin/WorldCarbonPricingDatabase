#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 14:37:49 2021

@author: gd
"""


# We need to produce data frames whose entries are consistent with the main records 
# (i.e., there should be a coverage factor value only for rows where a scheme is actually in place)
# The strategy implemented below uses the dictionaries of schemes created 
# (this will ensure that we don't include more - or less - schemes than those in the dataset)

# We first create default data frames with default coverage factor value 1.
# We then introduce scheme-jurisdiction - specific values.

# Create structure of the data frame and fill in default values 

cf_taxes = pd.DataFrame()

for scheme in taxes_1_list:
    for year in taxes_scope[scheme]["jurisdictions"].keys():
        for jurisdiction in taxes_scope[scheme]["jurisdictions"][year]:        
            for sector in wcpd_all_jur.ipcc_code.unique():
                
                if sector in taxes_scope[scheme]["sectors"][year]:
                    cf_taxes = cf_taxes.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_CO2":1}, ignore_index=True)
                else:
                    cf_taxes = cf_taxes.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_CO2":"NA"}, ignore_index=True)

cf_ets = pd.DataFrame()

for scheme in ets_1_list+ets_2_list:
    for year in ets_scope[scheme]["jurisdictions"].keys():
        for jurisdiction in ets_scope[scheme]["jurisdictions"][year]:
            for sector in wcpd_all_jur.ipcc_code.unique():
                 
                if sector in ets_scope[scheme]["sectors"][year]:
                    cf_ets = cf_ets.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_CO2":1}, ignore_index=True)
                else:
                    cf_ets = cf_ets.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_CO2":"NA"}, ignore_index=True)


cf = pd.concat([cf_taxes, cf_ets])

# Define ad-hoc values
## EU ETS interaction with national carbon taxes

ipcc_code = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A","1A2C",
             "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
             "1A2K", "1A2L", "1A2M", "2A1", "2A2", "2A3", "2A4A",
             "2C1", "2H1"]

eu_ets_cf = {"Estonia":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.9, "comment":""}, 
             "Latvia":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.9, "comment":""}, 
             "Norway":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.9, "comment":""}, 
             "Poland":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.9, "comment":""}}

## National carbon taxes

est_tax_cf = {"Estonia":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.1,
                         "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"}}
lva_tax_cf = {"Latvia":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.1,
                         "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"}}
nor_tax_cf = {"Norway":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.1,
                         "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"}}
pol_tax_cf = {"Poland":{"year":[i for i in range (2005,2023)], "ipcc_code":ipcc_code, "value":0.1,
                         "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"}}
    
    
# Write values
cf_scheme = {"eu_ets":eu_ets_cf, "est_tax":est_tax_cf, "lva_tax":lva_tax_cf,
             "nor_tax":nor_tax_cf, "pol_tax":pol_tax_cf}

for scheme in cf_scheme.keys():
    for jur in cf_scheme[scheme].keys():
        
        rowSel = (cf.scheme_id==scheme) & (cf.jurisdiction==jur) & (cf.year.isin(cf_scheme[scheme][jur]["year"])) & (cf.ipcc_code.isin(cf_scheme[scheme][jur]["ipcc_code"]))
        
        cf.loc[rowSel, "cf_CO2"] = cf_scheme[scheme][jur]["value"]
        cf.loc[rowSel, "source"] = ""
        cf.loc[rowSel, "comment"] = cf_scheme[scheme][jur]["comment"]
