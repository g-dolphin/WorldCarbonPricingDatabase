#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:57:58 2022

@author: gd
"""

# This script creates the files recording the tax exemption/rebate data
# Current records have been manually constructed by encoding entries in raw csv files.
# The next update of this file will code these exemptions in the dedicated section below

#--------------------------------Exemption/rebate coding-----------------------------

# 'Argentina'

tax_ex_arg_I_jur = ["Argentina"]

tax_ex_arg_I_ipcc = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                     "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F",
                     "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L",
                     "1A2M", "1A3A2", "1A3B", "1A3C", "1A3D2", "1A3E1",
                     "1A4A", "1A4B", "1A4C1", "1A4C2", "1A4C3", "1A5A",
                     "1A5B", "1A5C"]

tax_ex_arg_I_fuel = ["Coal"]

tax_ex_arg_I_jur_scope = {2019:tax_ex_arg_I_jur, 2020:tax_ex_arg_I_jur, 
                          2021:tax_ex_arg_I_jur, 2022:tax_ex_arg_I_jur}

tax_ex_arg_I_ipcc_scope = {2019:tax_ex_arg_I_ipcc, 2020:tax_ex_arg_I_ipcc, 
                           2021:tax_ex_arg_I_ipcc, 2022:tax_ex_arg_I_ipcc}

tax_ex_arg_I_fuel_scope = {2019:tax_ex_arg_I_fuel, 2020:tax_ex_arg_I_fuel, 
                           2021:tax_ex_arg_I_fuel, 2022:tax_ex_arg_I_fuel}

tax_ex_arg_I_value = {2019:0.9, 2020:0.8, 2021:0.7, 2022:0.6}

tax_ex_arg_I = {"jurisdiction": tax_ex_arg_I_jur_scope, "ipcc": tax_ex_arg_I_ipcc_scope,
                "fuel":tax_ex_arg_I_fuel_scope, "value":tax_ex_arg_I_value}

tax_ex_arg_I_source = {2019:"db(WBCPDB[2020])", 2020:"db(WBCPDB[2020])", 
                       2021:"db(WBCPDB[2020])", 2022:"db(WBCPDB[2023])",}

# 'Australia' - no exemptions

# 'Colombia' - no exemptions

# 'Chile' - no exemptions

# 'Denmark' 

tax_ex_dnk_I_jur = ["Denmark"]

tax_ex_dnk_I_ipcc = ["1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F",
                     "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L",
                     "1A2M", "1A4C1"]

tax_ex_dnk_I_fuel = ["Oil", "Natural gas", "Coal"]

tax_ex_dnk_I_jur_scope = {1992:tax_ex_dnk_I_jur}

tax_ex_dnk_I_ipcc_scope = {1992:tax_ex_dnk_I_ipcc}

tax_ex_dnk_I_fuel_scope = {1992:tax_ex_dnk_I_fuel}

tax_ex_dnk_I_value = {1992:1}

tax_ex_dnk_I = {"jurisdiction": tax_ex_dnk_I_jur_scope, "ipcc": tax_ex_dnk_I_ipcc_scope,
                "fuel":tax_ex_dnk_I_fuel_scope, "value":tax_ex_dnk_I_value}

tax_ex_dnk_I_source = {1992:"report(NC-EIN[2006])"}

# ------------------

tax_ex_dnk_II_jur = ["Denmark"]

tax_ex_dnk_II_ipcc = ["1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F",
                       "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L",
                       "1A2M", "1A4C1"]

tax_ex_dnk_II_fuel = ["Oil", "Natural gas", "Coal"]

tax_ex_dnk_II_jur_scope = {1992:tax_ex_dnk_II_jur, 1993:tax_ex_dnk_II_jur, 1994:tax_ex_dnk_II_jur,
                           1995:tax_ex_dnk_II_jur, 1996:tax_ex_dnk_II_jur, 1997:tax_ex_dnk_II_jur,
                           1998:tax_ex_dnk_II_jur, 1999:tax_ex_dnk_II_jur, 2000:tax_ex_dnk_II_jur, 
                           2001:tax_ex_dnk_II_jur, 2002:tax_ex_dnk_II_jur, 2003:tax_ex_dnk_II_jur,
                           2004:tax_ex_dnk_II_jur}

tax_ex_dnk_II_ipcc_scope = {1992:tax_ex_dnk_II_ipcc, 1993:tax_ex_dnk_II_ipcc, 1994:tax_ex_dnk_II_ipcc,
                           1995:tax_ex_dnk_II_ipcc, 1996:tax_ex_dnk_II_ipcc, 1997:tax_ex_dnk_II_ipcc,
                           1998:tax_ex_dnk_II_ipcc, 1999:tax_ex_dnk_II_ipcc, 2000:tax_ex_dnk_II_ipcc, 
                           2001:tax_ex_dnk_II_ipcc, 2002:tax_ex_dnk_II_ipcc, 2003:tax_ex_dnk_II_ipcc,
                           2004:tax_ex_dnk_II_ipcc}

tax_ex_dnk_II_fuel_scope = {1992:tax_ex_dnk_II_fuel, 1993:tax_ex_dnk_II_fuel, 1994:tax_ex_dnk_II_fuel,
                           1995:tax_ex_dnk_II_fuel, 1996:tax_ex_dnk_II_fuel, 1997:tax_ex_dnk_II_fuel,
                           1998:tax_ex_dnk_II_fuel, 1999:tax_ex_dnk_II_fuel, 2000:tax_ex_dnk_II_fuel, 
                           2001:tax_ex_dnk_II_fuel, 2002:tax_ex_dnk_II_fuel, 2003:tax_ex_dnk_II_fuel,
                           2004:tax_ex_dnk_II_fuel}

tax_ex_dnk_II_value = {1992:0.5, 1993:0.5, 1994:0.5, 1995:0.5, 
                       1996:0.5, 1997:0.5, 1998:0.5, 
                       1999:0.42, 2000:0.32, 2001:0.32, 
                       2002:0.32, 2003:0.32, 2004:0.32}

tax_ex_dnk_II = {"jurisdiction": tax_ex_dnk_II_jur_scope, "ipcc": tax_ex_dnk_II_ipcc_scope,
                 "fuel":tax_ex_dnk_II_fuel_scope, "value":tax_ex_dnk_II_value}

tax_ex_dnk_II_source_value = "report(NC-EIN[2006]); the 1996 reform introduced voluntary agreements to improve energy-efficiency, the rate recorded is for companies with a voluntary agreement"
tax_ex_dnk_II_source = {1992:tax_ex_dnk_II_source_value, 1993:tax_ex_dnk_II_source_value, 1994:tax_ex_dnk_II_source_value, 
                        1995:tax_ex_dnk_II_source_value, 1996:tax_ex_dnk_II_source_value, 1997:tax_ex_dnk_II_source_value, 
                        1998:tax_ex_dnk_II_source_value, 1999:tax_ex_dnk_II_source_value, 2000:tax_ex_dnk_II_source_value, 
                        2001:tax_ex_dnk_II_source_value, 2002:tax_ex_dnk_II_source_value, 2003:tax_ex_dnk_II_source_value, 
                        2004:tax_ex_dnk_II_source_value}

# ------------------

tax_ex_dnk_III_jur = ["Denmark"]

tax_ex_dnk_III_ipcc = ["1A4C1"]

tax_ex_dnk_III_fuel = ["Oil", "Natural gas", "Coal"]

tax_ex_dnk_III_jur_scope = {2005:tax_ex_dnk_III_jur}

tax_ex_dnk_III_ipcc_scope = {2005:tax_ex_dnk_III_ipcc}

tax_ex_dnk_III_fuel_scope = {2005:tax_ex_dnk_III_fuel}

tax_ex_dnk_III_value = {2005:0.25}

tax_ex_dnk_III = {"jurisdiction": tax_ex_dnk_III_jur_scope, "ipcc": tax_ex_dnk_III_ipcc_scope,
                 "fuel":tax_ex_dnk_III_fuel_scope, "value":tax_ex_dnk_III_value}

tax_ex_dnk_III_source_value = "report(NC-EIN[2006]); the 1996 reform introduced voluntary agreements to improve energy-efficiency, the rate recorded is for companies with a voluntary agreement"
tax_ex_dnk_III_source = {2005:tax_ex_dnk_III_source_value}

# 'Estonia' - no exemptions

# 'Finland' - no exemptions

tax_ex_fin_I_jur = ["Finland"]

tax_ex_fin_I_ipcc = ["1A3B"]

tax_ex_fin_I_fuel = ["Oil", "Natural gas", "Coal"]

tax_ex_fin_I_jur_scope = {2024:tax_ex_fin_I_jur}

tax_ex_fin_I_ipcc_scope = {2024:tax_ex_fin_I_ipcc}

tax_ex_fin_I_fuel_scope = {2024:tax_ex_fin_I_fuel}

tax_ex_fin_I_value = {2024:0.195}

tax_ex_fin_I = {"jurisdiction": tax_ex_fin_I_jur_scope, "ipcc": tax_ex_fin_I_ipcc_scope,
                "fuel":tax_ex_fin_I_fuel_scope, "value":tax_ex_fin_I_value}

tax_ex_fin_I_source = {2024:"db(WBCPDB[2024])"}

# 'France' - no exemptions

# 'Iceland' - no exemptions

# 'Ireland' - no exemptions

# 'Japan' - no exemptions

# 'Liechtenstein' - no exemptions

# 'Mexico' - no exemptions

tax_ex_mex_I_jur = ["Mexico"]

tax_ex_mex_I_ipcc = ["1A3B"]

tax_ex_mex_I_fuel = ["Oil"]

tax_ex_mex_I_jur_scope = {year:tax_ex_mex_I_jur for year in range(2022,2025)}

tax_ex_mex_I_ipcc_scope = {year:tax_ex_mex_I_ipcc for year in range(2022,2025)}

tax_ex_mex_I_fuel_scope = {year:tax_ex_mex_I_fuel for year in range(2022,2025)}

tax_ex_mex_I_value = {year:1 for year in range(2022, 2025)}

tax_ex_mex_I = {"jurisdiction": tax_ex_mex_I_jur_scope, "ipcc": tax_ex_mex_I_ipcc_scope,
                "fuel":tax_ex_mex_I_fuel_scope, "value":tax_ex_mex_I_value}

tax_ex_mex_I_source = {year:"db(WBCPDB[2024])" for year in range(2022, 2025)}

# 'Norway' - no exemptions

# 'Poland' - no exemptions

# 'Portugal'

tax_ex_prt_I_jur = ["Portugal"]

tax_ex_prt_I_ipcc = ["1A3A1"]

tax_ex_prt_I_fuel = ["Oil", "Natural gas", "Coal"]

tax_ex_prt_I_jur_scope = {2018:tax_ex_prt_I_jur}

tax_ex_prt_I_ipcc_scope = {2018:tax_ex_prt_I_ipcc}

tax_ex_prt_I_fuel_scope = {2018:tax_ex_prt_I_fuel}

tax_ex_prt_I_value = {2018:1}

tax_ex_prt_I = {"jurisdiction": tax_ex_prt_I_jur_scope, "ipcc": tax_ex_prt_I_ipcc_scope,
                "fuel":tax_ex_prt_I_fuel_scope, "value":tax_ex_prt_I_value}

tax_ex_prt_I_source = {2018:"leg(PRT[2014], PRT[2016], PRT[2018])"}

# ------------------

tax_ex_prt_II_jur = ["Portugal"]

tax_ex_prt_II_ipcc = ["1A1A1", "1A1A2", "1A1A3"]

tax_ex_prt_II_fuel = ["Coal"]

tax_ex_prt_II_jur_scope = {2018:tax_ex_prt_II_jur, 2019:tax_ex_prt_II_jur, 2020:tax_ex_prt_II_jur}

tax_ex_prt_II_ipcc_scope = {2018:tax_ex_prt_II_ipcc, 2019:tax_ex_prt_II_ipcc, 2020:tax_ex_prt_II_ipcc}

tax_ex_prt_II_fuel_scope = {2018:tax_ex_prt_II_fuel, 2019:tax_ex_prt_II_fuel, 2020:tax_ex_prt_II_fuel}

tax_ex_prt_II_value = {2018:0.9 , 2019:0.75, 2020:0.5}

tax_ex_prt_II = {"jurisdiction": tax_ex_prt_II_jur_scope, "ipcc": tax_ex_prt_II_ipcc_scope,
                "fuel":tax_ex_prt_II_fuel_scope, "value":tax_ex_prt_II_value}

tax_ex_prt_II_source = {2018:"leg(PRT[2014], PRT[2016], PRT[2018])",
                        2019:"leg(PRT[2014], PRT[2016], PRT[2018])",
                        2020:"leg(PRT[2014], PRT[2016], PRT[2018])"}

# ------------------

tax_ex_prt_III_jur = ["Portugal"]

tax_ex_prt_III_ipcc = ["1A1A1", "1A1A2", "1A1A3"]

tax_ex_prt_III_fuel = ["Coal", "Natural gas", "Oil"]

tax_ex_prt_III_jur_scope = {2021:tax_ex_prt_III_jur}

tax_ex_prt_III_ipcc_scope = {2021:tax_ex_prt_III_ipcc}

tax_ex_prt_III_fuel_scope = {2021:tax_ex_prt_III_fuel}

tax_ex_prt_III_value = {2021:0.25}

tax_ex_prt_III = {"jurisdiction": tax_ex_prt_III_jur_scope, "ipcc": tax_ex_prt_III_ipcc_scope,
                "fuel":tax_ex_prt_III_fuel_scope, "value":tax_ex_prt_III_value}

tax_ex_prt_III_source = {2021:"leg(PRT[2014], PRT[2016], PRT[2018])"}

# 'Slovenia'

tax_ex_slo_I_jur = ["Slovenia"]

tax_ex_slo_I_ipcc = ["1A1A1"]

tax_ex_slo_I_fuel = ["Coal"]

tax_ex_slo_I_jur_scope = {1996:tax_ex_slo_I_jur, 1997:tax_ex_slo_I_jur, 1998:tax_ex_slo_I_jur,
                          1999:tax_ex_slo_I_jur, 2000:tax_ex_slo_I_jur, 2001:tax_ex_slo_I_jur, 
                          2002:tax_ex_slo_I_jur, 2003:tax_ex_slo_I_jur, 2004:tax_ex_slo_I_jur, 
                          2005:tax_ex_slo_I_jur, 2006:tax_ex_slo_I_jur, 2007:tax_ex_slo_I_jur, 
                          2008:tax_ex_slo_I_jur, 2009:tax_ex_slo_I_jur, 2010:tax_ex_slo_I_jur, 
                          2011:tax_ex_slo_I_jur, 2012:tax_ex_slo_I_jur, 2013:tax_ex_slo_I_jur, 
                          2014:tax_ex_slo_I_jur, 2015:tax_ex_slo_I_jur}

tax_ex_slo_I_ipcc_scope = {1996:tax_ex_slo_I_ipcc, 1997:tax_ex_slo_I_ipcc, 1998:tax_ex_slo_I_ipcc,
                          1999:tax_ex_slo_I_ipcc, 2000:tax_ex_slo_I_ipcc, 2001:tax_ex_slo_I_ipcc, 
                          2002:tax_ex_slo_I_ipcc, 2003:tax_ex_slo_I_ipcc, 2004:tax_ex_slo_I_ipcc, 
                          2005:tax_ex_slo_I_ipcc, 2006:tax_ex_slo_I_ipcc, 2007:tax_ex_slo_I_ipcc, 
                          2008:tax_ex_slo_I_ipcc, 2009:tax_ex_slo_I_ipcc, 2010:tax_ex_slo_I_ipcc, 
                          2011:tax_ex_slo_I_ipcc, 2012:tax_ex_slo_I_ipcc, 2013:tax_ex_slo_I_ipcc, 
                          2014:tax_ex_slo_I_ipcc, 2015:tax_ex_slo_I_ipcc}

tax_ex_slo_I_fuel_scope = {1996:tax_ex_slo_I_fuel, 1997:tax_ex_slo_I_fuel, 1998:tax_ex_slo_I_fuel,
                          1999:tax_ex_slo_I_fuel, 2000:tax_ex_slo_I_fuel, 2001:tax_ex_slo_I_fuel, 
                          2002:tax_ex_slo_I_fuel, 2003:tax_ex_slo_I_fuel, 2004:tax_ex_slo_I_fuel, 
                          2005:tax_ex_slo_I_fuel, 2006:tax_ex_slo_I_fuel, 2007:tax_ex_slo_I_fuel, 
                          2008:tax_ex_slo_I_fuel, 2009:tax_ex_slo_I_fuel, 2010:tax_ex_slo_I_fuel, 
                          2011:tax_ex_slo_I_fuel, 2012:tax_ex_slo_I_fuel, 2013:tax_ex_slo_I_fuel, 
                          2014:tax_ex_slo_I_fuel, 2015:tax_ex_slo_I_fuel}

tax_ex_slo_I_value = {1996:0.5, 1997:0.5, 1998:0.5,
                      1999:0.5, 2000:0.5, 2001:0.5, 
                      2002:0.5, 2003:0.5, 2004:0.5, 
                      2005:0.5, 2006:0.5, 2007:0.5, 
                      2008:0.5, 2009:0.5, 2010:0.5, 
                      2011:0.5, 2012:0.5, 2013:0.5, 
                      2014:0.5, 2015:0.5}

tax_ex_slo_I = {"jurisdiction": tax_ex_slo_I_jur_scope, "ipcc": tax_ex_slo_I_ipcc_scope,
                "fuel":tax_ex_slo_I_fuel_scope, "value":tax_ex_slo_I_value}

tax_ex_slo_I_source_value = "leg(SLO-CO2[1996]); art. 4 of the legislation stipulates that coal used for electricity generation is subject to 50% of the base tax rate"
tax_ex_slo_I_source = {1996:tax_ex_slo_I_source_value, 1997:tax_ex_slo_I_source_value, 
                        1998:tax_ex_slo_I_source_value, 1999:tax_ex_slo_I_source_value, 2000:tax_ex_slo_I_source_value, 
                        2001:tax_ex_slo_I_source_value, 2002:tax_ex_slo_I_source_value, 2003:tax_ex_slo_I_source_value, 
                        2004:tax_ex_slo_I_source_value, 2005:tax_ex_slo_I_source_value, 2006:tax_ex_slo_I_source_value,
                        2007:tax_ex_slo_I_source_value, 2008:tax_ex_slo_I_source_value, 2009:tax_ex_slo_I_source_value,
                        2010:tax_ex_slo_I_source_value, 2011:tax_ex_slo_I_source_value, 2012:tax_ex_slo_I_source_value,
                        2013:tax_ex_slo_I_source_value, 2014:tax_ex_slo_I_source_value, 2015:tax_ex_slo_I_source_value}

# ------------------

tax_ex_slo_II_jur = ["Slovenia"]

tax_ex_slo_II_ipcc = ["4C1"]

tax_ex_slo_II_fuel = ["NA"]

tax_ex_slo_II_jur_scope = {1996:tax_ex_slo_II_jur, 1997:tax_ex_slo_II_jur, 1998:tax_ex_slo_II_jur,
                          1999:tax_ex_slo_II_jur, 2000:tax_ex_slo_II_jur, 2001:tax_ex_slo_II_jur, 
                          2002:tax_ex_slo_II_jur, 2003:tax_ex_slo_II_jur, 2004:tax_ex_slo_II_jur, 
                          2005:tax_ex_slo_II_jur, 2006:tax_ex_slo_II_jur, 2007:tax_ex_slo_II_jur, 
                          2008:tax_ex_slo_II_jur, 2009:tax_ex_slo_II_jur, 2010:tax_ex_slo_II_jur, 
                          2011:tax_ex_slo_II_jur, 2012:tax_ex_slo_II_jur, 2013:tax_ex_slo_II_jur, 
                          2014:tax_ex_slo_II_jur, 2015:tax_ex_slo_II_jur}

tax_ex_slo_II_ipcc_scope = {1996:tax_ex_slo_II_ipcc, 1997:tax_ex_slo_II_ipcc, 1998:tax_ex_slo_II_ipcc,
                          1999:tax_ex_slo_II_ipcc, 2000:tax_ex_slo_II_ipcc, 2001:tax_ex_slo_II_ipcc, 
                          2002:tax_ex_slo_II_ipcc, 2003:tax_ex_slo_II_ipcc, 2004:tax_ex_slo_II_ipcc, 
                          2005:tax_ex_slo_II_ipcc, 2006:tax_ex_slo_II_ipcc, 2007:tax_ex_slo_II_ipcc, 
                          2008:tax_ex_slo_II_ipcc, 2009:tax_ex_slo_II_ipcc, 2010:tax_ex_slo_II_ipcc, 
                          2011:tax_ex_slo_II_ipcc, 2012:tax_ex_slo_II_ipcc, 2013:tax_ex_slo_II_ipcc, 
                          2014:tax_ex_slo_II_ipcc, 2015:tax_ex_slo_II_ipcc}

tax_ex_slo_II_fuel_scope = {1996:tax_ex_slo_II_fuel, 1997:tax_ex_slo_II_fuel, 1998:tax_ex_slo_II_fuel,
                          1999:tax_ex_slo_II_fuel, 2000:tax_ex_slo_II_fuel, 2001:tax_ex_slo_II_fuel, 
                          2002:tax_ex_slo_II_fuel, 2003:tax_ex_slo_II_fuel, 2004:tax_ex_slo_II_fuel, 
                          2005:tax_ex_slo_II_fuel, 2006:tax_ex_slo_II_fuel, 2007:tax_ex_slo_II_fuel, 
                          2008:tax_ex_slo_II_fuel, 2009:tax_ex_slo_II_fuel, 2010:tax_ex_slo_II_fuel, 
                          2011:tax_ex_slo_II_fuel, 2012:tax_ex_slo_II_fuel, 2013:tax_ex_slo_II_fuel, 
                          2014:tax_ex_slo_II_fuel, 2015:tax_ex_slo_II_fuel}

tax_ex_slo_II_value = {1996:0.5, 1997:0.5, 1998:0.9,
                       1999:0.9, 2000:0.9, 2001:0.9, 
                       2002:0.9, 2003:0.9, 2004:0.9, 
                       2005:0.9, 2006:0.9, 2007:0.9, 
                       2008:0.9, 2009:0.9, 2010:0.9, 
                       2011:0.9, 2012:0.9, 2013:0.9, 
                       2014:0.9, 2015:0.9}

tax_ex_slo_II = {"jurisdiction": tax_ex_slo_II_jur_scope, "ipcc": tax_ex_slo_II_ipcc_scope,
                "fuel":tax_ex_slo_II_fuel_scope, "value":tax_ex_slo_II_value}

tax_ex_slo_II_source_value = "leg(SLO-CO2[1996], SLO-CO2[1998], SLO-CO2[2000], SLO-CO2[2002]); art. 4 of the legislation stipulates that organic compounds incinerated in refuse incineration plants are subject to 10% of the base tax rate"
tax_ex_slo_II_source = {1996:tax_ex_slo_II_source_value, 1997:tax_ex_slo_II_source_value, 
                        1998:tax_ex_slo_II_source_value, 1999:tax_ex_slo_II_source_value, 2000:tax_ex_slo_II_source_value, 
                        2001:tax_ex_slo_II_source_value, 2002:tax_ex_slo_II_source_value, 2003:tax_ex_slo_II_source_value, 
                        2004:tax_ex_slo_II_source_value, 2005:tax_ex_slo_II_source_value, 2006:tax_ex_slo_II_source_value,
                        2007:tax_ex_slo_II_source_value, 2008:tax_ex_slo_II_source_value, 2009:tax_ex_slo_II_source_value,
                        2010:tax_ex_slo_II_source_value, 2011:tax_ex_slo_II_source_value, 2012:tax_ex_slo_II_source_value,
                        2013:tax_ex_slo_II_source_value, 2014:tax_ex_slo_II_source_value, 2015:tax_ex_slo_II_source_value}

# ------------------

tax_ex_slo_III_jur = ["Slovenia"]

tax_ex_slo_III_ipcc = ["1A1A2"]

tax_ex_slo_III_fuel = ["Coal"]

tax_ex_slo_III_jur_scope = {1996:tax_ex_slo_III_jur, 1997:tax_ex_slo_III_jur}

tax_ex_slo_III_ipcc_scope = {1996:tax_ex_slo_III_ipcc, 1997:tax_ex_slo_III_ipcc}

tax_ex_slo_III_fuel_scope = {1996:tax_ex_slo_III_fuel, 1997:tax_ex_slo_III_fuel}

tax_ex_slo_III_value = {1996:0.7, 1997:0.7}

tax_ex_slo_III = {"jurisdiction": tax_ex_slo_III_jur_scope, "ipcc": tax_ex_slo_III_ipcc_scope,
                "fuel":tax_ex_slo_III_fuel_scope, "value":tax_ex_slo_III_value}

tax_ex_slo_III_source_value = "leg(SLO-CO2[1996]); art. 4 of the legislation stipulates that coal used for electricity generation is subject to 30% of the base tax rate"
tax_ex_slo_III_source = {1996:tax_ex_slo_III_source_value, 1997:tax_ex_slo_III_source_value}
# ------------------

tax_ex_slo_IV_jur = ["Slovenia"]

tax_ex_slo_IV_ipcc = ["1A1A2"]

tax_ex_slo_IV_fuel = ["Natural gas"]

tax_ex_slo_IV_jur_scope = {1998:tax_ex_slo_IV_jur, 1999:tax_ex_slo_IV_jur, 2000:tax_ex_slo_IV_jur}

tax_ex_slo_IV_ipcc_scope = {1998:tax_ex_slo_IV_ipcc, 1999:tax_ex_slo_IV_ipcc, 2000:tax_ex_slo_IV_ipcc}

tax_ex_slo_IV_fuel_scope = {1998:tax_ex_slo_IV_fuel, 1999:tax_ex_slo_IV_fuel, 2000:tax_ex_slo_IV_fuel}

tax_ex_slo_IV_value = {1998:0.3, 1999:0.3, 2000:0.3}

tax_ex_slo_IV = {"jurisdiction": tax_ex_slo_IV_jur_scope, "ipcc": tax_ex_slo_IV_ipcc_scope,
                "fuel":tax_ex_slo_IV_fuel_scope, "value":tax_ex_slo_IV_value}

tax_ex_slo_IV_source_value = "leg(SLO-CO2[1998]); art. 4 of the legislation stipulates that natural gas and liquefied petroleum gas are subject to 70% of the base tax rate"
tax_ex_slo_IV_source = {1998:tax_ex_slo_IV_source_value, 1999:tax_ex_slo_IV_source_value, 2000:tax_ex_slo_IV_source_value}

# 'Sweden'

tax_ex_swe_I_jur = ["Sweden"]

tax_ex_swe_I_ipcc = ["1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F",
                     "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L",
                     "1A2M"]

tax_ex_swe_I_fuel = ["Coal", "Natural gas", "Oil"]

tax_ex_swe_I_jur_scope = {1991:tax_ex_swe_I_jur, 1992:tax_ex_swe_I_jur, 1993:tax_ex_swe_I_jur,
                          1994:tax_ex_swe_I_jur, 1995:tax_ex_swe_I_jur, 
                          1996:tax_ex_swe_I_jur, 1997:tax_ex_swe_I_jur, 1998:tax_ex_swe_I_jur,
                          1999:tax_ex_swe_I_jur, 2000:tax_ex_swe_I_jur, 2001:tax_ex_swe_I_jur, 
                          2002:tax_ex_swe_I_jur, 2003:tax_ex_swe_I_jur, 2004:tax_ex_swe_I_jur, 
                          2005:tax_ex_swe_I_jur, 2006:tax_ex_swe_I_jur, 2007:tax_ex_swe_I_jur, 
                          2008:tax_ex_swe_I_jur, 2009:tax_ex_swe_I_jur, 2010:tax_ex_swe_I_jur}

tax_ex_swe_I_ipcc_scope = {1991:tax_ex_swe_I_ipcc, 1992:tax_ex_swe_I_ipcc, 1993:tax_ex_swe_I_ipcc,
                          1994:tax_ex_swe_I_ipcc, 1995:tax_ex_swe_I_ipcc, 
                          1996:tax_ex_swe_I_ipcc, 1997:tax_ex_swe_I_ipcc, 1998:tax_ex_swe_I_ipcc,
                          1999:tax_ex_swe_I_ipcc, 2000:tax_ex_swe_I_ipcc, 2001:tax_ex_swe_I_ipcc, 
                          2002:tax_ex_swe_I_ipcc, 2003:tax_ex_swe_I_ipcc, 2004:tax_ex_swe_I_ipcc, 
                          2005:tax_ex_swe_I_ipcc, 2006:tax_ex_swe_I_ipcc, 2007:tax_ex_swe_I_ipcc, 
                          2008:tax_ex_swe_I_ipcc, 2009:tax_ex_swe_I_ipcc, 2010:tax_ex_swe_I_ipcc}

tax_ex_swe_I_fuel_scope = {1991:tax_ex_swe_I_fuel, 1992:tax_ex_swe_I_fuel, 1993:tax_ex_swe_I_fuel,
                          1994:tax_ex_swe_I_fuel, 1995:tax_ex_swe_I_fuel,
                          1996:tax_ex_swe_I_fuel, 1997:tax_ex_swe_I_fuel, 1998:tax_ex_swe_I_fuel,
                          1999:tax_ex_swe_I_fuel, 2000:tax_ex_swe_I_fuel, 2001:tax_ex_swe_I_fuel, 
                          2002:tax_ex_swe_I_fuel, 2003:tax_ex_swe_I_fuel, 2004:tax_ex_swe_I_fuel, 
                          2005:tax_ex_swe_I_fuel, 2006:tax_ex_swe_I_fuel, 2007:tax_ex_swe_I_fuel, 
                          2008:tax_ex_swe_I_fuel, 2009:tax_ex_swe_I_fuel, 2010:tax_ex_swe_I_fuel}

tax_ex_swe_I_value = {1991:0.75, 1992:0.75, 
                      1993:0.75, 1994:0.75, 1995:0.75,
                      1996:0.75, 1997:0.5, 1998:0.5,
                      1999:0.5, 2000:0.5, 2001:0.65, 
                      2002:0.7, 2003:0.75, 2004:0.79, 
                      2005:0.79, 2006:0.79, 2007:0.79, 
                      2008:0.85, 2009:0.85, 2010:0.85}

tax_ex_swe_I = {"jurisdiction": tax_ex_swe_I_jur_scope, "ipcc": tax_ex_swe_I_ipcc_scope,
                "fuel":tax_ex_swe_I_fuel_scope, "value":tax_ex_swe_I_value}

tax_ex_swe_I_source_value = "report(SMF-CT[2011])"
tax_ex_swe_I_source = {1991:tax_ex_swe_I_source_value,
                        1992:tax_ex_swe_I_source_value, 1993:tax_ex_swe_I_source_value, 1994:tax_ex_swe_I_source_value, 
                        1995:tax_ex_swe_I_source_value, 1996:tax_ex_swe_I_source_value, 1997:tax_ex_swe_I_source_value, 
                        1998:tax_ex_swe_I_source_value, 1999:tax_ex_swe_I_source_value, 2000:tax_ex_swe_I_source_value, 
                        2001:tax_ex_swe_I_source_value, 2002:tax_ex_swe_I_source_value, 2003:tax_ex_swe_I_source_value,
                        2004:tax_ex_swe_I_source_value, 2005:tax_ex_swe_I_source_value, 2006:tax_ex_swe_I_source_value, 
                        2007:tax_ex_swe_I_source_value, 2008:tax_ex_swe_I_source_value, 2009:tax_ex_swe_I_source_value, 
                        2010:tax_ex_swe_I_source_value}

# ------------------

tax_ex_swe_II_jur = ["Sweden"]

tax_ex_swe_II_ipcc = ["1A4C1"]

tax_ex_swe_II_fuel = ["Coal", "Natural gas", "Oil"]

tax_ex_swe_II_jur_scope = {2000:tax_ex_swe_II_jur, 2001:tax_ex_swe_II_jur, 
                          2002:tax_ex_swe_II_jur, 2003:tax_ex_swe_II_jur, 2004:tax_ex_swe_II_jur, 
                          2005:tax_ex_swe_II_jur, 2006:tax_ex_swe_II_jur, 2007:tax_ex_swe_II_jur, 
                          2008:tax_ex_swe_II_jur, 2009:tax_ex_swe_II_jur, 2010:tax_ex_swe_II_jur,
                          2011:tax_ex_swe_II_jur, 2012:tax_ex_swe_II_jur, 2013:tax_ex_swe_II_jur,
                          2014:tax_ex_swe_II_jur, 2015:tax_ex_swe_II_jur, 2016:tax_ex_swe_II_jur,
                          2017:tax_ex_swe_II_jur, 2018:tax_ex_swe_II_jur, 2019:tax_ex_swe_II_jur,
                          2020:tax_ex_swe_II_jur, 2021:tax_ex_swe_II_jur}

tax_ex_swe_II_ipcc_scope = {2000:tax_ex_swe_II_ipcc, 2001:tax_ex_swe_II_ipcc, 
                           2002:tax_ex_swe_II_ipcc, 2003:tax_ex_swe_II_ipcc, 2004:tax_ex_swe_II_ipcc, 
                           2005:tax_ex_swe_II_ipcc, 2006:tax_ex_swe_II_ipcc, 2007:tax_ex_swe_II_ipcc, 
                           2008:tax_ex_swe_II_ipcc, 2009:tax_ex_swe_II_ipcc, 2010:tax_ex_swe_II_ipcc,
                           2011:tax_ex_swe_II_ipcc, 2012:tax_ex_swe_II_ipcc, 2013:tax_ex_swe_II_ipcc,
                           2014:tax_ex_swe_II_ipcc, 2015:tax_ex_swe_II_ipcc, 2016:tax_ex_swe_II_ipcc,
                           2017:tax_ex_swe_II_ipcc, 2018:tax_ex_swe_II_ipcc, 2019:tax_ex_swe_II_ipcc,
                           2020:tax_ex_swe_II_ipcc, 2021:tax_ex_swe_II_ipcc}

tax_ex_swe_II_fuel_scope = {2000:tax_ex_swe_II_fuel, 2001:tax_ex_swe_II_fuel, 
                          2002:tax_ex_swe_II_fuel, 2003:tax_ex_swe_II_fuel, 2004:tax_ex_swe_II_fuel, 
                          2005:tax_ex_swe_II_fuel, 2006:tax_ex_swe_II_fuel, 2007:tax_ex_swe_II_fuel, 
                          2008:tax_ex_swe_II_fuel, 2009:tax_ex_swe_II_fuel, 2010:tax_ex_swe_II_fuel,
                          2008:tax_ex_swe_II_fuel, 2009:tax_ex_swe_II_fuel, 2010:tax_ex_swe_II_fuel,
                          2011:tax_ex_swe_II_fuel, 2012:tax_ex_swe_II_fuel, 2013:tax_ex_swe_II_fuel,
                          2014:tax_ex_swe_II_fuel, 2015:tax_ex_swe_II_fuel, 2016:tax_ex_swe_II_fuel,
                          2017:tax_ex_swe_II_fuel, 2018:tax_ex_swe_II_fuel, 2019:tax_ex_swe_II_fuel,
                          2020:tax_ex_swe_II_fuel, 2021:tax_ex_swe_II_fuel}

tax_ex_swe_II_value = {2000:0.5, 2001:0.65, 
                      2002:0.7, 2003:0.75, 2004:0.79, 
                      2005:0.79, 2006:0.79, 2007:0.79, 
                      2008:0.79, 2009:0.79, 2010:0.79,
                      2011:0.7, 2012:0.7, 2013:0.7,
                      2014:0.7, 2015:0.7, 2016:0.7,
                      2017:0.7, 2018:0.7, 2019:0.7,
                      2020:0.7, 2021:0.7}

tax_ex_swe_II = {"jurisdiction": tax_ex_swe_II_jur_scope, "ipcc": tax_ex_swe_II_ipcc_scope,
                "fuel":tax_ex_swe_II_fuel_scope, "value":tax_ex_swe_II_value}

tax_ex_swe_II_source_value = "report(SMF-CT[2011]); extrapolation from 2011 onward"
tax_ex_swe_II_source = {2000:tax_ex_swe_II_source_value, 2001:tax_ex_swe_II_source_value, 2002:tax_ex_swe_II_source_value, 
                        2003:tax_ex_swe_II_source_value, 2004:tax_ex_slo_IV_source_value, 2005:tax_ex_slo_IV_source_value,
                        2006:tax_ex_swe_II_source_value, 2007:tax_ex_slo_IV_source_value, 2008:tax_ex_slo_IV_source_value,
                        2009:tax_ex_swe_II_source_value, 2010:tax_ex_slo_IV_source_value, 2011:tax_ex_slo_IV_source_value,
                        2012:tax_ex_swe_II_source_value, 2013:tax_ex_slo_IV_source_value, 2014:tax_ex_slo_IV_source_value,
                        2015:tax_ex_swe_II_source_value, 2016:tax_ex_slo_IV_source_value, 2017:tax_ex_slo_IV_source_value,
                        2018:tax_ex_swe_II_source_value, 2019:tax_ex_slo_IV_source_value, 2020:tax_ex_slo_IV_source_value, 
                        2021:tax_ex_slo_IV_source_value}

# 'Switzerland' - no exemptions

# 'United Kingdom' - no exemptions

# Canada - British Columbia

tax_ex_can_bc_I_jur = ["British Columbia"]

tax_ex_can_bc_I_ipcc = ["1A4C1"]

tax_ex_can_bc_I_fuel = ["Oil"]

tax_ex_can_bc_I_jur_scope = {2014:tax_ex_can_bc_I_jur, 2015:tax_ex_can_bc_I_jur, 2016:tax_ex_can_bc_I_jur,
                             2017:tax_ex_can_bc_I_jur, 2018:tax_ex_can_bc_I_jur, 2019:tax_ex_can_bc_I_jur,
                             2020:tax_ex_can_bc_I_jur, 2021:tax_ex_can_bc_I_jur}

tax_ex_can_bc_I_ipcc_scope = {2014:tax_ex_can_bc_I_ipcc, 2015:tax_ex_can_bc_I_ipcc, 2016:tax_ex_can_bc_I_ipcc,
                             2017:tax_ex_can_bc_I_ipcc, 2018:tax_ex_can_bc_I_ipcc, 2019:tax_ex_can_bc_I_ipcc,
                             2020:tax_ex_can_bc_I_ipcc, 2021:tax_ex_can_bc_I_ipcc}

tax_ex_can_bc_I_fuel_scope = {2014:tax_ex_can_bc_I_fuel, 2015:tax_ex_can_bc_I_fuel, 2016:tax_ex_can_bc_I_fuel,
                             2017:tax_ex_can_bc_I_fuel, 2018:tax_ex_can_bc_I_fuel, 2019:tax_ex_can_bc_I_fuel,
                             2020:tax_ex_can_bc_I_fuel, 2021:tax_ex_can_bc_I_fuel}

tax_ex_can_bc_I_value = {2014:1, 2015:1, 2016:1, 
                        2017:1, 2018:1, 2019:1, 
                        2020:1, 2021:1}

tax_ex_can_bc_I = {"jurisdiction": tax_ex_can_bc_I_jur_scope, "ipcc": tax_ex_can_bc_I_ipcc_scope,
                "fuel":tax_ex_can_bc_I_fuel_scope, "value":tax_ex_can_bc_I_value}

tax_ex_can_bc_I_source = {2014:"report(WB[2014])", 2015:"report(WB[2014])", 2016:"report(WB[2014])", 
                          2017:"report(WB[2014])", 2018:"report(WB[2014])", 2019:"report(WB[2014])", 
                          2020:"report(WB[2014])", 2021:"report(WB[2014])"}

# Canada - Alberta

tax_ex_can_ab_I_jur = ["Alberta"]

tax_ex_can_ab_I_ipcc = ["1A4C1"]

tax_ex_can_ab_I_fuel = ["Coal", "Natural gas", "Oil"]

tax_ex_can_ab_I_jur_scope = {2014:tax_ex_can_ab_I_jur, 2015:tax_ex_can_ab_I_jur, 2016:tax_ex_can_ab_I_jur}

tax_ex_can_ab_I_ipcc_scope = {2014:tax_ex_can_ab_I_ipcc, 2015:tax_ex_can_ab_I_ipcc, 2016:tax_ex_can_ab_I_ipcc}

tax_ex_can_ab_I_fuel_scope = {2014:tax_ex_can_ab_I_fuel, 2015:tax_ex_can_ab_I_fuel, 2016:tax_ex_can_ab_I_fuel}

tax_ex_can_ab_I_value = {2014:1, 2015:1, 2016:1}

tax_ex_can_ab_I = {"jurisdiction":tax_ex_can_ab_I_jur_scope, "ipcc": tax_ex_can_ab_I_ipcc_scope,
                   "fuel":tax_ex_can_ab_I_fuel_scope, "value":tax_ex_can_ab_I_value}

tax_ex_can_ab_I_source = {2014:"web(ALB[2019])", 2015:"web(ALB[2019])", 2016:"web(ALB[2019])"}
#-------------------------------------------------------------------------------------

tax_exemptions = [tax_ex_arg_I, tax_ex_dnk_I, tax_ex_dnk_II, tax_ex_dnk_III, 
                  tax_ex_prt_I, tax_ex_prt_II, tax_ex_prt_II, tax_ex_slo_I,
                  tax_ex_slo_II, tax_ex_slo_III, tax_ex_slo_IV, tax_ex_swe_I,
                  tax_ex_swe_II, tax_ex_can_bc_I, tax_ex_can_ab_I]

tax_exemptions_sources = [tax_ex_arg_I_source, tax_ex_dnk_I_source, tax_ex_dnk_II_source, tax_ex_dnk_III_source, 
                          tax_ex_prt_I_source, tax_ex_prt_II_source, tax_ex_prt_II_source, tax_ex_slo_I_source,
                          tax_ex_slo_II_source, tax_ex_slo_III_source, tax_ex_slo_IV_source, tax_ex_swe_I_source,
                          tax_ex_swe_II_source, tax_ex_can_bc_I_source, tax_ex_can_ab_I_source]
