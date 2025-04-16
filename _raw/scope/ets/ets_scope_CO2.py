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
    
    # European Union ETS (eu_ets)
    
    ## Jurisdictions
    
    # initial country scope (2005)
    eu_ets_jur_I = ["Austria", "Belgium", "Cyprus", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                     "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                     "Netherlands", "Poland", "Portugal", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # Bulgaria an Romania join the EU - and the EU ETS (2007)
    eu_ets_jur_II = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                     "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                     "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # EEA countries (Iceland, Norway, Liechtenstein) join the EU ETS (2008)
    eu_ets_jur_III = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", 
                     "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", 
                     "Netherlands", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom", "Norway", "Iceland", "Liechtenstein"]
    
    # Croatia joins the EU - and the EU ETS (2013)
    eu_ets_jur_IV = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
                     "Ireland", "Italy", "Latvia", "Lithuania", "Liechtenstein", "Luxembourg", "Malta", 
                     "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden", "United Kingdom"]
    
    # The United Kingdom leaves the European Union - and the EU ETS (2021)
    eu_ets_jur_V = ["Austria", "Belgium", "Bulgaria", "Cyprus", "Croatia", "Czech Republic", "Denmark", 
                     "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
                     "Ireland", "Italy", "Latvia", "Lithuania", "Liechtenstein", "Luxembourg", "Malta", 
                     "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Slovak Republic", 
                     "Slovenia", "Spain", "Sweden"]
    
    
    ## IPCC categories
    
    # initial sectoral scope 
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
    
    # extension to maritime transport emissions (2024)
    eu_ets_ipcc_III = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                       "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                       "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                       "1A3D1", "1A3D2",
                       "1C1A", "1C2B",
                       "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", 
                       "2B4", "2B5", "2B6", "2B7", "2B8F",
                       "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1"]
    
    
    ## scope dictionaries
    
    eu_ets_jur_scope = {year: eu_ets_jur_I for year in range(2005, 2007)}
    eu_ets_jur_scope.update({year: eu_ets_jur_II for year in range(2007, 2008)})
    eu_ets_jur_scope.update({year: eu_ets_jur_III for year in range(2008, 2013)})
    eu_ets_jur_scope.update({year: eu_ets_jur_IV for year in range(2013, 2021)})
    eu_ets_jur_scope.update({year: eu_ets_jur_V for year in range(2021, 2023)})
    
    eu_ets_ipcc_scope = {year: eu_ets_ipcc_I for year in range(2005, 2012)}
    eu_ets_ipcc_scope.update({year: eu_ets_ipcc_II for year in range(2012, 2024)})    
    eu_ets_ipcc_scope[2024] = eu_ets_ipcc_III

    ## Sources dictionary
    
    eu_ets_scope_sources = {2005:"leg(EC[2003])", 2006:"leg(EC[2003])", 
                               2007:"leg(EC[2003])", 2008:"leg(EC[2003])", 
                               2009:"leg(EC[2003])", 2010:"leg(EC[2003])", 
                               2011:"leg(EC[2003])", 2012:"leg(EC[2014])", 
                               2013:"leg(EC[2014])", 2014:"leg(EC[2014])",
                               2015:"leg(EC[2014])", 2016:"leg(EC[2014])", 
                               2017:"leg(EC[2014])", 2018:"leg(EC[2018])", 
                               2019:"leg(EC[2018])", 2020:"leg(EC[2018], EC[2020])", 
                               2021:"leg(EC[2018], EC[2020])", 2022:" ",
                               2023:" ", 2024:" "}

    #----------------------------------------------------------------------------

    # AUT-Austrian ETS (aut_ets)

    # Jurisdiction
    aut_ets_jur_I = ["Austria"]

    # IPCC categories - covering categories not covered by the EU ETS
    aut_ets_ipcc_I = ["1A3B", "1A3C", "1A3D2", "1A3E1",  
                      "1A4A", "1A4B", "1A4C1", "1A4C2", "1A4C3",
                      "1A5A", "1A5B"]

    ## scope dictionaries
    
    aut_ets_jur_scope = {year:aut_ets_jur_I for year in range(2022,2025)}
    
    aut_ets_ipcc_scope = {year:aut_ets_jur_I for year in range(2022,2025)}
    
    ## Sources dictionary
    
    aut_ets_scope_sources = {2021:"gvt(DEU-UBA[2021])", 2022:"gvt(DEU-UBA[2021])",
                             2023: " ", 2024: " "}

    #----------------------------------------------------------------------------
    
    # CAN-Federal OBPS (can_ets)
    
    ## Jurisdiction
    
    # initial province scope (2019-2020)
    can_obps_jur_I = ["Manitoba", "Ontario", "New Brunswick", "Prince Edward Island", "Yukon", "Nunavut"]

    # New Brunswick transitions to its provincial OBPS (2021)
    can_obps_jur_II = ["Manitoba", "Ontario", "Prince Edward Island", "Yukon", "Nunavut"]

    # Ontario transitions to its provincial OBPS (2022)
    can_obps_jur_III = ["Manitoba", "Prince Edward Island", "Yukon", "Nunavut"]

    ## IPCC categories
    
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
    
    ## scope dictionaries
    can_obps_jur_scope = {2019:can_obps_jur_I, 2020:can_obps_jur_I,
                             2021:can_obps_jur_II, 2022:can_obps_jur_III,
                             2023:can_obps_jur_III, 2024:can_obps_jur_III}
    
    can_obps_ipcc_scope = {year:can_obps_ipcc_I for year in range(2019, 2025)}
    
    ## Sources dictionary
    
    can_obps_scope_sources = {2019:"leg(SOR[2019])",
                              2020:"leg(SOR[2019])", 2021:"leg(SOR[2019])",
                              2022:"leg(SOR[2019])", 2023: " ",
                              2024: " "}

    #----------------------------------------------------------------------------
    
    # China national ETS (chn_ets)

    ## Jurisdiction
    
    chn_ets_jur_I = ["China"]
    
    ## IPCC categories
    
    chn_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3"]
    
    ## scope dictionaries
    chn_ets_jur_scope = {year: chn_ets_jur_I for year in range(2021, 2025)}

    chn_ets_ipcc_scope = {year: chn_ets_ipcc_I for year in range(2021, 2025)}
    
    ## Sources dictionary
    
    chn_ets_scope_sources = {2021: "gvt(BJ[2020]), report(ICAP[2021])",
                             2022: "report(ICAP[2023])",
                             2023: " ",
                             2024: " "}

    #----------------------------------------------------------------------------

    # DEU-German ETS (deu_ets)

    # Jurisdiction
    deu_ets_jur_I = ["Germany"]

    # IPCC categories - covering categories not covered by the EU ETS
    deu_ets_ipcc_I = ["1A3B", "1A3C", "1A3D2", "1A3E1",  
                      "1A4A", "1A4B", "1A4C1", "1A4C2", "1A4C3",
                      "1A5A", "1A5B"]

    ## scope dictionaries
    
    deu_ets_jur_scope = {2021:deu_ets_jur_I, 2022:deu_ets_jur_I}
    
    deu_ets_ipcc_scope = {2021:deu_ets_ipcc_I, 2022:deu_ets_jur_I}
    
    ## Sources dictionary
    
    deu_ets_scope_sources = {2021:"gvt(DEU-UBA[2021])", 2022:"gvt(DEU-UBA[2021])",
                             2023: " ", 2024:" "}

    #----------------------------------------------------------------------------
    
    # Mexico ETS (mex_ets)
    
    ## Jurisdiction
    mex_ets_jur_I = ["Mexico"]
    
    
    ## IPCC categories
    mex_ets_ipcc_I = ["1A1A1", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C", "1A2D",
                      "1A2E", "1A2G", "1A2I",  "1B1A11", "1B1A12", "1B1A13", 
                      "1B1A14", "1B1A21", "1B1A22", "1B1B", "1B2A1", "1B2A2", 
                      "1B2A31", "1B2A32", "1B2A33", "1B2A34", "1B2A35", "1B2A36", 
                      "1B2B1", "1B2B2", "1B2B31", "1B2B32", "1B2B33", "1B2B34", 
                      "1B2B35", "1B2B36", "2A1", "2A2", "2A3", "2B1", "2B10", 
                      "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                      "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                      "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2H1", "2H2"]
    
    ## scope dictionaries
    
    mex_ets_jur_scope = {2021:mex_ets_jur_I,
                         2022:mex_ets_jur_I}
    
    mex_ets_ipcc_scope = {2021:mex_ets_ipcc_I,
                          2022:mex_ets_ipcc_I}
    
    ## Sources dictionary
    
    mex_ets_scope_sources = {2021:"leg(MX[2019])",
                             2022:"report(ICAP[2023])",
                             2023: " ",
                             2024: " "}

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
    
    che_ets_jur_I = ["Switzerland"]
    
    ## IPCC categories (source: CO2 Ordinance)
    che_ets_ipcc_I = ["1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                      "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                      "1A2J", "1A2K", "1A2L", "1A2M",
                      "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", "2B4",
                      "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F",
                      "2C1", "2C2", "2C3", "2C4", 
                      "2C5", "2C6", "2C7", "2H1"]

    che_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                      "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                      "1A2J", "1A2K", "1A2L", "1A2M",
                      "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", "2B4",
                      "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F",
                      "2C1", "2C2", "2C3", "2C4", 
                      "2C5", "2C6", "2C7", "2H1"]
    
    ## scope dictionaries
    che_ets_jur_scope = {year: che_ets_jur_I for year in range(2008, 2025)}
    
    che_ets_ipcc_scope = {year: che_ets_ipcc_I for year in range(2008, 2020)}
    che_ets_ipcc_scope.update({year: che_ets_ipcc_II for year in range(2020, 2025)})
    
    ## Sources dictionary
    
    che_ets_scope_sources = {year:"gvt(CH[2009])" for year in range(2008, 2013)}
    che_ets_scope_sources.update({year:"gvt(CH[2009])" for year in range(2013, 2022)})
    che_ets_scope_sources.update({year:" " for year in range(2022, 2025)})
    
    #----------------------------------------------------------------------------

    # IDN-Indonesia ETS (idn_ets)

    # Jurisdiction
    idn_ets_jur_I = ["Indonesia"]

    # IPCC categories - covering categories not covered by the EU ETS
    idn_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3"]

    ## scope dictionaries
    
    idn_ets_jur_scope = {year: idn_ets_jur_I for year in range(2023, 2025)}
    
    idn_ets_ipcc_scope = {year: idn_ets_ipcc_I for year in range(2023, 2025)}
    
    ## Sources dictionary
    
    idn_ets_scope_sources = {2023:" ", 2024:" "}

    #----------------------------------------------------------------------------
    
    # Kazakhstan
    
    ## Jurisdiction
    
    kaz_ets_jur_I = ["Kazakhstan"]
    
    ## IPCC categories
    
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

    # scope extension in phase three (2018-2021)
    kaz_ets_ipcc_III = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A2A", "1A2B", "1A2C", 
                          "1B2A1", "1B2A2", "1B2A31", "1B2A32", "1B2A33", "1B2A34", 
                          "1B2A35", "1B2A36", "1B2B1", "1B2B2", "1B2B31", "1B2B32", 
                          "1B2B33", "1B2B34", "1B2B35", "1B2B36", "2A1", "2A2", "2B1", 
                          "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", 
                          "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", 
                          "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2C7"]
    
    ## scope dictionaries
    kaz_ets_jur_scope = {year: kaz_ets_jur_I for year in range(2013, 2025)}
    
    kaz_ets_ipcc_scope = {year: kaz_ets_ipcc_I for year in range(2013, 2016)}
    kaz_ets_ipcc_scope.update({year: kaz_ets_ipcc_II for year in range(2016, 2018)})
    kaz_ets_ipcc_scope.update({year: kaz_ets_ipcc_III for year in range(2018, 2025)})
    
    ## Sources dictionary
    
    kaz_ets_scope_sources = {2013: "leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2014: "leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2015: "leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2016: "", 2017: "", 
                                2018: "leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2019: "leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])",
                                2020: "leg(KZ[2007]), gvt(KZ[2021]), report(ICAP - KZ[2021])", 
                                2021: "leg(KZ[2021]), gvt(KZ[2021]), report(ICAP - KZ[2021])",
                                2022: "report(ICAP[2023])",
                                2023: " ",
                                2024: " "}

    #----------------------------------------------------------------------------
    
    # Korea, Rep.
    
    ## Jurisdiction
    
    kor_ets_jur_I = ["Korea, Rep."]
    
    ## IPCC categories
    
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
    kor_ets_jur_scope = {year: kor_ets_jur_I for year in range(2015, 2025)}
    
    kor_ets_ipcc_scope = {year: kor_ets_ipcc_I for year in range(2015, 2018)}
    kor_ets_ipcc_scope.update({year: kor_ets_ipcc_II for year in range(2018, 2021)})
    kor_ets_ipcc_scope.update({year: kor_ets_ipcc_III for year in range(2021, 2025)})
    
    ## Sources dictionary
    
    kor_ets_scope_sources = {2015: "leg(KR[2012], KR[2013])", 
                             2016: "leg(KR[2012], KR[2013])", 
                             2017: "leg(KR[2017])", 2018:"leg(KR[2018])", 
                             2019: "leg(KR[2018])",
                             2020: "leg(KR[2020])", 2021:"leg(KR[2020])",
                             2022: "report(ICAP[2023])",
                             2023: "",
                             2024: ""}

    #----------------------------------------------------------------------------
    # Montenegro

    mne_ets_jur_I = ["Montenegro"]

    mne_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                      "1A2B", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                      "2A1", "2A2", "2A3", "2A4A", 
                      "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1"]

    mne_ets_jur_scope = {year: mne_ets_jur_I for year in range(2020, 2025)}
    
    mne_ets_ipcc_scope = {year: mne_ets_ipcc_I for year in range(2020, 2025)}

    ## Sources dictionary
    
    mne_ets_scope_sources = {2020: "report(ICAP[2023])", 2021:"report(ICAP[2023])",
                             2022: "report(ICAP[2023])",
                             2023: " ",
                             2024: " "}

    #----------------------------------------------------------------------------
    # United Kingdom
    
    ## Jurisdictions
    
    gbr_ets_jur_I = ["United Kingdom"]
 
    
    ## IPCC categories
    
    gbr_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                      "1C1A", "1C2B",
                      "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", 
                      "2B4", "2B5", "2B6", "2B7", "2B8F",
                      "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1"]
    
    
    ## scope dictionaries
    
    gbr_ets_jur_scope = {year: gbr_ets_jur_I for year in range(2021, 2025)}
    
    gbr_ets_ipcc_scope = {year: gbr_ets_ipcc_I for year in range(2021, 2025)}
    
    ## Sources dictionary
    
    gbr_ets_scope_sources = {year: "leg(UK-SI[2020])" for year in range(2021, 2025)}

    #------------------------------------------------------------------------
    # USA-Regional Greenhouse Gas Initiative
    
    ## Jurisdictions
    # initial state scope (2009)
    usa_rggi_jur_I = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", 
                       "New Hampshire", "New Jersey", "New York", "Rhode Island", "Vermont"]
    
    # New Jersey withdrawal (2012)
    usa_rggi_jur_II = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", 
                       "New Hampshire", "New York", "Rhode Island", "Vermont"]
    
    ## IPCC categories
    
    # scope of the RGGI scheme is limited to IPCC sector 1A1A
    usa_rggi_ipcc_I = ["1A1A1", "1A1A2", "1A1A3"]
    
    ## scope dictionaries
    usa_rggi_jur_scope = {year: usa_rggi_jur_I for year in range(2009, 2012)}
    usa_rggi_jur_scope.update({year: usa_rggi_jur_II for year in range(2012, 2018)})
    usa_rggi_jur_scope.update({year: usa_rggi_jur_I for year in range(2018, 2025)})
    
    usa_rggi_ipcc_scope = {year: usa_rggi_ipcc_I for year in range(2009, 2025)}
    
    ## Sources dictionary
    
    usa_rggi_scope_sources = {year:"gvt(RGGI-MOU[2005])" for year in range(2009, 2012)}
    usa_rggi_scope_sources.update({year: "gvt(RGGI-MOU[2005], NJ[2011])" for year in range(2012, 2018)})
    usa_rggi_scope_sources.update({year: " " for year in range(2018, 2025)})
    
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
    # USA-Oregon 

    usa_or_ets_jur_I = ["Oregon"]

    usa_or_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                         "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",
                         "1A2L", "1A2M", "1A3B", "1A4A", "1A4B", "1A5A"]

    usa_or_ets_jur_scope = {year: usa_or_ets_jur_I for year in range(2022, 2025)}

    
    usa_or_ets_ipcc_scope = {year: usa_or_ets_ipcc_I for year in range(2022, 2025)}

    ## Sources dictionary
    
    usa_or_ets_scope_sources = {year: "report(ICAP[2023])" for year in range(2022, 2025)}


    #----------------------------------------------------------------------------
    # USA-Massachusetts
    
    ## Jurisdiction
    usa_ma_ets_jur_I = ["Massachusetts"]
    
    
    ## IPCC categories
    usa_ma_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3"]
    
    ## scope dictionaries
    
    usa_ma_ets_jur_scope = {year: usa_ma_ets_jur_I for year in range(2018, 2025)}
    
    usa_ma_ets_ipcc_scope = {year: usa_ma_ets_ipcc_I for year in range(2018, 2025)}
    
    ## Sources dictionary
    
    usa_ma_ets_scope_sources = {year: "leg(MA[2017])" for year in range(2018, 2025)}

    #------------------------------------------------------------------------
    # USA-Washington

    usa_wa_ets_jur_I = ["Washington"]

    usa_wa_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                         "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",
                         "1A2L", "1A2M", "1A5A", "1C1A", "1C1B",
                         "2A1", "2A2", "2A3", "2C1", "2C5", "2H1",  
                         "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                         "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                         "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                         "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                         "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                         "2G3", "2G4", "2H1", "2H2", "2H3"]

    usa_wa_ets_jur_scope = {2023:usa_wa_ets_jur_I, 2024:usa_wa_ets_jur_I}
    
    usa_wa_ets_ipcc_scope = {2023:usa_wa_ets_ipcc_I, 2024:usa_wa_ets_ipcc_I}

    ## Sources dictionary
    
    usa_wa_ets_scope_sources = {2023:"report(ICAP[2023])",
                                2024: " "}

    #------------------------------------------------------------------------
    
    # Beijing Municipality
    
    ## Jurisdiction
    
    chn_bj_ets_jur_I = ["Beijing Municipality"]
    
    ## IPCC categories
    
    chn_bj_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D",  
                         "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",  
                         "1A2L", "1A2M", "2A1","2B8A", "2B8B", "2B8C", "2B8D", 
                         "2B8E", "4D1", "4D2"]

    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_bj_ets_ipcc_II = ["1A2A", "1A2B", "1A2C", "1A2D",  
                          "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K",  
                          "1A2L", "1A2M", "2A1","2B8A", "2B8B", "2B8C", "2B8D", 
                          "2B8E", "4D1", "4D2"]
    
    ## scope dictionaries
    chn_bj_ets_jur_scope = {year: chn_bj_ets_jur_I for year in range(2013, 2023)}
    
    chn_bj_ets_ipcc_scope = {year: chn_bj_ets_ipcc_I for year in range(2013, 2021)}
    chn_bj_ets_ipcc_scope.update({year: chn_bj_ets_ipcc_II for year in range(2021, 2023)})
    
    ## Sources dictionary
    
    chn_bj_ets_scope_sources = {year: "gvt(BJ[2020]), report(ICAP[2021])" for year in range(2013, 2022)}
    chn_bj_ets_scope_sources[2022] = "report(ICAP[2023])"

    #----------------------------------------------------------------------------
    
    # Chongqing Municipality
    
    ## Jurisdiction
    
    chn_cq_ets_jur_I = ["Chongqing Municipality"]
    
    ## IPCC categories

    chn_cq_ets_ipcc_I = ["1A1A1", "1A2A", "2A1", "2B5", "2C1", "2C2", "2C3"]
    
    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_cq_ets_ipcc_II = ["1A2A", "2A1", "2B5", "2C1", "2C2", "2C3"]

    ## scope dictionaries
    chn_cq_ets_jur_scope = {year: chn_cq_ets_jur_I for year in range(2014, 2023)}
    
    chn_cq_ets_ipcc_scope = {year: chn_cq_ets_ipcc_I for year in range(2014, 2021)}
    chn_cq_ets_ipcc_scope.update({year: chn_cq_ets_ipcc_II for year in range(2021, 2023)})

    ## Sources dictionary
    
    chn_cq_ets_scope_sources = {2014:"report(ICAP[2021])",
                                2015:"report(ICAP[2021])", 2016:"report(ICAP[2021])", 
                                2017:"report(ICAP[2021])", 2018:"report(ICAP[2021])", 
                                2019:"report(ICAP[2021])",
                                2020:"report(ICAP[2021])", 2021:"report(ICAP[2021])",
                                2022:"report(ICAP[2023])"}
    

    #----------------------------------------------------------------------------
    
    # Fujian Province
    
    ## Jurisdiction
    
    chn_fj_ets_jur_I = ["Fujian Province"]
    
    ## IPCC categories
    
    chn_fj_ets_ipcc_I = ["1A1A1", "1A2A", "1A2B", "1A2D", "1A2K", "1A3A2", "2A4A", 
                         "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", 
                         "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", 
                         "2B9B", "2C1", "2C3", "2C4", "2C5","2C6", "2C7", "2H1"]

    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_fj_ets_ipcc_II = ["1A2A", "1A2B", "1A2D", "1A2K", "1A3A2", "2A4A", 
                          "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", 
                          "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", 
                          "2B9B", "2C1", "2C3", "2C4", "2C5","2C6", "2C7", "2H1"]

    ## scope dictionaries
    chn_fj_ets_jur_scope = {year: chn_fj_ets_jur_I for year in range(2016, 2023)}
    
    chn_fj_ets_ipcc_scope = {year: chn_fj_ets_ipcc_I for year in range(2016, 2021)}
    chn_fj_ets_ipcc_scope.update({year: chn_fj_ets_ipcc_II for year in range(2021, 2023)})
    
    ## Sources dictionary
    
    chn_fj_ets_scope_sources = {year: "web(FJ[2018]), report(ICAP[2021])" for year in range(2016, 2022)}
    chn_fj_ets_scope_sources[2022] = "report(ICAP[2023])"
    

    #----------------------------------------------------------------------------
    
    # Guangdong Province
    
    ## Jurisdiction
    
    chn_gd_ets_jur_I = ["Guangdong Province"]
    
    ## IPCC categories
    
    # initial scope (2013-2015)
    chn_gd_ets_ipcc_I = ["1A1A1", "1A2A", "2A1", "2B8A", "2B8B", "2B8C", "2B8D", 
                         "2B8E", "2C1"]

    # extension to papermaking and domestic aviation (2016)
    chn_gd_ets_ipcc_II = ["1A1A1", "1A2A", "1A2D", "1A3A2", "2A1", "2B8A", 
                          "2B8B", "2B8C", "2B8D", "2B8E", "2C1", "2H1"]

    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_gd_ets_ipcc_III = ["1A2A", "1A2D", "1A3A2", "2A1", "2B8A", 
                            "2B8B", "2B8C", "2B8D", "2B8E", "2C1", "2H1"]

    ## scope dictionaries
    chn_gd_ets_jur_scope = {year: chn_gd_ets_jur_I for year in range(2013, 2023)}

    chn_gd_ets_ipcc_scope = {year: chn_gd_ets_ipcc_I for year in range(2013, 2016)}
    chn_gd_ets_ipcc_scope.update({year: chn_gd_ets_ipcc_II for year in range(2016, 2021)})
    chn_gd_ets_ipcc_scope.update({year: chn_gd_ets_ipcc_III for year in range(2021, 2023)})

    ## Sources dictionary
    
    chn_gd_ets_scope_sources = {year: "report(ICAP[2021])" for year in range(2013, 2022)}
    chn_gd_ets_scope_sources[2022] = "report(ICAP[2023])"


    #----------------------------------------------------------------------------
    
    # Hubei Province
    
    ## Jurisdiction
    
    chn_hb_ets_jur_I = ["Hubei Province"]
    
    ## IPCC categories
    
    # initial scope (2014-2015)
    chn_hb_ets_ipcc_I = ["1A1A1", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2G", 
                         "1A2L", "2A1", "2A3", "2B1", "2B10", "2B2", "2B3", "2B4", 
                         "2B5", "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", 
                         "2B8F", "2B9A", "2B9B", "2C1", "2C3", "2C4", "2C5", "2C6", 
                         "2C7", "2G1", "2H1", "2H2"]

    # extension to new IPCC categories over the threshold (2016)
    chn_hb_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D", 
                          "1A2E", "1A2G", "1A2L", "2A1", "2A3", "2A4A", "2B1", "2B10", 
                          "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                          "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                          "2C3", "2C4", "2C5", "2C6", "2C7", "2G1", "2H1", "2H2"]

    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_hb_ets_ipcc_III = ["1A2A", "1A2B", "1A2C", "1A2D", 
                           "1A2E", "1A2G", "1A2L", "2A1", "2A3", "2A4A", "2B1", "2B10", 
                           "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", 
                           "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                           "2C3", "2C4", "2C5", "2C6", "2C7", "2G1", "2H1", "2H2"]

    ## scope dictionaries
    chn_hb_ets_jur_scope = {year: chn_hb_ets_jur_I for year in range(2014, 2023)}
    
    chn_hb_ets_ipcc_scope = {year: chn_hb_ets_ipcc_I for year in range(2014, 2016)}
    chn_hb_ets_ipcc_scope.update({year: chn_hb_ets_ipcc_II for year in range(2016, 2021)})
    chn_hb_ets_ipcc_scope.update({year: chn_hb_ets_ipcc_III for year in range(2021, 2023)})

    ## Sources dictionary
    
    chn_hb_ets_scope_sources = {2014:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])",
                                   2015:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2016:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2017:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2018:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])", 
                                   2019:"leg(HB[2014]), gvt(HB[2014]), report(ICAP[2021])",
                                   2020:"leg(HB[2020]), report(ICAP[2021])", 
                                   2021:"leg(HB[2020]), report(ICAP[2021])", 2022:"report(ICAP[2023])"}
    

    #----------------------------------------------------------------------------
    
    # Shanghai Municipality
    
    ## Jurisdiction
    
    chn_sh_ets_jur_I = ["Shanghai Municipality"]
    
    ## IPCC categories
    
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

    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_sh_ets_ipcc_III = ["1A2A", "1A2B", "1A2C", "1A2D", 
                          "1A2K", "1A2L", "1A3A2", "1A3C", "1A3D2", "1A4A", "2B1", 
                          "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", 
                          "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", 
                          "2C3", "2C4", "2C5", "2C6", "2C7", "2H1"]
    
    ## scope dictionaries
    chn_sh_ets_jur_scope = {year: chn_sh_ets_jur_I for year in range(2013, 2023)}
    
    chn_sh_ets_ipcc_scope = {year: chn_sh_ets_ipcc_I for year in range(2013, 2016)}
    chn_sh_ets_ipcc_scope.update({year: chn_sh_ets_ipcc_II for year in range(2016, 2021)})
    chn_sh_ets_ipcc_scope.update({year: chn_sh_ets_ipcc_III for year in range(2021, 2023)})

    ## Sources dictionary
    chn_sh_ets_scope_sources = {year: "report(ICAP[2021])" for year in range(2013, 2022)}
    chn_sh_ets_scope_sources[2022] = "report(ICAP[2023])"
    
    #----------------------------------------------------------------------------
    
    # Shenzhen
    
    ## Jurisdiction
    
    chn_sz_ets_jur_I = ["Shenzhen"]
    
    ## IPCC categories
    
    chn_sz_ets_ipcc_I = ["1A1A1", "1A1A2", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", 
                         "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", 
                         "1A2M", "1A3B", "1A3D2", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                         "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36"]
    
    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_sz_ets_ipcc_II = ["1A2A", "1A2B", "1A2C", "1A2D", "1A2E", 
                         "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", 
                         "1A2M", "1A3B", "1A3D2", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                         "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36"]

    ## scope dictionaries
    chn_sz_ets_jur_scope = {year: chn_sz_ets_jur_I for year in range(2013, 2023)}
    
    chn_sz_ets_ipcc_scope = {year: chn_sz_ets_ipcc_I for year in range(2013, 2021)}
    chn_sz_ets_ipcc_scope.update({year: chn_sz_ets_ipcc_II for year in range(2021, 2023)})

    ## Sources dictionary
    
    chn_sz_ets_scope_sources = {year: "report(ICAP[2021])" for year in range(2013, 2022)}
    chn_sz_ets_scope_sources[2022] = "report(ICAP[2023])"


    #----------------------------------------------------------------------------
    
    # Tianjin Municipality
    
    ## Jurisdiction
    
    chn_tj_ets_jur_I = ["Tianjin Municipality"]
    
    ## IPCC categories
    
    # initial scope (2013-2018)
    chn_tj_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2C", "1B2A31", "1B2B31", 
                         "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A", 
                         "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1"]

    # extension to papermaking, aviation, and building materials (2019)
    chn_tj_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2C", "1A2D", "1A2K", 
                          "1A3A2", "1B2A31", "1B2B31", "2B1", "2B10", "2B2", "2B3", 
                          "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", 
                          "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2H1"]

    # introduction of China national ETS and integration of "1A1A1", "1A1A2", "1A1A3" categories into that mechanism (2021)
    chn_tj_ets_ipcc_III = ["1A2A", "1A2C", "1A2D", "1A2K", 
                          "1A3A2", "1B2A31", "1B2B31", "2B1", "2B10", "2B2", "2B3", 
                          "2B4", "2B5", "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", 
                          "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2H1"]

    ## scope dictionaries
    chn_tj_ets_jur_scope = {year: chn_tj_ets_jur_I for year in range(2013, 2023)}
    
    chn_tj_ets_ipcc_scope = {year: chn_tj_ets_ipcc_I for year in range(2013, 2019)}
    chn_tj_ets_ipcc_scope.update({year: chn_tj_ets_ipcc_II for year in range(2019, 2021)})
    chn_tj_ets_ipcc_scope.update({year: chn_tj_ets_ipcc_III for year in range(2021, 2023)})
    
    ## Sources dictionary
    
    chn_tj_ets_scope_sources = {year: "report(ICAP[2021])" for year in range(2013, 2023)}

    #----------------------------------------------------------------------------
    
    # CAN - Alberta
    
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
    
    # CAN-British Columbia

    ## Jurisdiction
    can_bc_ets_jur_I = ["British Columbia"]

    #----------------------------------------------------------------------------
    
    # CAN-Ontario

    ## Jurisdiction
    can_on_ets_jur_I = ["Ontario"]

    #----------------------------------------------------------------------------
    
    # CAN-Quebec
    
    ## Jurisdiction
    can_qc_cat_jur_I = ["Quebec"]
    
    
    ## IPCC categories
    can_qc_cat_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "2A1", "2A2", "2A3", 
                         "2A4", "2A4A", "2A4B", "2A4C", "2A4D", "2B1", "2B10", "2B2", 
                         "2B3", "2B4", "2B5", "2B6", "2B7", "2B8", "2B8A", "2B8B", 
                         "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B", "2C1", "2C2", 
                         "2C3", "2C4", "2C5", "2C6", "2C7", "2D1", "2D2","2D3", "2D4", 
                         "2E", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2", 
                         "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## scope dictionaries
    
    can_qc_cat_jur_scope = {2013:can_qc_cat_jur_I, 2014:can_qc_cat_jur_I}
    
    can_qc_cat_ipcc_scope = {2013:can_qc_cat_ipcc_I, 2014:can_qc_cat_ipcc_I}
    
    ## Sources dictionary
    
    can_qc_cat_scope_sources = {2013:"leg(QC[2011], QC[2012], QC[2013])", 
                                   2014:"leg(QC[2011], QC[2012], QC[2013])"}
    

    #----------------------------------------------------------------------------

    # CAN-Saskatchewan
    # Saskatchewan is coded as a stand alone scheme encompassing the Federal OBPS
    # and the provincial OBPS because the existing  structure does not allow to 
    # account for differences in sectoral scope between jurisdictions
    
    ## Jurisdiction
    
    can_sk_ets_jur_I = ["Saskatchewan"]

    ## IPCC categories

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

    # all emitters transfer to Provincial OBPS
    can_sk_ets_ipcc_II = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
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

    ## scope dictionaries
    can_sk_ets_jur_scope = {year:can_sk_ets_jur_I for year in range(2019, 2025)}

    can_sk_ets_ipcc_scope = {year:can_sk_ets_ipcc_I for year in range(2019, 2023)}  
    can_sk_ets_ipcc_scope.update({year:can_sk_ets_ipcc_II for year in range(2023, 2025)})

    ## Sources dictionary
    
    can_sk_ets_scope_sources = {year: "leg(SOR[2019]), gvt(ECCC[2021], SASK[2019])" for year in range(2019, 2023)}
    can_sk_ets_scope_sources.update({year: "db(WBCPD[2024])" for year in range(2023, 2025)})

    #----------------------------------------------------------------------------
    
    # CAN-New Brunswick
    
    ## Jurisdiction
    
    can_nb_ets_jur_I = ["New Brunswick"]

    ## IPCC categories 

    # Provincial OBPS (2021)
    can_nb_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1B", "1A2B", "1A2D", "1A2E", 
                         "1A2J", "2A2", "2H1", "2H2", "3D1"]
    
    ## scope dictionaries
    can_nb_ets_jur_scope = {year:can_nb_ets_jur_I for year in range(2021, 2025)}
    
    can_nb_ets_ipcc_scope = {year:can_nb_ets_ipcc_I for year in range(2021, 2025)}     
    
    ## Sources dictionary
    
    can_nb_ets_scope_sources = {2021:"gvt(ECCC[2021])", 2022:"gvt(ECCC[2021])",
                                2023: " ", 2024: " "}    


    #----------------------------------------------------------------------------
    
    # CAN-Nova Scotia
    
    ## Jurisdiction
    
    can_ns_ets_jur_I = ["Nova Scotia"]

    ## IPCC categories

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
                            2023:can_ns_ets_jur_I}
    
    can_ns_ets_ipcc_scope = {2019:can_ns_ets_ipcc_I, 2020:can_ns_ets_ipcc_I,
                                2021:can_ns_ets_ipcc_I, 2022:can_ns_ets_ipcc_I,
                                2023:can_ns_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_ns_ets_scope_sources = {2019:"gvt(ECCC[2021])", 2020:"gvt(ECCC[2021])",
                                   2021:"gvt(ECCC[2021])", 2022:"gvt(ECCC[2021])",
                                   2023:"gvt(ECCC[2021])"}     


    #----------------------------------------------------------------------------
    
    # CAN-Nova Scotia
    # Nova Scotia OBPS replacing the NS ETS

    ## Jurisdiction
    
    can_ns_ets_II_jur_I = ["Nova Scotia"]

    ## IPCC categories
    can_ns_ets_II_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A5A", "1B2A", "1B2A1", 
                         "1B2A2", "1B2A3", "1B2A31", "1B2A32", "1B2A33", "1B2A34", 
                         "1B2A35", "1B2A36", "1B2B", "1B2B1", "1B2B2", "1B2B3", 
                         "1B2B31", "1B2B32", "1B2B33", "1B2B34", "1B2B35", "1B2B36"]
    
    ## scope dictionaries
    can_ns_ets_II_jur_scope = {2024:can_ns_ets_II_jur_I}
    
    can_ns_ets_II_ipcc_scope = {2024:can_ns_ets_II_ipcc_I}     
    
    ## Sources dictionary
    
    can_ns_ets_II_scope_sources = {2024:"MULT-rep-035"} 

    #----------------------------------------------------------------------------
    
    # CAN-Newfoundland and Labrador
    
    ## Jurisdiction
    
    can_nl_ets_jur_I = ["Newfoundland and Labrador"]

    ## IPCC categories

    # Provincial OBPS for industrial emitters and federal OBPS for electricity  
    # and transmission sectors
    can_nl_ets_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A2A", "1A2B", "1A2D", 
                         "1A2I", "1B1A", "1B1A1", "1B1A11", "1B1A12", "1B1A13", 
                         "1B1A14", "1B1A2", "1B1A21", "1B1A22", "1B2A34", "2C1", 
                         "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2H1"]
    
    ## scope dictionaries
    can_nl_ets_jur_scope = {2019:can_nl_ets_jur_I, 2020:can_nl_ets_jur_I,
                               2021:can_nl_ets_jur_I, 2022:can_nl_ets_jur_I}
    
    can_nl_ets_ipcc_scope = {2019:can_nl_ets_ipcc_I, 2020:can_nl_ets_ipcc_I,
                             2021:can_nl_ets_ipcc_I, 2022:can_nl_ets_ipcc_I}     
    
    ## Sources dictionary
    
    can_nl_ets_scope_sources = {2019:"gvt(NL[2019])", 2020:"gvt(NL[2019])",
                                   2021:"gvt(NL[2019])", 2022:"gvt(NL[2019])"}  

    
    #------------------------------All schemes dictionaries--------------------------------#
    
    ets_scope = {"eu_ets":{"jurisdictions":eu_ets_jur_scope, 
                                  "sectors":eu_ets_ipcc_scope}, 
                    "aut_ets":{"jurisdictions":aut_ets_jur_scope, 
                              "sectors":aut_ets_ipcc_scope},
                    "che_ets":{"jurisdictions":che_ets_jur_scope, 
                              "sectors":che_ets_ipcc_scope},
                    "deu_ets":{"jurisdictions":deu_ets_jur_scope, 
                              "sectors":deu_ets_ipcc_scope}, 
                    "gbr_ets":{"jurisdictions":gbr_ets_jur_scope, 
                              "sectors":gbr_ets_ipcc_scope},    
                    "idn_ets":{"jurisdictions":idn_ets_jur_scope, 
                              "sectors":idn_ets_ipcc_scope},                               
                    "kaz_ets":{"jurisdictions":kaz_ets_jur_scope, 
                              "sectors":kaz_ets_ipcc_scope},
                    "kor_ets":{"jurisdictions":kor_ets_jur_scope, 
                              "sectors":kor_ets_ipcc_scope},
                    "mex_ets":{"jurisdictions":mex_ets_jur_scope, 
                              "sectors":mex_ets_ipcc_scope},  
                    "mne_ets":{"jurisdictions":mne_ets_jur_scope, 
                              "sectors":mne_ets_ipcc_scope},                        
                    "nzl_ets":{"jurisdictions":nzl_ets_jur_scope, 
                              "sectors":nzl_ets_ipcc_scope}, 
                    "chn_ets":{"jurisdictions":chn_ets_jur_scope, 
                              "sectors":chn_ets_ipcc_scope},
                    "chn_bj_ets":{"jurisdictions":chn_bj_ets_jur_scope, 
                              "sectors":chn_bj_ets_ipcc_scope},
                    "chn_cq_ets":{"jurisdictions":chn_cq_ets_jur_scope, 
                              "sectors":chn_cq_ets_ipcc_scope},
                    "chn_fj_ets":{"jurisdictions":chn_fj_ets_jur_scope, 
                              "sectors":chn_fj_ets_ipcc_scope},
                    "chn_gd_ets":{"jurisdictions":chn_gd_ets_jur_scope, 
                              "sectors":chn_gd_ets_ipcc_scope},
                    "chn_hb_ets":{"jurisdictions":chn_hb_ets_jur_scope, 
                              "sectors":chn_hb_ets_ipcc_scope},
                    "chn_sh_ets":{"jurisdictions":chn_sh_ets_jur_scope, 
                              "sectors":chn_sh_ets_ipcc_scope},
                    "chn_sz_ets":{"jurisdictions":chn_sz_ets_jur_scope, 
                              "sectors":chn_sz_ets_ipcc_scope},
                    "chn_tj_ets":{"jurisdictions":chn_tj_ets_jur_scope, 
                              "sectors":chn_tj_ets_ipcc_scope},
                    "can_obps":{"jurisdictions":can_obps_jur_scope, 
                              "sectors":can_obps_ipcc_scope},
                    "can_ab_ets":{"jurisdictions":can_ab_ets_jur_scope, 
                              "sectors":can_ab_ets_ipcc_scope},
                    "can_sk_ets":{"jurisdictions":can_sk_ets_jur_scope, 
                              "sectors":can_sk_ets_ipcc_scope},
                    "can_nb_ets":{"jurisdictions":can_nb_ets_jur_scope, 
                              "sectors":can_nb_ets_ipcc_scope},
                    "can_ns_ets":{"jurisdictions":can_ns_ets_jur_scope, 
                              "sectors":can_ns_ets_ipcc_scope},
                    "can_ns_ets_II":{"jurisdictions":can_ns_ets_II_jur_scope, 
                              "sectors":can_ns_ets_II_ipcc_scope},
                    "can_nl_ets":{"jurisdictions":can_nl_ets_jur_scope, 
                              "sectors":can_nl_ets_ipcc_scope}, 
                    "can_qc_cat":{"jurisdictions":can_qc_cat_jur_scope, 
                              "sectors":can_qc_cat_ipcc_scope}, 
                    "usa_ca_ets":{"jurisdictions":usa_ca_ets_jur_scope, 
                              "sectors":usa_ca_ets_ipcc_scope}, 
                    "usa_ma_ets":{"jurisdictions":usa_ma_ets_jur_scope, 
                              "sectors":usa_ma_ets_ipcc_scope},
                    "usa_or_ets":{"jurisdictions":usa_or_ets_jur_scope, 
                              "sectors":usa_or_ets_ipcc_scope},
                    "usa_rggi":{"jurisdictions":usa_rggi_jur_scope, 
                              "sectors":usa_rggi_ipcc_scope},
                    "usa_wa_ets":{"jurisdictions":usa_wa_ets_jur_scope, 
                              "sectors":usa_wa_ets_ipcc_scope}}

    ets_scope_sources = {"eu_ets":eu_ets_scope_sources,
                            "aut_ets":aut_ets_scope_sources,
                            "che_ets":che_ets_scope_sources,
                            "deu_ets":deu_ets_scope_sources,
                            "gbr_ets":gbr_ets_scope_sources,
                            "idn_ets":idn_ets_scope_sources,
                            "kaz_ets":kaz_ets_scope_sources,
                            "kor_ets":kor_ets_scope_sources,
                            "mex_ets":mex_ets_scope_sources,
                            "mne_ets":mne_ets_scope_sources,                            
                            "nzl_ets":nzl_ets_scope_sources,
                            "chn_ets":chn_ets_scope_sources,
                            "chn_bj_ets":chn_bj_ets_scope_sources,
                            "chn_cq_ets":chn_cq_ets_scope_sources,
                            "chn_fj_ets":chn_fj_ets_scope_sources,
                            "chn_gd_ets":chn_gd_ets_scope_sources,
                            "chn_hb_ets":chn_hb_ets_scope_sources,
                            "chn_sh_ets":chn_sh_ets_scope_sources,
                            "chn_sz_ets":chn_sz_ets_scope_sources,
                            "chn_tj_ets":chn_tj_ets_scope_sources,
                            "can_obps":can_obps_scope_sources,
                            "can_ab_ets":can_ab_ets_scope_sources,
                            "can_sk_ets":can_sk_ets_scope_sources,
                            "can_nb_ets":can_nb_ets_scope_sources,
                            "can_nb_ets_II":can_ns_ets_II_scope_sources,
                            "can_ns_ets":can_ns_ets_scope_sources,
                            "can_ns_ets_II":can_ns_ets_II_scope_sources,
                            "can_nl_ets":can_nl_ets_scope_sources,
                            "can_qc_cat":can_qc_cat_scope_sources,
                            "usa_ca_ets":usa_ca_ets_scope_sources,
                            "usa_ma_ets":usa_ma_ets_scope_sources,
                            "usa_or_ets":usa_or_ets_scope_sources,
                            "usa_rggi":usa_rggi_scope_sources,
                            "usa_wa_ets":usa_wa_ets_scope_sources}
    
    data_and_sources = {"data":ets_scope, "sources":ets_scope_sources}
    
    return data_and_sources


