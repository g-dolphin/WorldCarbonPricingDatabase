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
                                                "year":year, "ipcc_code":sector, "cf_co2":1}, ignore_index=True)
                else:
                    cf_taxes = cf_taxes.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_co2":"NA"}, ignore_index=True)

cf_ets = pd.DataFrame()

for scheme in ets_1_list+ets_2_list:
    for year in ets_scope[scheme]["jurisdictions"].keys():
        for jurisdiction in ets_scope[scheme]["jurisdictions"][year]:
            for sector in wcpd_all_jur.ipcc_code.unique():
                 
                if sector in ets_scope[scheme]["sectors"][year]:
                    cf_ets = cf_ets.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_co2":1}, ignore_index=True)
                else:
                    cf_ets = cf_ets.append({'scheme_id':scheme, "jurisdiction":jurisdiction,
                                                "year":year, "ipcc_code":sector, "cf_co2":"NA"}, ignore_index=True)


cf = pd.concat([cf_taxes, cf_ets])

# Ad-hoc values
## EU ETS interaction with national carbon taxes


# Write files

for scheme in taxes_1_list+ets_1_list:
    cf.loc[cf.scheme_id==scheme, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverageFactor/"+scheme+"_cf.csv", index=None)
    
    
    
    
    
    
    