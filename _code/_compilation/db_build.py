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

etsPricesModule = SourceFileLoader('ets_prices', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/ets_prices.py').load_module()
taxRatesModule = SourceFileLoader('tax_rates', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/tax_rates.py').load_module()
etsCoverageModule = SourceFileLoader('ets_coverage', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverage/ets_coverage.py').load_module()
taxCoverageModule = SourceFileLoader('taxes_coverage', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverage/taxes_coverage.py').load_module()

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

# Jurisdiction lists

ctry_list = list(nat_jur.Jurisdiction.unique())
subnat_list = list(subnat_jur.Jurisdiction.unique())
all_jur_list = ctry_list + subnat_list


#----------------------------DB structure------------------------#

all_jur = all_jur[["Jurisdiction", "Year", "IPCC_cat_code", "Product"]]
all_jur_sources = all_jur_sources[["Jurisdiction", "Year", "IPCC_cat_code", "Product"]]


#------------------------Primary:Emissions trading systems---------------------------#

ets_1_list = ["eu_ets", "nzl_ets", "che_ets", "kor_ets", "kaz_ets", 
              "us_ca_cat", "us_rggi", 'can_obps',
              "can_nl_ets", "can_ns_ets", "can_qc_cat", "can_ab_ets", "can_sk_ets",
              "chn_sh_ets",
              'chn_sz_ets', 'chn_sh_ets', 'chn_bj_ets', 'chn_gd_ets', 'chn_tj_ets', 
              'chn_hb_ets', 'chn_cq_ets', 'chn_fj_ets']

ets_prices = etsPricesModule.prices_df("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price")
ets_coverage = etsCoverageModule.coverage()["data"]
ets_coverage_sources = etsCoverageModule.coverage()["sources"]

def ets_db_values(scheme_list, scheme_no):
    
    if scheme_no == "scheme_1":
        columns = {"id":"ets_id", "dummy":"ets", "price":"ets_price", 
                   "curr_code":"ets_curr_code"}
    if scheme_no == "scheme_2":
        columns = {"id":"ets_2_id", "dummy":"ets_2", "price":"ets_2_price", 
                   "curr_code":"ets_2_curr_code"}
    
    for scheme in scheme_list:
        for year in ets_coverage[scheme]["jurisdictions"].keys():   
            selection = (all_jur.Year==year) & (all_jur.Jurisdiction.isin(ets_coverage[scheme]["jurisdictions"][year])) & (all_jur.IPCC_cat_code.isin(ets_coverage[scheme]["sectors"][year]))
            selection_sources = (all_jur_sources.Year==year) & (all_jur_sources.Jurisdiction.isin(ets_coverage[scheme]["jurisdictions"][year])) & (all_jur_sources.IPCC_cat_code.isin(ets_coverage[scheme]["sectors"][year]))
    
            all_jur.loc[selection, columns["dummy"]] = 1
            all_jur.loc[selection, columns["id"]] = scheme
            
            # Coverage data source
            all_jur_sources.loc[selection_sources, columns["dummy"]] = ets_coverage_sources[scheme][year]
            
            try:        
                all_jur.loc[selection, columns["price"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==year), "allowance_price"].item()
                all_jur.loc[selection, columns["curr_code"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==year), "currency_code"].item()
                
                # Price data source
                all_jur_sources.loc[selection_sources, columns["price"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==year), "source"].item()+"; "+ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==year), "comment"].item()
                
            except:
                print(scheme, year)

ets_db_values(ets_1_list, "scheme_1")

#--------------------------------Primary:Carbon taxes--------------------------------#

taxes_1_list = ["can_ab_tax", "arg_tax", "can_bc_tax", "aus_tax", "can_tax_I",
               "can_tax_II", "chl_tax", "col_tax", "dnk_tax", "est_tax", "fin_tax",
               "fra_tax", "isl_tax", "irl_tax", "jpn_tax", "lva_tax", "lie_tax",
               "mex_tax", "can_nb_tax", "can_nl_tax", "can_nt_tax", "nor_tax_I",
               "nor_tax_II", "pol_tax", "prt_tax", "can_pe_tax", "sgp_tax",
               "slo_tax", "zaf_tax", "swe_tax", "che_tax", "gbr_tax",
               "ukr_tax"] #, "mex_zac_tax", "esp_tax"

tax_rates = taxRatesModule.prices_df("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price/")
taxes_coverage = taxCoverageModule.coverage()["data"]
taxes_coverage_sources = taxCoverageModule.coverage()["sources"]

def tax_db_values(scheme_list, scheme_no):
    
    if scheme_no == "scheme_1":
        columns = {"id":"tax_id", "dummy":"tax", "rate":"tax_rate_excl_ex_clcu", 
                   "curr_code":"tax_curr_code"}
    if scheme_no == "scheme_2":
        columns = {"id":"tax_2_id", "dummy":"tax_2",  
                   "rate":"tax_2_rate_excl_ex_clcu", "curr_code":"tax_2_curr_code"}

    for scheme in scheme_list:

        for year in taxes_coverage[scheme]["jurisdictions"].keys():   
            selection = (all_jur.Year==year) & (all_jur.Jurisdiction.isin(taxes_coverage[scheme]["jurisdictions"][year])) & (all_jur.IPCC_cat_code.isin(taxes_coverage[scheme]["sectors"][year])) & (all_jur.Product.isin(taxes_coverage[scheme]["fuels"][year]))
            selection_sources = (all_jur_sources.Year==year) & (all_jur_sources.Jurisdiction.isin(taxes_coverage[scheme]["jurisdictions"][year])) & (all_jur_sources.IPCC_cat_code.isin(taxes_coverage[scheme]["sectors"][year])) & (all_jur_sources.Product.isin(taxes_coverage[scheme]["fuels"][year]))
    
            all_jur.loc[selection, columns["dummy"]] = 1
            all_jur.loc[selection, columns["id"]] = scheme
            
            # Coverage data source 
            all_jur_sources.loc[selection_sources, columns["dummy"]] = taxes_coverage_sources[scheme][year]
            
            try:        
                all_jur.loc[selection & (all_jur.Product == "Oil"), columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==year), "Oil"].item()
                all_jur.loc[selection & (all_jur.Product == "Natural gas"),columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==year), "Natural gas"].item()            
                all_jur.loc[selection & (all_jur.Product == "Coal/peat"), columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==year), "Coal/peat"].item()
                
                all_jur.loc[selection, columns["curr_code"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==year), "currency_code"].item()
                
                
                # Price data source
                all_jur_sources.loc[selection_sources, columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==year), "source"].item()+"; "+tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==year), "comment"].item()
                
            except:
                print(scheme, year)
 
