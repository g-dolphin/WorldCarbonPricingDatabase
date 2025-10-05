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



# Separate sector code by digit
## Create placeholders for the new columns
wcpd_all_jur['ipcc_code_full'] = '' #16th column (index 15)
wcpd_all_jur['ipcc_code_1st'] = '' #17th column (index 16)
wcpd_all_jur['ipcc_code_2nd'] = '' #18th column (index 17)
wcpd_all_jur['ipcc_code_3rd'] = '' #19th column (index 18)
wcpd_all_jur['ipcc_code_4th'] = '' #20th column (index 19)
wcpd_all_jur['ipcc_code_5th'] = '' #21st column (index 20)
wcpd_all_jur['ipcc_code_6th'] = '' #22nd column (index 21)

## Fill in IPCC_cat_code_full with a copy of IPCC_cat_code that all has the max length of 6
wcpd_all_jur['ipcc_code_full'] = wcpd_all_jur.iloc[:, 2].str.ljust(6, "_") # the 3rd col is ipcc_code

## Special case 1: sectors that cannot be disaggregated
list1 = ['20', '200', '2000', '20000', '200000']
index1 = np.isin(wcpd_all_jur.ipcc_code, list1)
wcpd_all_jur.loc[index1, 'ipcc_code_1st'] = wcpd_all_jur.loc[index1, 'ipcc_code_full']

## Special case 2: sectors that end with 10
list2 = ['2B10']
index2 = np.isin(wcpd_all_jur.ipcc_code, list2)
wcpd_all_jur.loc[index2, 'ipcc_code_1st'] = '2'
wcpd_all_jur.loc[index2, 'ipcc_code_2nd'] = 'B'
wcpd_all_jur.loc[index2, 'ipcc_code_3rd'] = '10'

## All the other cases: each letter/number represents a level of disaggregation

def Extract(lst, i):
    return list( map(itemgetter(i), lst ))

list3 = list1+list2 
index3 = np.logical_not(np.isin(wcpd_all_jur.ipcc_code, list3))
wcpd_all_jur.loc[index3, 'ipcc_code_1st'] = Extract(wcpd_all_jur.loc[index3, 'ipcc_code_full'], 0)
wcpd_all_jur.loc[index3, 'ipcc_code_2nd'] = Extract(wcpd_all_jur.loc[index3, 'ipcc_code_full'], 1)
wcpd_all_jur.loc[index3, 'ipcc_code_3rd'] = Extract(wcpd_all_jur.loc[index3, 'ipcc_code_full'], 2)
wcpd_all_jur.loc[index3, 'ipcc_code_4th'] = Extract(wcpd_all_jur.loc[index3, 'ipcc_code_full'], 3)
wcpd_all_jur.loc[index3, 'ipcc_code_5th'] = Extract(wcpd_all_jur.loc[index3, 'ipcc_code_full'], 4)
wcpd_all_jur.loc[index3, 'ipcc_code_6th'] = Extract(wcpd_all_jur.loc[index3, 'ipcc_code_full'], 5)

## Replace all the blank space and drop the IPCC_cat_code_full variable
wcpd_all_jur[['ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd', 
        'ipcc_code_4th', 'ipcc_code_5th', 'ipcc_code_6th']] = wcpd_all_jur[['ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd', 
        'ipcc_code_4th', 'ipcc_code_5th', 'ipcc_code_6th']].replace('_', '', regex=True, inplace=True)
wcpd_all_jur.drop('ipcc_code_full', inplace=True, axis=1)
 

# Aggregate emissions over products for national jurisdictions
## note: by setting min_count=1, the sum of NaN is NaN but the sum of NaN and other values will be a valid number
temp = wcpd_all_jur.groupby(['jurisdiction', 'year', 'ipcc_code'], as_index=False)[['tax', 'ets']].sum(min_count=1)
wcpd_all_jur = pd.merge(wcpd_all_jur, temp, on=['jurisdiction', 'year', 'ipcc_code'], how='left')
wcpd_all_jur = wcpd_all_jur.rename(columns={'tax_x': 'tax', 'tax_y': 'tax_ipcc',
                                'ets_x': 'ets', 'ets_y': 'ets_ipcc'})

# Create a temporary dataset that does not have product-specific rows for IPCC sectors
wcpd_all_jur_IPCC = wcpd_all_jur.drop_duplicates(subset = ['jurisdiction', 'year', 'ipcc_code'])[:]
cols = [3,4,5,6,7,8,9]
wcpd_all_jur_IPCC.drop(wcpd_all_jur_IPCC.columns[cols], axis = 1, inplace = True)
#wcpd_all_jur_IPCC.drop(["Unnamed: 0"], axis=1, inplace=True)


# Aggregate emissions to different sector levels
## Create the new variable
wcpd_all_jur_IPCC["tax_ipcc_agg"] = wcpd_all_jur_IPCC["tax_ipcc"][:]
wcpd_all_jur_IPCC["ets_ipcc_agg"] = wcpd_all_jur_IPCC["ets_ipcc"][:]

## Define merge keys
keys_1st = [['jurisdiction', 'year', 'ipcc_code_1st'], 'ipcc_code_2nd', 'ipcc_code_3rd']
keys_2nd = [['jurisdiction', 'year', 'ipcc_code_1st', 'ipcc_code_2nd'], 'ipcc_code_3rd', 'ipcc_code_4th']
keys_3rd = [['jurisdiction', 'year', 'ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd'], 'ipcc_code_4th', 'ipcc_code_5th']
keys_4th = [['jurisdiction', 'year', 'ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd', 'ipcc_code_4th'], 'ipcc_code_5th', 'ipcc_code_6th']
keys_5th = [['jurisdiction', 'year', 'ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd', 'ipcc_code_4th', 'ipcc_code_5th'], 'ipcc_code_6th']
keys_all = [keys_4th, keys_3rd, keys_2nd, keys_1st] # aggregate from bottom to top

