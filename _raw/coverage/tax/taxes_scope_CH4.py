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
    
    ## Fuels
    
    sgp_tax_fuel_I = []

    ## Coverage dictionaries
    sgp_tax_jur_coverage = {2019:sgp_tax_jur_I, 
                            2020:sgp_tax_jur_I, 2021:sgp_tax_jur_I}
    
    sgp_tax_ipcc_coverage = {2019:sgp_tax_ipcc_I, 
                             2020:sgp_tax_ipcc_I, 2021:sgp_tax_ipcc_I}     

    sgp_tax_fuel_coverage = {2019:sgp_tax_fuel_I, 
                             2020:sgp_tax_fuel_I, 2021:sgp_tax_fuel_I} 
    
    ## Sources dictionary
    
    sgp_tax_coverage_sources = {2019:"", 
                                2020:"",
                                2021:""}

    #----------------------------------------------------------------------------

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_coverage = {"sgp_tax":{"jurisdictions":sgp_tax_jur_coverage, 
                                  "sectors":sgp_tax_ipcc_coverage,
                                  "fuels":sgp_tax_fuel_coverage}}
    
    taxes_coverage_sources = {"sgp_tax":sgp_tax_coverage_sources}
    
    
    data_and_sources = {"data":taxes_coverage, "sources":taxes_coverage_sources}
    
    
    return data_and_sources
    