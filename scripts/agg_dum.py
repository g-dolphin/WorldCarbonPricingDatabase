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

ipcc_codes = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/wcpd_dataset/dataset_structure/IPCC2006_category_codes_links.csv")

multivalue_dict = defaultdict(list)

for idx,row in ipcc_codes.iterrows():
    multivalue_dict[row['parent_category']].append(row['IPCC_CODE'])


# Assign values to aggregate categories if values in all subcategories is identical (UNDER DEVELOPMENT)
# Disaggregation levels

# Extract disaggregation levels
level_6 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 6]
level_5 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 5]
level_4 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 4]
level_3 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 3]
level_2 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 2]
level_1 = [x for x in list(ipcc_codes.IPCC_CODE.unique()) if len(x) == 1]

ipcc_code_levels = [level_5, level_4, level_3, level_2, level_1]

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

indir_nat = "/Users/gd/GitHub/WorldCarbonPricingDatabase/data/national_jur"
indir_subnat = "/Users/gd/GitHub/WorldCarbonPricingDatabase/data/subnat_jur"

nat_jur = concatenate(indir_nat)
subnat_jur = concatenate(indir_subnat)
all_jur = pd.concat([nat_jur, subnat_jur])

# Data type pre-processing

all_jur["Tax_dummy"] = pd.to_numeric(all_jur["Tax_dummy"], errors='coerce')
all_jur["ETS_dummy"] = pd.to_numeric(all_jur["ETS_dummy"], errors='coerce')
all_jur["Tax_dummy"] = all_jur["Tax_dummy"].fillna(0)
all_jur["ETS_dummy"] = all_jur["ETS_dummy"].fillna(0)
all_jur["Tax_dummy"] = all_jur["Tax_dummy"].astype(int)
all_jur["ETS_dummy"] = all_jur["ETS_dummy"].astype(int)

# Aggregate at IPCC sector level (from product level)

all_jur_agg = all_jur.groupby(["Jurisdiction", "Year", "IPCC_cat_code"]).sum()
all_jur_agg = all_jur_agg.reset_index()

all_jur_agg["Tax_dummy"] = np.where(all_jur_agg.Tax_dummy==3,1,0)
all_jur_agg["ETS_dummy"] = np.where(all_jur_agg.ETS_dummy==3,1,0)

# Dummy calculation

# For each level, check whether all values for lower disaggregation level are equal to 1
for jur in all_jur.Jurisdiction.unique():
    for yr in all_jur.Year.unique():
        for level in ipcc_code_levels:
            for ipcc_code in level:
                x_tax = 1
                x_ets = 1
                
                for ipcc_code_1 in multivalue_dict[ipcc_code]:
                    x_tax *=  all_jur_agg.loc[(all_jur_agg.Jurisdiction==jur) & (all_jur_agg.Year==yr) & (all_jur_agg.IPCC_cat_code==ipcc_code_1), "Tax_dummy"].item()
                    x_ets *=  all_jur_agg.loc[(all_jur_agg.Jurisdiction==jur) & (all_jur_agg.Year==yr) & (all_jur_agg.IPCC_cat_code==ipcc_code_1), "ETS_dummy"].item()
                    
                all_jur.loc[(all_jur.Jurisdiction==jur) & (all_jur.Year==yr) & (all_jur.IPCC_cat_code==ipcc_code), "Tax_dummy"] = x_tax
                all_jur.loc[(all_jur.Jurisdiction==jur) & (all_jur.Year==yr) & (all_jur.IPCC_cat_code==ipcc_code), "ETS_dummy"] = x_ets
            
            
            
            