#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:40:49 2020

@author: GD
"""

import pandas as pd
import os
import glob
import numpy as np

from collections import defaultdict


# Assign values to aggregate categories if values in all subcategories is identical (UNDER DEVELOPMENT)

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

indir_nat = "/Users/gd/Desktop/wcpd_temp/data/nat_jur"
indir_subnat = "/Users/gd/Desktop/wcpd_temp/data/subnat_jur"

nat_jur = concatenate(indir_nat)
subnat_jur = concatenate(indir_subnat)
all_jur = pd.concat([nat_jur, subnat_jur])

# Data type pre-processing

all_jur["tax_dummy"] = pd.to_numeric(all_jur["tax_dummy"], errors='coerce')
all_jur["ets_dummy"] = pd.to_numeric(all_jur["ets_dummy"], errors='coerce')
all_jur["tax_dummy"] = all_jur["tax_dummy"].fillna(0)
all_jur["ets_dummy"] = all_jur["ets_dummy"].fillna(0)
all_jur["tax_dummy"] = all_jur["tax_dummy"].astype(int)
all_jur["ets_dummy"] = all_jur["ets_dummy"].astype(int)

# Aggregate at IPCC sector level (from product level)
 
all_jur_agg = all_jur.groupby(["Jurisdiction", "Year", "IPCC_cat_code"]).sum()
all_jur_agg = all_jur_agg.reset_index()

# Replace all '3' values (which indicate that all fuels are covered) with '1'
# and all other values with '0'

all_jur_agg["tax_dummy"] = np.where(all_jur_agg.tax_dummy==3,1,0)
all_jur_agg["ets_dummy"] = np.where(all_jur_agg.ets_dummy==3,1,0)

# Aggregate sectors dummy calculation

# IPCC code levels
ipcc_codes = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/wcpd_dataset/aux_files/other/IPCC2006_category_codes_links.csv")

ipcc_sec_subsec_dict = defaultdict(list)

for idx,row in ipcc_codes.iterrows():
    ipcc_sec_subsec_dict[row['parent_category']].append(row['IPCC_CODE'])


# Extract disaggregation levels
level_6 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 6]
level_5 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 5]
level_4 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 4]
level_3 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 3]
level_2 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 2]
level_1 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 1]

ipcc_code_levels = [level_5, level_4, level_3, level_2, level_1]

# For each level, check whether all values for lower disaggregation level are equal to 1
for jur in all_jur.Jurisdiction.unique():
    for yr in all_jur.Year.unique():
        for level in [level_5]:#ipcc_code_levels:
            for ipcc_code in level:

                if len(ipcc_sec_subsec_dict[ipcc_code]) != 0: #check the list is not empty
                    x_tax = 1
                    x_ets = 1                
                    
                    for ipcc_code_1 in ipcc_sec_subsec_dict[ipcc_code]:
                        x_tax *=  all_jur_agg.loc[(all_jur_agg.Jurisdiction==jur) & (all_jur_agg.Year==yr) & (all_jur_agg.IPCC_cat_code==ipcc_code_1), "tax_dummy"].item()
                        x_ets *=  all_jur_agg.loc[(all_jur_agg.Jurisdiction==jur) & (all_jur_agg.Year==yr) & (all_jur_agg.IPCC_cat_code==ipcc_code_1), "ets_dummy"].item()
                                        
                else:
                    x_tax = all_jur_agg.loc[(all_jur_agg.Jurisdiction==jur) & (all_jur_agg.Year==yr) & (all_jur_agg.IPCC_cat_code==ipcc_code), "tax_dummy"].item()
                    x_ets = all_jur_agg.loc[(all_jur_agg.Jurisdiction==jur) & (all_jur_agg.Year==yr) & (all_jur_agg.IPCC_cat_code==ipcc_code), "ets_dummy"].item()

                all_jur.loc[(all_jur.Jurisdiction==jur) & (all_jur.Year==yr) & (all_jur.IPCC_cat_code==ipcc_code), "tax_dummy"] = x_tax
                all_jur.loc[(all_jur.Jurisdiction==jur) & (all_jur.Year==yr) & (all_jur.IPCC_cat_code==ipcc_code), "ets_dummy"] = x_ets


                
            
            
            