tax_db_values(taxes_1_list, "scheme_1")

#----------------------------Second pricing scheme----------------------#
# NOTE: The "second pricing scheme" columns are only used when, for a given 
#       jurisdiction, at least one sector is (in any given year) either 
#       (i) covered by >1 carbon tax; OR 
#       (ii) covered by >1 emissions trading system.
#       In all other cases, i.e. cases where there is no strict overlap,
#       the pricing scheme information is recorded in the primary columns
#----------------------------Second:Emissions trading systems------------#

ets_2_list = ["us_ma_ets"]
ets_db_values(ets_2_list, "scheme_2")

#----------------------------Second:carbon taxes------------#

tax_2_list = []
tax_db_values(tax_2_list, "scheme_2")

#----------------------------------------------------------------#
 
# Blank cells filling

all_jur.loc[all_jur.tax!=1, "tax"] = 0
all_jur.loc[all_jur.ets!=1, "ets"] = 0

#---------------------Sector-fuel coverage exceptions----------------------#
 
# Format: all_jur.loc[(all_jur.Jurisdiction=="jur_name") & (all_jur.Year==yr) & (all_jur.IPCC_cat_code=="ipcc_code") & (all_jur.Product=="prod_name"), ] #"Tax_dummy", "ETS_dummy"


#------------------------------Exemptions----------------------------------#

