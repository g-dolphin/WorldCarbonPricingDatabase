#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 15:31:01 2021

@author: GD
"""

# This script creates coverage carbon pricing mechanisms coverage binary variables
# at sector and jurisdiction level

import pandas as pd
import os
import glob
import numpy as np

file_root_I = '/Users/GD/Documents/GitHub/WorldCarbonPricingDatabase/Data'

def concatenate(indir):#,outfile):
    os.chdir(indir) #sets the current directory to 'indir'
    fileList=glob.glob("*.csv") #this command generates a list of csv files
    dfList = []

    #each iteration of the loop will add a dataframe to the list
    for filename in fileList:
        df=pd.read_csv(filename, header=0)
        dfList.append(df)

    #'axis=0' ensures that we are concatenating vertically, 
    concatDf=pd.concat(dfList,axis=0) 

    #    concatDf.to_csv(outfile,index=None)
    return concatDf

cp_ctry = concatenate(file_root_I+"/national_jur")
cp_subnat = concatenate(file_root_I+"/subnat_jur")

cp_all = pd.concat([cp_ctry, cp_subnat]).sort_values(by=["Jurisdiction", "Year"])

cp_all.drop(['Tax_rate_excl_ex_clc', 'Tax_ex_rate',
       'Tax_rate_incl_ex_clc', 'Tax_curr_code', 'ETS_price', 'ETS_curr_code'], axis=1, inplace=True)

cp_all_aggsector = cp_all.groupby(["Jurisdiction", "Year", "IPCC_cat_code", "IEA_CODE"]).sum()
cp_all_aggsector["Tax_dummy"] = np.where(cp_all_aggsector.Tax_dummy>0, 1, 0)
cp_all_aggsector["ETS_dummy"] = np.where(cp_all_aggsector.ETS_dummy>0, 1, 0)

cp_all_aggjur = cp_all.groupby(["Jurisdiction", "Year"]).sum()
cp_all_aggjur["Tax_dummy"] = np.where(cp_all_aggjur.Tax_dummy>0, 1, 0)
cp_all_aggjur["ETS_dummy"] = np.where(cp_all_aggjur.ETS_dummy>0, 1, 0)
