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
gas = "CO2" # or CH4 / F-GASES / SF6

# Load modules

gen_func = SourceFileLoader('general', '/Users/gd/GitHub/ECP/_code/compilation/dependencies/ecp_v3_gen_func.py').load_module()

etsPricesModule = SourceFileLoader('ets_prices', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/ets_prices.py').load_module()
taxRatesModule = SourceFileLoader('tax_rates', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/tax_rates.py').load_module()
etsScopeModule = SourceFileLoader('ets_scope', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/scope/ets/ets_scope_'+gas+'.py').load_module()
taxScopeModule = SourceFileLoader('taxes_scope', '/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/scope/tax/taxes_scope_'+gas+'.py').load_module()


#----------------------------DB structure------------------------#

stream = open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/jurisdictions.py")
read_file = stream.read()
exec(read_file)

if gas == "CO2":
    wcpd_structure = pd.read_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/_aux_files/wcpd_structure/wcpd_structure_CO2.csv")
else:
    wcpd_structure = pd.read_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/_aux_files/wcpd_structure/wcpd_structure_nonCO2.csv")

# Jurisdiction lists

ctry_list = ctries
subnat_list = subnat_can + subnat_chn + subnat_jpn + subnat_usa + subnat_mex
all_jur_list = ctry_list + subnat_list

wcpd_all_jur = pd.DataFrame()
wcpd_all_jur_sources = pd.DataFrame()

for jur in all_jur_list:

    temp = wcpd_structure.copy()
    temp["jurisdiction"] = jur
    
    if (wcpd_all_jur.empty == True):
        wcpd_all_jur = temp
        wcpd_all_jur_sources = temp
        
    else:
        wcpd_all_jur = pd.concat([wcpd_all_jur, temp], axis=0)
        wcpd_all_jur_sources = pd.concat([wcpd_all_jur_sources, temp], axis=0)

#------------------------Prices and scopes modules---------------------------#

ets_prices = etsPricesModule.prices_df("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price")
#ets_prices = ets_prices.loc[ets_prices.ghg==gas]

ets_scope = etsScopeModule.scope()["data"]
ets_scope_sources = etsScopeModule.scope()["sources"]

tax_rates = taxRatesModule.prices_df("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price/", gas)
tax_rates.rename(columns={"product":"em_type"}, inplace=True)

taxes_scope = taxScopeModule.scope()["data"]
taxes_scope_sources = taxScopeModule.scope()["sources"]

#------------------------Dataframe production functions---------------------------#

def ets_db_values(scheme_list, scheme_no):
    
    if scheme_no == "scheme_1":
        columns = {"id":"ets_id", "binary":"ets", "price":"ets_price", 
                   "curr_code":"ets_curr_code"}
    if scheme_no == "scheme_2":
        columns = {"id":"ets_2_id", "binary":"ets_2", "price":"ets_2_price", 
                   "curr_code":"ets_2_curr_code"}
    
    for scheme in scheme_list:
        for yr in ets_scope[scheme]["jurisdictions"].keys():   
            selection = (wcpd_all_jur.year==yr) & (wcpd_all_jur.jurisdiction.isin(ets_scope[scheme]["jurisdictions"][yr])) & (wcpd_all_jur.ipcc_code.isin(ets_scope[scheme]["sectors"][yr]))
            selection_sources = (wcpd_all_jur_sources.year==yr) & (wcpd_all_jur_sources.jurisdiction.isin(ets_scope[scheme]["jurisdictions"][yr])) & (wcpd_all_jur_sources.ipcc_code.isin(ets_scope[scheme]["sectors"][yr]))
    
            wcpd_all_jur.loc[selection, columns["binary"]] = 1
            wcpd_all_jur.loc[selection, columns["id"]] = scheme
            
            # Scope data source
            wcpd_all_jur_sources.loc[selection_sources, columns["binary"]] = ets_scope_sources[scheme][yr]
            
            try:        
                wcpd_all_jur.loc[selection, columns["price"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "allowance_price"].item()
                wcpd_all_jur.loc[selection, columns["curr_code"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "currency_code"].item()
                
                # Price data source
                wcpd_all_jur_sources.loc[selection_sources, columns["price"]] = ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "source"].item()+"; "+ets_prices.loc[(ets_prices.scheme_id==scheme) & (ets_prices.year==yr), "comment"].item()
                
            except:
                print(scheme, yr)


def tax_db_values(scheme_list, scheme_no, gas):
    
    if scheme_no == "scheme_1":
        columns = {"id":"tax_id", "binary":"tax", "rate":"tax_rate_excl_ex_clcu", 
                   "curr_code":"tax_curr_code"}
    if scheme_no == "scheme_2":
        columns = {"id":"tax_2_id", "binary":"tax_2",  
                   "rate":"tax_2_rate_excl_ex_clcu", "curr_code":"tax_2_curr_code"}

    for scheme in scheme_list:
        for yr in taxes_scope[scheme]["jurisdictions"].keys():
            if gas == "CO2":   
                selection = (wcpd_all_jur.year==yr) & (wcpd_all_jur.jurisdiction.isin(taxes_scope[scheme]["jurisdictions"][yr])) & (wcpd_all_jur.ipcc_code.isin(taxes_scope[scheme]["sectors"][yr])) & (wcpd_all_jur.Product.isin(taxes_scope[scheme]["fuels"][yr]))
                selection_sources = (wcpd_all_jur_sources.year==yr) & (wcpd_all_jur_sources.jurisdiction.isin(taxes_scope[scheme]["jurisdictions"][yr])) & (wcpd_all_jur_sources.ipcc_code.isin(taxes_scope[scheme]["sectors"][yr])) & (wcpd_all_jur_sources.Product.isin(taxes_scope[scheme]["fuels"][yr]))

                wcpd_all_jur.loc[selection, columns["binary"]] = 1
                wcpd_all_jur.loc[selection, columns["id"]] = scheme
                
                # Scope data source 
                wcpd_all_jur_sources.loc[selection_sources, columns["binary"]] = taxes_scope_sources[scheme][yr]
                
                try:
                    for type_em in ["Oil", "Natural gas", "Coal"]:
                        wcpd_all_jur.loc[selection & (wcpd_all_jur.Product == type_em), columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "rate"].item()                
                        wcpd_all_jur.loc[selection & (wcpd_all_jur.Product == type_em), columns["curr_code"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "currency_code"].item()
                    
    #                   # Price data source
                        value = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "source"].item()+"; "+tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr) & (tax_rates.em_type==type_em), "comment"].item()
                        wcpd_all_jur_sources.loc[selection_sources & (wcpd_all_jur_sources.Product == type_em), columns["rate"]] = value
                    
                except:
                    print(scheme, yr)

            else:

                selection = (wcpd_all_jur.year==yr) & (wcpd_all_jur.jurisdiction.isin(taxes_scope[scheme]["jurisdictions"][yr])) & (wcpd_all_jur.ipcc_code.isin(taxes_scope[scheme]["sectors"][yr])) 
                selection_sources = (wcpd_all_jur_sources.year==yr) & (wcpd_all_jur_sources.jurisdiction.isin(taxes_scope[scheme]["jurisdictions"][yr])) & (wcpd_all_jur_sources.ipcc_code.isin(taxes_scope[scheme]["sectors"][yr]))

                wcpd_all_jur.loc[selection, columns["binary"]] = 1
                wcpd_all_jur.loc[selection, columns["id"]] = scheme
                
                # Scope data source 
                wcpd_all_jur_sources.loc[selection_sources, columns["binary"]] = taxes_scope_sources[scheme][yr]
                
                try:
                    wcpd_all_jur.loc[selection, columns["rate"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr), "rate"].item()                
                    wcpd_all_jur.loc[selection, columns["curr_code"]] = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr), "currency_code"].item()
                