# Price-based exemptions
# Add (price-based) exemptions/rebate column for carbon taxes

all_jur = all_jur.merge(price_exemptions_all_jur[["Jurisdiction", "Year", "IPCC_cat_code", "Product", "Tax_ex_rate"]], 
                        on = ["Jurisdiction", "Year", "IPCC_cat_code", "Product"], how="left")
all_jur.rename(columns={"Tax_ex_rate":"tax_ex_rate"}, inplace=True)

all_jur_sources = all_jur_sources.merge(price_exemptions_all_jur[["Jurisdiction", "Year", "IPCC_cat_code", "Product", "Tax_ex_rate_sources"]], 
                                        on = ["Jurisdiction", "Year", "IPCC_cat_code", "Product"], how="left")
all_jur_sources.rename(columns={"Tax_ex_rate_sources":"tax_ex_rate"}, inplace=True)

## Filling "tax_ex_rate" column with "NA" if no tax scheme
all_jur.loc[all_jur.tax!=1, "tax_ex_rate"] = "NA"
#all_jur.loc[(all_jur.Tax_dummy==1) & (all_jur.Tax_ex_rate==""), :] #checking whether we've missed any exemptions

all_jur.loc[all_jur.tax_ex_rate=="NA", "tax_ex_rate"] = np.nan # changing "NA" to NaN to be able to execute column multiplication
all_jur.loc[all_jur.tax_ex_rate=="", "tax_ex_rate"] = np.nan
all_jur.loc[all_jur.tax_rate_excl_ex_clcu=="NA", "tax_rate_excl_ex_clcu"] = np.nan # changing "NA" to NaN to be able to execute column multiplication
all_jur.loc[all_jur.tax_rate_excl_ex_clcu=="", "tax_rate_excl_ex_clcu"] = np.nan

all_jur["tax_ex_rate"] = all_jur["tax_ex_rate"].astype(float)
all_jur["tax_rate_excl_ex_clcu"] = all_jur["tax_rate_excl_ex_clcu"].astype(float)

## Calculate tax rate including rebate
all_jur.loc[:, "tax_rate_incl_ex_clcu"] = all_jur.loc[:, "tax_rate_excl_ex_clcu"]*(1-all_jur.loc[:, "tax_ex_rate"])
 

# Quantity-based exemptions
# - many tax schemes in EU countries do not apply to emissions from entities 
# covered by the EU ETS
# - only a certain % of emissions within a sector is subject to the price/tax
 



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
all_jur = all_jur[["Jurisdiction", "Year", "IPCC_cat_code", #"IEA_CODE", 
                   "Product", "tax", "ets", "tax_id",
                   "tax_rate_excl_ex_clcu", "tax_ex_rate", 
                   "tax_rate_incl_ex_clcu", "tax_curr_code", "ets_id", "ets_price",
                   "ets_curr_code"]]

all_jur_sources = all_jur_sources[["Jurisdiction", "Year", "IPCC_cat_code", 
                                   "Product", "tax", "ets",
                                   "tax_rate_excl_ex_clcu", "tax_ex_rate",
                                   "ets_price"]]

# Breaking up dataframe into single jurisdiction .csv files
std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))



for jur in countries_dic:
    all_jur.loc[all_jur.Jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/national/CP_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    all_jur.loc[all_jur.Jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/subnational/CP_"+subnat_dic[jur]+".csv", index=None)

for jur in countries_dic.remove("Georgia"):
    all_jur_sources.loc[all_jur_sources.Jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/national/CP_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    all_jur_sources.loc[all_jur_sources.Jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/subnational/CP_"+subnat_dic[jur]+".csv", index=None)
    
    
