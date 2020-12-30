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
        df=pd.read_csv(filename, header=0)
        dfList.append(df)

    #'axis=0' ensures that we are concatenating vertically,
    concatDf=pd.concat(dfList,axis=0)

    #    concatDf.to_csv(outfile,index=None)
    return concatDf

indir = ".../GitHub/WorldCarbonPricingDatabase/Data/national_jur"
indir = ".../GitHub/WorldCarbonPricingDatabase/Data/subnat_jur"