#                   # Price data source
                    value = tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr), "source"].item()+"; "+tax_rates.loc[(tax_rates.scheme_id==scheme) & (tax_rates.year==yr), "comment"].item()
                    wcpd_all_jur_sources.loc[selection_sources, columns["rate"]] = value
                    
                except:
                    print(scheme, yr)


#--------------------------------Primary pricing mechanism--------------------------------#

ets_1_list = list(ets_scope.keys()) #list of identifiers of ETS covering the selected gas
ets_1_list.remove("usa_ma_ets") #second scheme

taxes_1_list = list(taxes_scope.keys()) # list of identifiers of taxes covering the selected gas

ets_db_values(ets_1_list, "scheme_1")
tax_db_values(taxes_1_list, "scheme_1", gas)

#----------------------------Secondary pricing mechanism----------------------#
# NOTE: The "second pricing scheme" columns are only used when, for a given 
#       jurisdiction, at least one sector is (in any given year) either 
#       (i) covered by >1 carbon tax; OR 
#       (ii) covered by >1 emissions trading system.
#       In all other cases, i.e. cases where there is no strict overlap,
#       the pricing scheme information is recorded in the primary columns
#----------------------------Second:Emissions trading systems------------#

ets_2_list = ["usa_ma_ets"]
ets_db_values(ets_2_list, "scheme_2")

