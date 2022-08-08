#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:55:02 2021

@author: gd
"""



# Assigning the correct prices to each jurisdiction-year-sector entry requires
# a scheme-specific identifier and a mapping between carbon pricing scheme and jurisdiction-year-sector

# This is the best way to robustly deal with cases where 1) prices in one jurisdiction
# arise from multi-jurisdictions schemes and 2) the applicable scheme changes from one year to the other
# 3) more than one scheme apply to the same sector and/or emissions 
# e.g. Chinese Provinces with pilot ETS joining the national one
# e.g. Canadian Province with province level ETS becoming subject to federal tax
# e.g. Switzerland joining EU ETS in 2021


#------------------------Emissions trading systems----------------------------#
# For emissions trading systems, a script-based update of coverage is feasible
# because, when a sector is covered, all fuels within that sector are covered.
# For carbon taxes, it is more tricky - and one has to take greater care - 
# because a given fuel may be subject to the tax in one sector but not another. 

def scope():
    
    # EU ETS
    
    ## Jurisdictions
    
    # initial country coverage (2005)
    eu_ets_ctry_I = []
    
    
    ## Sectors
    
    # initial sectoral coverage 
    eu_ets_ipcc_I = []
    
    
    ## Coverage dictionaries
    
    eu_ets_jur_coverage = {}
    
    eu_ets_ipcc_coverage = {}

    eu_ets_ipcc_coverage = {} # need to specify which F gas is covered
    
    ## Sources dictionary
    
    eu_ets_coverage_sources = {}

    #-------------------------------------------------------------------------

    
    # California CaT
    
    ## Jurisdictions
    
    # initial coverage
    usa_ca_ets_ctry_I = ["California"]
    
    ## Sectors
    
    # initial sectoral coverage 
    usa_ca_ets_ipcc_I = []
    
    ## Gases
    
    usa_ca_ets_ghg_I = []
    
    ## Coverage dictionaries
    
    usa_ca_ets_jur_coverage = {}
    
    usa_ca_ets_ipcc_coverage = {}
    
    usa_ca_ets_ghg_coverage = {}
    
    
    ## Sources dictionary
    
    usa_ca_ets_coverage_sources = {}
    
    #----------------------------------------------------------------------------
    
    # Chongqing Municipality
    
    ## Jurisdiction
    
    chn_cq_ets_jur_I = ["Chongqing Municipality"]
    
    ## Sectors
    
    chn_cq_ets_ipcc_I = []
    
    ## Gases
    
    chn_cq_ets_ghg_I = []
    
    ## Coverage dictionaries
    chn_cq_ets_jur_coverage = {2014:chn_cq_ets_jur_I,
                           2015:chn_cq_ets_jur_I, 2016:chn_cq_ets_jur_I,
                           2017:chn_cq_ets_jur_I, 2018:chn_cq_ets_jur_I,
                           2019:chn_cq_ets_jur_I, 2020:chn_cq_ets_jur_I,
                           2021:chn_cq_ets_jur_I}
    
    chn_cq_ets_ipcc_coverage = {2014:chn_cq_ets_ipcc_I,
                            2015:chn_cq_ets_ipcc_I, 2016:chn_cq_ets_ipcc_I,
                            2017:chn_cq_ets_ipcc_I, 2018:chn_cq_ets_ipcc_I,
                            2019:chn_cq_ets_ipcc_I, 2020:chn_cq_ets_ipcc_I,
                            2021:chn_cq_ets_ipcc_I}

    chn_cq_ets_ghg_coverage = {}

    ## Sources dictionary
    
    chn_cq_ets_coverage_sources = {2014:, 2015:, 
                                   2016:, 2017:, 
                                   2018:, 2019:, 
                                   2020:, 2021:}
    
    
    #----------------------------------------------------------------------------
    
    # Korea, Rep.
    
    ## Jurisdiction
    
    kor_ets_jur_I = ["Korea, Rep."]
    
    ## Sectors
    
    # initial scope (2015)
    kor_ets_ipcc_I = []
        
    # phase 2 scope (2018)
    kor_ets_ipcc_II = []
    
    # phase 3 scope (2021)
    kor_ets_ipcc_III = []
    
    ## Gases
    
    kor_ets_ghg_I = []
    
    
    ## Coverage dictionaries
    kor_ets_jur_coverage = {2015:kor_ets_jur_I, 2016:kor_ets_jur_I,
                            2017:kor_ets_jur_I, 2018:kor_ets_jur_I,
                            2019:kor_ets_jur_I, 2020:kor_ets_jur_I,
                            2021:kor_ets_jur_I}
    
    kor_ets_ipcc_coverage = {2015:kor_ets_ipcc_I, 2016:kor_ets_ipcc_I,
                            2017:kor_ets_ipcc_I, 2018:kor_ets_ipcc_II,
                            2019:kor_ets_ipcc_II, 2020:kor_ets_ipcc_II,
                            2021:kor_ets_ipcc_III}
    
    kor_ets_ghg_coverage = {}
    
    ## Sources dictionary
    
    kor_ets_coverage_sources = {2015:, 
                                2016:, 
                                2017:, 2018:, 
                                2019:,
                                2020:, 2021:}

    #----------------------------------------------------------------------------
    
    # New Zealand
    
    ## Jurisdiction
    
    nzl_ets_jur_I = ["New Zealand"]
    
    ## Sectors
    
    # initial scope (2008)
    nzl_ets_ipcc_I = []
    
    # extension to power, industry, liquid fuels (road transport, heating fuels, 
    # domestic aviation) (2010)
    nzl_ets_ipcc_II = []
    
    # extension to waste and synthetic GHGs (2013)
    nzl_ets_ipcc_III = []
    
    ## Gases
    
    nzl_ets_ghg_I = []
    
    ## Coverage dictionaries
    
    nzl_ets_jur_coverage = {2008:nzl_ets_jur_I,
                            2009:nzl_ets_jur_I, 2010:nzl_ets_jur_I,
                            2011:nzl_ets_jur_I, 2012:nzl_ets_jur_I,
                            2013:nzl_ets_jur_I, 2014:nzl_ets_jur_I,
                            2015:nzl_ets_jur_I, 2016:nzl_ets_jur_I,
                            2017:nzl_ets_jur_I, 2018:nzl_ets_jur_I,
                            2019:nzl_ets_jur_I, 2020:nzl_ets_jur_I,
                            2021:nzl_ets_jur_I}
    
    nzl_ets_ipcc_coverage = {2008:nzl_ets_ipcc_I,
                            2009:nzl_ets_ipcc_I, 2010:nzl_ets_ipcc_II,
                            2011:nzl_ets_ipcc_II, 2012:nzl_ets_ipcc_II,
                            2013:nzl_ets_ipcc_III, 2014:nzl_ets_ipcc_III,
                            2015:nzl_ets_ipcc_III, 2016:nzl_ets_ipcc_III,
                            2017:nzl_ets_ipcc_III, 2018:nzl_ets_ipcc_III,
                            2019:nzl_ets_ipcc_III, 2020:nzl_ets_ipcc_III,
                            2021:nzl_ets_ipcc_III}
    
    nzl_ets_ghg_coverage = {}

    ## Sources dictionary
    
    nzl_ets_coverage_sources = {2008:, 2009:,
                               2010:, 2011:, 
                               2012:, 2013:, 
                               2014:, 2015:, 
                               2016:, 2017:, 
                               2018:, 2019:,
                               2020:, 2021:}
    
    #----------------------------------------------------------------------------
    
    # Nova Scotia
    
    ## Jurisdiction
    
    can_ns_ets_jur_I = ["Nova Scotia"]

    ## Sectors

    # Provincial OBPS for industrial emitters and federal OBPS for electricity  
    # and transmission sectors
    can_ns_ets_ipcc_I = []
    
    ## Coverage dictionaries
    can_ns_ets_jur_coverage = {2019:can_ns_ets_jur_I, 2020:can_ns_ets_jur_I,
                               2021:can_ns_ets_jur_I}
    
    can_ns_ets_ipcc_coverage = {2019:can_ns_ets_ipcc_I, 2020:can_ns_ets_ipcc_I,
                                2021:can_ns_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_ns_ets_coverage_sources = {2019:, 2020:,
                                   2021:}  
    
    #----------------------------------------------------------------------------
    
    # Switzerland
    
    ## Jurisdiction
    
    che_ets_jur_I = ["Switzerland"]
    
    ## Sectors (source: CO2 Ordinance)
    che_ets_ipcc_I = []

    ## Gases
    
    che_ets_ghg_I = []
    
    ## Coverage dictionaries
    che_ets_jur_coverage = {2008:che_ets_jur_I,
                            2009:che_ets_jur_I, 2010:che_ets_jur_I,
                            2011:che_ets_jur_I, 2012:che_ets_jur_I,
                            2013:che_ets_jur_I, 2014:che_ets_jur_I,
                            2015:che_ets_jur_I, 2016:che_ets_jur_I,
                            2017:che_ets_jur_I, 2018:che_ets_jur_I,
                            2019:che_ets_jur_I, 2020:che_ets_jur_I,
                            2021:che_ets_jur_I}
    
    che_ets_ipcc_coverage = {2008:che_ets_ipcc_I,
                            2009:che_ets_ipcc_I, 2010:che_ets_ipcc_I,
                            2011:che_ets_ipcc_I, 2012:che_ets_ipcc_I,
                            2013:che_ets_ipcc_I, 2014:che_ets_ipcc_I,
                            2015:che_ets_ipcc_I, 2016:che_ets_ipcc_I,
                            2017:che_ets_ipcc_I, 2018:che_ets_ipcc_I,
                            2019:che_ets_ipcc_I, 2020:che_ets_ipcc_I,
                            2021:che_ets_ipcc_I}
    
    nzl_ets_ghg_coverage = {}
    
    ## Sources dictionary
    
    che_ets_coverage_sources = {2008:, 2009:,
                               2010:, 2011:, 
                               2012:, 
                               2013:, 
                               2014:,
                               2015:, 
                               2016:, 
                               2017:, 
                               2018:, 
                               2019:,
                               2020:, 
                               2021:}

    #------------------------------All schemes dictionaries--------------------------------#
    
    ets_coverage = {"eu_ets":{"jurisdictions":eu_ets_jur_coverage, 
                                  "sectors":eu_ets_ipcc_coverage,
                                  "gases":eu_ets_ghg_coverage},
                    "usa_ca_ets":{"jurisdictions":usa_ca_ets_jur_coverage, 
                                  "sectors":usa_ca_ets_ipcc_coverage,
                                  "gases":usa_ca_ets_ghg_coverage},
                    "kor_ets":{"jurisdictions":kor_ets_jur_coverage, 
                                  "sectors":kor_ets_ipcc_coverage,
                                  "gases":kor_ets_ghg_coverage},
                    "nzl_ets":{"jurisdictions":nzl_ets_jur_coverage, 
                                  "sectors":nzl_ets_ipcc_coverage,
                                  "gases":nzl_ets_ghg_coverage},
                    "che_ets":{"jurisdictions":che_ets_jur_coverage, 
                                  "sectors":che_ets_ipcc_coverage,
                                  "gases":che_ets_ghg_coverage},
                    "can_ns_ets":{"jurisdictions":can_ns_ets_jur_coverage, 
                                  "sectors":can_ns_ets_ipcc_coverage,
                                  "gases":can_ns_ets_ghg_coverage},
                    "chn_cq_ets":{"jurisdictions":chn_cq_ets_jur_coverage, 
                                  "sectors":chn_cq_ets_ipcc_coverage,
                                  "gases":chn_cq_ets_ghg_coverage}}

    ets_coverage_sources = {"eu_ets":eu_ets_coverage_sources,
                            "usa_ca_ets":usa_ca_ets_coverage_sources,
                            "kor_ets":kor_ets_coverage_sources,
                            "nzl_ets":nzl_ets_coverage_sources,
                            "che_ets":che_ets_coverage_sources,
                            "can_ns_ets":can_ns_ets_coverage_sources,
                            "chn_cq_ets":chn_cq_ets_coverage_sources}
    
    data_and_sources = {"data":ets_coverage, "sources":ets_coverage_sources}
    
    return data_and_sources


