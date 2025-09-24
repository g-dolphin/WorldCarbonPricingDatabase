# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 07:54:30 2021

@author: gd
"""
    
def scope():     

    # British Columbia
    
    ## Jurisdiction
    
    can_bc_tax_jur_I = ["British Columbia"]

    ## IPCC categories
    
    # initial scope
    can_bc_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2", "1A3B", "1A3C",
                         "1A3D2", "1A3E1", "1A4A", "1A4B", "1A4C1",
                         "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C"]

    ## Fuels
    
    can_bc_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_bc_tax_jur_scope = {year:can_bc_tax_jur_I for year in range(2008, 2023)}
    
    can_bc_tax_ipcc_scope = {year:can_bc_tax_ipcc_I for year in range(2008, 2023)}
    
    can_bc_tax_fuel_scope = {year:can_bc_tax_fuel_I for year in range(2008, 2023)}
    
    ## Sources dictionary
    
    can_bc_tax_scope_sources = {year:"leg(BC-CTA[2008]), gvt(BCGOV[2021])" for year in range(2008, 2023)}

   #----------------------------------------------------------------------------
    
    # Canada Federal Charge for most provinces
    
    ## Jurisdiction
    
    # initial province scope (2019)    
    can_tax_I_jur_I = ["Manitoba", "Ontario", "Saskatchewan", "New Brunswick"]

    # New Brunswick opts out and Alberta joins in (2020-2021)
    can_tax_I_jur_II = ["Manitoba", "Ontario", "Saskatchewan", "Alberta"]

    # Prince Edward Island and Newfoundland and Labrador replaces its carbon levy with the Federal backstop (2023)
    can_tax_I_jur_III = ["Manitoba", "Ontario", "Saskatchewan", "Alberta", "Prince Edward Island",
                         "Newfoundland and Labrador", "New Brunswick"]

    ## IPCC categories
    
    can_tax_I_ipcc_I = ["1A1A3", "1A1B", "1A1C", "1A2G", "1A2H", "1A2J", "1A2K", 
                       "1A2L", "1A2M", "1A3A2", "1A3B", "1A3C", "1A3D1", 
                       "1A3D2", "1A3E1", "1A4A", "1A4B", "1A5A", "1A5B", 
                       "1A5C"]

    ## Fuels
    
    can_tax_I_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_tax_I_jur_scope = {2019:can_tax_I_jur_I, 2020:can_tax_I_jur_II,
                             2021:can_tax_I_jur_II, 2022:can_tax_I_jur_II,
                             2023:can_tax_I_jur_III, 2024:can_tax_I_jur_III}
    
    can_tax_I_ipcc_scope = {year:can_tax_I_ipcc_I for year in range(2019, 2025)}
    
    can_tax_I_fuel_scope = {year:can_tax_I_fuel_I for year in range(2019, 2025)}

    ## Sources dictionary
    
    can_tax_I_scope_sources = {2019:"gvt(ECCC[2019])", 2020:"gvt(ECCC[2019])", 
                                  2021:"gvt(ECCC[2019])", 2022:"gvt(ECCC[2019])",
                                  2023:"gvt(ECCC[2019])", 2024:"gvt(ECCC[2019])"}

    #----------------------------------------------------------------------------

    # Colombia
    
    ## Jurisdiction
    
    col_tax_jur_I = ["Colombia"]

    ## IPCC categories
    
    col_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M"]
    
    ## Fuels
    
    col_tax_fuel_I = ["Oil", "Natural gas"]
    col_tax_fuel_II = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    col_tax_jur_scope = {year:col_tax_jur_I for year in range(2022, 2025)}
    
    col_tax_ipcc_scope = {year:col_tax_ipcc_I for year in range(2022, 2025)}

    col_tax_fuel_scope = {year:col_tax_fuel_I for year in range(2022, 2024)}
    col_tax_fuel_scope[2024] = col_tax_fuel_II   

    ## Sources dictionary
    
    col_tax_scope_sources = {year: "gvt(COL-DIAN[2022]), db(WBCPD[2024])" for year in range(2022, 2025)}                    

    #----------------------------------------------------------------------------

    # Poland
    
    ## Gases covered: All 
    
    ## Jurisdictions    
    
    pol_tax_jur_I = ["Poland"]
    
    ## IPCC categories
    pol_tax_ipcc_I = ["1A1A1", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", 
                      "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M"]
    
    ## 1A2K and 1A2M relevant for CH4 and N2O 
    
    ## Fuels

    pol_tax_fuel_I = ["Oil", "Coal", "Natural gas"]      
    
    ## scope dictionaries

    pol_tax_jur_scope = {year:pol_tax_jur_I for year in range(1990, 2025)}

    pol_tax_ipcc_scope = {year:pol_tax_ipcc_I for year in range(1990, 2025)}

    pol_tax_fuel_scope = {year:pol_tax_fuel_I for year in range(1990, 2025)}

    ## Sources dictionary
    
    pol_tax_scope_sources = {year:"report(OCED[2012], OECD-EP-P[2015])" for year in range(1990, 2022)}
    pol_tax_scope_sources.update({year: "db(WBCPD[2023]" for year in range(2022,2025)})


    #----------------------------------------------------------------------------

    # Singapore
    
    ## Gases covered: All 
    
    ## Jurisdiction
    
    sgp_tax_jur_I = ["Singapore"]

    ## Sectors
    
    sgp_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                      "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                      "1A2J", "1A2K", "1A2L", "1A2M", "2A1", "2A2", "2A3", "2A4A", 
                      "2A4B", "2A4C", "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5",
                      "2B6", "2B7", "2B9A", "2B9B", "2B10", "2C1", "2C2", "2C3",
                      "2C5", "2D1", "2D2", "2D3", "2D4", "2E"]

    ## Fuels
    
    sgp_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    sgp_tax_jur_scope = {year:sgp_tax_jur_I for year in range(2019, 2025)}
    
    sgp_tax_ipcc_scope = {year:sgp_tax_ipcc_I for year in range(2019, 2025)}  

    sgp_tax_fuel_scope = {year:sgp_tax_fuel_I for year in range(2019, 2025)}
    
    ## Sources dictionary
    
    sgp_tax_scope_sources = {year:"leg(SPG[2018])" for year in range(2019, 2025)}
    
    
    #----------------------------------------------------------------------------

    # Mexico - National 
    
    ## Jurisdiction
    
    mex_tax_jur_I = ["Mexico"]

    ## IPCC categories
    
    mex_tax_ipcc_I = ["1A1A1", "1A1B", "1A1C", 
                      "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                      "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M",
                      "1A3A2", "1A3B", "1A4B", "1A4C1"]
    
    ## Fuels
    
    mex_tax_fuel_I = ["Oil", "Coal"]

    ## scope dictionaries
    
    mex_tax_jur_scope = {year:mex_tax_jur_I for year in range(2014, 2025)}
    
    mex_tax_ipcc_scope = {year:mex_tax_ipcc_I for year in range(2014, 2025)}
    
    mex_tax_fuel_scope = {year:mex_tax_fuel_I for year in range(2014, 2025)}
    
    ## Sources dictionary
    
    mex_tax_scope_sources = {year:"leg(LIEP[2012])" for year in range(2014, 2025)}

    
    #----------------------------------------------------------------------------
    
    # Mexico - State 
    
    ## Jurisdiction
    
    ## Check jurisdiction name 
    mex_em_tax_jur_I = ["Mexico State"]

    ## IPCC categories - "any installation located in a specific location on a permanent basis that carries out an industrial, commercial, service or any other activity that generates pollutant air emissions"
    
    mex_em_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                         "1A2A", "1A2B", "1A2C", "1A2D", "1A2E",
                         "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                         "1A2K", "1A2L", "1A2M",  
                         "2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C",
                         "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5", 
                         "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D",
                         "2B8E", "2B8F", "2B9A", "2B9B", "2B10", "2C1",
                         "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1",
                         "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4",
                         "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                         "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## Fuels
    
    mex_em_tax_fuel_I = ["Oil", "Coal", "Natural gas"] 

    ## scope dictionaries
    
    mex_em_tax_jur_scope = {year:mex_em_tax_jur_I for year in range(2022, 2025)}
    
    mex_em_tax_ipcc_scope = {year:mex_em_tax_ipcc_I for year in range(2022, 2025)}
    
    mex_em_tax_fuel_scope = {year:mex_em_tax_fuel_I for year in range(2022, 2025)}
    
    ## Sources dictionary
    
    mex_em_tax_scope_sources = {year:"rep(MEX-EM[2023])" for year in range(2022, 2025)}
    
   #----------------------------------------------------------------------------
    
    # Durango (Mexico)
    
    ## Gases covered: All 
    
    mex_dg_tax_jur_I = ["Durango"]
    
    mex_dg_tax_ipcc_I = {"1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                          "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F",
                          "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L",
                          "1A2M", "2A1", "2A2", "2A4A", "2A4B", "2A4C", "2A4D",
                          "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7",
                          "2B8A", "2B8B", "2B8C", "2B8D", "2B8F", "2B9A", "2B9B", 
                          "2B10", "2C1", "2C2", "2C3", "2C3", "2C4", "2C4", "2C5",
                          "2C6","2C7", "2D1", "2D2", "2D3", "2D4", "20", "200", "2000",
                          "200000", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6", "2G1", "2G2",
                          "2G3", "2G4", "2H1", "2H2", "2H3"}

    mex_dg_tax_fuel_I = {"Oil", "Coal", "Natural Gas"}
    
    ## scope dictionaries
    mex_dg_tax_jur_scope = {year: mex_dg_tax_jur_I for year in range(2024, 2025)}
    
    mex_dg_tax_ipcc_scope = {year: mex_dg_tax_ipcc_I for year in range(2024, 2025)}  

    mex_dg_tax_fuel_scope = {year: mex_dg_tax_fuel_I for year in range(2024, 2025)}
    
    mex_dg_tax_scope_sources = {year:"rep(MEX-dg[2023]), leg(MEX-dg[2022])" for year in range(2024, 2025)}
      
    #----------------------------------------------------------------------------
    

    # Mexico - Guanajuato
    
    ## Jurisdiction
    
    mex_gj_tax_jur_I = ["Guanajuato"]

    ## IPCC categories
    
    mex_gj_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                         "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                         "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", 
                         "2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C", "2A4D",
                         "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A",
                         "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B",
                         "2B10", "2C1","2C2","2C3", "2C4", "2C5","2C6", "2C7",
                         "2D1", "2D2", "2D3","2D4", "20", "200", "2000", "20000",
                         "200000", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                         "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## Fuels
    
    mex_gj_tax_fuel_I = ["Coal", "Natural gas", "Oil"]

    ## scope dictionaries
    mex_gj_tax_jur_scope = {year: mex_gj_tax_jur_I for year in range(2024, 2025)}
    
    mex_gj_tax_ipcc_scope = {year: mex_gj_tax_ipcc_I for year in range(2024, 2025)}  

    mex_gj_tax_fuel_scope = {year: mex_gj_tax_fuel_I for year in range(2024, 2025)}
    
    ## Sources dictionary
    
    mex_gj_tax_scope_sources = {year: "leg(MEX-GJ[2023]) " for year in range(2024, 2025)}
    
    #----------------------------------------------------------------------------
    
    # Queretaro (Mexico)
    
    ## Gases covered: All 
    
    mex_qt_tax_jur_I = ["Queretaro"]
    
    # IPCC categories 
    
    mex_qt_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                         "1A2A", "1A2B", "1A2C", "1A2D", "1A2E",
                         "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                         "1A2K", "1A2L", "1A2M",  
                         "2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C",
                         "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5", 
                         "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D",
                         "2B8E", "2B8F", "2B9A", "2B9B", "2B10", "2C1",
                         "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1",
                         "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4",
                         "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                         "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    mex_qt_tax_fuel_I = ["Oil", "Natural gas", "Coal"]
    
    mex_qt_tax_fuel_scope = {year:mex_qt_tax_fuel_I for year in range(2023, 2025)}
    
    mex_qt_tax_ipcc_scope = {year:mex_qt_tax_ipcc_I for year in range(2023, 2025)}
    
    mex_qt_tax_jur_scope = {year: mex_qt_tax_jur_I for year in range(2023, 2025)}
   
    mex_qt_tax_scope_sources = {year: "web(MEX-QT[2022]), web(MEX-QT[2025]), db(WBCPD[2024])" for year in range(2023, 2025)}
      

    #----------------------------------------------------------------------------

    # Tamaulipas (Mexico)
    
    ## Jurisdiction
    
    mex_tm_tax_jur_I = ["Tamaulipas"]

    ## Sectors
    
    mex_tm_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                         "1A2J", "1A2K", "1A2L", "1A2M", 
                         "1A4A", "1A4B", "1A4C1", "1A4C2", "1A4C3", "1A5A",
                         "2A1", "2A2", "2A3", "2A4A", 
                         "2A4B", "2A4C", "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5",
                         "2B6", "2B7", "2B9A", "2B9B", "2B10", "2C1", "2C2", "2C3",
                         "2C5", "2D1", "2D2", "2D3", "2D4", "2E"]

     ## Fuels
    
    mex_tm_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

   ## scope dictionaries
    mex_tm_tax_jur_scope = {year:mex_tm_tax_jur_I for year in [2021, 2022, 2024]}
    
    mex_tm_tax_ipcc_scope = {year:mex_tm_tax_ipcc_I for year in [2021, 2022, 2024]}

    mex_tm_tax_fuel_scope = {year:mex_tm_tax_fuel_I for year in [2021, 2022, 2024]}

    ## Sources dictionary
    
    mex_tm_tax_scope_sources = {year:"web(MEX-TM[2023], web(MEX-TM[2024a]), web(MEX-TM[2024b]), db(WCPDB[2024])" for year in [2021, 2022, 2024]}

    #----------------------------------------------------------------------------

    # Mexico - Yucatan
    
    ## Jurisdiction
    
    mex_yu_tax_jur_I = ["Yucatan"]

    ## IPCC categories
    
    mex_yu_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                         "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                         "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", 
                         "2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C", "2A4D",
                         "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A",
                         "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B",
                         "2B10", "2C1","2C2","2C3", "2C4", "2C5","2C6", "2C7",
                         "2D1", "2D2", "2D3","2D4", "20", "200", "2000", "20000",
                         "200000", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                         "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## Fuels
    
    mex_yu_tax_fuel_I = ["Coal", "Natural gas", "Oil"]

    ## scope dictionaries
    mex_yu_tax_jur_scope = {year: mex_yu_tax_jur_I for year in range(2022, 2025)}
    
    mex_yu_tax_ipcc_scope = {year: mex_yu_tax_ipcc_I for year in range(2022, 2025)}  

    mex_yu_tax_fuel_scope = {year: mex_yu_tax_fuel_I for year in range(2022, 2025)}
    
    ## Sources dictionary
    
    mex_yu_tax_scope_sources = {year: "leg(MEX-YU[2022])" for year in range(2022, 2025)}

    #----------------------------------------------------------------------------

    # Zacatecas (Mexico)
    
    ## Jurisdiction
    
    mex_za_tax_jur_I = ["Zacatecas"]

    ## Sectors
    
    mex_za_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                         "1A2A", "1A2B", "1A2C", "1A2D", "1A2E",
                         "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                         "1A2K", "1A2L", "1A2M",  
                         "2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C",
                         "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5", 
                         "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D",
                         "2B8E", "2B8F", "2B9A", "2B9B", "2B10", "2C1",
                         "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1",
                         "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4",
                         "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                         "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]

    ## Fuels
    
    mex_za_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    ## 6/2025 changed from 2019 to 2017 based on tax code course in project folder  
    mex_za_tax_jur_scope = {year:mex_za_tax_jur_I for year in range(2017, 2025)}
    
    mex_za_tax_ipcc_scope = {year:mex_za_tax_ipcc_I for year in range(2017, 2025)}

    mex_za_tax_fuel_scope = {year:mex_za_tax_fuel_I for year in range(2017, 2025)}

    ## Sources dictionary
    
    mex_za_tax_scope_sources = {year:"leg(MEX-ZA[2016])" for year in range(2017, 2025)}
    
    
    #----------------------------------------------------------------------------
    
    # Norway
    
    ## Gases covered: CH4 explicitly 
    
    # tax on vented and flared emissions 
    
    ## Jurisdictions    
    
    nor_tax_I_jur_I = ["Norway"]
    
    ## IPCC categories
    
    nor_tax_I_ipcc_I = ["1B2A1", "1B2A2", "1B2B2", "1B2B1"] 
    
    ## Fuels

    nor_tax_I_fuel_I = ["Oil", "Natural gas"]
    
    
    ## scope dictionaries

    nor_tax_I_jur_scope = {year:nor_tax_I_jur_I for year in range(1991, 2025)}

    nor_tax_I_ipcc_scope = {year:nor_tax_I_ipcc_I for year in range(1991, 2025)}
    
    nor_tax_I_fuel_scope = {year:nor_tax_I_fuel_I for year in range(1991, 2025)}
    

    ## Sources dictionary
    
    nor_tax_I_scope_sources = {year: "leg(NOR-EA[1990])" for year in range(1991, 2025)}
    
    
    #----------------------------------------------------------------------------

    # South Africa 
    
    ## Gases covered: All 
    
    ## Jurisdiction
    
    zaf_tax_jur_I = ["South Africa"]
    
    
    ## IPCC categories
    
    zaf_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                      "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                      "1A2J", "1A2K", "1A2L", "1A2M", "1A3A1", "1A3A2", "1A3B", 
                      "1A3C", "1A3D", "1A3D1", "1A3D2", "1A3E", "1A3E1", "1A4A", 
                      "1A4C1", "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C", "1B1A", 
                      "1B1A1", "1B1A11", "1B1A12", "1B1A13", "1B1A14", "1B1A2", 
                      "1B1A21", "1B1A22", "1B1C1", "1B1C2", "1B1C3", "1B2A1", "1B2A2", "1B2A3", "1B2A31", 
                      "1B2A32", "1B2A33", "1B2A34", "1B2A35", "1B2A36", "1B2B1", 
                      "1B2B2", "1B2B3", "1B2B31", "1B2B32", "1B2B33", "1B2B34", 
                      "1B2B35", "1B2B36", "1B3A", "1B3B", "1B3C", "1C1A", "1C1B", "1C1C", "1C2A", 
                      "1C2B", "1C3", "2A1", "2A2", "2A3", "2A4", "2A4A", "2A4B", 
                      "2A4C", "2A4D", "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", 
                      "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", 
                      "2B9A", "2B9B", "2B10", "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", 
                      "2C7", "2D1", "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4", "2F1A",
                      "2F1B", "2F2", "2F3", 
                      "2F4", "2F5", "2F6", "2G1A", "2G1B", "2G2", "2G3", "2G4", "2H1", 
                      "2H2", "2H3", "4C1", "5A1", "5A2", "5B"]
    
    ## Fuel
    zaf_tax_fuel_I = ["Coal", "Oil", "Natural gas"]    
    
    ## scope dictionaries
    zaf_tax_jur_scope = {year:zaf_tax_jur_I for year in range(2019, 2025)}
    
    zaf_tax_ipcc_scope = {year:zaf_tax_ipcc_I for year in range(2019, 2025)}  

    zaf_tax_fuel_scope = {year:zaf_tax_fuel_I for year in range(2019, 2025)}
    
    ## Sources dictionary
    
    zaf_tax_scope_sources = {year:"leg(SA[2019])" for year in range(2019, 2025)}
    
    

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_scope = {"can_tax_I":{"jurisdictions":can_tax_I_jur_scope, 
                              "sectors":can_tax_I_ipcc_scope,
                              "fuels":can_tax_I_fuel_scope},
       #            "can_tax_II":{"jurisdictions":can_tax_II_jur_scope, 
       #                       "sectors":can_tax_II_ipcc_scope,
       #                       "fuels":can_tax_II_fuel_scope},
                    "can_bc_tax":{"jurisdictions":can_bc_tax_jur_scope, 
                              "sectors":can_bc_tax_ipcc_scope,
                              "fuels":can_bc_tax_fuel_scope},
                    "col_tax":{"jurisdictions":col_tax_jur_scope, 
                              "sectors":col_tax_ipcc_scope,
                              "fuels":col_tax_fuel_scope},
                    ## two norway taxes, use I
                    "nor_tax":{"jurisdictions": nor_tax_I_jur_scope,
                               "sectors": nor_tax_I_ipcc_scope,
                               "fuels": nor_tax_I_fuel_scope},
                    "pol_tax":{"jurisdictions":pol_tax_jur_scope,
                               "sectors": pol_tax_ipcc_scope,
                               "fuels": pol_tax_fuel_scope},
                    "sgp_tax":{"jurisdictions":sgp_tax_jur_scope, 
                              "sectors":sgp_tax_ipcc_scope,
                              "fuels":sgp_tax_fuel_scope},
                    "zaf_tax":{"jurisdictions":zaf_tax_jur_scope,
                               "sectors": zaf_tax_ipcc_scope,
                               "fuels": zaf_tax_fuel_scope},
                    "mex_tax":{"jurisdictions": mex_tax_jur_scope,
                               "sectors": mex_tax_ipcc_scope,
                               "fuels": mex_tax_fuel_scope},
                    "mex_em_tax":{"jurisdictions":mex_em_tax_jur_scope,
                                  "sectors": mex_em_tax_ipcc_scope,
                                  "fuels": mex_em_tax_fuel_scope},
                    "mex_dg_tax":{"jurisdictions":mex_dg_tax_jur_scope,
                                   "sectors": mex_dg_tax_ipcc_scope,
                                   "fuels": mex_dg_tax_fuel_scope},
                    "mex_gj_tax":{"jurisdictions":mex_gj_tax_jur_scope,
                                  "sectors": mex_gj_tax_ipcc_scope,
                                  "fuels": mex_gj_tax_fuel_scope},
                    "mex_qt_tax":{"jurisdictions":mex_qt_tax_jur_scope,
                                  "sectors": mex_qt_tax_ipcc_scope,
                                  "fuels": mex_qt_tax_fuel_scope},
                    "mex_tm_tax":{"jurisdictions":mex_tm_tax_jur_scope, 
                                  "sectors":mex_tm_tax_ipcc_scope,
                                  "fuels":mex_tm_tax_fuel_scope},
                    "mex_yu_tax":{"jurisdictions":mex_yu_tax_jur_scope, 
                                  "sectors":mex_yu_tax_ipcc_scope,
                                  "fuels":mex_yu_tax_fuel_scope},
                    "mex_za_tax":{"jurisdictions":mex_za_tax_jur_scope, 
                                  "sectors":mex_za_tax_ipcc_scope,
                                  "fuels":mex_za_tax_fuel_scope}}
    
    taxes_scope_sources = {
        "can_tax_I":can_tax_I_scope_sources,
    #    "can_tax_II":can_tax_II_scope_sources,
        "can_bc_tax":can_bc_tax_scope_sources,
        "col_tax":col_tax_scope_sources,
        "nor_tax":nor_tax_I_scope_sources,
        "pol_tax":pol_tax_scope_sources,
        "sgp_tax":sgp_tax_scope_sources,
        "mex_tax": mex_tax_scope_sources,
        "mex_em_tax":mex_em_tax_scope_sources,
        "mex_dg_tax":mex_dg_tax_scope_sources,
        "mex_gj_tax":mex_gj_tax_scope_sources,
        "mex_qt_tax":mex_qt_tax_scope_sources,
        "mex_tm_tax":mex_tm_tax_scope_sources,
        "mex_yu_tax": mex_yu_tax_scope_sources,
        "mex_za_tax":mex_za_tax_scope_sources,
        "zaf_tax": zaf_tax_scope_sources
        }
                                
    
    data_and_sources = {"data":taxes_scope, "sources":taxes_scope_sources}
    
    
    return data_and_sources
    
