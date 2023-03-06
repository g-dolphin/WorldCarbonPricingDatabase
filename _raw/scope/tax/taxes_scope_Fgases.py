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

    # Denmark
    
    ## Gases

    dnk_tax_gas_scope_I = []

    ## Jurisdiction
    
    dnk_tax_jur_I = ["Denmark"]

    ## Sectors
    
    dnk_tax_ipcc_I = []
    

    ## scope dictionaries
    dnk_tax_gas_scope = {}
    
    
    dnk_tax_jur_scope = {
                            2001:dnk_tax_jur_I, 
                            2002:dnk_tax_jur_I, 2003:dnk_tax_jur_I, 
                            2004:dnk_tax_jur_I, 2005:dnk_tax_jur_I, 
                            2006:dnk_tax_jur_I, 2007:dnk_tax_jur_I, 
                            2008:dnk_tax_jur_I, 2009:dnk_tax_jur_I, 
                            2010:dnk_tax_jur_I, 2011:dnk_tax_jur_I, 
                            2012:dnk_tax_jur_I, 2013:dnk_tax_jur_I, 
                            2014:dnk_tax_jur_I, 2015:dnk_tax_jur_I, 
                            2016:dnk_tax_jur_I, 2017:dnk_tax_jur_I,
                            2018:dnk_tax_jur_I, 2019:dnk_tax_jur_I, 
                            2020:dnk_tax_jur_I, 2021:dnk_tax_jur_I}
    
    dnk_tax_ipcc_scope = {
                            2001:dnk_tax_jur_I, 
                            2002:dnk_tax_jur_I, 2003:dnk_tax_jur_I, 
                            2004:dnk_tax_jur_I, 2005:dnk_tax_jur_I, 
                            2006:dnk_tax_jur_I, 2007:dnk_tax_jur_I, 
                            2008:dnk_tax_jur_I, 2009:dnk_tax_jur_I, 
                            2010:dnk_tax_jur_I, 2011:dnk_tax_jur_I, 
                            2012:dnk_tax_jur_I, 2013:dnk_tax_jur_I, 
                            2014:dnk_tax_jur_I, 2015:dnk_tax_jur_I, 
                            2016:dnk_tax_jur_I, 2017:dnk_tax_jur_I,
                            2018:dnk_tax_jur_I, 2019:dnk_tax_jur_I, 
                            2020:dnk_tax_jur_I, 2021:dnk_tax_jur_I}     
    
    ## Sources dictionary
    
    dnk_tax_scope_sources = {2001:"",
                                2002:"",
                                2003:"",
                                2004:"",
                                2005:"",
                                2006:"",
                                2007:"",
                                2008:"",
                                2009:"",
                                2010:"",
                                2011:"",
                                2012:"",
                                2013:"",
                                2014:"",
                                2015:"",
                                2016:"",
                                2017:"",
                                2018:"",
                                2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------   

    # Iceland
    
    ## Gases

    isl_tax_gas_scope_I = ["SF6", "HFCs", "PFCs"]

    ## Jurisdiction
    
    isl_tax_II_jur_I = ["Iceland"]

    ## Sectors
    
    isl_tax_II_ipcc_I = ["2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C",
                          "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5", 
                          "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D",
                          "2B8E", "2B8F", "2B9A", "2B9B", "2B10", "2C1",
                          "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1",
                          "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4",
                          "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                          "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]
    

    ## scope dictionaries
    isl_tax_gas_scope = {2020:isl_tax_gas_scope_I, 2021:isl_tax_gas_scope_I}

    isl_tax_II_jur_scope = {2020:isl_tax_II_jur_I, 2021:isl_tax_II_jur_I}
    
    isl_tax_II_ipcc_scope = {2020:isl_tax_II_ipcc_I, 2021:isl_tax_II_ipcc_I}     
    
    ## Sources dictionary
    
    isl_tax_II_scope_sources = {2020:"",
                                   2021:""}

    #----------------------------------------------------------------------------   

    # Singapore
    
    ## Gases

    sgp_tax_gas_I = ["SF6", "HFCs", "PFCs"]

    ## Jurisdiction
    
    sgp_tax_jur_I = ["Singapore"]

    ## Sectors
    
    sgp_tax_ipcc_I = ["2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C",
                      "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5", 
                      "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D",
                      "2B8E", "2B8F", "2B9A", "2B9B", "2B10", "2C1",
                      "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1",
                      "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4",
                      "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                      "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]

    ## scope dictionaries
    sgp_tax_gas_scope = {2019:sgp_tax_gas_I, 
                            2020:sgp_tax_gas_I, 2021:sgp_tax_gas_I}
    
    sgp_tax_jur_scope = {2019:sgp_tax_jur_I, 
                            2020:sgp_tax_jur_I, 2021:sgp_tax_jur_I}
    
    sgp_tax_ipcc_scope = {2019:sgp_tax_ipcc_I, 
                             2020:sgp_tax_ipcc_I, 2021:sgp_tax_ipcc_I}     
    
    ## Sources dictionary
    
    sgp_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------   

    # Spain

    ## Gases

    esp_tax_gas_I = ["SF6", "HFCs", "PFCs"]

    ## Jurisdiction
    
    esp_tax_jur_I = ["Spain"]

    ## Sectors
    
    esp_tax_ipcc_I = ["2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C",
                      "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5", 
                      "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D",
                      "2B8E", "2B8F", "2B9A", "2B9B", "2B10", "2C1",
                      "2C2", "2C3", "2C4", "2C5", "2C6", "2C7", "2D1",
                      "2D2", "2D3", "2D4", "2E1", "2E2", "2E3", "2E4",
                      "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                      "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]

    ## scope dictionaries
    esp_tax_gas_scope = {2014:esp_tax_gas_I, 2015:esp_tax_gas_I, 
                            2016:esp_tax_gas_I, 2017:esp_tax_gas_I,
                            2018:esp_tax_gas_I, 2019:esp_tax_gas_I, 
                            2020:esp_tax_gas_I, 2021:esp_tax_gas_I}
    
    esp_tax_jur_scope = {2014:esp_tax_jur_I, 2015:esp_tax_jur_I, 
                            2016:esp_tax_jur_I, 2017:esp_tax_jur_I,
                            2018:esp_tax_jur_I, 2019:esp_tax_jur_I, 
                            2020:esp_tax_jur_I, 2021:esp_tax_jur_I}
    
    esp_tax_ipcc_scope = {2014:esp_tax_ipcc_I, 2015:esp_tax_ipcc_I,
                             2016:esp_tax_ipcc_I, 2017:esp_tax_ipcc_I,
                             2018:esp_tax_ipcc_I, 2019:esp_tax_ipcc_I, 
                             2020:esp_tax_ipcc_I, 2021:esp_tax_ipcc_I}     

    
    ## Sources dictionary
    
    esp_tax_scope_sources = {2014:"",
                                2015:"",
                                2016:"",
                                2017:"",
                                2018:"",
                                2019:"", 
                                2020:"",
                                2021:""}

    
   #----------------------------------------------------------------------------

    # Tamaulipas (Mexico)

    ## Gases

    mex_tm_tax_gas_I = ["SF6", "HFCs", "PFCs"]

    ## Jurisdiction
    
    mex_tm_tax_jur_I = ["Tamaulipas"]

    ## Sectors
    
    mex_tm_tax_ipcc_I = []


    ## scope dictionaries
    mex_tm_tax_gas_scope = {}

    mex_tm_tax_jur_scope = {2019:mex_tm_tax_jur_I, 
                            2020:mex_tm_tax_jur_I, 2021:mex_tm_tax_jur_I}
    
    mex_tm_tax_ipcc_scope = {2019:mex_tm_tax_ipcc_I, 
                             2020:mex_tm_tax_ipcc_I, 2021:mex_tm_tax_ipcc_I}     

    
    ## Sources dictionary
    
    mex_tm_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------

    # Zacatecas (Mexico)

    ## Gases

    mex_za_tax_gas_I = ["SF6", "HFCs", "PFCs"]

    ## Jurisdiction
    
    mex_za_tax_jur_I = ["Zacatecas"]

    ## Sectors
    
    mex_za_tax_ipcc_I = []

    ## scope dictionaries
    mex_za_tax_gas_scope = {}

    mex_za_tax_jur_scope = {2019:mex_za_tax_jur_I, 
                            2020:mex_za_tax_jur_I, 2021:mex_za_tax_jur_I}
    
    mex_za_tax_ipcc_scope = {2019:mex_za_tax_ipcc_I, 
                             2020:mex_za_tax_ipcc_I, 2021:mex_za_tax_ipcc_I}     

    ## Sources dictionary
    
    mex_za_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_scope = {"dnk_tax":{"gases":dnk_tax_gas_scope,
                                 "jurisdictions":dnk_tax_jur_scope, 
                                  "sectors":dnk_tax_ipcc_scope},
                   "isl_tax":{"gases":isl_tax_gas_scope,
                                 "jurisdictions":isl_tax_II_jur_scope, 
                                 "sectors":isl_tax_II_ipcc_scope},
                    "sgp_tax":{"gases":sgp_tax_gas_scope,
                                 "jurisdictions":sgp_tax_jur_scope, 
                                 "sectors":sgp_tax_ipcc_scope},
                    "esp_tax":{"gases":esp_tax_gas_scope,
                                 "jurisdictions":esp_tax_jur_scope, 
                                 "sectors":esp_tax_ipcc_scope},
                    "mex_tm_tax":{"gases":mex_tm_tax_gas_scope,
                                    "jurisdictions":mex_tm_tax_jur_scope,
                                    "sectors":mex_tm_tax_ipcc_scope},
                    "mex_za_tax":{"gases":mex_za_tax_gas_scope,
                                    "jurisdictions":mex_za_tax_jur_scope,
                                    "sectors":mex_za_tax_ipcc_scope}}
    
    taxes_scope_sources = {"dnk_tax":dnk_tax_scope_sources,
                           "isl_tax_II":isl_tax_II_scope_sources,
                            "sgp_tax":sgp_tax_scope_sources,
                            "esp_tax":esp_tax_scope_sources,
                            "mex_tm_tax":mex_tm_tax_scope_sources,
                            "mex_za_tax":mex_za_tax_scope_sources}
    
    
    data_and_sources = {"data":taxes_scope, "sources":taxes_scope_sources}
    
    
    return data_and_sources
    