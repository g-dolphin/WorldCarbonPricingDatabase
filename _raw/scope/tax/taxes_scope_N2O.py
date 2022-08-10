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
    
def coverage():     

    # Singapore
    
    ## Jurisdiction
    
    sgp_tax_jur_I = ["Singapore"]

    ## Sectors
    
    sgp_tax_ipcc_I = []
    

    ## Coverage dictionaries
    sgp_tax_jur_coverage = {2019:sgp_tax_jur_I, 
                            2020:sgp_tax_jur_I, 2021:sgp_tax_jur_I}
    
    sgp_tax_ipcc_coverage = {2019:sgp_tax_ipcc_I, 
                             2020:sgp_tax_ipcc_I, 2021:sgp_tax_ipcc_I}     

    
    ## Sources dictionary
    
    sgp_tax_coverage_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------

    # Tamaulipas (Mexico)

    ## Jurisdiction
    
    mex_tm_tax_jur_I = ["Tamaulipas"]

    ## Sectors
    
    mex_tm_tax_ipcc_I = []
    

    ## Coverage dictionaries
    mex_tm_tax_jur_coverage = {2019:mex_tm_tax_jur_I, 
                            2020:mex_tm_tax_jur_I, 2021:mex_tm_tax_jur_I}
    
    mex_tm_tax_ipcc_coverage = {2019:mex_tm_tax_ipcc_I, 
                             2020:mex_tm_tax_ipcc_I, 2021:mex_tm_tax_ipcc_I}     
    
    ## Sources dictionary
    
    mex_tm_tax_coverage_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------

    # Zacatecas (Mexico)
    
    ## Jurisdiction
    
    mex_za_tax_jur_I = ["Zacatecas"]

    ## Sectors
    
    mex_za_tax_ipcc_I = []

    ## Coverage dictionaries
    mex_za_tax_jur_coverage = {2019:mex_za_tax_jur_I, 
                            2020:mex_za_tax_jur_I, 2021:mex_za_tax_jur_I}
    
    mex_za_tax_ipcc_coverage = {2019:mex_za_tax_ipcc_I, 
                             2020:mex_za_tax_ipcc_I, 2021:mex_za_tax_ipcc_I}     

    ## Sources dictionary
    
    mex_za_tax_coverage_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_coverage = {"sgp_tax":{"jurisdictions":sgp_tax_jur_coverage, 
                                  "sectors":sgp_tax_ipcc_coverage,
                                  "fuels":sgp_tax_fuel_coverage}}
    
    taxes_coverage_sources = {"sgp_tax":sgp_tax_coverage_sources}
    
    
    data_and_sources = {"data":taxes_coverage, "sources":taxes_coverage_sources}
    
    
    return data_and_sources
    