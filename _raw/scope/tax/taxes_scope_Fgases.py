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

    # Denmark
    
    ## Jurisdiction
    
    dnk_tax_jur_I = ["Denmark"]

    ## Sectors
    
    dnk_tax_ipcc_I = []
    
    ## Fuels
    
    dnk_tax_fuel_I = ["Oil"]
    dnk_tax_fuel_II = ["Oil", "Coal"]

    ## Coverage dictionaries
    dnk_tax_jur_coverage = {
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
    
    dnk_tax_ipcc_coverage = {
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

    dnk_tax_fuel_coverage = {2001:,
                             2002:, 2003:,
                             2004:, 2005:,
                             2006:, 2007:,
                             2008:, 2009:,
                             2010:, 2011:, 
                             2012:, 2013:,
                             2014:, 2015:,
                             2016:, 2017:,
                             2018:, 2019:, 
                             2020:, 2021:} 
    
    ## Sources dictionary
    
    esp_tax_coverage_sources = {2001:"",
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
    
    # Iceland
    
    ## Jurisdiction
    
    isl_tax_II_jur_I = ["Iceland"]

    ## Sectors
    
    isl_tax_II_ipcc_I = []
    
    ## Fuels
    
    isl_tax_II_fuel_I = ["Oil"]
    isl_tax_II_fuel_II = ["Oil", "Coal"]

    ## Coverage dictionaries
    isl_tax_II_jur_coverage = {2020:isl_tax_II_jur_I, 2021:isl_tax_II_jur_I}
    
    isl_tax_II_ipcc_coverage = {2020:isl_tax_II_ipcc_I, 2021:isl_tax_II_ipcc_I}     

    isl_tax_II_fuel_coverage = {2020:, 2021:} 
    
    ## Sources dictionary
    
    isl_tax_II_coverage_sources = {2020:"",
                                   2021:""}

    #----------------------------------------------------------------------------   

    # Singapore
    
    ## Gases

    sgp_tax_gas_I = [""]

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

    # Spain
    
    ## Jurisdiction
    
    esp_tax_jur_I = ["Spain"]

    ## Sectors
    
    esp_tax_ipcc_I = []

    ## Coverage dictionaries
    esp_tax_jur_coverage = {2014:esp_tax_jur_I, 2015:esp_tax_jur_I, 
                            2016:esp_tax_jur_I, 2017:esp_tax_jur_I,
                            2018:esp_tax_jur_I, 2019:esp_tax_jur_I, 
                            2020:esp_tax_jur_I, 2021:esp_tax_jur_I}
    
    esp_tax_ipcc_coverage = {2014:esp_tax_ipcc_I, 2015:esp_tax_ipcc_I,
                             2016:esp_tax_ipcc_I, 2017:esp_tax_ipcc_I,
                             2018:esp_tax_ipcc_I, 2019:esp_tax_ipcc_I, 
                             2020:esp_tax_ipcc_I, 2021:esp_tax_ipcc_I}     

    
    ## Sources dictionary
    
    esp_tax_coverage_sources = {2014:"",
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

    mex_tm_tax_gas_I = ["SF6", "HFC", "PFC"]

    ## Jurisdiction
    
    mex_tm_tax_jur_I = ["Tamaulipas"]

    ## Sectors
    
    mex_tm_tax_ipcc_I = []
    
    ## Fuels
    
    mex_tm_tax_fuel_I = []

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

    ## Gases

    mex_tm_tax_gas_I = ["SF6", "HFC", "PFC"]

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

    taxes_coverage = {"dnk_tax":{"jurisdictions":dnk_tax_jur_coverage, 
                                  "sectors":dnk_tax_ipcc_coverage,
                                  "fuels":dnk_tax_fuel_coverage},
                      "isl_tax":{"jurisdictions":isl_tax_II_jur_coverage, 
                                  "sectors":isl_tax_II_ipcc_coverage,
                                  "fuels":isl_tax_II_fuel_coverage},
                      "sgp_tax":{"jurisdictions":sgp_tax_jur_coverage, 
                                  "sectors":sgp_tax_ipcc_coverage,
                                  "fuels":sgp_tax_fuel_coverage},
                      "esp_tax":{"jurisdictions":esp_tax_jur_coverage, 
                                  "sectors":esp_tax_ipcc_coverage,
                                  "fuels":esp_tax_fuel_coverage}}
    
    taxes_coverage_sources = {"dnk_tax":dnk_coverage_sources,
                              "isl_tax_II":isl_tax_II_coverage_sources,
                              "sgp_tax":sgp_tax_coverage_sources,
                              "esp_tax":esp_tax_coverage_sources}
    
    
    data_and_sources = {"data":taxes_coverage, "sources":taxes_coverage_sources}
    
    
    return data_and_sources
    