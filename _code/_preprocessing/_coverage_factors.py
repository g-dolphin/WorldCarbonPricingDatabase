#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 14:37:49 2021

@author: gd
"""


# We need to produce data frames whose entries are consistent with the main records (i.e., there should be a coverage factor value only for rows where a scheme is actually in place)
# The strategy implemented below uses the dictionaries of schemes created (this will ensure that we don't include more - or less - schemes than those in the dataset)
# We first create default data frames with default coverage factor value 1.
# We then introduce scheme-jurisdiction - specific values.

# Create structure of the data frame 

for scheme in taxes_1_list:
    for year in taxes_coverage[scheme]["jurisdictions"].keys():
        for jurisdiction in taxes_coverage[scheme]["jurisdictions"][year]:        
            for sector in ipcc:

                df = df.append({'scheme_id':scheme, "Jurisdiction":jurisdiction,
                                "Year":year, "ipcc_code":sector}, ignore_index=True)

for scheme in ets_1_list:
    print(scheme)
    for year in ets_coverage[scheme]["jurisdictions"].keys():
        print(year)
        for jurisdiction in ets_coverage[scheme]["jurisdictions"][year]:
            print(jurisdiction)
            for sector in ipcc:
                 
                df = df.append({'scheme_id':scheme, "Jurisdiction":jurisdiction,
                                "Year":year, "ipcc_code":sector}, ignore_index=True)

# Fill values

for scheme in taxes_1_list:
    for year in taxes_coverage[scheme]["jurisdictions"].keys():
        for jurisdiction in taxes_coverage[scheme]["jurisdictions"][year]:        
            
            row = (df.scheme_id==scheme) & (df.Year==year) & (df.Jurisdiction==jurisdiction) & (~df.ipcc_code.isin(taxes_coverage[scheme]["sectors"][year]))
            row2 = (df.scheme_id==scheme) & (df.Year==year) & (df.Jurisdiction==jurisdiction) & (df.ipcc_code.isin(taxes_coverage[scheme]["sectors"][year]))
            
            df.loc[row, "coverage_factor"] = "NA"
            df.loc[row2, "coverage_factor"] = 1

for scheme in ets_1_list:
    for year in ets_coverage[scheme]["jurisdictions"].keys():
        for jurisdiction in ets_coverage[scheme]["jurisdictions"][year]:        
            
            row = (df.scheme_id==scheme) & (df.year==year) & (df.jurisdiction==jurisdiction) & (~df.ipcc_code.isin(ets_coverage[scheme]["sectors"][year]))
            row2 = (df.scheme_id==scheme) & (df.year==year) & (df.jurisdiction==jurisdiction) & (df.ipcc_code.isin(ets_coverage[scheme]["sectors"][year]))
            
            df.loc[row, "coverage_factor"] = "NA"
            df.loc[row2, "coverage_factor"] = 1


# EU ETS interaction with national carbon taxes



for scheme_dic in [taxes_1_list, ets_1_list]:
    for scheme in ["can_obps"]:#schemes:
        df.loc[df.scheme_id==scheme, :].to_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/wcpd_dataset/source_data/design_and_prices/exemptions/quantity_exemptions/"+scheme+"_qty_ex.csv", index=None)
    
    
    
    
    
    
    