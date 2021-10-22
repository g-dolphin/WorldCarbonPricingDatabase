#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:45:58 2020

@author: GD
"""
import os
import glob
import pandas as pd

#Some code to download and concatenate files for specific jurisdictions

def concatenate(indir):#,outfile):
    os.chdir(indir) #sets the current directory to 'indir'
    fileList=glob.glob("*.csv") #this command generates a list of csv files
    dfList = []

    #each iteration of the loop will add a dataframe to the list
    for filename in fileList:
        df=pd.read_csv(filename, keep_default_na=False, header=0)
        dfList.append(df)

    #'axis=0' ensures that we are concatenating vertically,
    concatDf=pd.concat(dfList,axis=0)

    #    concatDf.to_csv(outfile,index=None)
    return concatDf

indir_nat = ".../GitHub/WorldCarbonPricingDatabase/_data/national"
indir_subnat = ".../GitHub/WorldCarbonPricingDatabase/_data/subnat"

nat_jur = concatenate(indir_nat)
subnat_jur = concatenate(indir_subnat)

# Jurisdiction lists

ctry_list = list(nat_jur.Jurisdiction.unique())
subnat_list = list(subnat_jur.Jurisdiction.unique())
all_jur = ctry_list + subnat_list


# Breaking up dataframe into single jurisdiction .csv files
std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))

for ctry in ctry_list:
    nat_jur.loc[nat_jur.Jurisdiction==ctry, :].to_csv("/Users/GD/Documents/GitHub/WorldCarbonPricingDatabase/Sources/national_jur/CP_"+countries_dic[ctry]+".csv", index=None)
for jur in subnat_list:
    subnat_jur.loc[subnat_jur.Jurisdiction==jur, :].to_csv("/Users/GD/Documents/GitHub/WorldCarbonPricingDatabase/Sources/subnat_jur/CP_"+subnat_dic[jur]+".csv", index=None)

