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

    # Korea, Rep.
    
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
    kor_ets_jur_scope = {year: kor_ets_jur_I for year in range(2015,2025)}
    
    kor_ets_ipcc_scope = {
        2015:kor_ets_ipcc_I, 2016:kor_ets_ipcc_I,
        2017:kor_ets_ipcc_I, 2018:kor_ets_ipcc_II,
        2019:kor_ets_ipcc_II, 2020:kor_ets_ipcc_II,
        2021:kor_ets_ipcc_III, 2022:kor_ets_ipcc_III,
        2023:kor_ets_ipcc_III, 2024:kor_ets_ipcc_III
        }
    
    ## Sources dictionary
    
    kor_ets_scope_sources = {2015:"leg(KR[2012], KR[2013])", 
                             2016:"leg(KR[2012], KR[2013])", 
                             2017:"leg(KR[2017])", 2018:"leg(KR[2018])", 
                             2019:"leg(KR[2018])",
                             2020:"leg(KR[2020])", 2021:"leg(KR[2020])"}

    #----------------------------------------------------------------------------
    
    # New Zealand
    
    ## Jurisdiction
    
    nzl_ets_jur_I = ["New Zealand"]
    
    ## IPCC categories
    
    # initial scope (2008)
    nzl_ets_ipcc_I = ["3B1A", "3B1B"]
    
    # extension to power, industry, liquid fuels (road transport, heating fuels, 
    # domestic aviation) (2010)
    nzl_ets_ipcc_II = ["1A1A1", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C", "1A2D", 
                       "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", 
                       "1A2L", "1A2M", "1A3A2", "1A3B", "1A3C", "1A4A", "1A4B",
                       "1A4C1", "1A4C2", "1A4C3", 
                       "2A1", "2A2", "2A3", "2A4A",
                       "2A4B", "2A4C", "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5",
                       "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F",
                       "2B9A", "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7",
                       "2D1", "2D2", "2D3", "2D4", "2F1", "2F2", "2F3", "2F4", "2F5",
                       "2F6", "2G1", "2G2", "2G3", "2G4", "2H1",
                       "3B1A", "3B1B"]
    
    # extension to waste and synthetic GHGs (2013)
    nzl_ets_ipcc_III = ["1A1A1", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C", "1A2D", 
                        "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", 
                        "1A2L", "1A2M", "1A3A2", "1A3B", "1A3C", "1A4A", "1A4B",
                        "1A4C1", "1A4C2", "1A4C3", 
                        "2A1", "2A2", "2A3", "2A4A",
                        "2A4B", "2A4C", "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5",
                        "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F",
                        "2B9A", "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7",
                        "2D1", "2D2", "2D3", "2D4", "2F1", "2F2", "2F3", "2F4", "2F5",
                        "2F6", "2G1", "2G2", "2G3", "2G4", "2H1",
                        "3B1A", "3B1B",
                        "4A1", "4C1", "4C2"]
    
    ## scope dictionaries
    
    nzl_ets_jur_scope = {year: nzl_ets_jur_I for year in range(2008, 2025)}
    
    nzl_ets_ipcc_scope = {year: nzl_ets_ipcc_I for year in range(2008, 2010)}
    nzl_ets_ipcc_scope.update({year: nzl_ets_ipcc_II for year in range(2010, 2013)})
    nzl_ets_ipcc_scope.update({year: nzl_ets_ipcc_III for year in range(2013, 2025)})    

    ## Sources dictionary
    
    nzl_ets_scope_sources = {2008:"leg(NZ-CCR[2008])", 2009:"leg(NZ-CCR[2008])",
                             2010:"leg(NZ-CCR[2008])", 2011:"leg(NZ-CCR[2011])", 
                             2012:"leg(NZ-CCR[2011])", 2013:"leg(NZ-CCR[2013])", 
                             2014:"leg(NZ-CCR[2013])", 2015:"leg(NZ-CCR[2013])", 
                             2016:"leg(NZ-CCR[2013])", 2017:"leg(NZ-CCR[2013])", 
                             2018:"leg(NZ-CCR[2013])", 2019:"leg(NZ-CCR[2013])",
                             2020:"leg(NZ-CCR[2020])", 2021:"leg(NZ-CCR[2020])",
                             2022:"leg(NZ-CCR[2020]), report(ICAP[2023])",
                             2023: " ", 2024: " "}

    #----------------------------------------------------------------------------

    # Switzerland
    
    ## Jurisdiction
    
    che_tax_jur_I = ["Switzerland"]

    ## IPCC categories
    
    # initial scope
    che_tax_ipcc_I = ["1A1A2", "1A1A3", "1A4A", "1A4B"]

    ## Fuels
    
    che_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    che_tax_jur_scope = {year: che_tax_jur_I for year in range(2008, 2025)}
    
    che_tax_ipcc_scope = {year: che_tax_ipcc_I for year in range(2008, 2025)}
    
    che_tax_fuel_scope = {year: che_tax_fuel_I for year in range(2008, 2025)}
    
    ## Sources dictionary
    
    che_tax_scope_sources = {year: "gvt(CH[2005], CH[2009])" for year in range(2008, 2014)}
    che_tax_scope_sources.update({year: "gvt(CH[2005], CH[2009])" for year in range(2014, 2025)})

    #----------------------------------------------------------------------------

    # California-Quebec-Ontario
    
    ## Jurisdictions
    
    usa_ca_ets_jur_I = ["California"]
    usa_ca_ets_jur_II = ["California", "Quebec"]
    usa_ca_ets_jur_III = ["California", "Quebec", "Ontario"]
    
    ## IPCC categories
    
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
    
    usa_ca_ets_jur_scope = {2013:usa_ca_ets_jur_I, 2014:usa_ca_ets_jur_I, 
                           2015:usa_ca_ets_jur_II, 2016:usa_ca_ets_jur_II, 
                           2017:usa_ca_ets_jur_II, 2018:usa_ca_ets_jur_III, 
                           2019:usa_ca_ets_jur_II, 2020:usa_ca_ets_jur_II, 
                           2021:usa_ca_ets_jur_II, 2022:usa_ca_ets_jur_II, 
                           2023:usa_ca_ets_jur_II, 2024:usa_ca_ets_jur_II}
    
    usa_ca_ets_ipcc_scope = {year: usa_ca_ets_ipcc_I for year in range(2013, 2015)}
    usa_ca_ets_ipcc_scope.update({year: usa_ca_ets_ipcc_II for year in range(2015, 2025)})

    ## Sources dictionary
    
    usa_ca_ets_scope_sources = {year: "leg(CA-AB32[2006]), gvt(CARB-FRO[2011])" for year in range(2012, 2025)}
    
    #----------------------------------------------------------------------------
    
    # Chongqing Municipality
    
    ## Jurisdiction
    
    chn_cq_ets_jur_I = ["Chongqing Municipality"]
    
    ## Sectors
    
    chn_cq_ets_ipcc_I = ["1A1A1", "1A2A", "2A1", "2B5", "2C1", "2C2", "2C3"]
    
    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_cq_ets_ipcc_II = ["1A2A", "2A1", "2B5", "2C1", "2C2", "2C3"]
    
    ## scope dictionaries
    chn_cq_ets_jur_scope = {2014:chn_cq_ets_jur_I,
                           2015:chn_cq_ets_jur_I, 2016:chn_cq_ets_jur_I,
                           2017:chn_cq_ets_jur_I, 2018:chn_cq_ets_jur_I,
                           2019:chn_cq_ets_jur_I, 2020:chn_cq_ets_jur_I,
                           2021:chn_cq_ets_jur_I, 2022:chn_cq_ets_jur_I,
                           2023:chn_cq_ets_jur_I, 2024:chn_cq_ets_jur_I}
    
    chn_cq_ets_ipcc_scope = {2014:chn_cq_ets_ipcc_I,
                            2015:chn_cq_ets_ipcc_I, 2016:chn_cq_ets_ipcc_I,
                            2017:chn_cq_ets_ipcc_I, 2018:chn_cq_ets_ipcc_I,
                            2019:chn_cq_ets_ipcc_I, 2020:chn_cq_ets_ipcc_I,
                            2021:chn_cq_ets_ipcc_II, 2022:chn_cq_ets_ipcc_II,
                            2023:chn_cq_ets_ipcc_II, 2024:chn_cq_ets_ipcc_II}

    ## Sources dictionary
    
    chn_cq_ets_scope_sources = {2014:"report(ICAP[2021])",
                                   2015:"report(ICAP[2021])", 2016:"report(ICAP[2021])", 
                                   2017:"report(ICAP[2021])", 2018:"report(ICAP[2021])", 
                                   2019:"report(ICAP[2021])",
                                   2020:"report(ICAP[2021])", 2021:"report(ICAP[2021])"}
    
    #----------------------------------------------------------------------------
    
    # Alberta
    
    ## Jurisdiction
    
    can_ab_ets_jur_I = ["Alberta"]

    ## IPCC categories

    # SGER (2007-2017)   
    can_ab_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A2C", "1A2E", "1A4C1", "1B1A", 
                         "1B1A1", "1B1A11", "1B1A12", "1B1A13", "1B1A14", "1B1A2", 
                         "1B1A21", "1B1A22", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                         "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36", 
                         "2A1", "2A2", "2A3", "2A4", "2A4A", "2A4B", "2A4C", "2A4D", 
                         "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2H2", 
                         "4A", "4A1", "4A2"]

    # CCIR (2018-2019)   
    can_ab_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                          "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                          "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "1B1A", "1B1A1", 
                          "1B1A11", "1B1A12", "1B1A13", "1B1A14", "1B1A2", "1B1A21", 
                          "1B1A22", "1B1B", "1B2", "1B2A", "1B2A1", "1B2A2", "1B2A3", 
                          "1B2A31", "1B2A32", "1B2A33", "1B2A34", "1B2A35", "1B2A36", 
                          "1B2B", "1B2B1", "1B2B2", "1B2B3", "1B2B31", "1B2B32", 
                          "1B2B33", "1B2B34", "1B2B35", "1B2B36", "1B3", "2A1", 
                          "2A2", "2A3", "2A4", "2A4A", "2A4B", "2A4C", "2A4D", 
                          "2B", "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", 
                          "2B7", "2B8", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", 
                          "2B8F", "2B9", "2B9A", "2B9B", "2C1", "2C2", "2C3", 
                          "2C4", "2C5", "2C6", "2C7", "2D1", "2D2", "2D3", "2D4", 
                          "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", 
                          "2G2", "2G3", "2G4", "2H1", "2H2", "2H3", "3C1", "4A", 
                          "4A1", "4A2", "4A3", "4B", "4C", "4C1", "4C2", "4D", 
                          "4D1", "4D2", "4E"]

    # TIER (2020-2022)   
    can_ab_ets_ipcc_III = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", 
                           "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                           "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "1B1A", 
                           "1B1A1", "1B1A11", "1B1A12", "1B1A13", "1B1A14", "1B1A2", 
                           "1B1A21", "1B1A22", "1B1B", "1B2", "1B2A", "1B2A1", 
                           "1B2A2", "1B2A3", "1B2A31", "1B2A32", "1B2A33", "1B2A34", 
                           "1B2A35", "1B2A36", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                           "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36", 
                           "1B3", "2A1", "2A2", "2A3", "2A4", "2A4A", "2A4B", "2A4C", 
                           "2A4D", "2B", "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", 
                           "2B6", "2B7", "2B8", "2B8A", "2B8B", "2B8C", "2B8D", 
                           "2B8E", "2B8F", "2B9", "2B9A", "2B9B", "2C1", "2C2", 
                           "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2", "2D3",
                           "2D4", "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", 
                           "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3", "3C1",
                           "3C2", "3C3", "3C4", "3C5", "3C6", "3C7", "3C8", "4A", 
                           "4A1", "4A2", "4A3", "4D", "4D1", "4D2"]  
    
    ## scope dictionaries
    can_ab_ets_jur_scope = {year: can_ab_ets_jur_I for year in range(2007, 2023)}
    
    can_ab_ets_ipcc_scope = {year: can_ab_ets_ipcc_I for year in range(2007, 2018)}
    can_ab_ets_ipcc_scope.update({year: can_ab_ets_ipcc_II for year in range(2018, 2020)})
    can_ab_ets_ipcc_scope.update({year: can_ab_ets_ipcc_III for year in range(2020, 2025)})
    
    ## Sources dictionary
    
    can_ab_ets_scope_sources = {year: "gvt(SGER[2009], SGER[2019])" for year in range(2007, 2018)}
    can_ab_ets_scope_sources.update({year: "gvt(ALBGOV[2019])" for year in range(2018, 2020)})
    can_ab_ets_scope_sources.update({year: "gvt(ABGOV[2021], ABGOV[2021b])" for year in range(2020, 2023)})
    can_ab_ets_scope_sources.update({year: "db(WBCPD[2024])" for year in range(2023, 2025)}) 

    #----------------------------------------------------------------------------
    
    # Nova Scotia
    
    ## Jurisdiction
    
    can_ns_ets_jur_I = ["Nova Scotia"]

    ## Sectors

    # Provincial OBPS for industrial emitters and federal OBPS for electricity  
    # and transmission sectors
    can_ns_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "1B2A", "1B2A1", 
                         "1B2A2", "1B2A3", "1B2A31", "1B2A32", "1B2A33", "1B2A34", 
                         "1B2A35", "1B2A36", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                         "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36"]
    
    ## scope dictionaries
    can_ns_ets_jur_scope = {2019:can_ns_ets_jur_I, 2020:can_ns_ets_jur_I,
                            2021:can_ns_ets_jur_I, 2022:can_ns_ets_jur_I,
                            2023:can_ns_ets_jur_I, 2024:can_ns_ets_jur_I}
    
    can_ns_ets_ipcc_scope = {2019:can_ns_ets_ipcc_I, 2020:can_ns_ets_ipcc_I,
                             2021:can_ns_ets_ipcc_I, 2022:can_ns_ets_ipcc_I,
                             2023:can_ns_ets_ipcc_I, 2024:can_ns_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_ns_ets_scope_sources = {2019:"gvt(ECCC[2021])", 2020:"gvt(ECCC[2021])",
                                   2021:"gvt(ECCC[2021])"}     


    
    #------------------------------All schemes dictionaries--------------------------------#
    
    ets_scope = {"che_ets":{"jurisdictions":che_ets_jur_scope, 
                            "sectors":che_ets_ipcc_scope},
                 "kor_ets":{"jurisdictions":kor_ets_jur_scope, 
                            "sectors":kor_ets_ipcc_scope},
                 "nzl_ets":{"jurisdictions":nzl_ets_jur_scope, 
                            "sectors":nzl_ets_ipcc_scope},
                 "can_ab_ets":{"jurisdictions":can_ab_ets_jur_scope,
                               "sectors":can_ab_ets_ipcc_scope},
                 "can_ns_ets":{"jurisdictions":can_ns_ets_jur_scope, 
                               "sectors":can_ns_ets_ipcc_scope},
                 "chn_cq_ets":{"jurisdictions":chn_cq_ets_jur_scope, 
                                "sectors":chn_cq_ets_ipcc_scope},
                 "usa_ca_ets":{"jurisdictions":usa_ca_ets_jur_scope, 
                                "sectors":usa_ca_ets_ipcc_scope}}

    ets_scope_sources = {"che_ets":che_ets_scope_sources,
                         "kor_ets":kor_ets_scope_sources,
                         "nzl_ets":nzl_ets_scope_sources,
                         "can_ab_ets":can_ab_ets_scope_sources,
                         "can_ns_ets":can_ns_ets_scope_sources,
                         "usa_ca_ets":usa_ca_ets_scope_sources,
                         "chn_cq_ets":chn_cq_ets_scope_sources}
    
    data_and_sources = {"data":ets_scope, "sources":ets_scope_sources}
    
    return data_and_sources