## Case 1: Aggregate to the 5th level (which is the second to last most disaggregate level)

### Sum by the specific sector aggregation level and merge the new dataset back to the original dataset
rows = wcpd_all_jur_IPCC[wcpd_all_jur_IPCC[keys_5th[1]].str.len() > 0] # only select observations at one more disaggregated level to avoid double counting
temp = rows.groupby(keys_5th[0], as_index=False)[['tax_ipcc_agg', 'ets_ipcc_agg']].sum(min_count=1)

wcpd_all_jur_IPCC = wcpd_all_jur_IPCC.merge(temp,on=keys_5th[0],how="left")
wcpd_all_jur_IPCC.loc[(wcpd_all_jur[keys_5th[1]].str.len() > 0), "tax_ipcc_agg_y"] = np.NaN # avoid filling in more disaggregated levels
wcpd_all_jur_IPCC.loc[(wcpd_all_jur[keys_5th[1]].str.len() > 0), "ets_ipcc_agg_y"] = np.NaN
 
### Replace dummy only when data is unavailable in the original dataset
wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys_5th[1]].str.len() == 0), 'tax_ipcc_agg_x'] = wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys_5th[1]].str.len() == 0), 'tax_ipcc_agg_y']
wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys_5th[1]].str.len() == 0), 'tax_ipcc_agg_x'] = wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys_5th[1]].str.len() == 0), 'tax_ipcc_agg_y']
wcpd_all_jur_IPCC.drop(['tax_ipcc_agg_y'],inplace=True,axis=1)
wcpd_all_jur_IPCC.drop(['ets_ipcc_agg_y'],inplace=True,axis=1)
wcpd_all_jur_IPCC.rename(columns={'tax_ipcc_agg_x':'tax_ipcc_agg','ets_ipcc_agg_x':'ets_ipcc_agg'},inplace=True)
  
## Case 2: Aggregate to other levels
for keys in keys_all:
    
    ### Sum by the specific sector aggregation level and merge the new dataset back to the original dataset
    rows = wcpd_all_jur_IPCC[(wcpd_all_jur_IPCC[keys[1]].str.len() > 0) & (wcpd_all_jur_IPCC[keys[2]].str.len() == 0)]
    temp = rows.groupby(keys[0], as_index=False)[['tax_ipcc_agg', 'ets_ipcc_agg']].sum(min_count=1)
    wcpd_all_jur_IPCC = wcpd_all_jur_IPCC.merge(temp,on=keys[0],how="left") 
    wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys[1]].str.len() > 0), "tax_ipcc_agg_y"] = np.NaN # avoid filling in more disaggregated levels
    wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys[1]].str.len() > 0), "ets_ipcc_agg_y"] = np.NaN
     
    ### Replace dummy only when data is unavailable in the original dataset 
    wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys[1]].str.len() == 0), 'tax_ipcc_agg_x'] = wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys[1]].str.len() == 0), 'tax_ipcc_agg_y']
    wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys[1]].str.len() == 0), 'ets_ipcc_agg_x'] = wcpd_all_jur_IPCC.loc[(wcpd_all_jur_IPCC[keys[1]].str.len() == 0), 'ets_ipcc_agg_y']
    wcpd_all_jur_IPCC.drop(['tax_ipcc_agg_y'], inplace=True, axis=1)
    wcpd_all_jur_IPCC.drop(['ets_ipcc_agg_y'], inplace=True, axis=1)
    wcpd_all_jur_IPCC.rename(columns={'tax_ipcc_agg_x':'tax_ipcc_agg', 'ets_ipcc_agg_x':'ets_ipcc_agg'},inplace=True)

# merge wcpd_all_jur_IPCC back to wcpd_all_jur
keys_all = ['jurisdiction', 'year', 'ipcc_code', 'ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd', 'ipcc_code_4th', 'ipcc_code_5th', 'ipcc_code_6th']
wcpd_all_jur.drop(['tax', 'ets', 'tax_ipcc', 'ets_ipcc'], inplace=True,axis=1)
wcpd_all_jur_IPCC.drop(['tax_ipcc', 'ets_ipcc', 'tax_curr_code',
                  'ets_id', 'ets_price', 'ets_curr_code'],
                 axis=1, inplace=True)
wcpd_all_jur = wcpd_all_jur.merge(wcpd_all_jur_IPCC, on=keys_all, how="left")
wcpd_all_jur.drop(['ipcc_code_1st', 'ipcc_code_2nd', 'ipcc_code_3rd', 
             'ipcc_code_4th', 'ipcc_code_5th', 'ipcc_code_6th'], #, 'Unnamed: 0'
             axis=1, inplace=True)

wcpd_all_jur.rename(columns={'tax_ipcc_agg':'tax', 'ets_ipcc_agg':'ets'}, inplace=True)

# set value to 1 if > 0
wcpd_all_jur["tax"] = np.where(wcpd_all_jur.tax>0,1,0)
wcpd_all_jur["ets"] = np.where(wcpd_all_jur.ets>0,1,0)

# re-ordering columns
wcpd_all_jur = wcpd_all_jur[['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax',
                 'ets', 'tax_id', 'tax_rate_excl_ex_clcu', 'tax_ex_rate', 
                 'tax_rate_incl_ex_clcu','tax_curr_code', 'ets_id', 
                 'ets_price', 'ets_curr_code']]


                    


