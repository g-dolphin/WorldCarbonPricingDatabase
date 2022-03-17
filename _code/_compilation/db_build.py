#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 19:20:51 2021

@author: gd
"""

import os
import glob
import pandas as pd
import numpy as np

from importlib.machinery import SourceFileLoader

# Specify greenhouse gas for which the dataset is built
gas = "CO2" # or CH4 / HFCs / PFCs / SF6

# Load modules
etsPricesModule = SourceFileLoader('ets_prices', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/ets_prices.py').load_module()
taxRatesModule = SourceFileLoader('tax_rates', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/tax_rates.py').load_module()
etsScopeModule = SourceFileLoader('ets_scope', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/scope/ets/ets_scope_'+gas+'.py').load_module()
taxScopeModule = SourceFileLoader('taxes_scope', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/scope/tax/taxes_scope_'+gas+'.py').load_module()

# 1. Load original dataset

def concatenate(indir):#,outfile):
    os.chdir(indir) #sets the current directory to 'indir'
    fileList=glob.glob("*.csv") #this command generates a list of csv files
    dfList = []

    #each iteration of the loop will add a dataframe to the list
    for filename in fileList:
        df=pd.read_csv(filename, keep_default_na=False, header=0, encoding='latin-1')
        dfList.append(df)

    #'axis=0' ensures that we are concatenating vertically,
    concatDf=pd.concat(dfList,axis=0)

    #    concatDf.to_csv(outfile,index=None)
    return concatDf

indir_nat = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/national"
indir_subnat = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/subnational"
indir_nat_sources = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/national"
indir_subnat_sources = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/subnational"

indir_exemptions_nat = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price_exemptions/national"
indir_exemptions_subnat = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price_exemptions/subnat"

nat_jur = concatenate(indir_nat)
subnat_jur = concatenate(indir_subnat)
all_jur = pd.concat([nat_jur, subnat_jur])

nat_jur_sources = concatenate(indir_nat_sources)
subnat_jur_sources = concatenate(indir_subnat_sources)
all_jur_sources = pd.concat([nat_jur_sources, subnat_jur_sources])

price_exemptions_nat = concatenate(indir_exemptions_nat)
price_exemptions_subnat = concatenate(indir_exemptions_subnat)
price_exemptions_all_jur = pd.concat([price_exemptions_nat, price_exemptions_subnat])

price_exemptions_all_jur.rename(columns={'Jurisdiction':"jurisdiction", 
                                         'Year':"year", 'IPCC_cat_code':"ipcc_code", 
                                         'Tax_ex_rate':"tax_ex_rate",
                                         'Tax_ex_rate_sources':"tax_ex_rate_sources"}, inplace=True)

price_exemptions_all_jur.replace(to_replace={"Coal/peat":"Coal"}, inplace=True)

# Jurisdiction lists

ctry_list = list(nat_jur.jurisdiction.unique())
subnat_list = list(subnat_jur.jurisdiction.unique())
all_jur_list = ctry_list + subnat_list


#----------------------------DB structure------------------------#

all_jur = all_jur[["jurisdiction", "year", "ipcc_code", "Product"]]
all_jur_sources = all_jur_sources[["jurisdiction", "year", "ipcc_code", "Product"]]

all_jur_sources["year"] = all_jur_sources["year"].astype(int)

#------------------------Primary:Emissions trading systems---------------------------#

ets_1_list = {"CO2":["eu_ets", "nzl_ets", "che_ets", "kor_ets", "kaz_ets", 
                     "us_ca_cat", "us_rggi", 'can_obps',
                     "can_nl_ets", "can_ns_ets", "can_qc_cat", "can_ab_ets", "can_sk_ets",
                     "chn_sh_ets",
                     'chn_sz_ets', 'chn_sh_ets', 'chn_bj_ets', 'chn_gd_ets', 'chn_tj_ets', 
                     'chn_hb_ets', 'chn_cq_ets', 'chn_fj_ets']}

ets_prices = etsPricesModule.prices_df("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price")
#ets_prices = ets_prices.loc[ets_prices.ghg==gas]

ets_scope = etsScopeModule.scope()["data"]
ets_scope_sources = etsScopeModule.scope()["sources"]

def ets_db_values(scheme_list, scheme_no):
    
    if scheme_no == "scheme_1":
        columns = {"id":"ets_id", "binary":"ets", "price":"ets_price", 
                   "curr_code":"ets_curr_code"}
    if scheme_no == "scheme_2":
        columns = {"id":"ets_2_id", "binary":"ets_2", "price":"ets_2_price", 
                   "curr_code":"ets_2_curr_code"}
    
    for scheme in scheme_list:
        for yr in ets_scope[scheme]["jurisdictions"].keys():   
            selection = (all_jur.year==yr) & (all_jur.jurisdiction.isin(ets_scope[scheme]["jurisdictions"][yr])) & (all_jur.ipcc_code.isin(ets_scope[scheme]["sectors"][yr]))
            selection_sources = (all_jur_sources.year==yr) & (all_jur_sources.jurisdiction.isin(ets_scope[scheme]["jurisdictions"][yr])) & (all_jur_sources.ipcc_code.isin(ets_scope[scheme]["sectors"][yr]))
    
            all_jur.loc[selection, columns["binary"]] = 1
            all_jur.loc[selection, columns["id"]] = scheme
            
            # Scope data source
            all_jur_sources.loc[selection_sources, columns["binary"]] = ets_scope_sources[scheme][yr]
            
            try:        
                all_jur.loc[selection, columns["price"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "allowance_price"].item()
                all_jur.loc[selection, columns["curr_code"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "currency_code"].item()
                
                # Price data source
                all_jur_sources.loc[selection_sources, columns["price"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "source"].item()+"; "+ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "comment"].item()
                
            except:
                print(scheme, yr)

ets_db_values(ets_1_list[gas], "scheme_1")

#--------------------------------Primary:Carbon taxes--------------------------------#

taxes_1_list = {"CO2":["can_ab_tax", "arg_tax", "can_bc_tax", "aus_tax", "can_tax_I",
                       "can_tax_II", "chl_tax", "col_tax", "dnk_tax", "est_tax", "fin_tax",
                       "fra_tax", "isl_tax", "irl_tax", "jpn_tax", "lva_tax", "lie_tax",
                       "mex_tax", "can_nb_tax", "can_nl_tax", "can_nt_tax", "nor_tax_I",
                       "nor_tax_II", "pol_tax", "prt_tax", "can_pe_tax", "sgp_tax",
                       "slo_tax", "zaf_tax", "swe_tax", "che_tax", "gbr_tax",
                       "ukr_tax"]} #, "mex_zac_tax", "esp_tax"

tax_rates = taxRatesModule.prices_df("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price/")
tax_rates.rename(columns={"product":"em_type"}, inplace=True)
tax_rates = tax_rates.loc[tax_rates.ghg==gas]

taxes_scope = taxScopeModule.scope()["data"]
taxes_scope_sources = taxScopeModule.scope()["sources"]

def tax_db_values(scheme_list, scheme_no):
    
    if scheme_no == "scheme_1":
        columns = {"id":"tax_id", "binary":"tax", "rate":"tax_rate_excl_ex_clcu", 
                   "curr_code":"tax_curr_code"}
    if scheme_no == "scheme_2":
        columns = {"id":"tax_2_id", "binary":"tax_2",  
                   "rate":"tax_2_rate_excl_ex_clcu", "curr_code":"tax_2_curr_code"}

    for scheme in scheme_list:
        print(scheme)
        for yr in taxes_scope[scheme]["jurisdictions"].keys():   
            selection = (all_jur.year==yr) & (all_jur.jurisdiction.isin(taxes_scope[scheme]["jurisdictions"][yr])) & (all_jur.ipcc_code.isin(taxes_scope[scheme]["sectors"][yr])) & (all_jur.Product.isin(taxes_scope[scheme]["fuels"][yr]))
            selection_sources = (all_jur_sources.year==yr) & (all_jur_sources.jurisdiction.isin(taxes_scope[scheme]["jurisdictions"][yr])) & (all_jur_sources.ipcc_code.isin(taxes_scope[scheme]["sectors"][yr])) & (all_jur_sources.Product.isin(taxes_scope[scheme]["fuels"][yr]))
    
            all_jur.loc[selection, columns["binary"]] = 1
            all_jur.loc[selection, columns["id"]] = scheme
            
            # Scope data source 
            all_jur_sources.loc[selection_sources, columns["binary"]] = taxes_scope_sources[scheme][yr]
            
            try:
                for type_em in ["Oil", "Natural gas", "Coal"]:
                    all_jur.loc[selection & (all_jur.Product == type_em), columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "rate"].item()                
                    all_jur.loc[selection & (all_jur.Product == type_em), columns["curr_code"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "currency_code"].item()
                
#                   # Price data source
                    value = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "source"].item()+"; "+tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "comment"].item()
                    all_jur_sources.loc[selection_sources & (all_jur_sources.Product == type_em), columns["rate"]] = value
                
            except:
                print(scheme, yr)
 
tax_db_values(taxes_1_list[gas], "scheme_1")

#----------------------------Second pricing scheme----------------------#
# NOTE: The "second pricing scheme" columns are only used when, for a given 
#       jurisdiction, at least one sector is (in any given year) either 
#       (i) covered by >1 carbon tax; OR 
#       (ii) covered by >1 emissions trading system.
#       In all other cases, i.e. cases where there is no strict overlap,
#       the pricing scheme information is recorded in the primary columns
#----------------------------Second:Emissions trading systems------------#

ets_2_list = {"CO2":["us_ma_ets"]}
ets_db_values(ets_2_list, "scheme_2")

#----------------------------Second:carbon taxes------------#

tax_2_list = {"CO2":[]}
tax_db_values(tax_2_list, "scheme_2")

#----------------------------------------------------------------#
 
# Blank cells filling

all_jur.loc[all_jur.tax!=1, "tax"] = 0
all_jur.loc[all_jur.ets!=1, "ets"] = 0

#---------------------Sector-fuel scope exceptions----------------------#
 
# Format: all_jur.loc[(all_jur.Jurisdiction=="jur_name") & (all_jur.Year==yr) & (all_jur.IPCC_cat_code=="ipcc_code") & (all_jur.Product=="prod_name"), ] #"Tax_dummy", "ETS_dummy"


#------------------------------Exemptions----------------------------------#

# Price-based exemptions
# Add (price-based) exemptions/rebate column for carbon taxes

all_jur = all_jur.merge(price_exemptions_all_jur[["jurisdiction", "year", "ipcc_code", "Product", "tax_ex_rate"]], 
                        on = ["jurisdiction", "year", "ipcc_code", "Product"], how="left")

all_jur_sources = all_jur_sources.merge(price_exemptions_all_jur[["jurisdiction", "year", "ipcc_code", "Product", "tax_ex_rate_sources"]], 
                                        on = ["jurisdiction", "year", "ipcc_code", "Product"], how="left")
all_jur_sources.rename(columns={"tax_ex_rate_sources":"tax_ex_rate"}, inplace=True)

## Filling "tax_ex_rate" column with "NA" if no tax scheme
all_jur.loc[all_jur.tax!=1, "tax_ex_rate"] = "NA"
#all_jur.loc[(all_jur.tax==1) & (all_jur.tax_ex_rate==""), :] #checking whether we've missed any exemptions

all_jur.loc[all_jur.tax_ex_rate=="NA", "tax_ex_rate"] = np.nan # changing "NA" to NaN to be able to execute column multiplication
all_jur.loc[all_jur.tax_ex_rate=="", "tax_ex_rate"] = np.nan
all_jur.loc[all_jur.tax_rate_excl_ex_clcu=="NA", "tax_rate_excl_ex_clcu"] = np.nan # changing "NA" to NaN to be able to execute column multiplication
all_jur.loc[all_jur.tax_rate_excl_ex_clcu=="", "tax_rate_excl_ex_clcu"] = np.nan

all_jur["tax_ex_rate"] = all_jur["tax_ex_rate"].astype(float)
all_jur["tax_rate_excl_ex_clcu"] = all_jur["tax_rate_excl_ex_clcu"].astype(float)

## Calculate tax rate including rebate
all_jur.loc[:, "tax_rate_incl_ex_clcu"] = all_jur.loc[:, "tax_rate_excl_ex_clcu"]*(1-all_jur.loc[:, "tax_ex_rate"])


# Fill 'NA' values

## For 'Product' keys
all_jur.fillna({"Product":"NA"}, inplace=True)
all_jur_sources.fillna({"Product":"NA"}, inplace=True)

tax_cols = ['tax_id', 'tax_rate_excl_ex_clcu', 'tax_curr_code',
            'tax_ex_rate', 'tax_rate_incl_ex_clcu']

ets_1_cols = ['ets_id', 'ets_price', 'ets_curr_code']
ets_2_cols = ['ets_2_id']#, 'ets_2_price', 'ets_curr_code']

all_jur.loc[all_jur.tax==0.0, tax_cols] = "NA" 
all_jur.loc[all_jur.ets==0.0, ets_1_cols] = "NA"

# Re-ordering columns
all_jur = all_jur[["jurisdiction", "year", "ipcc_code",
                   "Product", "tax", "ets", "tax_id",
                   "tax_rate_excl_ex_clcu", "tax_ex_rate", 
                   "tax_rate_incl_ex_clcu", "tax_curr_code", "ets_id", "ets_price",
                   "ets_curr_code"]]

all_jur_sources = all_jur_sources[["jurisdiction", "year", "ipcc_code", 
                                   "Product", "tax", "ets",
                                   "tax_rate_excl_ex_clcu", "tax_ex_rate",
                                   "ets_price"]]

# Breaking up dataframe into single jurisdiction .csv files
std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))



for jur in countries_dic:
    all_jur.loc[all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/national/CP_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    all_jur.loc[all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/subnational/CP_"+subnat_dic[jur]+".csv", index=None)

for jur in countries_dic:
    all_jur_sources.loc[all_jur_sources.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/national/CP_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    all_jur_sources.loc[all_jur_sources.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/subnational/CP_"+subnat_dic[jur]+".csv", index=None)
    
    
