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
    
    mex_tm_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
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
 
    ## Sectors
    
    mex_tm_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    mex_tm_tax_jur_scope = {2019:mex_tm_tax_jur_I, 
                            2020:mex_tm_tax_jur_I, 2021:mex_tm_tax_jur_I}
    
    mex_tm_tax_ipcc_scope = {2019:mex_tm_tax_ipcc_I, 
                             2020:mex_tm_tax_ipcc_I, 2021:mex_tm_tax_ipcc_I}     
    
    mex_tm_tax_fuel_scope = {2019:mex_tm_tax_fuel_I, 
                             2020:mex_tm_tax_fuel_I, 2021:mex_tm_tax_fuel_I}  

    ## Sources dictionary
    
    mex_tm_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

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
    mex_za_tax_jur_scope = {2019:mex_za_tax_jur_I, 
                            2020:mex_za_tax_jur_I, 2021:mex_za_tax_jur_I}
    
    mex_za_tax_ipcc_scope = {2019:mex_za_tax_ipcc_I, 
                             2020:mex_za_tax_ipcc_I, 2021:mex_za_tax_ipcc_I}   

    mex_za_tax_fuel_scope = {2019:mex_za_tax_fuel_I, 
                             2020:mex_za_tax_fuel_I, 2021:mex_za_tax_fuel_I}     

    ## Sources dictionary
    
    mex_za_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_scope = {"sgp_tax":{"jurisdictions":sgp_tax_jur_scope, 
                              "sectors":sgp_tax_ipcc_scope,
                              "fuels":sgp_tax_fuel_scope},
                    "mex_tm_tax":{"jurisdictions":mex_tm_tax_jur_scope, 
                                  "sectors":mex_tm_tax_ipcc_scope,
                                  "fuels":mex_tm_tax_fuel_scope},
                    "mex_za_tax":{"jurisdictions":mex_za_tax_jur_scope, 
                                  "sectors":mex_za_tax_ipcc_scope,
                                  "fuels":mex_za_tax_fuel_scope}}
    
    taxes_scope_sources = {"sgp_tax":sgp_tax_scope_sources,
                            "mex_tm_tax":mex_tm_tax_scope_sources,
                            "mex_za_tax":mex_za_tax_scope_sources}
    
    
    data_and_sources = {"data":taxes_scope, "sources":taxes_scope_sources}
    
    
    return data_and_sources
    