tax_2_list = []
tax_db_values(tax_2_list, "scheme_2", gas)

#----------------------------------------------------------------#
 
# Blank cells filling

wcpd_all_jur.loc[wcpd_all_jur.tax!=1, "tax"] = 0
wcpd_all_jur.loc[wcpd_all_jur.ets!=1, "ets"] = 0

#---------------------Sector-fuel scope exceptions----------------------#
 



#------------------------------Tax exemptions/rebates----------------------------------#

# Price-based exemptions
# Add (price-based) exemptions/rebate column for carbon taxes

stream = open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/_price_exemptions/tax/_price_exemptions_"+gas+".py")
read_file = stream.read()
exec(read_file)

## Calculate tax rate including rebate
wcpd_all_jur.loc[:, "tax_rate_incl_ex_clcu"] = wcpd_all_jur.loc[:, "tax_rate_excl_ex_clcu"]*(1-wcpd_all_jur.loc[:, "tax_ex_rate"])


#---------------------------------- Fill 'NA' values----------------------------------#

## For 'Product' keys
wcpd_all_jur.fillna({"Product":"NA"}, inplace=True)
wcpd_all_jur_sources.fillna({"Product":"NA"}, inplace=True)

tax_cols = ['tax_id', 'tax_rate_excl_ex_clcu', 'tax_curr_code',
            'tax_ex_rate', 'tax_rate_incl_ex_clcu']

ets_1_cols = ['ets_id', 'ets_price', 'ets_curr_code']
ets_2_cols = ['ets_2_id', 'ets_2_price', 'ets_2_curr_code']

wcpd_all_jur.loc[wcpd_all_jur.tax==0.0, tax_cols] = "NA" 
wcpd_all_jur.loc[wcpd_all_jur.ets==0.0, ets_1_cols] = "NA"
wcpd_all_jur.loc[wcpd_all_jur.ets==0.0, ets_2_cols] = "NA"

wcpd_all_jur_sources.fillna("NA", inplace=True)

# Re-ordering columns
wcpd_all_jur = wcpd_all_jur[["jurisdiction", "year", "ipcc_code",
                   "Product", "tax", "ets", "tax_id",
                   "tax_rate_excl_ex_clcu", "tax_ex_rate", 
                   "tax_rate_incl_ex_clcu", "tax_curr_code", "ets_id", "ets_price",
                   "ets_curr_code", "ets_2_id", "ets_2_price", "ets_2_curr_code"]]

wcpd_all_jur_sources = wcpd_all_jur_sources[["jurisdiction", "year", "ipcc_code", 
                                   "Product", "tax", "ets",
                                   "tax_rate_excl_ex_clcu", "tax_ex_rate",
                                   "ets_price"]]

#------------------------------Calculating aggregate IPCC categories scope values----------------------------------#

stream = open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/sector_agg_scope.py")
read_file = stream.read()
exec(read_file)

#------------------------------Writing files----------------------------------#

# Breaking up dataframe into single jurisdiction .csv files
std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))


for jur in countries_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/"+gas+"/national/wcpd_"+gas.lower()+"_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/"+gas+"/subnational/wcpd_"+gas.lower()+"_"+subnat_dic[jur]+".csv", index=None)

for jur in countries_dic:
    wcpd_all_jur_sources.loc[wcpd_all_jur_sources.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/"+gas+"/national/wcpd_"+gas.lower()+"_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    wcpd_all_jur_sources.loc[wcpd_all_jur_sources.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/sources/"+gas+"/subnational/wcpd_"+gas.lower()+"_"+subnat_dic[jur]+".csv", index=None)
    
    

