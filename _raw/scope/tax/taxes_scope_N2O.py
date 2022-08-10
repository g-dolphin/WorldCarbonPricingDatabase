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
    
    sgp_tax_ipcc_I = []
    

    ## scope dictionaries
    sgp_tax_jur_scope = {2019:sgp_tax_jur_I, 
                            2020:sgp_tax_jur_I, 2021:sgp_tax_jur_I}
    
    sgp_tax_ipcc_scope = {2019:sgp_tax_ipcc_I, 
                             2020:sgp_tax_ipcc_I, 2021:sgp_tax_ipcc_I}     

    
    ## Sources dictionary
    
    sgp_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------

    # Tamaulipas (Mexico)

    ## Jurisdiction
    
    mex_tm_tax_jur_I = ["Tamaulipas"]

    ## Sectors
    
    mex_tm_tax_ipcc_I = []
    

    ## scope dictionaries
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
    
    ## Jurisdiction
    
    mex_za_tax_jur_I = ["Zacatecas"]

    ## Sectors
    
    mex_za_tax_ipcc_I = []

    ## scope dictionaries
    mex_za_tax_jur_scope = {2019:mex_za_tax_jur_I, 
                            2020:mex_za_tax_jur_I, 2021:mex_za_tax_jur_I}
    
    mex_za_tax_ipcc_scope = {2019:mex_za_tax_ipcc_I, 
                             2020:mex_za_tax_ipcc_I, 2021:mex_za_tax_ipcc_I}     

    ## Sources dictionary
    
    mex_za_tax_scope_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_scope = {"sgp_tax":{"jurisdictions":sgp_tax_jur_scope, 
                              "sectors":sgp_tax_ipcc_scope},
                    "mex_tm_tax":{"jurisdictions":mex_tm_tax_jur_scope, 
                                  "sectors":mex_tm_tax_ipcc_scope},
                    "mex_za_tax":{"jurisdictions":mex_za_tax_jur_scope, 
                                    "sectors":mex_za_tax_ipcc_scope}}
    
    taxes_scope_sources = {"sgp_tax":sgp_tax_scope_sources,
                            "mex_tm_tax":mex_tm_tax_scope_sources,
                            "mex_za_tax":mex_za_tax_scope_sources}
    
    
    data_and_sources = {"data":taxes_scope, "sources":taxes_scope_sources}
    
    
    return data_and_sources
    