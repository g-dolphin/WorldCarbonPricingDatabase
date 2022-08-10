#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:16:17 2021

@author: GD
"""

import pandas as pd
import glob
import os
import numpy as np

path_prices = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price/"

def prices_df(path_prices, gas):

    dfList = []
    
    #each iteration of the loop will add a dataframe to the list
    os.chdir(path_prices)
    fileList = glob.glob("*_tax*_prices.csv")

    for fileName in fileList:        
        df=pd.read_csv(fileName, keep_default_na=False, header=0, encoding="latin-1",
                       dtype={"product":str})

        df = df.loc[df.ghg==gas]

        df["rate"].replace(["NA", ""], np.nan, inplace=True)
        df["rate"] = df["rate"].astype(float)
        
        dfList.append(df)

    #'axis=0' ensures that we are concatenating vertically,
    concatDf=pd.concat(dfList,axis=0)

    return concatDf




