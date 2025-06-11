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
                                  2023:" ", 2024:" "}
    
    #----------------------------------------------------------------------------
    
    # Canada Federal Charge for Yukon and Nunavut
    
    ## Jurisdiction
    
    can_tax_II_jur_I = ["Yukon", "Nunavut"]

    ## IPCC categories
    
    # excluding aviation fuels
    can_tax_II_ipcc_I = ["1A1A3", "1A1B", "1A1C", "1A2G", "1A2H", "1A2J", "1A2K", 
                       "1A2L", "1A2M", "1A3B", "1A3C", "1A3D1", "1A3D2", 
                       "1A3E1", "1A4A", "1A4B", "1A5A", "1A5B", "1A5C"]

    ## Fuels
    
    can_tax_II_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_tax_II_jur_scope = {year:can_tax_II_jur_I for year in range(2019, 2025)}
    
    can_tax_II_ipcc_scope = {year:can_tax_II_ipcc_I for year in range(2019, 2025)}
    
    can_tax_II_fuel_scope = {year:can_tax_II_fuel_I for year in range(2019, 2025)}

    ## Sources dictionary
    
    can_tax_II_scope_sources = {2019:"gvt(ECCC[2019])", 2020:"gvt(ECCC[2019])", 
                                   2021:"gvt(ECCC[2019])", 2022:"gvt(ECCC[2019])",
                                   2023:" ", 2024:" "}

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
    
    col_tax_scope_sources = {year: "gvt(COL-DIAN[2022]), db(WBCPD[2024])" for year in range(2023, 2025)}                    

    #----------------------------------------------------------------------------

    # Singapore
    
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
    sgp_tax_jur_scope = {2019:sgp_tax_jur_I, 
                         2020:sgp_tax_jur_I, 2021:sgp_tax_jur_I}
    
    sgp_tax_ipcc_scope = {2019:sgp_tax_ipcc_I, 
                          2020:sgp_tax_ipcc_I, 2021:sgp_tax_ipcc_I}    

    sgp_tax_fuel_scope = {2019:sgp_tax_fuel_I, 
                             2020:sgp_tax_fuel_I, 2021:sgp_tax_fuel_I}     
    
    ## Sources dictionary
    
    sgp_tax_scope_sources = {2019:"", 
                             2020:"",
                             2021:""}

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
    mex_tm_tax_jur_scope = {year:mex_tm_tax_jur_I for year in range(2019, 2025)}
    
    mex_tm_tax_ipcc_scope = {year:mex_tm_tax_ipcc_I for year in range(2019, 2025)}

    mex_tm_tax_fuel_scope = {year:mex_tm_tax_fuel_I for year in range(2019, 2025)}

    ## Sources dictionary
    
    mex_tm_tax_scope_sources = {year:" " for year in range(2019, 2025)}

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
    mex_za_tax_jur_scope = {year:mex_za_tax_jur_I for year in range(2019, 2025)}
    
    mex_za_tax_ipcc_scope = {year:mex_za_tax_ipcc_I for year in range(2019, 2025)}

    mex_za_tax_fuel_scope = {year:mex_za_tax_fuel_I for year in range(2019, 2025)}

    ## Sources dictionary
    
    mex_za_tax_scope_sources = {year:" " for year in range(2019, 2025)}

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_scope = {"can_tax_I":{"jurisdictions":can_tax_I_jur_scope, 
                              "sectors":can_tax_I_ipcc_scope,
                              "fuels":can_tax_I_fuel_scope},
                    "can_tax_II":{"jurisdictions":can_tax_II_jur_scope, 
                              "sectors":can_tax_II_ipcc_scope,
                              "fuels":can_tax_II_fuel_scope},
                    "can_bc_tax":{"jurisdictions":can_bc_tax_jur_scope, 
                              "sectors":can_bc_tax_ipcc_scope,
                              "fuels":can_bc_tax_fuel_scope},
                    "col_tax":{"jurisdictions":col_tax_jur_scope, 
                              "sectors":col_tax_ipcc_scope,
                              "fuels":col_tax_fuel_scope},
                    "sgp_tax":{"jurisdictions":sgp_tax_jur_scope, 
                              "sectors":sgp_tax_ipcc_scope,
                              "fuels":sgp_tax_fuel_scope},
                    "mex_tm_tax":{"jurisdictions":mex_tm_tax_jur_scope, 
                                  "sectors":mex_tm_tax_ipcc_scope,
                                  "fuels":mex_tm_tax_fuel_scope},
                    "mex_za_tax":{"jurisdictions":mex_za_tax_jur_scope, 
                                  "sectors":mex_za_tax_ipcc_scope,
                                  "fuels":mex_za_tax_fuel_scope}}
    
    taxes_scope_sources = {
        "can_tax_I":can_tax_I_scope_sources,
        "can_tax_II":can_tax_II_scope_sources,
        "can_bc_tax":can_bc_tax_scope_sources,
        "col_tax":col_tax_scope_sources,
        "sgp_tax":sgp_tax_scope_sources,
        "mex_tm_tax":mex_tm_tax_scope_sources,
        "mex_za_tax":mex_za_tax_scope_sources
        }
                                
    
    data_and_sources = {"data":taxes_scope, "sources":taxes_scope_sources}
    
    
    return data_and_sources
    