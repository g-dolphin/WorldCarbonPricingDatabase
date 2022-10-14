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
    usa_rggi_prices = pd.read_csv(path_prices+"/usa_rggi_prices.csv")
    usa_rggi_prices.loc[:, "allowance_price"] = usa_rggi_prices.allowance_weighted_price/0.90718474
    usa_rggi_prices = usa_rggi_prices.drop(["allowance_weighted_price"], axis=1)

    # California CaT
    usa_ma_ets_prices = pd.read_csv(path_prices+"/usa_ma_ets_prices.csv")
    usa_ma_ets_prices = usa_ma_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # Quebec CaT
    can_qc_cat_prices = pd.read_csv(path_prices+"/can_qc_cat_prices.csv")
    can_qc_cat_prices = can_qc_cat_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
    # California CaT
    usa_ca_ets_prices = pd.read_csv(path_prices+"/usa_ca_ets_prices.csv")
    usa_ca_ets_prices = usa_ca_ets_prices.rename(columns={"allowance_weighted_price":"allowance_price"})
    
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
    

    # ICAP Prices (EU ETS, NZL ETS, KOR ETS, CHN PROV ETS, CAN PROV)
    icap_raw = pd.read_csv(path_prices+"/_ICAP_allowance_prices.csv",
                           delimiter=";", encoding= 'latin-1', header=2, 
                           low_memory=False)
    
    icap_raw.drop([0,1], axis=0, inplace=True)
    
    icap_raw.rename(columns={"Unnamed: 0":"Date"}, inplace=True)
    
    chn_pilots_cols = []
    
    for i in range(251,273,3):
        chn_pilots_cols = chn_pilots_cols + ["Unnamed: "+ str(i)]
    
    drop_cols = []
    
    for col in icap_raw.columns:
        if "Unnamed" in col and col not in chn_pilots_cols:
            drop_cols = drop_cols + [col]
    
    icap_raw.drop(drop_cols, axis=1, inplace=True)
    
    ## drop unnecessary columns
    
    drop_list = ['New ETS 5', 'New ETS 6', 'New ETS 7', 
                 'New ETS 8', 'New ETS 9', 'New ETS 10', 
                 'Chinese Pilots', 'Kazakhstan']
    
    icap_raw.drop(drop_list, axis=1, inplace=True)
    
    ## rename columns
    icap_raw.rename(columns={"QuÃ©bec":"Quebec", "South Korea":"Korea, Rep.",
                             "Unnamed: 251":"Shenzhen", "Unnamed: 254":"Shanghai", 
                             "Unnamed: 257":"Beijing", "Unnamed: 260":"Guangdong",
                             "Unnamed: 263":"Tianjin", "Unnamed: 266":"Hubei",
                             "Unnamed: 269":"Chongqing", "Unnamed: 272":"Fujian"}, inplace=True)
    
    ## replace "," with "." in columns; convert to float
    
    for col in list(icap_raw.columns)[1:]:  
        icap_raw[col] = icap_raw[col].str.replace(",", ".")
        icap_raw[col] = icap_raw[col].astype(float)
    
    ## extract year from date string
    
    icap_raw["year"] = icap_raw["Date"].str[6:]
        
    icap_raw_average = icap_raw.groupby(by="year").mean()
    
    ## replace column names with carbon pricing scheme identifiers
    
    name_id_dic = {'European Union':"eu_ets", 'New Zealand':"nzl_ets", "Germany":"deu_ets",
                   'RGGI':"usa_rggi", "United Kingdom":"gbr_ets", "China":"chn_ets",
                   'California':"usa_ca_ets", 'Quebec':"can_qc_cat", 
                   'Switzerland':"che_ets", 'Korea, Rep.':"kor_ets",
                   "Nova Scotia":"can_ns_ets", "Ontario":"can_on_ets",
                   'Shenzhen':"chn_sz_ets",'Shanghai':"chn_sh_ets", 'Beijing':"chn_bj_ets", 
                   'Guangdong':"chn_gd_ets", 'Tianjin':"chn_tj_ets", 
                   'Hubei':"chn_hb_ets", 'Chongqing':"chn_cq_ets", 'Fujian':"chn_fj_ets"}
    
    icap_raw_average = icap_raw_average.rename(columns=name_id_dic)
    icap_raw_average = icap_raw_average.reset_index()
    
    icap_raw_average = icap_raw_average.drop(["usa_rggi", "can_on_ets", "che_ets", 
                                              "usa_ca_ets", "can_qc_cat", "can_ns_ets"], axis=1)
    
    ## add currency codes
    icap_raw_average = icap_raw_average.melt(id_vars=["year"])
    icap_raw_average.columns = ["year", "scheme_id", "allowance_price"]
    
    icap_raw_average["currency_code"] = ""
    
    curr_codes = {"eu_ets":"EUR", "nzl_ets":"NZD", "kor_ets":"KRW",
                  "gbr_ets":"GBP", 'chn_ets':'CNY', "deu_ets":"EUR",
                  "chn_sz_ets":"CNY", "chn_sh_ets":"CNY", "chn_bj_ets":"CNY", 
                  'chn_gd_ets':"CNY", 'chn_tj_ets':"CNY", 'chn_hb_ets':"CNY",
                  'chn_cq_ets':"CNY", 'chn_fj_ets':"CNY"}
    
    for scheme in curr_codes.keys():
        icap_raw_average.loc[icap_raw_average.scheme_id==scheme, "currency_code"] = curr_codes[scheme]
    
    icap_raw_average["source"] = "db(ICAP-ETS[2021])"
    icap_raw_average["comment"] = "yearly average of daily prices provided by ICAP"
    icap_raw_average["year"] = icap_raw_average["year"].astype(int)
    
    ## manually add EU ETS prices for 2005/2006/2007 - from Bloomberg
    icap_raw_average.loc[(icap_raw_average.scheme_id=="eu_ets") & (icap_raw_average.year==2005), "allowance_price"] = 21.56337209
    icap_raw_average.loc[(icap_raw_average.scheme_id=="eu_ets") & (icap_raw_average.year==2006), "allowance_price"] = 18.00976096
    icap_raw_average.loc[(icap_raw_average.scheme_id=="eu_ets") & (icap_raw_average.year==2007), "allowance_price"] = 0.717649402
        
    #-------------------------------------------------------------------
    
    # Aggregate data from all the sources
    df = pd.concat([usa_rggi_prices, can_qc_cat_prices, usa_ca_ets_prices,
                    usa_ma_ets_prices,
                    che_ets_prices, kaz_ets_prices,
                    icap_raw_average, can_obps_prices, 
                    can_ab_ets_prices, can_sk_ets_prices, 
                    can_nb_ets_prices, can_ns_ets_prices, 
                    can_nl_ets_prices])
    
    df["allowance_price"] =  df["allowance_price"].round(2)

    return df

