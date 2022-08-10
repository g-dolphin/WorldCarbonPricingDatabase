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
# For emissions trading systems, a script-based update of scope is feasible
# because, when a sector is covered, all fuels within that sector are covered.
# For carbon taxes, it is more tricky - and one has to take greater care - 
# because a given fuel may be subject to the tax in one sector but not another. 

def scope():
    
    # EU ETS
    
    ## Gases

    eu_ets_gas_I = ["PFC"]

    ## Jurisdictions
    
    # PFC emissions from aluminum production included from Phase III of EU ETS onward
    eu_ets_jur_I = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
                     "Ireland", "Italy", "Latvia", "Lithuania", "Liechtenstein", "Luxembourg", "Malta", 
                     "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # The United Kingdom leaves the European Union - and the EU ETS (2021)
    eu_ets_jur_II = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
                     "Ireland", "Italy", "Latvia", "Lithuania", "Liechtenstein", "Luxembourg", "Malta", 
                     "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden"]
    
    ## Sectors
    
    # initial sectoral scope 
    eu_ets_ipcc_I = ["2C3"]
    
    
    ## scope dictionaries

    eu_ets_gas_scope = {2013:eu_ets_gas_I, 2014:eu_ets_gas_I, 2015:eu_ets_gas_I,
                        2016:eu_ets_gas_I, 2017:eu_ets_gas_I, 2018:eu_ets_gas_I,
                        2019:eu_ets_gas_I, 2020:eu_ets_gas_I, 2021:eu_ets_gas_I} 

    eu_ets_jur_scope = {2013:eu_ets_jur_I, 2014:eu_ets_jur_I, 2015:eu_ets_jur_I,
                        2016:eu_ets_jur_I, 2017:eu_ets_jur_I, 2018:eu_ets_jur_I,
                        2019:eu_ets_jur_I, 2020:eu_ets_jur_I, 2021:eu_ets_jur_II}
    
    eu_ets_ipcc_scope = {2013:eu_ets_ipcc_I, 2014:eu_ets_ipcc_I, 2015:eu_ets_ipcc_I,
                         2016:eu_ets_ipcc_I, 2017:eu_ets_ipcc_I, 2018:eu_ets_ipcc_I,
                         2019:eu_ets_ipcc_I, 2020:eu_ets_ipcc_I, 2021:eu_ets_ipcc_I}

    
    ## Sources dictionary
    
    eu_ets_scope_sources = {2013:,2014:,2015:,
                            2016:,2017:,2018:,
                            2019:,2020:,2021:}

    #-------------------------------------------------------------------------

    
    # California CaT

    ## Gases

    usa_ca_ets_gas_I = ["HFC", "PFC", "NF3", "SF6"]
    
    ## Jurisdictions
    
    # initial scope
    usa_ca_ets_jur_I = ["California"]
    usa_ca_ets_jur_II = ["California", "Quebec"]
    usa_ca_ets_jur_III = ["California", "Quebec", "Ontario"]

    ## Sectors
    
    usa_ca_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                        "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",
                        "1A2L", "1A2M", "1A5A", "1C1A", "1C1B",
                        "2A1", "2A2", "2A3", "2C1", "2C5", "2H1",  
                        "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                        "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                        "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                        "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                        "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                        "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    usa_ca_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                         "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",
                         "1A2L", "1A2M", "1A3B", "1A4A", "1A4B", "1A5A", "1C1A", "1C1B",
                         "2A1", "2A2", "2A3", "2C1", "2C5", "2H1",  
                         "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                         "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                         "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                         "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                         "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                         "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## scope dictionaries

    usa_ca_ets_gas_scope = {2012:usa_ca_ets_gas_I, 2013:usa_ca_ets_gas_I, 2014:usa_ca_ets_gas_I, 
                            2015:usa_ca_ets_gas_I, 2016:usa_ca_ets_gas_I, 2017:usa_ca_ets_gas_I,
                            2018:usa_ca_ets_gas_I, 2019:usa_ca_ets_gas_I, 2020:usa_ca_ets_gas_I,
                            2021:usa_ca_ets_gas_I}

    usa_ca_ets_jur_scope = {2012:usa_ca_ets_jur_I, 2013:usa_ca_ets_jur_I, 2014:usa_ca_ets_jur_II, 
                            2015:usa_ca_ets_jur_II, 2016:usa_ca_ets_jur_II, 2017:usa_ca_ets_jur_II,
                            2018:usa_ca_ets_jur_III, 2019:usa_ca_ets_jur_II, 2020:usa_ca_ets_jur_II,
                            2021:usa_ca_ets_jur_II}
    
    usa_ca_ets_ipcc_scope = {2012:usa_ca_ets_ipcc_I, 2013:usa_ca_ets_ipcc_I, 2014:usa_ca_ets_ipcc_II, 
                             2015:usa_ca_ets_ipcc_II, 2016:usa_ca_ets_ipcc_II, 2017:usa_ca_ets_ipcc_II,
                             2018:usa_ca_ets_ipcc_II, 2019:usa_ca_ets_ipcc_II, 2020:usa_ca_ets_ipcc_II,
                             2021:usa_ca_ets_ipcc_II}
    
    
    ## Sources dictionary
    
    usa_ca_ets_scope_sources = {2012:"leg(CA-AB32(2006))", 2013:"leg(CA-AB32(2006))", 2014:"leg(CA-AB32(2006))", 
                                2015:"leg(CA-AB32(2006))", 2016:"leg(CA-AB32(2006))", 2017:"leg(CA-AB32(2006))",
                                2018:"leg(CA-AB32(2006))", 2019:"leg(CA-AB32(2006))", 2020:"leg(CA-AB32(2006))",
                                2021:"leg(CA-AB32(2006))"}
    
    #----------------------------------------------------------------------------
    
    # Chongqing Municipality
    
    ## Gases

    chn_cq_ets_gas_I = []

    ## Jurisdiction
    
    chn_cq_ets_jur_I = ["Chongqing Municipality"]
    
    ## Sectors
    
    chn_cq_ets_ipcc_I = []
    
    ## Gases
    
    chn_cq_ets_gas_I = []
    
    ## scope dictionaries
    chn_cq_ets_jur_scope = {2014:chn_cq_ets_jur_I,
                           2015:chn_cq_ets_jur_I, 2016:chn_cq_ets_jur_I,
                           2017:chn_cq_ets_jur_I, 2018:chn_cq_ets_jur_I,
                           2019:chn_cq_ets_jur_I, 2020:chn_cq_ets_jur_I,
                           2021:chn_cq_ets_jur_I}
    
    chn_cq_ets_ipcc_scope = {2014:chn_cq_ets_ipcc_I,
                            2015:chn_cq_ets_ipcc_I, 2016:chn_cq_ets_ipcc_I,
                            2017:chn_cq_ets_ipcc_I, 2018:chn_cq_ets_ipcc_I,
                            2019:chn_cq_ets_ipcc_I, 2020:chn_cq_ets_ipcc_I,
                            2021:chn_cq_ets_ipcc_I}

    chn_cq_ets_gas_scope = {}

    ## Sources dictionary
    
    chn_cq_ets_scope_sources = {2014:, 2015:, 
                                   2016:, 2017:, 
                                   2018:, 2019:, 
                                   2020:, 2021:}
    
    
    #----------------------------------------------------------------------------
    
    # Korea, Rep.
    
    ## Gases

    kor_ets_gas_I = ["PFC", "HFC", "SF6"]

    ## Jurisdiction
    
    kor_ets_jur_I = ["Korea, Rep."]
    
    ## Sectors
    
    # initial scope (2015)
    kor_ets_ipcc_I = ["1A1A1", "1A2A", "1A1B",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2L", "1A2M",
                      "1A3A2", "1A4A", "1A4B",
                      "2A1", "2A2", "2A3", "2A4A", 
                      "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                      "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2B10",
                      "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2", 
                      "2D3", "2D4", "2H1", "2H2",
                      "4A1", "4D1", "4D2"]
        
    # phase 2 scope (2018)
    kor_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A1B",
                  "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                  "1A2I", "1A2J", "1A2L", "1A2M",
                  "1A3A2", 
                  "1A4A", "1A4B",
                  "2A1", "2A2", "2A3", "2A4A", 
                  "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                  "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2B10",
                  "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2", 
                  "2D3", "2D4", "2H1", "2H2",
                  "4A1", "4D1", "4D2"]
    
    # phase 3 scope (2021)
    kor_ets_ipcc_III = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A1B",
                        "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                        "1A2I", "1A2J", "1A2K", "1A2L", "1A2M",
                        "1A3A2", "1A3B", "1A3C", "1A3D2",
                        "1A4A", "1A4B",
                        "2A1", "2A2", "2A3", "2A4A", 
                        "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                        "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2B10",
                        "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2", 
                        "2D3", "2D4", "2H1", "2H2",
                        "4A1", "4D1", "4D2"]
    
    
    ## scope dictionaries
    kor_ets_gas_scope = {2015:kor_ets_gas_I, 2016:kor_ets_gas_I,
                            2017:kor_ets_gas_I, 2018:kor_ets_gas_I,
                            2019:kor_ets_gas_I, 2020:kor_ets_gas_I,
                            2021:kor_ets_gas_I}

    kor_ets_jur_scope = {2015:kor_ets_jur_I, 2016:kor_ets_jur_I,
                            2017:kor_ets_jur_I, 2018:kor_ets_jur_I,
                            2019:kor_ets_jur_I, 2020:kor_ets_jur_I,
                            2021:kor_ets_jur_I}
    
    kor_ets_ipcc_scope = {2015:kor_ets_ipcc_I, 2016:kor_ets_ipcc_I,
                            2017:kor_ets_ipcc_I, 2018:kor_ets_ipcc_II,
                            2019:kor_ets_ipcc_II, 2020:kor_ets_ipcc_II,
                            2021:kor_ets_ipcc_III}
    
    
    ## Sources dictionary
    
    kor_ets_scope_sources = {2015:, 
                             2016:, 
                             2017:, 2018:, 
                             2019:,
                             2020:, 2021:}

    #----------------------------------------------------------------------------
    
    # New Zealand

    ## Gases

    nzl_ets_gas_I = []

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
    
    
    ## scope dictionaries
    nzl_ets_gas_scope = {2008:nzl_ets_jur_I,
                            2009:nzl_ets_jur_I, 2010:nzl_ets_jur_I,
                            2011:nzl_ets_jur_I, 2012:nzl_ets_jur_I,
                            2013:nzl_ets_jur_I, 2014:nzl_ets_jur_I,
                            2015:nzl_ets_jur_I, 2016:nzl_ets_jur_I,
                            2017:nzl_ets_jur_I, 2018:nzl_ets_jur_I,
                            2019:nzl_ets_jur_I, 2020:nzl_ets_jur_I,
                            2021:nzl_ets_jur_I}    

    nzl_ets_jur_scope = {2008:nzl_ets_jur_I,
                            2009:nzl_ets_jur_I, 2010:nzl_ets_jur_I,
                            2011:nzl_ets_jur_I, 2012:nzl_ets_jur_I,
                            2013:nzl_ets_jur_I, 2014:nzl_ets_jur_I,
                            2015:nzl_ets_jur_I, 2016:nzl_ets_jur_I,
                            2017:nzl_ets_jur_I, 2018:nzl_ets_jur_I,
                            2019:nzl_ets_jur_I, 2020:nzl_ets_jur_I,
                            2021:nzl_ets_jur_I}
    
    nzl_ets_ipcc_scope = {2008:nzl_ets_ipcc_I,
                            2009:nzl_ets_ipcc_I, 2010:nzl_ets_ipcc_II,
                            2011:nzl_ets_ipcc_II, 2012:nzl_ets_ipcc_II,
                            2013:nzl_ets_ipcc_III, 2014:nzl_ets_ipcc_III,
                            2015:nzl_ets_ipcc_III, 2016:nzl_ets_ipcc_III,
                            2017:nzl_ets_ipcc_III, 2018:nzl_ets_ipcc_III,
                            2019:nzl_ets_ipcc_III, 2020:nzl_ets_ipcc_III,
                            2021:nzl_ets_ipcc_III}
    

    ## Sources dictionary
    
    nzl_ets_scope_sources = {2008:, 2009:,
                               2010:, 2011:, 
                               2012:, 2013:, 
                               2014:, 2015:, 
                               2016:, 2017:, 
                               2018:, 2019:,
                               2020:, 2021:}
    
    #----------------------------------------------------------------------------
    
    # Switzerland

    ## Gases

    che_ets_gas_I = []

    ## Jurisdiction
    
    che_ets_jur_I = ["Switzerland"]
    
    ## Sectors (source: CO2 Ordinance)
    che_ets_ipcc_I = []
    
    ## scope dictionaries
    che_ets_jur_scope = {2008:che_ets_jur_I,
                            2009:che_ets_jur_I, 2010:che_ets_jur_I,
                            2011:che_ets_jur_I, 2012:che_ets_jur_I,
                            2013:che_ets_jur_I, 2014:che_ets_jur_I,
                            2015:che_ets_jur_I, 2016:che_ets_jur_I,
                            2017:che_ets_jur_I, 2018:che_ets_jur_I,
                            2019:che_ets_jur_I, 2020:che_ets_jur_I,
                            2021:che_ets_jur_I}
    
    che_ets_ipcc_scope = {2008:che_ets_ipcc_I,
                            2009:che_ets_ipcc_I, 2010:che_ets_ipcc_I,
                            2011:che_ets_ipcc_I, 2012:che_ets_ipcc_I,
                            2013:che_ets_ipcc_I, 2014:che_ets_ipcc_I,
                            2015:che_ets_ipcc_I, 2016:che_ets_ipcc_I,
                            2017:che_ets_ipcc_I, 2018:che_ets_ipcc_I,
                            2019:che_ets_ipcc_I, 2020:che_ets_ipcc_I,
                            2021:che_ets_ipcc_I}
    
    ## Sources dictionary
    
    che_ets_scope_sources = {2008:, 2009:,
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

   #----------------------------------------------------------------------------
    
    # Nova Scotia

    ## Gases

    can_ns_ets_gas_I = []

    ## Jurisdiction
    
    can_ns_ets_jur_I = ["Nova Scotia"]

    ## Sectors

    # Provincial OBPS for industrial emitters and federal OBPS for electricity  
    # and transmission sectors
    can_ns_ets_ipcc_I = []
    
    ## scope dictionaries
    can_ns_ets_jur_scope = {2019:can_ns_ets_jur_I, 2020:can_ns_ets_jur_I,
                               2021:can_ns_ets_jur_I}
    
    can_ns_ets_ipcc_scope = {2019:can_ns_ets_ipcc_I, 2020:can_ns_ets_ipcc_I,
                                2021:can_ns_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_ns_ets_scope_sources = {2019:, 2020:,
                                2021:}  

    #------------------------------All schemes dictionaries--------------------------------#
    
    ets_scope = {"eu_ets":{"gases":eu_ets_gas_scope,
                           "jurisdictions":eu_ets_jur_scope, 
                           "sectors":eu_ets_ipcc_scope},
                 "che_ets":{"gases":che_ets_gas_scope,
                            "jurisdictions":che_ets_jur_scope, 
                            "sectors":che_ets_ipcc_scope},
                 "kor_ets":{"gases":kor_ets_gas_scope,
                            "jurisdictions":kor_ets_jur_scope, 
                            "sectors":kor_ets_ipcc_scope},
                 "nzl_ets":{"jurisdictions":nzl_ets_jur_scope, 
                            "sectors":nzl_ets_ipcc_scope,
                            "gases":nzl_ets_gas_scope},
                 "can_ns_ets":{"jurisdictions":can_ns_ets_jur_scope, 
                                "sectors":can_ns_ets_ipcc_scope,
                                "gases":can_ns_ets_gas_scope},
                 "chn_cq_ets":{"jurisdictions":chn_cq_ets_jur_scope, 
                                "sectors":chn_cq_ets_ipcc_scope,
                                "gases":chn_cq_ets_gas_scope},
                 "usa_ca_ets":{"gases":usa_ca_ets_gas_scope,
                                "jurisdictions":usa_ca_ets_jur_scope, 
                                "sectors":usa_ca_ets_ipcc_scope}}

    ets_scope_sources = {"eu_ets":eu_ets_scope_sources,                            
                         "che_ets":che_ets_scope_sources,
                         "kor_ets":kor_ets_scope_sources,
                         "nzl_ets":nzl_ets_scope_sources,
                         "can_ns_ets":can_ns_ets_scope_sources,
                         "chn_cq_ets":chn_cq_ets_scope_sources,
                         "usa_ca_ets":usa_ca_ets_scope_sources}
    
    data_and_sources = {"data":ets_scope, "sources":ets_scope_sources}
    
    return data_and_sources


