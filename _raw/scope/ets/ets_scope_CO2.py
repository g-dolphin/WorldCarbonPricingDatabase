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
    eu_ets_ctry_I = ["Austria", "Belgium", "Cyprus", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                     "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                     "Netherlands", "Poland", "Portugal", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # Bulgaria an Romania join the EU - and the EU ETS (2007)
    eu_ets_ctry_II = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                     "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                     "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # EEA countries (Iceland, Norway, Liechtenstein) join the EU ETS (2008)
    eu_ets_ctry_III = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                     "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                     "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom", "Norway", "Iceland", "Liechtenstein"]
    
    # Croatia joins the EU - and the EU ETS (2013)
    eu_ets_ctry_IV = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
                     "Ireland", "Italy", "Latvia", "Lithuania", "Liechtenstein", "Luxembourg", "Malta", 
                     "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # The United Kingdom leaves the European Union - and the EU ETS (2021)
    eu_ets_ctry_V = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
                     "Ireland", "Italy", "Latvia", "Lithuania", "Liechtenstein", "Luxembourg", "Malta", 
                     "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden"]
    
    
    ## Sectors
    
    # initial sectoral coverage 
    eu_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                     "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                     "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", 
                     "2A1", "2A2", "2A3", "2A4A", 
                     "2B1", "2B2", "2B3", 
                     "2B4", "2B5", "2B6", "2B7", "2B8F", 
                     "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1"]
    
    # extension to domestic aviation and other industrial (processes) emissions (2012)
    eu_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                     "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                     "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                     "1C1A", "1C2B",
                     "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", 
                     "2B4", "2B5", "2B6", "2B7", "2B8F",
                     "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1"]
    
    
    ## Coverage dictionaries
    
    eu_ets_jur_coverage = {2005:eu_ets_ctry_I, 2006:eu_ets_ctry_I,
                            2007:eu_ets_ctry_II, 2008:eu_ets_ctry_II,
                            2009:eu_ets_ctry_III, 2010:eu_ets_ctry_III,
                            2011:eu_ets_ctry_III, 2012:eu_ets_ctry_III,
                            2013:eu_ets_ctry_IV, 2014:eu_ets_ctry_IV,
                            2015:eu_ets_ctry_IV, 2016:eu_ets_ctry_IV,
                            2017:eu_ets_ctry_IV, 2018:eu_ets_ctry_IV,
                            2019:eu_ets_ctry_IV, 2020:eu_ets_ctry_IV,
                            2021:eu_ets_ctry_V}
    
    eu_ets_ipcc_coverage = {2005:eu_ets_ipcc_I, 2006:eu_ets_ipcc_I,
                            2007:eu_ets_ipcc_I, 2008:eu_ets_ipcc_I,
                            2009:eu_ets_ipcc_I, 2010:eu_ets_ipcc_I,
                            2011:eu_ets_ipcc_I, 2012:eu_ets_ipcc_II,
                            2013:eu_ets_ipcc_II, 2014:eu_ets_ipcc_II,
                            2015:eu_ets_ipcc_II, 2016:eu_ets_ipcc_II,
                            2017:eu_ets_ipcc_II, 2018:eu_ets_ipcc_II,
                            2019:eu_ets_ipcc_II, 2020:eu_ets_ipcc_II,
                            2021:eu_ets_ipcc_II}
    
    
    ## Sources dictionary
    
    eu_ets_coverage_sources = {2005:"leg(EC[2003])", 2006:"leg(EC[2003])", 
                               2007:"leg(EC[2003])", 2008:"leg(EC[2003])", 
                               2009:"leg(EC[2003])", 2010:"leg(EC[2003])", 
                               2011:"leg(EC[2003])", 2012:"leg(EC[2014])", 
                               2013:"leg(EC[2014])", 2014:"leg(EC[2014])",
                               2015:"leg(EC[2014])", 2016:"leg(EC[2014])", 
                               2017:"leg(EC[2014])", 2018:"leg(EC[2018])", 
                               2019:"leg(EC[2018])", 2020:"leg(EC[2018], EC[2020])", 
                               2021:"leg(EC[2018], EC[2020])"}
    
    #------------------------------------------------------------------------
    
    # Regional Greenhouse Gas Initiative
    
    ## Jurisdictions
    # initial state coverage (2009)
    rggi_jur_I = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", 
                  "New Hampshire", "New Jersey", "New York", "Rhode Island", "Vermont"]
    
    # New Jersey withdrawal (2012)
    rggi_jur_II = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", 
                   "New Hampshire", "New York", "Rhode Island", "Vermont"]
    
    # Virginia joins the scheme (2021)
    rggi_jur_III = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", 
                    "New Hampshire", "New Jersey", "New York", "Rhode Island", "Vermont",
                    "Virginia"]
    
    ## Sectors
    
    # coverage of the RGGI scheme is limited to IPCC sector 1A1A
    rggi_ipcc_I = ["1A1A1", "1A1A2", "1A1A3"]
    
    ## Coverage dictionaries
    rggi_jur_coverage = { 2009:rggi_jur_I, 2010:rggi_jur_I,
                            2011:rggi_jur_I, 2012:rggi_jur_II,
                            2013:rggi_jur_II, 2014:rggi_jur_II,
                            2015:rggi_jur_II, 2016:rggi_jur_II,
                            2017:rggi_jur_II, 2018:rggi_jur_I,
                            2019:rggi_jur_I, 2020:rggi_jur_I,
                            2021:rggi_jur_III}
    
    rggi_ipcc_coverage = { 2009:rggi_ipcc_I, 2010:rggi_ipcc_I,
                            2011:rggi_ipcc_I, 2012:rggi_ipcc_I,
                            2013:rggi_ipcc_I, 2014:rggi_ipcc_I,
                            2015:rggi_ipcc_I, 2016:rggi_ipcc_I,
                            2017:rggi_ipcc_I, 2018:rggi_ipcc_I,
                            2019:rggi_ipcc_I, 2020:rggi_ipcc_I,
                            2021:rggi_ipcc_I}
    
    ## Sources dictionary
    
    us_rggi_coverage_sources = {2009:"gvt(RGGI-MOU[2005])", 2010:"gvt(RGGI-MOU[2005])", 
                                2011:"gvt(RGGI-MOU[2005])", 2012:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2013:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2014:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2015:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2016:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2017:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2018:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2019:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2020:"gvt(RGGI-MOU[2005], NJ[2011])", 
                                2021:"gvt(RGGI-MOU[2005], NJ[2011])"}
    
    #----------------------------------------------------------------------------
    
    # California-Quebec-Ontario
    
    ## Jurisdictions
    
    us_ca_cat_jur_I = ["California"]
    us_ca_cat_jur_II = ["California", "Quebec"]
    us_ca_cat_jur_III = ["California", "Quebec", "Ontario"]
    
    ## Sectors
    
    us_ca_cat_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                        "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",
                        "1A2L", "1A2M", "1A5A", "1C1A", "1C1B",
                        "2A1", "2A2", "2A3", "2C1", "2C5", "2H1",  
                        "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                        "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                        "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                        "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                        "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                        "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    us_ca_cat_ipcc_II = ["1A1A1", "1A1A2", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                         "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",
                         "1A2L", "1A2M", "1A3B", "1A4A", "1A4B", "1A5A", "1C1A", "1C1B",
                         "2A1", "2A2", "2A3", "2C1", "2C5", "2H1",  
                         "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                         "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                         "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                         "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                         "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                         "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    
    ## Coverage dictionaries
    
    us_ca_cat_jur_coverage = {2013:us_ca_cat_jur_I, 2014:us_ca_cat_jur_I, 
                           2015:us_ca_cat_jur_II, 2016:us_ca_cat_jur_II, 
                           2017:us_ca_cat_jur_II, 2018:us_ca_cat_jur_III, 
                           2019:us_ca_cat_jur_II, 2020:us_ca_cat_jur_II, 
                           2021:us_ca_cat_jur_II}
    
    us_ca_cat_ipcc_coverage = {2013:us_ca_cat_ipcc_I, 2014:us_ca_cat_ipcc_I, 
                           2015:us_ca_cat_ipcc_II, 2016:us_ca_cat_ipcc_II, 
                           2017:us_ca_cat_ipcc_II, 2018:us_ca_cat_ipcc_II, 
                           2019:us_ca_cat_ipcc_II, 2020:us_ca_cat_ipcc_II, 
                           2021:us_ca_cat_ipcc_II}

    ## Sources dictionary
    
    us_ca_cat_coverage_sources = {2012:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2013:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2014:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2015:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2016:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2017:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2018:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2019:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2020:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])", 
                                  2021:"leg(CA-AB32[2006]), gvt(CARB-FRO[2011])"}

    #----------------------------------------------------------------------------
    
    # Quebec
    
    ## Jurisdiction
    can_qc_cat_jur_I = ["Quebec"]
    
    
    ## Sectors
    can_qc_cat_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "2A1", "2A2", "2A3", 
                         "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                         "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                         "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                         "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                         "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                         "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## Coverage dictionaries
    
    can_qc_cat_jur_coverage = {2013:can_qc_cat_jur_I, 2014:can_qc_cat_jur_I}
    
    can_qc_cat_ipcc_coverage = {2013:can_qc_cat_ipcc_I, 2014:can_qc_cat_ipcc_I}
    
    ## Sources dictionary
    
    can_qc_cat_coverage_sources = {2013:"leg(QC[2011], QC[2012], QC[2013])", 
                                   2014:"leg(QC[2011], QC[2012], QC[2013])"}
    
    #----------------------------------------------------------------------------
    
    # Massachusetts (ETS)
    
    ## Jurisdiction
    us_ma_ets_jur_I = ["Massachusetts"]
    
    
    ## Sectors
    us_ma_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3"]
    
    ## Coverage dictionaries
    
    us_ma_ets_jur_coverage = {2018:us_ma_ets_jur_I, 2019:us_ma_ets_jur_I,
                              2020:us_ma_ets_jur_I, 2021:us_ma_ets_jur_I}
    
    us_ma_ets_ipcc_coverage = {2018:us_ma_ets_ipcc_I, 2019:us_ma_ets_ipcc_I,
                               2020:us_ma_ets_ipcc_I, 2021:us_ma_ets_ipcc_I}
    
    ## Sources dictionary
    
    us_ma_ets_coverage_sources = {2018:"leg(MA[2017])", 2019:"leg(MA[2017])", 
                                  2020:"leg(MA[2017])", 2021:"leg(MA[2017])"}
    
    #----------------------------------------------------------------------------
    
    # Mexico (ETS)
    
    ## Jurisdiction
    mex_ets_jur_I = ["Mexico"]
    
    
    ## Sectors
    mex_ets_ipcc_I = ["1A1A1", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C", "1A2D",
                      "1A2E", "1A2G", "1A2I",  "1B1A11", "1B1A12", "1B1A13", 
                      "1B1A14", "1B1A21", "1B1A22", "1B1B", "1B2A1", "1B2A2", 
                      "1B2A31", "1B2A32", "1B2A33", "1B2A34", "1B2A35", "1B2A36", 
                      "1B2B1", "1B2B2", "1B2B31", "1B2B32", "1B2B33", "1B2B34", 
                      "1B2B35", "1B2B36", "2A1", "2A2", "2A3", "2B1", "2B10", 
                      "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                      "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                      "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2H1", "2H2"]
    
    ## Coverage dictionaries
    
    mex_ets_jur_coverage = {2021:mex_ets_jur_I}
    
    mex_ets_ipcc_coverage = {2021:mex_ets_ipcc_I}
    
    ## Sources dictionary
    
    mex_ets_coverage_sources = {2021:"leg(MX[2019])"}

    #----------------------------------------------------------------------------
    
    # New Zealand
    
    ## Jurisdiction
    
    nzl_ets_jur_I = ["New Zealand"]
    
    ## Sectors
    
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
    

    ## Sources dictionary
    
    nzl_ets_coverage_sources = {2008:"leg(NZ-CCR[2008])", 2009:"leg(NZ-CCR[2008])",
                               2010:"leg(NZ-CCR[2008])", 2011:"leg(NZ-CCR[2011])", 
                               2012:"leg(NZ-CCR[2011])", 2013:"leg(NZ-CCR[2013])", 
                               2014:"leg(NZ-CCR[2013])", 2015:"leg(NZ-CCR[2013])", 
                               2016:"leg(NZ-CCR[2013])", 2017:"leg(NZ-CCR[2013])", 
                               2018:"leg(NZ-CCR[2013])", 2019:"leg(NZ-CCR[2013])",
                               2020:"leg(NZ-CCR[2020])", 2021:"leg(NZ-CCR[2020])"}

    #----------------------------------------------------------------------------
    
    # Switzerland
    
    ## Jurisdiction
    
    che_ets_jur_I = ["Switzerland"]
    
    ## Sectors (source: CO2 Ordinance)
    che_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                      "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                      "1A2J", "1A2K", "1A2L", "1A2M",
                      "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", "2B4",
                      "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F",
                      "2C1", "2C2", "2C3", "2C4", 
                      "2C5", "2C6", "2C7", "2H1"]
    
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
    
    ## Sources dictionary
    
    che_ets_coverage_sources = {2008:"gvt(CH[2009])", 2009:"gvt(CH[2009])",
                               2010:"gvt(CH[2009])", 2011:"gvt(CH[2009])", 
                               2012:"gvt(CH[2009])", 
                               2013:"leg(CHE-CO2[2012],CHE-FARC[2013])", 
                               2014:"leg(CHE-CO2[2012],CHE-FARC[2013])",
                               2015:"leg(CHE-CO2[2012],CHE-FARC[2013])", 
                               2016:"leg(CHE-CO2[2012],CHE-FARC[2013])", 
                               2017:"leg(CHE-CO2[2012],CHE-FARC[2013])", 
                               2018:"leg(CHE-CO2[2012],CHE-FARC[2013])", 
                               2019:"leg(CHE-CO2[2012],CHE-FARC[2013])",
                               2020:"leg(CHE-CO2[2012],CHE-FARC[2013])", 
                               2021:"leg(CHE-CO2[2020],CHE-FARC[2013])"}
    
    #----------------------------------------------------------------------------
    
    # Kazakhstan
    
    ## Jurisdiction
    
    kaz_ets_jur_I = ["Kazakhstan"]
    
    ## Sectors
    
    # initial scope (2013-2015)
    kaz_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A2A", "1A2B", "1A2C", 
                      "1B2A1", "1B2A2", "1B2A31", "1B2A32", "1B2A33", "1B2A34", 
                      "1B2A35", "1B2A36", "1B2B1", "1B2B2", "1B2B31", "1B2B32", 
                      "1B2B33", "1B2B34", "1B2B35", "1B2B36", "2B1", "2B10", 
                      "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                      "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                      "2C2", "2C3", "2C4", "2C5", "2C6", "2C7"]

    # the scheme was suspended between 2016-2017
    kaz_ets_ipcc_II = []

    # coverage extension in phase three (2018-2021)
    kaz_ets_ipcc_III = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A2A", "1A2B", "1A2C", 
                          "1B2A1", "1B2A2", "1B2A31", "1B2A32", "1B2A33", "1B2A34", 
                          "1B2A35", "1B2A36", "1B2B1", "1B2B2", "1B2B31", "1B2B32", 
                          "1B2B33", "1B2B34", "1B2B35", "1B2B36", "2A1", "2A2", "2B1", 
                          "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", 
                          "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", 
                          "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7"]
    
    ## Coverage dictionaries
    kaz_ets_jur_coverage = {2013:kaz_ets_jur_I, 2014:kaz_ets_jur_I,
                            2015:kaz_ets_jur_I, 2016:kaz_ets_jur_I,
                            2017:kaz_ets_jur_I, 2018:kaz_ets_jur_I,
                            2019:kaz_ets_jur_I, 2020:kaz_ets_jur_I,
                            2021:kaz_ets_jur_I}
    
    kaz_ets_ipcc_coverage = {2013:kaz_ets_ipcc_I, 2014:kaz_ets_ipcc_I,
                             2015:kaz_ets_ipcc_I, 2016:kaz_ets_ipcc_II,
                             2017:kaz_ets_ipcc_II, 2018:kaz_ets_ipcc_III,
                             2019:kaz_ets_ipcc_III, 2020:kaz_ets_ipcc_III,
                             2021:kaz_ets_ipcc_III}
    
    ## Sources dictionary
    
    kaz_ets_coverage_sources = {2013:"leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2014:"leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2015:"leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2016:"", 2017:"", 
                                2018:"leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2019:"leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])",
                                2020:"leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2021:"leg(KZ[2021]), gvt(KZ[2021]), report(ICAP - KZ[2021])"}

    #----------------------------------------------------------------------------
    
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
    
    ## Coverage dictionaries
    kor_ets_jur_coverage = {2015:kor_ets_jur_I, 2016:kor_ets_jur_I,
                            2017:kor_ets_jur_I, 2018:kor_ets_jur_I,
                            2019:kor_ets_jur_I, 2020:kor_ets_jur_I,
                            2021:kor_ets_jur_I}
    
    kor_ets_ipcc_coverage = {2015:kor_ets_ipcc_I, 2016:kor_ets_ipcc_I,
                            2017:kor_ets_ipcc_I, 2018:kor_ets_ipcc_II,
                            2019:kor_ets_ipcc_II, 2020:kor_ets_ipcc_II,
                            2021:kor_ets_ipcc_III}
    
    ## Sources dictionary
    
    kor_ets_coverage_sources = {2015:"leg(KR[2012], KR[2013])", 
                                2016:"leg(KR[2012], KR[2013])", 
                                2017:"leg(KR[2017])", 2018:"leg(KR[2018])", 
                                2019:"leg(KR[2018])",
                                2020:"leg(KR[2020])", 2021:"leg(KR[2020])"}

    #----------------------------------------------------------------------------
    
    # Beijing Municipality
    
    ## Jurisdiction
    
    chn_bj_ets_jur_I = ["Beijing Municipality"]
    
    ## Sectors
    
    chn_bj_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D",  
                         "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",  
                         "1A2L", "1A2M", "2A1","2B8A", "2B8B", "2B8C", "2B8D", 
                         "2B8E", "4D1", "4D2"]
    
    ## Coverage dictionaries
    chn_bj_ets_jur_coverage = {2013:chn_bj_ets_jur_I, 2014:chn_bj_ets_jur_I,
                           2015:chn_bj_ets_jur_I, 2016:chn_bj_ets_jur_I,
                           2017:chn_bj_ets_jur_I, 2018:chn_bj_ets_jur_I,
                           2019:chn_bj_ets_jur_I, 2020:chn_bj_ets_jur_I,
                           2021:chn_bj_ets_jur_I}
    
    chn_bj_ets_ipcc_coverage = {2013:chn_bj_ets_ipcc_I, 2014:chn_bj_ets_ipcc_I,
                            2015:chn_bj_ets_ipcc_I, 2016:chn_bj_ets_ipcc_I,
                            2017:chn_bj_ets_ipcc_I, 2018:chn_bj_ets_ipcc_I,
                            2019:chn_bj_ets_ipcc_I, 2020:chn_bj_ets_ipcc_I,
                            2021:chn_bj_ets_ipcc_I}
    
    ## Sources dictionary
    
    chn_bj_ets_coverage_sources = {2013:"gvt(BJ[2020]), report(ICAP[2021])", 
                                   2014:"gvt(BJ[2020]), report(ICAP[2021])",
                                   2015:"gvt(BJ[2020]), report(ICAP[2021])", 
                                   2016:"gvt(BJ[2020]), report(ICAP[2021])",
                                   2017:"gvt(BJ[2020]), report(ICAP[2021])", 
                                   2018:"gvt(BJ[2020]), report(ICAP[2021])", 
                                   2019:"gvt(BJ[2020]), report(ICAP[2021])", 
                                   2020:"gvt(BJ[2020]), report(ICAP[2021])", 
                                   2021:"gvt(BJ[2020]), report(ICAP[2021])"}
    

    #----------------------------------------------------------------------------
    
    # Chongqing Municipality
    
    ## Jurisdiction
    
    chn_cq_ets_jur_I = ["Chongqing Municipality"]
    
    ## Sectors
    
    chn_cq_ets_ipcc_I = ["1A1A1", "1A2A", "2A1", "2B5", "2C1", "2C2", "2C3"]
    
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

    ## Sources dictionary
    
    chn_cq_ets_coverage_sources = {2014:"report(ICAP[2021])",
                                   2015:"report(ICAP[2021])", 2016:"report(ICAP[2021])", 
                                   2017:"report(ICAP[2021])", 2018:"report(ICAP[2021])", 
                                   2019:"report(ICAP[2021])",
                                   2020:"report(ICAP[2021])", 2021:"report(ICAP[2021])"}
    

    #----------------------------------------------------------------------------
    
    # Fujian Province
    
    ## Jurisdiction
    
    chn_fj_ets_jur_I = ["Fujian Province"]
    
    ## Sectors
    
    chn_fj_ets_ipcc_I = ["1A1A1", "1A2A", "1A2B", "1A2D", "1A2K", "1A3A2", "2A4A", 
                     "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", 
                     "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", 
                     "2B9B", "2C1", "2C3", "2C4", "2C5","2C6", "2C7", "2H1"]
    
    ## Coverage dictionaries
    chn_fj_ets_jur_coverage = {2016:chn_fj_ets_jur_I,
                           2017:chn_fj_ets_jur_I, 2018:chn_fj_ets_jur_I,
                           2019:chn_fj_ets_jur_I, 2020:chn_fj_ets_jur_I,
                           2021:chn_fj_ets_jur_I}
    
    chn_fj_ets_ipcc_coverage = {2016:chn_fj_ets_ipcc_I,
                            2017:chn_fj_ets_ipcc_I, 2018:chn_fj_ets_ipcc_I,
                            2019:chn_fj_ets_ipcc_I, 2020:chn_fj_ets_ipcc_I,
                            2021:chn_fj_ets_ipcc_I}    
    
    ## Sources dictionary
    
    chn_fj_ets_coverage_sources = {2016:"web(FJ[2018]), report(ICAP[2021])", 
                                   2017:"web(FJ[2018]), report(ICAP[2021])", 
                                   2018:"web(FJ[2018]), report(ICAP[2021])", 
                                   2019:"web(FJ[2018]), report(ICAP[2021])",
                                   2020:"web(FJ[2018]), report(ICAP[2021])", 
                                   2021:"web(FJ[2018]), report(ICAP[2021])"}
    

    #----------------------------------------------------------------------------
    
    # Guangdong Province
    
    ## Jurisdiction
    
    chn_gd_ets_jur_I = ["Guangdong Province"]
    
    ## Sectors
    
    # initial scope (2013-2015)
    chn_gd_ets_ipcc_I = ["1A1A1", "1A2A", "2A1", "2B8A", "2B8B", "2B8C", "2B8D", 
                     "2B8E", "2C1"]

    # extension to papermaking and domestic aviation (2016)
    chn_gd_ets_ipcc_II = ["1A1A1", "1A2A", "1A2D", "1A3A2", "2A1", "2B8A", 
                      "2B8B", "2B8C", "2B8D", "2B8E", "2C1", "2H1"]
    
    ## Coverage dictionaries
    chn_gd_ets_jur_coverage = {2013:chn_gd_ets_jur_I, 2014:chn_gd_ets_jur_I,
                           2015:chn_gd_ets_jur_I, 2016:chn_gd_ets_jur_I,
                           2017:chn_gd_ets_jur_I, 2018:chn_gd_ets_jur_I,
                           2019:chn_gd_ets_jur_I, 2020:chn_gd_ets_jur_I,
                           2021:chn_gd_ets_jur_I}
    
    chn_gd_ets_ipcc_coverage = {2013:chn_gd_ets_ipcc_I, 2014:chn_gd_ets_ipcc_I,
                            2015:chn_gd_ets_ipcc_I, 2016:chn_gd_ets_ipcc_II,
                            2017:chn_gd_ets_ipcc_II, 2018:chn_gd_ets_ipcc_II,
                            2019:chn_gd_ets_ipcc_II, 2020:chn_gd_ets_ipcc_II,
                            2021:chn_gd_ets_ipcc_II}  

    ## Sources dictionary
    
    chn_gd_ets_coverage_sources = {2013:"report(ICAP[2021])", 
                                   2014:"report(ICAP[2021])",
                                   2015:"report(ICAP[2021])", 
                                   2016:"report(ICAP[2021])", 
                                   2017:"report(ICAP[2021])", 
                                   2018:"report(ICAP[2021])", 
                                   2019:"report(ICAP[2021])",
                                   2020:"report(ICAP[2021])", 
                                   2021:"report(ICAP[2021])"}


    #----------------------------------------------------------------------------
    
    # Hubei Province
    
    ## Jurisdiction
    
    chn_hb_ets_jur_I = ["Hubei Province"]
    
    ## Sectors
    
    # initial scope (2014-2015)
    chn_hb_ets_ipcc_I = ["1A1A1", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2G", 
                     "1A2L", "2A1", "2A3", "2B1", "2B10", "2B2", "2B3", "2B4", 
                     "2B5", "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", 
                     "2B8F", "2B9A", "2B9B", "2C1", "2C3", "2C4", "2C5", "2C6", 
                     "2C7", "2G1", "2H1", "2H2"]

    # extension to new sectors over the threshold (2016)
    chn_hb_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D", 
                      "1A2E", "1A2G", "1A2L", "2A1", "2A3", "2A4A", "2B1", "2B10", 
                      "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                      "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                      "2C3", "2C4", "2C5", "2C6", "2C7", "2G1", "2H1", "2H2"]
    
    ## Coverage dictionaries
    chn_hb_ets_jur_coverage = {2014:chn_hb_ets_jur_I,
                           2015:chn_hb_ets_jur_I, 2016:chn_hb_ets_jur_I,
                           2017:chn_hb_ets_jur_I, 2018:chn_hb_ets_jur_I,
                           2019:chn_hb_ets_jur_I, 2020:chn_hb_ets_jur_I,
                           2021:chn_hb_ets_jur_I}
    
    chn_hb_ets_ipcc_coverage = {2014:chn_hb_ets_ipcc_I,
                            2015:chn_hb_ets_ipcc_I, 2016:chn_hb_ets_ipcc_II,
                            2017:chn_hb_ets_ipcc_II, 2018:chn_hb_ets_ipcc_II,
                            2019:chn_hb_ets_ipcc_II, 2020:chn_hb_ets_ipcc_II,
                            2021:chn_hb_ets_ipcc_II}  

    ## Sources dictionary
    
    chn_hb_ets_coverage_sources = {2014:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])",
                                   2015:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2016:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2017:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2018:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2019:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])",
                                   2020:"leg(HB[2020]), report(ICAP[2021])", 
                                   2021:"leg(HB[2020]), report(ICAP[2021])"}
    

    #----------------------------------------------------------------------------
    
    # Shanghai Municipality
    
    ## Jurisdiction
    
    chn_sh_ets_jur_I = ["Shanghai Municipality"]
    
    ## Sectors
    
    # initial scope (2013-2015)
    chn_sh_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D", 
                         "1A2K", "1A2L", "1A3A2", "1A3C", "1A4A", "2B1", "2B10", "2B2", 
                         "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", "2B8C", 
                         "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C3", "2C4", 
                         "2C5", "2C6", "2C7", "2H1"]

    # extension to the shipping sector (2016)
    chn_sh_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D", 
                         "1A2K", "1A2L", "1A3A2", "1A3C", "1A3D2", "1A4A", "2B1", 
                         "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", 
                         "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                         "2C3", "2C4", "2C5", "2C6", "2C7", "2H1"]
    
    ## Coverage dictionaries
    chn_sh_ets_jur_coverage = {2013:chn_sh_ets_jur_I, 2014:chn_sh_ets_jur_I,
                           2015:chn_sh_ets_jur_I, 2016:chn_sh_ets_jur_I,
                           2017:chn_sh_ets_jur_I, 2018:chn_sh_ets_jur_I,
                           2019:chn_sh_ets_jur_I, 2020:chn_sh_ets_jur_I,
                           2021:chn_sh_ets_jur_I}
    
    chn_sh_ets_ipcc_coverage = {2013:chn_sh_ets_jur_I, 2014:chn_sh_ets_ipcc_I,
                            2015:chn_sh_ets_ipcc_I, 2016:chn_sh_ets_ipcc_II,
                            2017:chn_sh_ets_ipcc_II, 2018:chn_sh_ets_ipcc_II,
                            2019:chn_sh_ets_ipcc_II, 2020:chn_sh_ets_ipcc_II,
                            2021:chn_sh_ets_ipcc_II}  

    ## Sources dictionary
    
    chn_sh_ets_coverage_sources = {2013:"report(ICAP[2021])", 2014:"report(ICAP[2021])",
                                   2015:"report(ICAP[2021])", 2016:"report(ICAP[2021])", 
                                   2017:"report(ICAP[2021])", 2018:"report(ICAP[2021])", 
                                   2019:"report(ICAP[2021])", 2020:"report(ICAP[2021])", 
                                   2021:"report(ICAP[2021])"}
    
    #----------------------------------------------------------------------------
    
    # Shenzhen
    
    ## Jurisdiction
    
    chn_sz_ets_jur_I = ["Shenzhen"]
    
    ## Sectors
    
    chn_sz_ets_ipcc_I = ["1A1A1", "1A1A2", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", 
                         "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", 
                         "1A2M", "1A3B", "1A3D2", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                         "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36"]
    
    ## Coverage dictionaries
    chn_sz_ets_jur_coverage = {2013:chn_sz_ets_jur_I, 2014:chn_sz_ets_jur_I,
                           2015:chn_sz_ets_jur_I, 2016:chn_sz_ets_jur_I,
                           2017:chn_sz_ets_jur_I, 2018:chn_sz_ets_jur_I,
                           2019:chn_sz_ets_jur_I, 2020:chn_sz_ets_jur_I,
                           2021:chn_sz_ets_jur_I}
    
    chn_sz_ets_ipcc_coverage = {2013:chn_sz_ets_ipcc_I, 2014:chn_sz_ets_ipcc_I,
                            2015:chn_sz_ets_ipcc_I, 2016:chn_sz_ets_ipcc_I,
                            2017:chn_sz_ets_ipcc_I, 2018:chn_sz_ets_ipcc_I,
                            2019:chn_sz_ets_ipcc_I, 2020:chn_sz_ets_ipcc_I,
                            2021:chn_sz_ets_ipcc_I}

    ## Sources dictionary
    
    chn_sz_ets_coverage_sources = {2013:"report(ICAP[2021])", 2014:"report(ICAP[2021])",
                                   2015:"report(ICAP[2021])", 2016:"report(ICAP[2021])", 
                                   2017:"report(ICAP[2021])", 2018:"report(ICAP[2021])", 
                                   2019:"report(ICAP[2021])", 2020:"report(ICAP[2021])", 
                                   2021:"report(ICAP[2021])"}


    #----------------------------------------------------------------------------
    
    # Tianjin Municipality
    
    ## Jurisdiction
    
    chn_tj_ets_jur_I = ["Tianjin Municipality"]
    
    ## Sectors
    
    # initial scope (2013-2018)
    chn_tj_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2C", "1B2A31", "1B2B31", 
                         "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", 
                         "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1"]

    # extension to papermaking, aviation, and building materials (2019)
    chn_tj_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2C", "1A2D", "1A2K", 
                          "1A3A2", "1B2A31", "1B2B31", "2B1", "2B10", "2B2", "2B3", 
                          "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", 
                          "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2H1"]
    
    ## Coverage dictionaries
    chn_tj_ets_jur_coverage = {2013:chn_tj_ets_jur_I, 2014:chn_tj_ets_jur_I,
                               2015:chn_tj_ets_jur_I, 2016:chn_tj_ets_jur_I,
                               2017:chn_tj_ets_jur_I, 2018:chn_tj_ets_jur_I,
                               2019:chn_tj_ets_jur_I, 2020:chn_tj_ets_jur_I,
                               2021:chn_tj_ets_jur_I}
    
    chn_tj_ets_ipcc_coverage = {2013:chn_tj_ets_jur_I, 2014:chn_tj_ets_ipcc_I,
                            2015:chn_tj_ets_ipcc_I, 2016:chn_tj_ets_ipcc_I,
                            2017:chn_tj_ets_ipcc_I, 2018:chn_tj_ets_ipcc_I,
                            2019:chn_tj_ets_ipcc_II, 2020:chn_tj_ets_ipcc_II,
                            2021:chn_tj_ets_ipcc_II}     
    
    ## Sources dictionary
    
    chn_tj_ets_coverage_sources = {2013:"report(ICAP[2021])", 2014:"report(ICAP[2021])",
                                   2015:"report(ICAP[2021])", 2016:"report(ICAP[2021])", 
                                   2017:"report(ICAP[2021])", 2018:"report(ICAP[2021])", 
                                   2019:"report(ICAP[2021])", 2020:"report(ICAP[2021])", 
                                   2021:"report(ICAP[2021])"}


    #----------------------------------------------------------------------------
    
    # Canada Federal OBPS
    
    ## Jurisdiction
    
    # initial province coverage (2019-2020)
    can_obps_jur_I = ["Manitoba", "Ontario", "New Brunswick", "Prince Edward Island", "Yukon", "Nunavut"]

    # New Brunswick transitions to its provincial OBPS (2021)
    can_obps_jur_II = ["Manitoba", "Ontario", "Prince Edward Island", "Yukon", "Nunavut"]

    ## Sectors
    
    can_obps_ipcc_I = ["1A1A1", "1A1A2", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", 
                       "1A2F", "1A2I", "1B1", "1B1A", "1B1A1", "1B1A11", "1B1A12", 
                       "1B1A13", "1B1A14", "1B1A2", "1B1A21", "1B1A22", "1B1B", 
                       "1B2", "1B2A", "1B2A1", "1B2A2", "1B2A3", "1B2A31", "1B2A32", 
                       "1B2A33", "1B2A34", "1B2A35", "1B2A36", "1B2B", "1B2B1", 
                       "1B2B2", "1B2B3", "1B2B31", "1B2B32", "1B2B33", "1B2B34", 
                       "1B2B35", "1B2B36", "2A1", "2A2", "2A3", "2A4", "2A4A", 
                       "2A4B", "2A4C", "2A4D", "2B", "2B1", "2B10", "2B2", "2B3", 
                       "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", "2B8C", 
                       "2B8D", "2B8E", "2B8F", "2B9", "2B9A", "2B9B", "2C1", "2C2", 
                       "2C3", "2C4", "2C5", "2C6", "2C7", "2H1", "2H2"]
    
    ## Coverage dictionaries
    can_obps_jur_coverage = {2019:can_obps_jur_I, 2020:can_obps_jur_I,
                             2021:can_obps_jur_II}
    
    can_obps_ipcc_coverage = {2019:can_obps_ipcc_I, 2020:can_obps_ipcc_I,
                              2021:can_obps_ipcc_I}     
    
    ## Sources dictionary
    
    can_obps_coverage_sources = {2019:"leg(SOR[2019])",
                                 2020:"leg(SOR[2019])", 2021:"leg(SOR[2019])"}


    #----------------------------------------------------------------------------
    
    # Alberta
    
    ## Jurisdiction
    
    can_ab_ets_jur_I = ["Alberta"]

    ## Sectors

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

    # TIER (2020-2021)   
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
    
    ## Coverage dictionaries
    can_ab_ets_jur_coverage = {2007:can_ab_ets_jur_I, 2008:can_ab_ets_jur_I,
                               2009:can_ab_ets_jur_I, 2010:can_ab_ets_jur_I,
                               2011:can_ab_ets_jur_I, 2012:can_ab_ets_jur_I,
                               2013:can_ab_ets_jur_I, 2014:can_ab_ets_jur_I,
                               2015:can_ab_ets_jur_I, 2016:can_ab_ets_jur_I,
                               2017:can_ab_ets_jur_I, 2018:can_ab_ets_jur_I,
                               2019:can_ab_ets_jur_I, 2020:can_ab_ets_jur_I,
                               2021:can_ab_ets_jur_I}
    
    can_ab_ets_ipcc_coverage = {2007:can_ab_ets_ipcc_I, 2008:can_ab_ets_ipcc_I,
                                2009:can_ab_ets_ipcc_I, 2010:can_ab_ets_ipcc_I,
                                2011:can_ab_ets_ipcc_I, 2012:can_ab_ets_ipcc_I,
                                2013:can_ab_ets_ipcc_I, 2014:can_ab_ets_ipcc_I,
                                2015:can_ab_ets_ipcc_I, 2016:can_ab_ets_ipcc_I,
                                2017:can_ab_ets_ipcc_I, 2018:can_ab_ets_ipcc_II,
                                2019:can_ab_ets_ipcc_II, 2020:can_ab_ets_ipcc_III,
                                2021:can_ab_ets_ipcc_III}     
    
    ## Sources dictionary
    
    can_ab_ets_coverage_sources = {2007:"gvt(SGER[2009], SGER[2019])", 
                                   2008:"gvt(SGER[2009], SGER[2019])",
                                   2009:"gvt(SGER[2009], SGER[2019])", 
                                   2010:"gvt(SGER[2009], SGER[2019])",
                                   2011:"gvt(SGER[2009], SGER[2019])", 
                                   2012:"gvt(SGER[2009], SGER[2019])",
                                   2013:"gvt(SGER[2009], SGER[2019])", 
                                   2014:"gvt(SGER[2009], SGER[2019])",
                                   2015:"gvt(SGER[2009], SGER[2019])", 
                                   2016:"gvt(SGER[2009], SGER[2019])",
                                   2017:"gvt(SGER[2009], SGER[2019])", 
                                   2018:"gvt(ALBGOV[2019])",
                                   2019:"gvt(ALBGOV[2019])", 
                                   2020:"gvt(ABGOV[2021], ABGOV[2021b])",
                                   2021:"gvt(ABGOV[2021], ABGOV[2021b])"}    


    #----------------------------------------------------------------------------
    
    # Saskatchewan
    # Saskatchewan is coded as a stand alone scheme encompassing the Federal OBPS
    # and the provincial OBPS because the existing  structure does not allow to 
    # account for differences in sectoral coverage between jurisdictions
    
    ## Jurisdiction
    
    can_sk_ets_jur_I = ["Saskatchewan"]

    ## Sectors

    # Provincial OBPS for industrial emitters and federal OBPS for electricity  
    # and transmission sectors
    can_sk_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "1B1A", "1B1A1", 
                         "1B1A11", "1B1A12", "1B1A13", "1B1A14", "1B1A2", "1B1A21", 
                         "1B1A22", "1B1B", "1B2", "1B2A", "1B2A1", "1B2A2", "1B2A3", 
                         "1B2A31", "1B2A32", "1B2A33", "1B2A34", "1B2A35", "1B2A36", 
                         "1B2B", "1B2B1", "1B2B2", "1B2B3", "1B2B31", "1B2B32", 
                         "1B2B33", "1B2B34", "1B2B35", "1B2B36", "2A1", "2A2", 
                         "2A3", "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B", "2B1", 
                         "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", 
                         "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9", 
                         "2B9A", "2B9B", "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", 
                         "2C7", "2H1", "2H2", "4A", "4A1", "4A2", "4A3", "4D", 
                         "4D1", "4D2"]
    
    ## Coverage dictionaries
    can_sk_ets_jur_coverage = {2019:can_sk_ets_jur_I, 2020:can_sk_ets_jur_I,
                               2021:can_sk_ets_jur_I}
    
    can_sk_ets_ipcc_coverage = {2019:can_sk_ets_ipcc_I, 2020:can_sk_ets_ipcc_I,
                                2021:can_sk_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_sk_ets_coverage_sources = {2019:"leg(SOR[2019]), gvt(ECCC[2021], SASK[2019])", 
                                   2020:"leg(SOR[2019]), gvt(ECCC[2021], SASK[2019])",
                                   2021:"leg(SOR[2019]), gvt(ECCC[2021], SASK[2019])"}    


    #----------------------------------------------------------------------------
    
    # New Brunswick
    
    ## Jurisdiction
    
    can_nb_ets_jur_I = ["New Brunswick"]

    ## Sectors 

    # Provincial OBPS (2021)
    can_nb_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A2B", "1A2D", "1A2E", 
                         "1A2J", "2A2", "2H1", "2H2", "3D1"]
    
    ## Coverage dictionaries
    can_nb_ets_jur_coverage = {2021:can_nb_ets_jur_I}
    
    can_nb_ets_ipcc_coverage = {2021:can_nb_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_nb_ets_coverage_sources = {2021:"gvt(ECCC[2021])"}    


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
    
    ## Coverage dictionaries
    can_ns_ets_jur_coverage = {2019:can_ns_ets_jur_I, 2020:can_ns_ets_jur_I,
                               2021:can_ns_ets_jur_I}
    
    can_ns_ets_ipcc_coverage = {2019:can_ns_ets_ipcc_I, 2020:can_ns_ets_ipcc_I,
                                2021:can_ns_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_ns_ets_coverage_sources = {2019:"gvt(ECCC[2021])", 2020:"gvt(ECCC[2021])",
                                   2021:"gvt(ECCC[2021])"}     


    #----------------------------------------------------------------------------
    
    # Newfoundland and Labrador
    
    ## Jurisdiction
    
    can_nl_ets_jur_I = ["Newfoundland and Labrador"]

    ## Sectors

    # Provincial OBPS for industrial emitters and federal OBPS for electricity  
    # and transmission sectors
    can_nl_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A2A", "1A2B", "1A2D", 
                         "1A2I", "1B1A", "1B1A1", "1B1A11", "1B1A12", "1B1A13", 
                         "1B1A14", "1B1A2", "1B1A21", "1B1A22", "1B2A34", "2C1", 
                         "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2H1"]
    
    ## Coverage dictionaries
    can_nl_ets_jur_coverage = {2019:can_nl_ets_jur_I, 2020:can_nl_ets_jur_I,
                               2021:can_nl_ets_jur_I}
    
    can_nl_ets_ipcc_coverage = {2019:can_nl_ets_ipcc_I, 2020:can_nl_ets_ipcc_I,
                                2021:can_nl_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_nl_ets_coverage_sources = {2019:"gvt(NL[2019])", 2020:"gvt(NL[2019])",
                                   2021:"gvt(NL[2019])"}  

    
    #------------------------------All schemes dictionaries--------------------------------#
    
    ets_coverage = {"eu_ets":{"jurisdictions":eu_ets_jur_coverage, 
                                  "sectors":eu_ets_ipcc_coverage}, 
                    "us_rggi":{"jurisdictions":rggi_jur_coverage, 
                              "sectors":rggi_ipcc_coverage}, 
                    "us_ca_cat":{"jurisdictions":us_ca_cat_jur_coverage, 
                              "sectors":us_ca_cat_ipcc_coverage}, 
                    "us_ma_ets":{"jurisdictions":us_ma_ets_jur_coverage, 
                              "sectors":us_ma_ets_ipcc_coverage}, 
                    "can_qc_cat":{"jurisdictions":can_qc_cat_jur_coverage, 
                              "sectors":can_qc_cat_ipcc_coverage}, 
                    "che_ets":{"jurisdictions":che_ets_jur_coverage, 
                              "sectors":che_ets_ipcc_coverage}, 
                    "kaz_ets":{"jurisdictions":kaz_ets_jur_coverage, 
                              "sectors":kaz_ets_ipcc_coverage},
                    "kor_ets":{"jurisdictions":kor_ets_jur_coverage, 
                              "sectors":kor_ets_ipcc_coverage},
                    "mex_ets":{"jurisdictions":mex_ets_jur_coverage, 
                              "sectors":mex_ets_ipcc_coverage},                        
                    "nzl_ets":{"jurisdictions":nzl_ets_jur_coverage, 
                              "sectors":nzl_ets_ipcc_coverage}, 
                    "chn_bj_ets":{"jurisdictions":chn_bj_ets_jur_coverage, 
                              "sectors":chn_bj_ets_ipcc_coverage},
                    "chn_cq_ets":{"jurisdictions":chn_cq_ets_jur_coverage, 
                              "sectors":chn_cq_ets_ipcc_coverage},
                    "chn_fj_ets":{"jurisdictions":chn_fj_ets_jur_coverage, 
                              "sectors":chn_fj_ets_ipcc_coverage},
                    "chn_gd_ets":{"jurisdictions":chn_gd_ets_jur_coverage, 
                              "sectors":chn_gd_ets_ipcc_coverage},
                    "chn_hb_ets":{"jurisdictions":chn_hb_ets_jur_coverage, 
                              "sectors":chn_hb_ets_ipcc_coverage},
                    "chn_sh_ets":{"jurisdictions":chn_sh_ets_jur_coverage, 
                              "sectors":chn_sh_ets_ipcc_coverage},
                    "chn_sz_ets":{"jurisdictions":chn_sz_ets_jur_coverage, 
                              "sectors":chn_sz_ets_ipcc_coverage},
                    "chn_tj_ets":{"jurisdictions":chn_tj_ets_jur_coverage, 
                              "sectors":chn_tj_ets_ipcc_coverage},
                    "can_obps":{"jurisdictions":can_obps_jur_coverage, 
                              "sectors":can_obps_ipcc_coverage},
                    "can_ab_ets":{"jurisdictions":can_ab_ets_jur_coverage, 
                              "sectors":can_ab_ets_ipcc_coverage},
                    "can_sk_ets":{"jurisdictions":can_sk_ets_jur_coverage, 
                              "sectors":can_sk_ets_ipcc_coverage},
                    "can_nb_ets":{"jurisdictions":can_nb_ets_jur_coverage, 
                              "sectors":can_nb_ets_ipcc_coverage},
                    "can_ns_ets":{"jurisdictions":can_ns_ets_jur_coverage, 
                              "sectors":can_ns_ets_ipcc_coverage},
                    "can_nl_ets":{"jurisdictions":can_nl_ets_jur_coverage, 
                              "sectors":can_nl_ets_ipcc_coverage}}

    ets_coverage_sources = {"eu_ets":eu_ets_coverage_sources,
                            "us_rggi":us_rggi_coverage_sources,
                            "us_ca_cat":us_ca_cat_coverage_sources,
                            "us_ma_ets":us_ma_ets_coverage_sources,
                            "can_qc_cat":can_qc_cat_coverage_sources,
                            "che_ets":che_ets_coverage_sources,
                            "kaz_ets":kaz_ets_coverage_sources,
                            "kor_ets":kor_ets_coverage_sources,
                            "mex_ets":mex_ets_coverage_sources,
                            "nzl_ets":nzl_ets_coverage_sources,
                            "chn_bj_ets":chn_bj_ets_coverage_sources,
                            "chn_cq_ets":chn_cq_ets_coverage_sources,
                            "chn_fj_ets":chn_fj_ets_coverage_sources,
                            "chn_gd_ets":chn_gd_ets_coverage_sources,
                            "chn_hb_ets":chn_hb_ets_coverage_sources,
                            "chn_sh_ets":chn_sh_ets_coverage_sources,
                            "chn_sz_ets":chn_sz_ets_coverage_sources,
                            "chn_tj_ets":chn_tj_ets_coverage_sources,
                            "can_obps":can_obps_coverage_sources,
                            "can_ab_ets":can_ab_ets_coverage_sources,
                            "can_sk_ets":can_sk_ets_coverage_sources,
                            "can_nb_ets":can_nb_ets_coverage_sources,
                            "can_ns_ets":can_ns_ets_coverage_sources,
                            "can_nl_ets":can_nl_ets_coverage_sources}
    
    data_and_sources = {"data":ets_coverage, "sources":ets_coverage_sources}
    
    return data_and_sources


