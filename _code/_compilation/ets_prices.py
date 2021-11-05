#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:16:17 2021

@author: GD
"""

import pandas as pd

path_prices = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price"

# For NZL ETS/ EU ETS / KOR ETS / CHN PROV PILOT ETSs, prices are from ICAP
# For RGGI / CA-QC CAT / SWITZERLAND ETS / OBPS in Canadian Provinces, prices are from other sources


def prices_df(path_prices):
    # RGGI Prices - taken from ICAP
    rggi_prices = pd.read_csv(path_prices+"/us_rggi_prices.csv")
    rggi_prices.loc[:, "allowance_price"] = rggi_prices.allowance_weighted_price/0.90718474
    rggi_prices = rggi_prices.drop(["allowance_weighted_price"], axis=1)

    # California CaT
    us_ma_ets_prices = pd.read_csv(path_prices+"/us_ma_ets_prices.csv")
    us_ma_ets_prices = us_ma_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # Quebec CaT
    can_qc_cat_prices = pd.read_csv(path_prices+"/can_qc_cat_prices.csv")
    can_qc_cat_prices = can_qc_cat_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # California CaT
    us_ca_cat_prices = pd.read_csv(path_prices+"/us_ca_cat_prices.csv")
    us_ca_cat_prices = us_ca_cat_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # Kazakhstan
    kaz_ets_prices = pd.read_csv(path_prices+"/kaz_ets_prices.csv")
    kaz_ets_prices = kaz_ets_prices.rename(columns={"allowance_price":"allowance_price"})

    # Switzerland
    che_ets_prices = pd.read_csv(path_prices+"/che_ets_prices.csv")
    che_ets_prices = che_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # Canadian federal OBPS
    can_obps_prices = pd.read_csv(path_prices+"/can_obps_prices.csv")
    can_obps_prices = can_obps_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # Alberta
    can_ab_ets_prices = pd.read_csv(path_prices+"/can_ab_ets_prices.csv")
    can_ab_ets_prices = can_ab_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})

    # Saskatchewan
    can_sk_ets_prices = pd.read_csv(path_prices+"/can_sk_ets_prices.csv")
    can_sk_ets_prices = can_sk_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})

    # New Brunswick
    can_nb_ets_prices = pd.read_csv(path_prices+"/can_nb_ets_prices.csv")
    can_nb_ets_prices = can_nb_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})

    # Nova Scotia
    can_ns_ets_prices = pd.read_csv(path_prices+"/can_ns_ets_prices.csv")
    can_ns_ets_prices = can_ns_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})

    # Newfoundland and Labrador
    can_nl_ets_prices = pd.read_csv(path_prices+"//can_nl_ets_prices.csv")
    can_nl_ets_prices = can_nl_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    
    
    # ICAP Prices (EU ETS, NZL ETS, KOR ETS, CHN PROV ETS)
    icap = pd.read_csv(path_prices+"/_ICAP_allowance_prices.csv",
                       encoding= 'latin-1', header=2)
    
    icap.rename(columns={"Unnamed: 0":"Date"}, inplace=True)
    
    ## drop unnecessary columns
    drop_cols = [x for x in icap.columns if 'Unnamed' in x]
    icap.drop(drop_cols, axis=1, inplace=True)
    
    drop_list = ['New ETS 1', 'New ETS 2', 'New ETS 3', 'New ETS 4', 'New ETS 5', 
                 'New ETS 6', 'New ETS 7', 'New ETS 8', 'New ETS 9', 'New ETS 10', 
                 'Chinese Pilots', 'Kazakhstan']
    
    icap.drop(drop_list, axis=1, inplace=True)
    icap.drop([0,1], axis=0, inplace=True)
    
    ## rename columns
    icap.rename(columns={"Québec":"Quebec", "South Korea":"Korea, Rep."}, inplace=True)
    
    ## extract year from date string
    
    icap["year"] = icap["Date"].str[6:]
    
    ## set allowance price columns to numeric
    
    for col in ['European Union', 'New Zealand', 'RGGI', 'California', 'Quebec',
           'Ontario', 'Switzerland', 'Korea, Rep.', 'Shenzhen',
           'Shanghai', 'Beijing', 'Guangdong', 'Tianjin', 'Hubei', 'Chongqing',
           'Fujian']:
    
        icap[col] = icap[col].astype('float')
        
    icap_average = icap.groupby(by="year").mean()
    
    ## replace column names with scheme identifiers
    
    name_id_dic = {'European Union':"eu_ets", 'New Zealand':"nzl_ets", 'RGGI':"us_rggi", 
                   'California':"us_ca_cat", 'Quebec':"can_qc_cat", 
                   'Switzerland':"che_ets", 'Korea, Rep.':"kor_ets",
                   'Shenzhen':"chn_sz_ets",'Shanghai':"chn_sh_ets", 'Beijing':"chn_bj_ets", 
                   'Guangdong':"chn_gd_ets", 'Tianjin':"chn_tj_ets", 
                   'Hubei':"chn_hb_ets", 'Chongqing':"chn_cq_ets", 'Fujian':"chn_fj_ets"}
    
    icap_average = icap_average.rename(columns=name_id_dic)
    icap_average = icap_average.reset_index()
    
    icap_average = icap_average.drop(["us_rggi", "Ontario", "che_ets", 
                            "us_ca_cat", "can_qc_cat"], axis=1)
    
    ## add currency codes
    icap_average = icap_average.melt(id_vars=["year"])
    icap_average.columns = ["year", "scheme_id", "allowance_price"]
    
    icap_average["currency_code"] = ""
    
    curr_codes = {"eu_ets":"EUR", "nzl_ets":"NZD", "kor_ets":"KRW",
                  "chn_she_ets":"CNY", "chn_sha_ets":"CNY", "chn_bei_ets":"CNY", 
                  'chn_gua_ets':"CNY", 'chn_tia_ets':"CNY", 'chn_hub_ets':"CNY",
                  'chn_cho_ets':"CNY", 'chn_fuj_ets':"CNY"}
    
    for scheme in curr_codes.keys():
        icap_average.loc[icap_average.scheme_id==scheme, "currency_code"] = curr_codes[scheme]
    
    icap_average["source"] = "db(ICAP-ETS[2021])"
    icap_average["comment"] = "yearly average of daily prices provided by ICAP"
    icap_average["year"] = icap_average["year"].astype(int)
    
    ## manually add EU ETS prices for 2005/2006/2007 - from Bloomberg
    icap_average.loc[(icap_average.scheme_id=="eu_ets") & (icap_average.year==2005), "allowance_price"] = 21.56337209
    icap_average.loc[(icap_average.scheme_id=="eu_ets") & (icap_average.year==2006), "allowance_price"] = 18.00976096
    icap_average.loc[(icap_average.scheme_id=="eu_ets") & (icap_average.year==2007), "allowance_price"] = 0.717649402
    
    #-------------------------------------------------------------------
    
    # Aggregate data from all the sources
    df = pd.concat([rggi_prices, can_qc_cat_prices, us_ca_cat_prices,
                    us_ma_ets_prices,
                    che_ets_prices, kaz_ets_prices,
                    icap_average, can_obps_prices, 
                    can_ab_ets_prices, can_sk_ets_prices, 
                    can_nb_ets_prices, can_ns_ets_prices, 
                    can_nl_ets_prices])
    
    df["allowance_price"] =  df["allowance_price"].round(2)

    return df

