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

# GAS = "CO2" # change to N2O / CH4 if needed


def build_cf_df(schemes, scope_dict, gas):
    rows = []
    for scheme in schemes:
        scheme_scope = scope_dict[scheme]
        for year, jurisdictions in scheme_scope["jurisdictions"].items():
            applicable_sectors = set(scheme_scope["sectors"][year])
            # Create all combinations using MultiIndex
            index = pd.MultiIndex.from_product(
                [[scheme], jurisdictions, [year], wcpd_all_jur.ipcc_code.unique()],
                names=["scheme_id", "jurisdiction", "year", "ipcc_code"]
            )
            df = pd.DataFrame(index=index).reset_index()
            df["cf_" + gas] = df["ipcc_code"].apply(lambda x: 1 if x in applicable_sectors else "NA")
            rows.append(df)
    return pd.concat(rows, ignore_index=True)

cf_taxes_co2 = build_cf_df(taxes_1_list, taxes_scope_data, "CO2")
cf_ets_co2 = build_cf_df(ets_1_list, ets_scope_data, "CO2") #+ ets_2_list
cf_taxes_ch4 = build_cf_df(taxes_1_list, taxes_scope_data, "CH4")
cf_ets_ch4 = build_cf_df(ets_1_list, ets_scope_data, "CH4") #+ ets_2_list
cf_taxes_n2o = build_cf_df(taxes_1_list, taxes_scope_data, "N2O")
cf_ets_n2o = build_cf_df(ets_1_list, ets_scope_data, "N2O") #+ ets_2_list


cf = pd.concat([cf_taxes_co2, cf_ets_co2, cf_taxes_ch4, cf_ets_ch4, cf_taxes_n2o, cf_ets_n2o], ignore_index=True)

# Define ad-hoc values
## EU ETS interaction with national carbon taxes

industry_ipcc_codes = [
    "1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2C",
    "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
    "1A2K", "1A2L", "1A2M", "2A1", "2A2", "2A3", "2A4A",
    "2C1", "2H1"
]

eu_ets_cf = [
    {
        "jurisdiction": jurisdiction,
        "year": list(range(2005, 2025)),
        "ipcc_codes": industry_ipcc_codes,
        "value": 0.9,
        "comment": ""
    }
    for jurisdiction in ["Estonia", "Latvia", "Norway", "Poland"]
] + [
    {
        "jurisdiction": jurisdiction,
        "year": list(range(2013, 2025)),
        "ipcc_codes": ["1A3A1"],  # International aviation
        "value": 0.51,
        "comment": ""
    }
    for jurisdiction in [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden", "Norway", "Iceland", "Liechtenstein"
]
]

# EU-27 international aviation emissions (from EEA): 121742859 t CO2
# EU-27 EU-ETS covered emissions: ~62 MtCO₂
# coverage factor: 62/122 = 0.51

## UK ETS international aviation (ipcc code: "1A3A1")

gbr_ets_cf = [
    {
    "jurisdiction": "United Kingdom",
    "year": list(range(2021, 2025)),
    "ipcc_codes": ["1A3A1"],
    "value": 0.32,
    "comment": ""
    }
]

# UK ETS international aviation emissions (from EEA): 13.6 Mt CO2
# UK ETS covered emissions (UK-EEA flights): 5.4 MtCO₂
# coverage factor: 0.9/3.1 = 0.28

## Swiss ETS internation aviation (ipcc code: "1A3A1")
che_ets_cf = [
    {
    "jurisdiction": "Switzerland",
    "year": list(range(2021, 2025)),
    "ipcc_codes": ["1A3A1"],
    "value": 0.28,
    "comment": ""
    }
]

# Swiss ETS international aviation emissions (from EEA): 13.6 Mt CO2
# Swiss ETS covered emissions (CHE-EEA flights): 5.4 MtCO₂
# coverage factor: 5.4/13.6 = 0.32

## National carbon taxes

est_tax_cf = [
    {
    "jurisdiction":"Estonia",
    "year":list(range(2005, 2025)), 
    "ipcc_codes":industry_ipcc_codes, 
    "value":0.1,
    "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"
    }
    ]
lva_tax_cf = [
    {
    "jurisdiction":"Latvia",
    "year":list(range(2005, 2025)), 
    "ipcc_codes":industry_ipcc_codes, 
    "value":0.1,
    "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"
    }
    ]
nor_tax_cf = [
    {
    "jurisdiction":"Norway",
    "year":list(range(2005, 2025)), 
    "ipcc_codes":industry_ipcc_codes, 
    "value":0.1,
    "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"
    }
    ]
pol_tax_cf = [
    {
    "jurisdiction":"Poland",
    "year":list(range(2005, 2025)), 
    "ipcc_codes":industry_ipcc_codes, 
    "value":0.1,
    "comment":"introduction of the EU ETS; all ETS covered installations are exempt from the tax"
    }
    ]
    
    
# Write values
cf_scheme = {
    "eu_ets":eu_ets_cf, "est_tax":est_tax_cf, 
    "che_ets":che_ets_cf, "gbr_ets":gbr_ets_cf, 
    "lva_tax":lva_tax_cf, "nor_tax":nor_tax_cf, 
    "pol_tax":pol_tax_cf
    }

for scheme in cf_scheme.keys():
    for dic in cf_scheme[scheme]:
        
        rowSel = (cf.scheme_id==scheme) & (cf.jurisdiction==dic["jurisdiction"]) & (cf.year.isin(dic["year"])) & (cf.ipcc_code.isin(dic["ipcc_codes"]))
        
        cf.loc[rowSel, "cf_CO2"] = dic["value"]
        cf.loc[rowSel, "cf_CH4"] = "NA"
        cf.loc[rowSel, "cf_N2O"] = "NA"
        cf.loc[rowSel, "source"] = ""
        cf.loc[rowSel, "comment"] = dic["comment"]
