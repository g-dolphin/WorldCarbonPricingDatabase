#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:47:31 2021

@author: gd
"""

import os
import pandas as pd
import glob
import numpy as np

from operator import itemgetter

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

cp_nat = concatenate(indir_nat)
cp_subnat = concatenate(indir_subnat)
cp_all = pd.concat([cp_nat, cp_subnat])

# Separate sector code by digit
## Create placeholders for the new columns
cp_all['IPCC_cat_code_full'] = '' #16th column (index 15)
cp_all['IPCC_cat_code_1st'] = '' #17th column (index 16)
cp_all['IPCC_cat_code_2nd'] = '' #18th column (index 17)
cp_all['IPCC_cat_code_3rd'] = '' #19th column (index 18)
cp_all['IPCC_cat_code_4th'] = '' #20th column (index 19)
cp_all['IPCC_cat_code_5th'] = '' #21st column (index 20)
cp_all['IPCC_cat_code_6th'] = '' #22nd column (index 21)

## Fill in IPCC_cat_code_full with a copy of IPCC_cat_code that all has the max length of 6
cp_all['IPCC_cat_code_full'] = cp_all.iloc[:, 2].str.ljust(6, "_") # the 3rd col is IPCC_cat_code

## Special case 1: sectors that cannot be disaggregated
list1 = ['20', '200', '2000', '20000', '200000']
index1 = np.isin(cp_all.IPCC_cat_code, list1)
cp_all.loc[index1, 'IPCC_cat_code_1st'] = cp_all.loc[index1, 'IPCC_cat_code_full']

## Special case 2: sectors that end with 10
list2 = ['2B10']
index2 = np.isin(cp_all.IPCC_cat_code, list2)
cp_all.loc[index2, 'IPCC_cat_code_1st'] = '2'
cp_all.loc[index2, 'IPCC_cat_code_2nd'] = 'B'
cp_all.loc[index2, 'IPCC_cat_code_3rd'] = '10'

## All the other cases: each letter/number represents a level of disaggregation

def Extract(lst, i):
    return list( map(itemgetter(i), lst ))

list3 = list1+list2 
index3 = np.logical_not(np.isin(cp_all.IPCC_cat_code, list3))
cp_all.loc[index3, 'IPCC_cat_code_1st'] = Extract(cp_all.loc[index3, 'IPCC_cat_code_full'], 0)
cp_all.loc[index3, 'IPCC_cat_code_2nd'] = Extract(cp_all.loc[index3, 'IPCC_cat_code_full'], 1)
cp_all.loc[index3, 'IPCC_cat_code_3rd'] = Extract(cp_all.loc[index3, 'IPCC_cat_code_full'], 2)
cp_all.loc[index3, 'IPCC_cat_code_4th'] = Extract(cp_all.loc[index3, 'IPCC_cat_code_full'], 3)
cp_all.loc[index3, 'IPCC_cat_code_5th'] = Extract(cp_all.loc[index3, 'IPCC_cat_code_full'], 4)
cp_all.loc[index3, 'IPCC_cat_code_6th'] = Extract(cp_all.loc[index3, 'IPCC_cat_code_full'], 5)

## Replace all the blank space and drop the IPCC_cat_code_full variable
cp_all[['IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd', 
        'IPCC_cat_code_4th', 'IPCC_cat_code_5th', 'IPCC_cat_code_6th']] = cp_all[['IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd', 
        'IPCC_cat_code_4th', 'IPCC_cat_code_5th', 'IPCC_cat_code_6th']].replace('_', '', regex=True, inplace=True)
cp_all.drop('IPCC_cat_code_full', inplace=True, axis=1)
 

# Aggregate emissions over products for national jurisdictions
## note: by setting min_count=1, the sum of NaN is NaN but the sum of NaN and other values will be a valid number
temp = cp_all.groupby(['Jurisdiction', 'Year', 'IPCC_cat_code'], as_index=False)[['tax', 'ets']].sum(min_count=1)
cp_all = pd.merge(cp_all, temp, on=['Jurisdiction', 'Year', 'IPCC_cat_code'], how='left')
cp_all = cp_all.rename(columns={'tax_x': 'tax', 'tax_y': 'tax_IPCC',
                                'ets_x': 'ets', 'ets_y': 'ets_IPCC'})

# Create a temporary dataset that does not have product-specific rows for IPCC sectors
cp_all_IPCC = cp_all.drop_duplicates(subset = ['Jurisdiction', 'Year', 'IPCC_cat_code'])[:]
cols = [3,4,5,6,7,8,9]
cp_all_IPCC.drop(cp_all_IPCC.columns[cols], axis = 1, inplace = True)
#cp_all_IPCC.drop(["Unnamed: 0"], axis=1, inplace=True)


# Aggregate emissions to different sector levels
## Create the new variable
cp_all_IPCC["tax_IPCC_agg"] = cp_all_IPCC["tax_IPCC"][:]
cp_all_IPCC["ets_IPCC_agg"] = cp_all_IPCC["ets_IPCC"][:]

## Define merge keys
keys_1st = [['Jurisdiction', 'Year', 'IPCC_cat_code_1st'], 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd']
keys_2nd = [['Jurisdiction', 'Year', 'IPCC_cat_code_1st', 'IPCC_cat_code_2nd'], 'IPCC_cat_code_3rd', 'IPCC_cat_code_4th']
keys_3rd = [['Jurisdiction', 'Year', 'IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd'], 'IPCC_cat_code_4th', 'IPCC_cat_code_5th']
keys_4th = [['Jurisdiction', 'Year', 'IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd', 'IPCC_cat_code_4th'], 'IPCC_cat_code_5th', 'IPCC_cat_code_6th']
keys_5th = [['Jurisdiction', 'Year', 'IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd', 'IPCC_cat_code_4th', 'IPCC_cat_code_5th'], 'IPCC_cat_code_6th']
keys_all = [keys_4th, keys_3rd, keys_2nd, keys_1st] # aggregate from bottom to top

## Case 1: Aggregate to the 5th level (which is the second to last most disaggregate level)

### Sum by the specific sector aggregation level and merge the new dataset back to the original dataset
rows = cp_all_IPCC[cp_all_IPCC[keys_5th[1]].str.len() > 0] # only select observations at one more disaggregated level to avoid double counting
temp = rows.groupby(keys_5th[0], as_index=False)[['tax_IPCC_agg', 'ets_IPCC_agg']].sum(min_count=1)

cp_all_IPCC = cp_all_IPCC.merge(temp,on=keys_5th[0],how="left")
cp_all_IPCC.loc[(cp_all[keys_5th[1]].str.len() > 0), "tax_IPCC_agg_y"] = np.NaN # avoid filling in more disaggregated levels
cp_all_IPCC.loc[(cp_all[keys_5th[1]].str.len() > 0), "ets_IPCC_agg_y"] = np.NaN
 
### Replace dummy only when data is unavailable in the original dataset
cp_all_IPCC.loc[(cp_all_IPCC[keys_5th[1]].str.len() == 0), 'tax_IPCC_agg_x'] = cp_all_IPCC.loc[(cp_all_IPCC[keys_5th[1]].str.len() == 0), 'tax_IPCC_agg_y']
cp_all_IPCC.loc[(cp_all_IPCC[keys_5th[1]].str.len() == 0), 'tax_IPCC_agg_x'] = cp_all_IPCC.loc[(cp_all_IPCC[keys_5th[1]].str.len() == 0), 'tax_IPCC_agg_y']
cp_all_IPCC.drop(['tax_IPCC_agg_y'],inplace=True,axis=1)
cp_all_IPCC.drop(['ets_IPCC_agg_y'],inplace=True,axis=1)
cp_all_IPCC.rename(columns={'tax_IPCC_agg_x':'tax_IPCC_agg','ets_IPCC_agg_x':'ets_IPCC_agg'},inplace=True)
  
## Case 2: Aggregate to other levels
for keys in keys_all:
    
    ### Sum by the specific sector aggregation level and merge the new dataset back to the original dataset
    rows = cp_all_IPCC[(cp_all_IPCC[keys[1]].str.len() > 0) & (cp_all_IPCC[keys[2]].str.len() == 0)]
    temp = rows.groupby(keys[0], as_index=False)[['tax_IPCC_agg', 'ets_IPCC_agg']].sum(min_count=1)
    cp_all_IPCC = cp_all_IPCC.merge(temp,on=keys[0],how="left") 
    cp_all_IPCC.loc[(cp_all_IPCC[keys[1]].str.len() > 0), "tax_IPCC_agg_y"] = np.NaN # avoid filling in more disaggregated levels
    cp_all_IPCC.loc[(cp_all_IPCC[keys[1]].str.len() > 0), "ets_IPCC_agg_y"] = np.NaN
     
    ### Replace dummy only when data is unavailable in the original dataset 
    cp_all_IPCC.loc[(cp_all_IPCC[keys[1]].str.len() == 0), 'tax_IPCC_agg_x'] = cp_all_IPCC.loc[(cp_all_IPCC[keys[1]].str.len() == 0), 'tax_IPCC_agg_y']
    cp_all_IPCC.loc[(cp_all_IPCC[keys[1]].str.len() == 0), 'ets_IPCC_agg_x'] = cp_all_IPCC.loc[(cp_all_IPCC[keys[1]].str.len() == 0), 'ets_IPCC_agg_y']
    cp_all_IPCC.drop(['tax_IPCC_agg_y'], inplace=True, axis=1)
    cp_all_IPCC.drop(['ets_IPCC_agg_y'], inplace=True, axis=1)
    cp_all_IPCC.rename(columns={'tax_IPCC_agg_x':'tax_IPCC_agg', 'ets_IPCC_agg_x':'ets_IPCC_agg'},inplace=True)

# merge cp_all_IPCC back to cp_all
keys_all = ['Jurisdiction', 'Year', 'IPCC_cat_code', 'IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd', 'IPCC_cat_code_4th', 'IPCC_cat_code_5th', 'IPCC_cat_code_6th']
cp_all.drop(['tax', 'ets', 'tax_IPCC', 'ets_IPCC'], inplace=True,axis=1)
cp_all_IPCC.drop(['tax_IPCC', 'ets_IPCC', 'tax_curr_code',
                  'ets_id', 'ets_price', 'ets_curr_code'],
                 axis=1, inplace=True)
cp_all = cp_all.merge(cp_all_IPCC, on=keys_all, how="left")
cp_all.drop(['IPCC_cat_code_1st', 'IPCC_cat_code_2nd', 'IPCC_cat_code_3rd', 
             'IPCC_cat_code_4th', 'IPCC_cat_code_5th', 'IPCC_cat_code_6th'], #, 'Unnamed: 0'
             axis=1, inplace=True)

cp_all.rename(columns={'tax_IPCC_agg':'tax', 'ets_IPCC_agg':'ets'}, inplace=True)

# set value to 1 if > 0
cp_all["tax"] = np.where(cp_all.tax>0,1,0)
cp_all["ets"] = np.where(cp_all.ets>0,1,0)

# re-ordering columns
cp_all = cp_all[['Jurisdiction', 'Year', 'IPCC_cat_code', 'Product', 'tax',
                 'ets', 'tax_id', 'tax_rate_excl_ex_clcu', 'tax_ex_rate', 
                 'tax_rate_incl_ex_clcu','tax_curr_code', 'ets_id', 
                 'ets_price', 'ets_curr_code']]

# Write files
ctry_list = list(cp_nat.Jurisdiction.unique())
subnat_list = list(cp_subnat.Jurisdiction.unique())
all_jur_list = ctry_list + subnat_list

# Breaking up dataframe into single jurisdiction .csv files
std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))


for jur in countries_dic:
    if jur in countries_dic.keys():
        cp_all.loc[cp_all.Jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/national/CP_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    if jur in subnat_dic.keys():
        cp_all.loc[cp_all.Jurisdiction==jur, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data/subnational/CP_"+subnat_dic[jur]+".csv", index=None)
                    


