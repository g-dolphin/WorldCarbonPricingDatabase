#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 07:54:30 2021

@author: gd
"""
# mechanism scope sources to be checked: Switzerland, Denmark, Canadian Provinces (New Brunswick), Estonia, Ireland

def scope():    
    # Argentina
    
    ## Jurisdiction
    
    arg_tax_jur_I = ["Argentina"]

    ## IPCC categories
    
    arg_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                      "1A3B", "1A3C", "1A3D2", "1A3E1", "1A4A", "1A4B",
                      "1A4C1", "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C"]
    
    ## Fuels
    
    arg_tax_fuel_I = ["Oil"]
    arg_tax_fuel_II = ["Oil", "Coal"]

    ## scope dictionaries
    arg_tax_jur_scope = {year: arg_tax_jur_I for year in range(2018, 2025)}
    
    arg_tax_ipcc_scope = {year: arg_tax_ipcc_I for year in range(2018, 2025)}     

    arg_tax_fuel_scope = {2018: arg_tax_fuel_I}
    arg_tax_fuel_scope.update({year: arg_tax_fuel_II for year in range(2019, 2025)})

    ## Sources dictionary
    
    arg_tax_scope_sources = {2018:"leg(AR[2017),report(WB[2018]])", 
                             2019:"leg(AR[2017),report(WB[2018]])", 
                             2020:"leg(AR[2017),report(WB[2018]])",
                             2021:"leg(AR[2017),report(WB[2018]])",
                             2022:"leg(AR[2017),db(WBCPD[2023]])",
                             2023:"leg(AR[2017),db(WBCPD[2024]])", 
                             2024:"leg(AR[2017),db(WBCPD[2024]])"}

    
    #----------------------------------------------------------------------------
    
    # Australia (Carbon price mechanism)
    
    ## Jurisdiction
    
    aus_tax_jur_I = ["Australia"]

    ## IPCC categories
    
    aus_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C",
                      "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                      "1A2K", "1A2L", "1A2M"]
    
    ## Fuels
    
    aus_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    aus_tax_jur_scope = {2012:aus_tax_jur_I, 2013:aus_tax_jur_I, 
                            2014:aus_tax_jur_I}
    
    aus_tax_ipcc_scope = {2012:aus_tax_ipcc_I, 2013:aus_tax_ipcc_I, 
                             2014:aus_tax_ipcc_I}     

    aus_tax_fuel_scope = {2012:aus_tax_fuel_I, 2013:aus_tax_fuel_I, 
                             2014:aus_tax_fuel_I} 
    
    ## Sources dictionary
    
    aus_tax_scope_sources = {2012:"leg(AU-NGER[2011]),db(AU-CER-LEPID[2012])", 
                                2013:"leg(AU-NGER[2011]),db(AU-CER-LEPID[2013])", 
                                2014:"leg(AU-NGER[2011]),db(AU-CER-LEPID[2013])"}

    
    #----------------------------------------------------------------------------
   
    # Chile
    
    ## Jurisdiction
    
    chl_tax_jur_I = ["Chile"]

    ## IPCC categories
    
    chl_tax_ipcc_I = ["1A1A1", "1A2A",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M"]
    
    ## Fuels
    
    chl_tax_fuel_I = ["Oil", "Coal", "Natural gas"]

    ## scope dictionaries
    chl_tax_jur_scope = {year:chl_tax_jur_I for year in range(2017, 2025)}

    chl_tax_ipcc_scope = {year:chl_tax_ipcc_I for year in range(2017, 2025)}

    chl_tax_fuel_scope = {year:chl_tax_fuel_I for year in range(2017, 2025)}

    ## Sources dictionary
    
    chl_tax_scope_sources = {2017:"report(WB[2017])", 2018:"report(WB[2018])", 
                             2019:"report(WB[2018])", 2020:"report(WB[2018])",
                             2021:"report(WB[2021])", 2022:"db(WBCPD[2023])",
                             2023:"report(WB[2024])", 2024:"db(WBCPD[2024])"}
    
    #----------------------------------------------------------------------------

    # Baja California (mex_bc_tax) - currently inactive.

    ## Jurisdiction
    
    mex_bc_tax_jur_I = ["Baja California"]

    ## IPCC categories
    
    mex_bc_tax_ipcc_I = []
    
    ## Fuels
    
    mex_bc_tax_fuel_I = []

    ## scope dictionaries
    mex_bc_tax_jur_scope = {} #2020:
    
    mex_bc_tax_ipcc_scope = {} #2020:    

    mex_bc_tax_fuel_scope = {} #2020:
    
    ## Sources dictionary
    
    mex_bc_tax_scope_sources = {} #2020:

    #----------------------------------------------------------------------------
    
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

    # transition of large emitters to OBPS
    can_bc_tax_ipcc_II = ["1A3A2", "1A3B", "1A3C",
                         "1A3D2", "1A3E1", "1A4A", "1A4B", "1A4C1",
                         "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C"]

    ## Fuels
    
    can_bc_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_bc_tax_jur_scope = {year:can_bc_tax_jur_I for year in range(2008, 2025)}
    can_bc_tax_jur_scope.update({2024: can_bc_tax_jur_I})

    can_bc_tax_ipcc_scope = {year:can_bc_tax_ipcc_I for year in range(2008, 2024)}
    can_bc_tax_ipcc_scope.update({2024: can_bc_tax_ipcc_II})

    can_bc_tax_fuel_scope = {year:can_bc_tax_fuel_I for year in range(2008, 2025)}

    ## Sources dictionary
    
    can_bc_tax_scope_sources = {year:"leg(BC-CTA[2008]), gvt(BCGOV[2021])" for year in range(2008, 2024)}
    can_bc_tax_scope_sources.update({2025:"leg(BC-CTA[2008]), gvt(BCGOV[2024]), gvt(BCGOV[2025])"})
    

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
    
    col_tax_jur_scope = {year:col_tax_jur_I for year in range(2017, 2025)}
    
    col_tax_ipcc_scope = {year:col_tax_ipcc_I for year in range(2017, 2025)}

    col_tax_fuel_scope = {year:col_tax_fuel_I for year in range(2017, 2024)}
    col_tax_fuel_scope[2024] = col_tax_fuel_II   

    ## Sources dictionary
    
    col_tax_scope_sources = {year:"report(OECD-TEU-COL[2019]),gvt(COL-DIAN[2017])" for year in range(2017, 2022)}
    col_tax_scope_sources[2022] = "report(OECD-TEU-COL[2019]),gvt(COL-DIAN[2017]), db(WBCPD[2023])"
    col_tax_scope_sources.update({year: "gvt(COL-DIAN[2022]), db(WBCPD[2024])" for year in range(2023, 2025)})                        

    #----------------------------------------------------------------------------

    # Denmark
    
    ## Jurisdictions    
    
    dnk_tax_jur_I = ["Denmark"]
    
    ## IPCC categories
    dnk_tax_ipcc_I = ["1A1A1", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                        "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                        "1A2K", "1A2L", "1A2M", "1A3B", "1A4A", "1A4B",
                        "1A4C1"]

    dnk_tax_ipcc_II = ["1A1A3", "1A1B", "1A1C", "1A3B", "1A4A", "1A4B",
                        "1A4C1"]        
    
    ## Fuels

    dnk_tax_I_fuel_I = ["Oil", "Coal", "Natural gas"]      
    
    ## scope dictionaries

    dnk_tax_jur_scope = {year:dnk_tax_jur_I for year in range(1992, 2025)}

    dnk_tax_ipcc_scope = {year:dnk_tax_ipcc_I for year in range(1992, 2005)}
    dnk_tax_ipcc_scope.update({year: dnk_tax_ipcc_II for year in range(2005, 2025)})
    
    dnk_tax_fuel_scope = {year: dnk_tax_I_fuel_I for year in range(1992, 2025)}
    
    ## Sources dictionary
    
    dnk_tax_scope_sources = {year: "journal(WIE[2005]), report(NBER[2009], NC-EIN[2006], IEA-DK[2002])" for year in range(1992, 2022)}
    dnk_tax_scope_sources.update({year: "db(WBCPD[2023])" for year in range(2022, 2025)})

    #----------------------------------------------------------------------------
    
    # dgango (Mexico)
    
    ## Gases covered: All 
    
    mex_dg_tax_jur_I = ["dgango"]
    
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
    mex_dg_tax_jur_scope = {year: mex_dg_tax_jur_I for year in range(2023, 2025)}
    
    mex_dg_tax_ipcc_scope = {year: mex_dg_tax_ipcc_I for year in range(2024, 2025)}  

    mex_dg_tax_fuel_scope = {year: mex_dg_tax_fuel_I for year in range(2024, 2025)}
    
    mex_dg_tax_scope_sources = {year:"rep(MEX-dg[2023]), leg(MEX-dg[2022])" for year in range(2022, 2025)}
      
    #----------------------------------------------------------------------------
    
    # Estonia
    
    ## Jurisdiction
    
    est_tax_jur_I = ["Estonia"]

    ## IPCC categories
    
    # initial scope
    est_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", 
                      "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                      "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M"]

    ## Fuels
    
    est_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    est_tax_jur_scope = {year:est_tax_jur_I for year in range(2000, 2025)}
    
    est_tax_ipcc_scope = {year:est_tax_ipcc_I for year in range(2000, 2025)}
    
    est_tax_fuel_scope = {year:est_tax_fuel_I for year in range(2000, 2025)}

    ## Sources dictionary
    
    est_tax_scope_sources = {2000:"",
                              2001:"", 2002:"", 2003:"",
                              2004:"", 2005:"report(EST-SE[2009]) ", 
                              2006:"report(EST-SE[2009])",
                              2007:"report(EST-SE[2009])", 
                              2008:"report(EST-SE[2009])", 
                              2009:"report(EST-SE[2009])",
                              2010:"report(EST-SE[2009])", 
                              2011:"leg(EST-ECA[2005])", 
                              2012:"leg(EST-ECA[2005])",
                              2013:"leg(EST-ECA[2005])", 
                              2014:"leg(EST-ECA[2005])", 
                              2015:"leg(EST-ECA[2005])", 
                              2016:"leg(EST-ECA[2005]), report(OECD[2019]), db(WBCPD[2020])",
                              2017:"leg(EST-ECA[2005]), report(OECD[2019]), db(WBCPD[2020])", 
                              2018:"leg(EST-ECA[2005]), report(OECD[2019]), db(WBCPD[2020])", 
                              2019:"leg(EST-ECA[2005]), report(OECD[2019]), db(WBCPD[2020])", 
                              2020:"leg(EST-ECA[2005]), report(OECD[2019]), db(WBCPD[2020])",
                              2021:"",
                              2022:"db(WBCPD[2023])", 
                              2023:" ",
                              2024:" "}

    #----------------------------------------------------------------------------

    # Finland
    
    ## Jurisdictions    
    
    fin_tax_jur_I = ["Finland"]
    
    ## IPCC categories
    fin_tax_ipcc_I = ["1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                      "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                      "1A2K", "1A2L", "1A2M", "1A3A2", "1A3B",
                      "1A4A", "1A4B", "1A4C1", "1A4C2"]

    fin_tax_ipcc_II = ["1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                       "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                       "1A2K", "1A2L", "1A2M", "1A3A2", "1A3B", 
                       "1A4A", "1A4B", "1A4C1", "1A4C2"]

    ## Fuels

    fin_tax_I_fuel_I = ["Oil", "Coal", "Natural gas"]      
    
    ## scope dictionaries

    fin_tax_jur_scope = {year:fin_tax_jur_I for year in range(1990, 2025)}

    fin_tax_ipcc_scope = {year:fin_tax_ipcc_I for year in range(1990, 2005)}
    fin_tax_ipcc_scope.update({year: fin_tax_ipcc_II for year in range(2005, 2025)})
    
    fin_tax_fuel_scope = {year:fin_tax_I_fuel_I for year in range(1990, 2025)}

    ## Sources dictionary
    
    fin_tax_scope_sources = {year:"report(IEA-EPT[2015],WB[2014]),journal(VEH[2005]),web(USEPA[2015])" for year in range(1990, 2022)}
    fin_tax_scope_sources.update({year: "db(WBCPD[2023]), db(WBCPD[2024])" for year in range(2022,2025)})

    #----------------------------------------------------------------------------

    # France
    
    ## Jurisdiction
    
    fra_tax_jur_I = ["France"]

    ## IPCC categories
    
    # initial scope
    fra_tax_ipcc_I = ["1A1B", "1A1C",
                                "1A4A", "1A4B"]

    # extension to road transport (2015)
    fra_tax_ipcc_II = ["1A1B", "1A1C", "1A3B",
                      "1A4A", "1A4B"]

    ## Fuels
    
    fra_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    fra_tax_jur_scope = {year:fra_tax_jur_I for year in range(2014, 2025)}
    
    fra_tax_ipcc_scope = {2014: fra_tax_ipcc_I}
    fra_tax_ipcc_scope.update({year: fra_tax_ipcc_II for year in range(2015, 2025)})
    
    fra_tax_fuel_scope = {year:fra_tax_fuel_I for year in range(2014, 2025)}

    ## Sources dictionary
    
    fra_tax_scope_sources = {2014:"report(WB[2017]),news(LE-FRA[2020]),gvt(FRA[2019])"}
    fra_tax_scope_sources.update({year: "report(WB[2017]),news(LE-FRA[2020]),gvt(FRA[2019]),leg(FRA[2014])" for year in range(2015, 2021)})
    fra_tax_scope_sources[2021] = "db(WBCPD[2023]),gvt(FRA[2019]),leg(FRA[2014])"
    fra_tax_scope_sources[2022] = "db(WBCPD[2023])"
    fra_tax_scope_sources[2023] = "db(WBCPD[2024])"
    fra_tax_scope_sources[2024] = "db(WBCPD[2024])"

    #----------------------------------------------------------------------------

    # Hungary
    
    ## Jurisdiction
    
    hun_tax_jur_I = ["Hungary"]

    ## IPCC categories
    
    hun_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", 
                      "1C1A", "1C2B",
                      "2A1", "2A2", "2A3", "2A4A", "2B1", "2B2", "2B3", 
                      "2B4", "2B5", "2B6", "2B7", "2B8F",
                      "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", "2H1"]
    
    ## Fuels
    
    hun_tax_fuel_I = ["Oil", "Coal", "Natural gas"]

    ## scope dictionaries
    hun_tax_jur_scope = {year: hun_tax_jur_I for year in range(2023, 2025)}
    
    hun_tax_ipcc_scope = {year: hun_tax_ipcc_I for year in range(2023, 2025)}     

    hun_tax_fuel_scope = {year: hun_tax_fuel_I for year in range(2023, 2025)}

    ## Sources dictionary
    
    hun_tax_scope_sources = {year: " " for year in range(2023, 2025)}

    #----------------------------------------------------------------------------

    # Iceland
    
    ## Jurisdiction
    
    isl_tax_jur_I = ["Iceland"]

    ## IPCC categories
    
    # initial scope
    isl_tax_ipcc_I = ["1A1B", "1A1C", "1A3B", "1A4A", "1A4B", 
                      "1A4C1", "1A4C2"]

    ## Fuels
    
    isl_tax_fuel_I = ["Oil"]

    isl_tax_fuel_II = ["Oil", "Natural gas"]

    ## scope dictionaries
    
    isl_tax_jur_scope = {year:isl_tax_jur_I for year in range(2010, 2025)}
    
    isl_tax_ipcc_scope = {year:isl_tax_ipcc_I for year in range(2010, 2025)}
    
    isl_tax_fuel_scope = {year: isl_tax_fuel_I for year in range(2010, 2013)}
    isl_tax_fuel_scope.update({year: isl_tax_fuel_II for year in range(2013, 2025)})                       

    ## Sources dictionary
    
    isl_tax_scope_sources = {year: "leg(ISL-ENRTA[2009])" for year in range(2010, 2023)} 
    isl_tax_scope_sources.update({year: "leg(ISL-ENRTA[2009]), db(WBCPD[2024])" for year in range(2023, 2025)})

    #----------------------------------------------------------------------------

    # Ireland
    
    ## Jurisdiction
    
    irl_tax_jur_I = ["Ireland"]

    ## IPCC categories
    
    # initial scope
    irl_tax_ipcc_I = ["1A3A2", "1A3B", "1A3D1", 
                      "1A3D1", "1A3D2", "1A3E1", "1A4A", "1A4B", "1A4C1"]

    ## Fuels
    
    irl_tax_fuel_I = ["Oil", "Natural gas"]
    irl_tax_fuel_II = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    irl_tax_jur_scope = {year: irl_tax_jur_I for year in range(2010, 2025)}
    
    irl_tax_ipcc_scope = {year: irl_tax_ipcc_I for year in range(2010, 2025)}
    
    irl_tax_fuel_scope = {year: irl_tax_fuel_I for year in range(2010, 2013)}
    irl_tax_fuel_scope.update({year: irl_tax_fuel_II for year in range(2013, 2015)})
    irl_tax_fuel_scope[2015] = irl_tax_fuel_I
    irl_tax_fuel_scope.update({year: irl_tax_fuel_II for year in range(2016, 2025)}) 

    ## Sources dictionary
    
    irl_tax_scope_sources = {year:"leg(IRL-FA[2010])" for year in range(2010, 2025)}

    #----------------------------------------------------------------------------

    # Japan
    
    ## Jurisdiction
    
    jpn_tax_jur_I = ["Japan"]

    ## IPCC categories
    
    # initial scope
    jpn_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3",
                      "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                      "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M",
                      "1A3B"]

    ## Fuels
    
    jpn_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    jpn_tax_jur_scope = {year: jpn_tax_jur_I for year in range(2012, 2025)}
    
    jpn_tax_ipcc_scope = {year: jpn_tax_ipcc_I for year in range(2012, 2025)}
    
    jpn_tax_fuel_scope = {year:jpn_tax_fuel_I for year in range(2012, 2025)}
    
    ## Sources dictionary
    
    jpn_tax_scope_sources = {year: "leg(JP[2012]), gvt(MEJ-CT[2014])" for year in range(2012, 2025)}

    #----------------------------------------------------------------------------

    # Latvia
    
    ## Jurisdiction
    
    lva_tax_jur_I = ["Latvia"]

    ## IPCC categories
    
    # initial scope
    lva_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", 
                      "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                      "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M"]

    ## Fuels
    
    lva_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    lva_tax_jur_scope = {year:lva_tax_jur_I for year in range(2004, 2025)}
    
    lva_tax_ipcc_scope = {year:lva_tax_ipcc_I for year in range(2004, 2025)}
    
    lva_tax_fuel_scope = {year:lva_tax_fuel_I for year in range(2004, 2025)}

    ## Sources dictionary
    
    lva_tax_scope_sources = {year:"leg(LV-NRTL[2005])" for year in range(2004, 2025)}

    #----------------------------------------------------------------------------

    # Liechtenstein
    
    ## Jurisdiction
    
    lie_tax_jur_I = ["Liechtenstein"]

    ## IPCC categories
    
    # initial scope
    lie_tax_ipcc_I = ["1A1A2", "1A1A3", "1A4B"]

    ## Fuels
    
    lie_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    lie_tax_jur_scope = {year:lie_tax_jur_I for year in range(2008, 2025)}

    lie_tax_ipcc_scope = {year:lie_tax_ipcc_I for year in range(2008, 2025)}
    
    lie_tax_fuel_scope = {year:lie_tax_fuel_I for year in range(2008, 2025)}
    
    ## Sources dictionary
    
    lie_tax_scope_sources = {year:"gvt(CH[2005], CH[2009])" for year in range(2008, 2014)}
    lie_tax_scope_sources.update({year: "leg(CHE-CO2[2013], CHE-FARC[2013])" for year in range(2014, 2025)})

    #----------------------------------------------------------------------------

    # Luxembourg

    ## Jurisdiction
    
    lux_tax_jur_I = ["Luxembourg"]

    ## IPCC categories
    
    lux_tax_ipcc_I = ["1A1B", "1A1C", "1A3A1", "1A3A2",
                      "1A3B", "1A3C", "1A3D1", "1A3D2",
                      "1A4A", "1A4B", "1A4C1", "1A4C2", "1A4C3"]
    
    ## Fuels
    
    lux_tax_fuel_I = ["Oil", "Natural gas"]

    ## scope dictionaries
    lux_tax_jur_scope = {year: lux_tax_jur_I for year in range(2021, 2025)}
    
    lux_tax_ipcc_scope = {year: lux_tax_ipcc_I for year in range(2021, 2025)}

    lux_tax_fuel_scope = {year: lux_tax_fuel_I for year in range(2021, 2025)}
    
    ## Sources dictionary
    
    lux_tax_scope_sources = {year:"leg()" for year in range(2021, 2025)} 
    
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
    

    # Netherlands

    ## Jurisdiction
    
    nld_tax_jur_I = ["Netherlands"]

    ## IPCC categories
    
    nld_tax_ipcc_I = ["1A1B", "1A1C", "1A2A", "1A2B", "1A2C", "1A2D",
                      "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                      "1A2K", "1A2L", "1A2M"]
    
    ## Fuels
    
    nld_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    nld_tax_jur_scope = {year:nld_tax_jur_I for year in range(2021,2025)} 
    
    nld_tax_ipcc_scope = {year:nld_tax_ipcc_I for year in range(2021,2025)}   

    nld_tax_fuel_scope = {year:nld_tax_fuel_I for year in range(2021,2025)}
    
    ## Sources dictionary
    
    nld_tax_scope_sources = {2021:"db(WBCPD[2022])", 2022:"db(WBCPD[2023])",
                             2023:"db(WBCPD[2024])", 2024:"db(WBCPD[2024])"}

    #----------------------------------------------------------------------------

    # Netherlands

    ## Jurisdiction
    
    nld_tax_II_jur_I = ["Netherlands"]

    ## IPCC categories
    
    nld_tax_II_ipcc_I = ["1A1A", "1A1A1", "1A1A2",
                         "1A1A3"]
    
    ## Fuels
    
    nld_tax_II_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    nld_tax_II_jur_scope = {2022:nld_tax_II_jur_I} 
    
    nld_tax_II_ipcc_scope = {2022:nld_tax_II_ipcc_I}    

    nld_tax_II_fuel_scope = {2022:nld_tax_II_fuel_I}
    
    ## Sources dictionary
    
    nld_tax_II_scope_sources = {2022:"leg(NLD(2020)), leg(NLD(2022))"}

    #----------------------------------------------------------------------------

    # Norway
    
    ## Jurisdictions    
    
    nor_tax_I_jur_I = ["Norway"]
    nor_tax_II_jur_I = ["Norway"]
    
    ## IPCC categories
    nor_tax_I_ipcc_I = ["1A1A1", "1A1B", "1A1C", "1A2A", "1A2B", "1A2C",
                        "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J",
                        "1A2K", "1A2L", "1A2M", "1A3A2", "1A3B", "1A4A", "1A4B",
                        "1A4C2"]
    
    nor_tax_I_ipcc_II = ["1A1B", "1A1C", "1A3A2", "1A3B", "1A4A", "1A4B",
                         "1A4C2"]
    
    nor_tax_II_ipcc_I = ["1B2A1", "1B2A2", "1B2A32", "1B2A33"]
    
    ## Fuels

    nor_tax_I_fuel_I = ["Oil"]
    nor_tax_I_fuel_II = ["Oil", "Natural gas"]
    
    nor_tax_II_fuel_I = ["Oil", "Natural gas"]    
     
    
    ## scope dictionaries

    nor_tax_I_jur_scope = {year:nor_tax_I_jur_I for year in range(1991, 2025)}

    nor_tax_I_ipcc_scope = {year:nor_tax_I_ipcc_I for year in range(1991, 2008)}
    nor_tax_I_ipcc_scope.update({year: nor_tax_I_ipcc_II for year in range(2008, 2025)})
    
    nor_tax_I_fuel_scope = {year:nor_tax_I_fuel_I for year in range(1991, 2007)}
    nor_tax_I_fuel_scope.update({year: nor_tax_I_fuel_II for year in range(2007, 2025)})

    nor_tax_II_jur_scope = {year:nor_tax_II_jur_I for year in range(1991, 2025)}

    nor_tax_II_ipcc_scope = {year:nor_tax_II_ipcc_I for year in range(1991, 2025)}
    
    nor_tax_II_fuel_scope = {year:nor_tax_II_fuel_I for year in range(1991, 2025)}
    
    
    ## Sources dictionary
    
    nor_tax_I_scope_sources = {year: "leg(NOR-EA[1990])" for year in range(1991, 2025)}
    
    nor_tax_II_scope_sources = {year: "leg(NOR-EA[1990])" for year in range(1991, 2025)}
    
    
    #----------------------------------------------------------------------------

    # Poland
    
    ## Jurisdictions    
    
    pol_tax_jur_I = ["Poland"]
    
    ## IPCC categories
    pol_tax_ipcc_I = ["1A1A1", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", 
                      "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M"]
    
    
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
    
    # Portugal
    
    ## Jurisdiction
    
    prt_tax_jur_I = ["Portugal"]

    ## IPCC categories
    
    prt_tax_ipcc_I = ["1A1A2", "1A1A3", "1A1B", "1A1C",
                      "1A3A1", "1A3B", "1A4A", "1A4B", "1A4C1", "1A4C2"]
    
    ## Fuels
    
    prt_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    prt_tax_jur_scope = {year: prt_tax_jur_I for year in range(2015, 2025)}
    
    prt_tax_ipcc_scope = {year: prt_tax_ipcc_I for year in range(2015, 2025)}

    prt_tax_fuel_scope = {year:prt_tax_fuel_I for year in range(2015, 2025)}

    ## Sources dictionary
    
    prt_tax_scope_sources = {year:"leg(PRT[2014]), gvt(PRT[2014])" for year in range(2015, 2025)}
    
    
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
    
    mex_qt_tax_jur_scope = {year: mex_qt_tax_ipcc_I for year in range(2023, 2025)}
    
    mex_qt_tax_sources = {year: "web(MEX-QT[2022]), web(MEX-QT[2025]), db(WBCPD[2024])" for year in range(2023, 2025)}
      
    #----------------------------------------------------------------------------

    # Singapore 
    
    ## Jurisdiction
    
    sgp_tax_jur_I = ["Singapore"]
    
    
    ## IPCC categories
    
    sgp_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B",
                     "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I",
                     "1A2J", "1A2K", "1A2L", "1A2M", "2A1", "2A2", "2A3", "2A4A", 
                     "2A4B", "2A4C", "2A4D", "2B1", "2B2", "2B3", "2B4", "2B5",
                     "2B6", "2B7", "2B9A", "2B9B", "2B10", "2C1", "2C2", "2C3",
                     "2C5", "2D1", "2D2", "2D3", "2D4", "2E"]
    
    ## Fuel
    sgp_tax_fuel_I = ["Coal", "Oil", "Natural gas"]    
    
    ## scope dictionaries
    sgp_tax_jur_scope = {year:sgp_tax_jur_I for year in range(2019, 2025)}
    
    sgp_tax_ipcc_scope = {year:sgp_tax_ipcc_I for year in range(2019, 2025)}

    sgp_tax_fuel_scope = {year:sgp_tax_fuel_I for year in range(2019, 2025)}
    
    ## Sources dictionary
    
    sgp_tax_scope_sources = {2019:"leg(SG[2018])", 2020:"leg(SG[2018])",
                             2021:"leg(SG[2018])", 2022:"db(WBCPD[2023])",
                             2023:"db(WBCPD[2023])", 2024:"db(WBCPD[2023])"}
    
    #----------------------------------------------------------------------------

    # Slovenia
    
    ## Jurisdictions    
    
    slo_tax_jur_I = ["Slovenia"]
    
    ## IPCC categories
    slo_tax_ipcc_I = ["1A1A2", "1A1A3", "1A1B", "1A1C", 
                      "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                      "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", 
                      "1A4B", "1A4C1", "1A4C2", "4C1"]
    
    
    ## Fuels

    slo_tax_I_fuel_I = ["Oil", "Coal", "Natural gas"]      
    
    ## scope dictionaries

    slo_tax_jur_scope = {year: slo_tax_jur_I for year in range(1996, 2025)}

    slo_tax_ipcc_scope = {year: slo_tax_ipcc_I for year in range(1996, 2025)}
    
    slo_tax_fuel_scope = {year: slo_tax_I_fuel_I for year in range(1996, 2025)}
    
    ## Sources dictionary
    
    slo_tax_scope_sources = {1996:"leg(SLO-CO2[1996])",
                                1997:"leg(SLO-CO2[1997])", 1998:"leg(SLO-CO2[1998])",
                                1999:"leg(SLO-CO2[1998])", 2000:"leg(SLO-CO2[2000])",
                                2001:"leg(SLO-CO2[2000])", 2002:"leg(SLO-CO2[2000])",
                                2003:"leg(SLO-CO2[2000])", 2004:"leg(SLO-CO2[2000])",
                                2005:"leg(SLO-CO2[2000])", 2006:"leg(SLO-CO2[2000])",
                                2007:"leg(SLO-CO2[2006])", 2008:"leg(SLO-CO2[2008])",
                                2009:"leg(SLO-CO2[2009a])", 2010:"leg(SLO-CO2[2009b])",
                                2011:"leg(SLO-CO2[2010])", 2012:"leg(SLO-CO2[2011])",
                                2013:"leg(SLO-CO2[2012])", 2014:"leg(SLO-CO2[2013])",
                                2015:"leg(SLO-CO2[2014])", 2016:"leg(SLO-CO2[2016])",
                                2017:"leg(SLO-CO2[2016])", 2018:"leg(SLO-CO2[2018])",
                                2019:"leg(SLO-CO2[2018])", 2020:"leg(SLO-CO2[2020])",
                                2021:"leg(SLO-CO2[2020])", 2022:"leg(SLO-CO2[2020])",
                                2023:"leg(SLO-CO2[2020])", 2024:"leg(SLO-CO2[2020])"}
    
    #----------------------------------------------------------------------------

    # South Africa 
    
    ## Jurisdiction
    
    zaf_tax_jur_I = ["South Africa"]
    
    
    ## IPCC categories
    
    zaf_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                      "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                      "1A2J", "1A2K", "1A2L", "1A2M", "1A3A1", "1A3A2", "1A3B", 
                      "1A3C", "1A3D", "1A3D1", "1A3D2", "1A3E", "1A3E1", "1A4A", 
                      "1A4C1", "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C", "1B1A", 
                      "1B1A1", "1B1A11", "1B1A12", "1B1A13", "1B1A14", "1B1A2", 
                      "1B1A21", "1B1A22", "1B2A1", "1B2A2", "1B2A3", "1B2A31", 
                      "1B2A32", "1B2A33", "1B2A34", "1B2A35", "1B2A36", "1B2B1", 
                      "1B2B2", "1B2B3", "1B2B31", "1B2B32", "1B2B33", "1B2B34", 
                      "1B2B35", "1B2B36", "1B3", "1C1A", "1C1B", "1C1C", "1C2A", 
                      "1C2B", "1C3", "2A1", "2A2", "2A3", "2A4", "2A4A", "2A4B", 
                      "2A4C", "2A4D", "2B1", "2B10", "2B2", "2B3", "2B4", "2B5", 
                      "2B6", "2B7", "2B8A", "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", 
                      "2B9A", "2B9B", "2C1", "2C2", "2C3", "2C4", "2C5", "2C6", 
                      "2C7", "2D1", "2D2", "2D3", "2D4", "2E", "2F1", "2F2", "2F3", 
                      "2F4", "2F5", "2F6", "2G1", "2G2", "2G3", "2G4", "2H1", 
                      "2H2", "2H3", "5A1", "5A2"]
    
    ## Fuel
    zaf_tax_fuel_I = ["Coal", "Oil", "Natural gas"]    
    
    ## scope dictionaries
    zaf_tax_jur_scope = {year:zaf_tax_jur_I for year in range(2019, 2025)}
    
    zaf_tax_ipcc_scope = {year:zaf_tax_ipcc_I for year in range(2019, 2025)}  

    zaf_tax_fuel_scope = {year:zaf_tax_fuel_I for year in range(2019, 2025)}
    
    ## Sources dictionary
    
    zaf_tax_scope_sources = {year:"leg(SA[2019])" for year in range(2019, 2025)}
    
    
    #----------------------------------------------------------------------------

    # Sweden
    
    ## Jurisdictions    
    
    swe_tax_jur_I = ["Sweden"]
    
    ## IPCC categories
    swe_tax_ipcc_I = ["1A1B", "1A1C", "1A2A", "1A2B", "1A2C", "1A2D", "1A2E",
                      "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", "1A2L",
                      "1A2M", "1A3B", "1A4A", "1A4B", "1A4C1", "1A4C2"]

    swe_tax_ipcc_II = ["1A1B", "1A1C", "1A3B", "1A4A", "1A4B", "1A4C1", 
                       "1A4C2"]

    
    ## Fuels

    swe_tax_fuel_I = ["Oil", "Coal", "Natural gas"]      
    
    ## scope dictionaries

    swe_tax_jur_scope = {year:swe_tax_jur_I for year in range(1991, 2025)}

    swe_tax_ipcc_scope = {year:swe_tax_ipcc_I for year in range(1991, 2011)}
    swe_tax_ipcc_scope.update({year: swe_tax_ipcc_II for year in range(2011, 2025)})
    
    swe_tax_fuel_scope = {year:swe_tax_fuel_I for year in range(1991, 2025)}
    
    ## Sources dictionary
    
    swe_tax_scope_sources = {year:"report(SMF-CT[2011])" for year in range(1991, 2025)}

    #----------------------------------------------------------------------------

    # Switzerland
    
    ## Jurisdiction
    
    che_tax_jur_I = ["Switzerland"]

    ## IPCC categories
    
    # initial scope
    che_tax_ipcc_I = ["1A1A2", "1A1A3", "1A4A", "1A4B"]

    ## Fuels
    
    che_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    che_tax_jur_scope = {year: che_tax_jur_I for year in range(2008, 2025)}
    
    che_tax_ipcc_scope = {year: che_tax_ipcc_I for year in range(2008, 2025)}
    
    che_tax_fuel_scope = {year: che_tax_fuel_I for year in range(2008, 2025)}
    
    ## Sources dictionary
    
    che_tax_scope_sources = {year: "gvt(CH[2005], CH[2009])" for year in range(2008, 2014)}
    che_tax_scope_sources.update({year: "gvt(CH[2005], CH[2009])" for year in range(2014, 2025)})
    
    #----------------------------------------------------------------------------
    
    # Ukraine
    
    ## Jurisdiction
    
    ukr_tax_jur_I = ["Ukraine"]

    ## IPCC categories
    
    # initial scope
    ukr_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                      "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                      "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M",
                      "1A3A1", "1A3A2", "1A3B", "1A3C", "1A3D1", 
                      "1A3D1", "1A3D2", "1A3E1", "1A4A", "1A4B", "1A4C1",
                      "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C"]
    
    # the scheme was suspended between 2015-2016
    ukr_tax_ipcc_II = []
    
    ## Fuels
    
    ukr_tax_fuel_I = ["Oil", "Natural gas", "Coal"]
    
    # the scheme was suspended between 2015-2016
    ukr_tax_fuel_II = []

    ## scope dictionaries
    
    ukr_tax_jur_scope = {year: ukr_tax_jur_I for year in range(2011, 2025)}
    
    ukr_tax_ipcc_scope = {year: ukr_tax_ipcc_I for year in range(2011, 2025)}
    
    ukr_tax_fuel_scope = {year:ukr_tax_fuel_I for year in range(2011, 2025)}
    
    ## Sources dictionary
    
    ukr_tax_scope_sources = {2011:"leg(UA[2011], report(EBRD[2014])", 
                                2012:"leg(UA[2011], report(EBRD[2014])",
                                2013:"leg(UA[2011], report(EBRD[2014])", 
                                2014:"leg(UA[2011], report(EBRD[2014])", 
                                2015:"", 2016:"",
                                2017:"leg(UA[2011], report(EBRD[2014])", 
                                2018:"leg(UA[2011], report(EBRD[2014])", 
                                2019:"leg(UA[2011], report(EBRD[2014])", 
                                2020:"leg(UA[2011], report(EBRD[2014])",
                                2021:"leg(UA[2011], report(EBRD[2014])",
                                2022:"leg(UA[2011], report(EBRD[2014])",
                                2023:"leg(UA[2011], report(EBRD[2014])",
                                2024:"leg(UA[2011], report(EBRD[2014])"}
    
    #----------------------------------------------------------------------------
    
    # United Kingdom - carbon price support
    
    ## Jurisdiction
    
    gbr_tax_jur_I = ["United Kingdom"]

    ## IPCC categories
    
    # initial scope
    gbr_tax_ipcc_I = ["1A1A1", "1A1A2"]


    ## Fuels
    
    gbr_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    gbr_tax_jur_scope = {year: gbr_tax_jur_I for year in range(2013, 2025)}

    gbr_tax_ipcc_scope = {year: gbr_tax_ipcc_I for year in range(2013, 2025)}
    
    gbr_tax_fuel_scope = {year: gbr_tax_fuel_I for year in range(2013, 2025)}

    ## Sources dictionary
    
    gbr_tax_scope_sources = {year:"leg(UK[2013a], UK[2013b])" for year in range(2013, 2025)}

    #----------------------------------------------------------------------------

    # Uruguay
    
    ## Jurisdiction
    
    ury_tax_jur_I = ["Uruguay"]

    ## IPCC categories
    
    ury_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A",
                      "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H",
                      "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2",
                      "1A3B", "1A3C", "1A3D2", "1A3E1", "1A4A", "1A4B",
                      "1A4C1", "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C"]
    
    ## Fuels
    
    ury_tax_fuel_I = ["Oil"]

    ## scope dictionaries
    ury_tax_jur_scope = {year: ury_tax_jur_I for year in range(2022, 2025)}
    
    ury_tax_ipcc_scope = {year: ury_tax_ipcc_I for year in range(2022, 2025)}     

    ury_tax_fuel_scope = {year: ury_tax_fuel_I for year in range(2022, 2025)}

    ## Sources dictionary
    
    ury_tax_scope_sources = {year: " " for year in range(2022, 2025)}

    #----------------------------------------------------------------------------

    # Mexico - Baja California
    
    ## Jurisdiction
    
    mex_bc_tax_jur_I = ["Baja California"]

    ## IPCC categories
    
    mex_bc_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
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
    
    mex_bc_tax_fuel_I = ["Coal", "Natural gas", "Oil"]

    ## scope dictionaries
    mex_bc_tax_jur_scope = {2020: mex_bc_tax_jur_I, 2021: mex_bc_tax_jur_I}
    
    mex_bc_tax_ipcc_scope = {2020: mex_bc_tax_ipcc_I, 2021: mex_bc_tax_ipcc_I}  

    mex_bc_tax_fuel_scope = {2020: mex_bc_tax_fuel_I, 2021: mex_bc_tax_fuel_I}
    
    ## Sources dictionary
    
    mex_bc_tax_scope_sources = {2020:" ", 2021:" "}

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

    # Mexico - Tamaulipas
    
    ## Jurisdiction
    
    mex_tm_tax_jur_I = ["Tamaulipas"]

    ## IPCC categories
    
    mex_tm_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
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
    
    mex_tm_tax_fuel_I = ["Coal", "Natural gas", "Oil"]
    
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

    # Mexico - Zacatecas
    
    ## Jurisdiction
    
    mex_za_tax_jur_I = ["Zacatecas"]

    ## IPCC categories
    
    mex_za_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C",
                         "1A2A", "1A2B", "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", 
                         "1A2H", "1A2I", "1A2J", "1A2K", "1A2L", "1A2M", 
                         "2A1", "2A2", "2A3", "2A4A", "2A4B", "2A4C", "2A4D",
                         "2B1", "2B2", "2B3", "2B4", "2B5", "2B6", "2B7", "2B8A",
                         "2B8B", "2B8C", "2B8D", "2B8E", "2B8F", "2B9A", "2B9B",
                         "2B10", "2C1","2C2","2C3", "2C4", "2C5","2C6", "2C7",
                         "2D1", "2D2", "2D3","2D4", "2E1", "2E2", "2E3", "2E4",
                         "2E5", "2F1", "2F2", "2F3", "2F4", "2F5", "2F6",
                         "2G1", "2G2", "2G3", "2G4", "2H1", "2H2", "2H3"]
    
    ## Fuels
    
    mex_za_tax_fuel_I = ["Coal", "Natural gas", "Oil"]

    ## scope dictionaries
    mex_za_tax_jur_scope = {year:mex_za_tax_jur_I for year in range(2017, 2025)}
    
    mex_za_tax_ipcc_scope = {year:mex_za_tax_ipcc_I for year in range(2017, 2025)}

    mex_za_tax_fuel_scope = {year:mex_za_tax_fuel_I for year in range(2017, 2025)}
    
    ## sources dictionary 
    
    mex_za_tax_scope_sources = {year:"leg(MEX-ZA[2016])" for year in range(2017, 2025)}

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
    
    # Alberta
    
    ## Jurisdiction
    
    can_ab_tax_jur_I = ["Alberta"]

    ## IPCC categories (2017-2019)
    
    can_ab_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A2A", "1A2B", "1A2C", "1A2D", 
                         "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", "1A2J", "1A2K", 
                         "1A2L", "1A2M", "1A3B", "1A3D1", "1A3D2", 
                         "1A3E1", "1A4A", "1A4B", "1A4C1", "1A4C2", "1A4C3", "1A5A", 
                         "1A5B", "1A5C"]

    ## Fuels
    
    can_ab_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_ab_tax_jur_scope = {2017:can_ab_tax_jur_I, 2018:can_ab_tax_jur_I, 
                               2019:can_ab_tax_jur_I}
    
    can_ab_tax_ipcc_scope = {2017:can_ab_tax_ipcc_I, 2018:can_ab_tax_ipcc_I, 
                                2019:can_ab_tax_ipcc_I}
    
    can_ab_tax_fuel_scope = {2017:can_ab_tax_fuel_I, 2018:can_ab_tax_fuel_I,
                                2019:can_ab_tax_fuel_I}

    ## Sources dictionary
    
    can_ab_tax_scope_sources = {2017:"web(ALB[2019], AG-CLR[2018]), gvt(ALB-FP[2016])", 
                                   2018:"web(ALB[2019], AG-CLR[2018]), gvt(ALB-FP[2016])", 
                                   2019:"web(ALB[2019], AG-CLR[2018]), gvt(ALB-FP[2016])"}
    
    #----------------------------------------------------------------------------
    
    # New Brunswick
    
    ## Jurisdiction
    
    can_nb_tax_jur_I = ["New Brunswick"]

    ## IPCC categories (2020-2021)
    
    can_nb_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A3B", "1A3C", 
                         "1A3D1", "1A3D2", "1A3E1", "1A4A", "1A4B", 
                         "1A5A", "1A5B", "1A5C"]

    ## Fuels
    
    can_nb_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_nb_tax_jur_scope = {2020:can_nb_tax_jur_I, 2021:can_nb_tax_jur_I,
                            2022:can_nb_tax_jur_I}
    
    can_nb_tax_ipcc_scope = {2020:can_nb_tax_ipcc_I, 2021:can_nb_tax_ipcc_I,
                             2022:can_nb_tax_ipcc_I}
    
    can_nb_tax_fuel_scope = {2020:can_nb_tax_fuel_I, 2021:can_nb_tax_fuel_I,
                             2022:can_nb_tax_fuel_I}

    ## Sources dictionary
    
    can_nb_tax_scope_sources = {2020:"gvt(ECCC[2021]), report(KPMG[2020])", 
                                   2021:"gvt(ECCC[2021]), report(KPMG[2020])",
                                   2022:"gvt(ECCC[2021]), report(KPMG[2020])"}
    
    #----------------------------------------------------------------------------
    
    # Prince Edward Island
    
    ## Jurisdiction
    
    can_pe_tax_jur_I = ["Prince Edward Island"]

    ## IPCC categories
    
    can_pe_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2J", "1A2K", "1A2L", "1A2M", "1A3A2", "1A3B", "1A3C", 
                         "1A3D2", "1A3E1", "1A4A", "1A4B", "1A5A", 
                         "1A5B", "1A5C"]

    ## Fuels
    
    can_pe_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_pe_tax_jur_scope = {2019:can_pe_tax_jur_I, 2020:can_pe_tax_jur_I, 
                               2021:can_pe_tax_jur_I, 2022:can_pe_tax_jur_I}
    
    can_pe_tax_ipcc_scope = {2019:can_pe_tax_ipcc_I, 2020:can_pe_tax_ipcc_I, 
                                2021:can_pe_tax_ipcc_I, 2022:can_pe_tax_ipcc_I}
    
    can_pe_tax_fuel_scope = {2019:can_pe_tax_fuel_I, 2020:can_pe_tax_fuel_I, 
                                2021:can_pe_tax_fuel_I, 2022:can_pe_tax_fuel_I}

    ## Sources dictionary
    
    can_pe_tax_scope_sources = {2019:"gvt(ECCC[2021], PEI[2018])", 
                                   2020:"gvt(ECCC[2021], PEI[2018])", 
                                   2021:"gvt(ECCC[2021], PEI[2018])",
                                   2022:"gvt(ECCC[2021], PEI[2018])"}
    
    #----------------------------------------------------------------------------
    
    # Newfoundland and Labrador
    
    ## Jurisdiction
    
    can_nl_tax_jur_I = ["Newfoundland and Labrador"]

    ## IPCC categories
    
    can_nl_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2H", "1A2J", "1A2K", 
                         "1A2L", "1A2M", "1A3B", "1A3C", "1A3D1", "1A3D2", 
                         "1A3E1", "1A5A", "1A5B", "1A5C"]

    ## Fuels
    
    can_nl_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_nl_tax_jur_scope = {2019:can_nl_tax_jur_I, 2020:can_nl_tax_jur_I, 
                               2021:can_nl_tax_jur_I, 2022:can_nl_tax_jur_I}
    
    can_nl_tax_ipcc_scope = {2019:can_nl_tax_ipcc_I, 2020:can_nl_tax_ipcc_I, 
                                2021:can_nl_tax_ipcc_I, 2022:can_nl_tax_ipcc_I}
    
    can_nl_tax_fuel_scope = {2019:can_nl_tax_fuel_I, 2020:can_nl_tax_fuel_I, 
                                2021:can_nl_tax_fuel_I, 2022:can_nl_tax_fuel_I}

    ## Sources dictionary
    
    can_nl_tax_scope_sources = {2019:"leg(NL[2011])", 2020:"leg(NL[2011])", 
                                   2021:"leg(NL[2011])", 2022:"leg(NL[2011])",
                                   2023:" ", 2024:" "}
    
    #----------------------------------------------------------------------------
    
    # Northwest Territories
    
    ## Jurisdiction
    
    can_nt_tax_jur_I = ["Northwest Territories"]

    ## IPCC categories
    
    can_nt_tax_ipcc_I = ["1A1A1", "1A1A2", "1A1A3", "1A1B", "1A1C", "1A2A", "1A2B", 
                         "1A2C", "1A2D", "1A2E", "1A2F", "1A2G", "1A2H", "1A2I", 
                         "1A2K", "1A2L", "1A2M", "1A3B", "1A3C", "1A3D1", 
                         "1A3D2", "1A3E1", "1A4A", "1A4B", "1A4C1", 
                         "1A4C2", "1A4C3", "1A5A", "1A5B", "1A5C"]

    ## Fuels
    
    can_nt_tax_fuel_I = ["Oil", "Natural gas", "Coal"]

    ## scope dictionaries
    
    can_nt_tax_jur_scope = {year:can_nt_tax_jur_I for year in range(2019, 2025)}
    
    can_nt_tax_ipcc_scope = {year:can_nt_tax_ipcc_I for year in range(2019, 2025)}
    
    can_nt_tax_fuel_scope = {year:can_nt_tax_fuel_I for year in range(2019, 2025)}

    ## Sources dictionary
    
    can_nt_tax_scope_sources = {year: "gvt(NWT[2020], ECCC[2021])" for year in range(2019, 2023)}
    can_nt_tax_scope_sources.update({year: "db(WBCPD[2024])" for year in range(2023, 2025)})

    #------------------------------All schemes dictionaries--------------------------------#

    taxes_scope = {"arg_tax":{"jurisdictions":arg_tax_jur_scope, 
                                  "sectors":arg_tax_ipcc_scope,
                                  "fuels":arg_tax_fuel_scope}, 
                      "aus_tax":{"jurisdictions":aus_tax_jur_scope, 
                                  "sectors":aus_tax_ipcc_scope,
                                  "fuels":aus_tax_fuel_scope}, 
                      "chl_tax":{"jurisdictions":chl_tax_jur_scope, 
                                  "sectors":chl_tax_ipcc_scope,
                                  "fuels":chl_tax_fuel_scope},
                      "che_tax":{"jurisdictions":che_tax_jur_scope, 
                                  "sectors":che_tax_ipcc_scope,
                                  "fuels":che_tax_fuel_scope},                      
                      "col_tax":{"jurisdictions":col_tax_jur_scope, 
                                  "sectors":col_tax_ipcc_scope,
                                  "fuels":col_tax_fuel_scope},
                      "dnk_tax":{"jurisdictions":dnk_tax_jur_scope, 
                                  "sectors":dnk_tax_ipcc_scope,
                                  "fuels":dnk_tax_fuel_scope},
                      "est_tax":{"jurisdictions":est_tax_jur_scope, 
                                  "sectors":est_tax_ipcc_scope,
                                  "fuels":est_tax_fuel_scope},
                      "fin_tax":{"jurisdictions":fin_tax_jur_scope, 
                                  "sectors":fin_tax_ipcc_scope,
                                  "fuels":fin_tax_fuel_scope},
                      "fra_tax":{"jurisdictions":fra_tax_jur_scope, 
                                  "sectors":fra_tax_ipcc_scope,
                                  "fuels":fra_tax_fuel_scope},
                      "hun_tax":{"jurisdictions":hun_tax_jur_scope, 
                                  "sectors":hun_tax_ipcc_scope,
                                  "fuels":hun_tax_fuel_scope},
                      "isl_tax":{"jurisdictions":isl_tax_jur_scope, 
                                  "sectors":isl_tax_ipcc_scope,
                                  "fuels":isl_tax_fuel_scope},
                      "irl_tax":{"jurisdictions":irl_tax_jur_scope, 
                                  "sectors":irl_tax_ipcc_scope,
                                  "fuels":irl_tax_fuel_scope},
                      "jpn_tax":{"jurisdictions":jpn_tax_jur_scope, 
                                  "sectors":jpn_tax_ipcc_scope,
                                  "fuels":jpn_tax_fuel_scope},
                      "lva_tax":{"jurisdictions":lva_tax_jur_scope, 
                                  "sectors":lva_tax_ipcc_scope,
                                  "fuels":lva_tax_fuel_scope},
                      "lie_tax":{"jurisdictions":lie_tax_jur_scope, 
                                  "sectors":lie_tax_ipcc_scope,
                                  "fuels":lie_tax_fuel_scope},
                      "lux_tax":{"jurisdictions":lux_tax_jur_scope, 
                                  "sectors":lux_tax_ipcc_scope,
                                  "fuels":lux_tax_fuel_scope},
                      "mex_tax":{"jurisdictions":mex_tax_jur_scope, 
                                  "sectors":mex_tax_ipcc_scope,
                                  "fuels":mex_tax_fuel_scope},
                      "nld_tax":{"jurisdictions":nld_tax_jur_scope, 
                                  "sectors":nld_tax_ipcc_scope,
                                  "fuels":nld_tax_fuel_scope},
                      "nld_tax_II":{"jurisdictions":nld_tax_II_jur_scope, 
                                  "sectors":nld_tax_II_ipcc_scope,
                                  "fuels":nld_tax_II_fuel_scope},
                      "nor_tax_I":{"jurisdictions":nor_tax_I_jur_scope, 
                                  "sectors":nor_tax_I_ipcc_scope,
                                  "fuels":nor_tax_I_fuel_scope},
                      "nor_tax_II":{"jurisdictions":nor_tax_II_jur_scope, 
                                  "sectors":nor_tax_II_ipcc_scope,
                                  "fuels":nor_tax_II_fuel_scope},
                      "prt_tax":{"jurisdictions":prt_tax_jur_scope, 
                                  "sectors":prt_tax_ipcc_scope,
                                  "fuels":prt_tax_fuel_scope},
                      "pol_tax":{"jurisdictions":pol_tax_jur_scope, 
                                  "sectors":pol_tax_ipcc_scope,
                                  "fuels":pol_tax_fuel_scope},                      
                      "sgp_tax":{"jurisdictions":sgp_tax_jur_scope, 
                                  "sectors":sgp_tax_ipcc_scope,
                                  "fuels":sgp_tax_fuel_scope},
                      "swe_tax":{"jurisdictions":swe_tax_jur_scope, 
                                  "sectors":swe_tax_ipcc_scope,
                                  "fuels":swe_tax_fuel_scope},
                      "slo_tax":{"jurisdictions":slo_tax_jur_scope, 
                                  "sectors":slo_tax_ipcc_scope,
                                  "fuels":slo_tax_fuel_scope},
                      "zaf_tax":{"jurisdictions":zaf_tax_jur_scope, 
                                  "sectors":zaf_tax_ipcc_scope,
                                  "fuels":zaf_tax_fuel_scope},
                      "ukr_tax":{"jurisdictions":ukr_tax_jur_scope, 
                                  "sectors":ukr_tax_ipcc_scope,
                                  "fuels":ukr_tax_fuel_scope},
                     "ury_tax":{"jurisdictions":ury_tax_jur_scope, 
                                  "sectors":ury_tax_ipcc_scope,
                                  "fuels":ury_tax_fuel_scope}, 
                      "gbr_tax":{"jurisdictions":gbr_tax_jur_scope, 
                                  "sectors":gbr_tax_ipcc_scope,
                                  "fuels":gbr_tax_fuel_scope},
                      "can_tax_I":{"jurisdictions":can_tax_I_jur_scope, 
                                  "sectors":can_tax_I_ipcc_scope,
                                  "fuels":can_tax_I_fuel_scope},
                      "can_tax_II":{"jurisdictions":can_tax_II_jur_scope, 
                                  "sectors":can_tax_II_ipcc_scope,
                                  "fuels":can_tax_II_fuel_scope},
                      "can_ab_tax":{"jurisdictions":can_ab_tax_jur_scope, 
                                  "sectors":can_ab_tax_ipcc_scope,
                                  "fuels":can_ab_tax_fuel_scope},
                      "can_bc_tax":{"jurisdictions":can_bc_tax_jur_scope, 
                                  "sectors":can_bc_tax_ipcc_scope,
                                  "fuels":can_bc_tax_fuel_scope},
                      "can_nb_tax":{"jurisdictions":can_nb_tax_jur_scope, 
                                  "sectors":can_nb_tax_ipcc_scope,
                                  "fuels":can_nb_tax_fuel_scope},
                      "can_pe_tax":{"jurisdictions":can_pe_tax_jur_scope, 
                                  "sectors":can_pe_tax_ipcc_scope,
                                  "fuels":can_pe_tax_fuel_scope},
                      "can_nl_tax":{"jurisdictions":can_nl_tax_jur_scope, 
                                  "sectors":can_nl_tax_ipcc_scope,
                                  "fuels":can_nl_tax_fuel_scope},
                      "can_nt_tax":{"jurisdictions":can_nt_tax_jur_scope, 
                                  "sectors":can_nt_tax_ipcc_scope,
                                  "fuels":can_nt_tax_fuel_scope},
                      "mex_bc_tax":{"jurisdictions":mex_bc_tax_jur_scope,
                                    "sectors":mex_bc_tax_ipcc_scope,
                                    "fuels":mex_bc_tax_fuel_scope},
                      "mex_dg_tax":{"jurisdictions": mex_dg_tax_jur_scope,
                                     "sectors": mex_dg_tax_ipcc_scope,
                                     "fuels": mex_dg_tax_fuel_scope},
                      "mex_em_tax":{"juristicons": mex_em_tax_jur_scope,
                                    "sectors": mex_em_tax_jur_scope,
                                    "fuels": mex_em_tax_fuel_scope},
                      "mex_gj_tax":{"jurisdictions":mex_gj_tax_jur_scope,
                                    "sectors":mex_gj_tax_ipcc_scope,
                                    "fuels":mex_gj_tax_fuel_scope},
                      "mex_qt_tax":{"jurisdictions": mex_qt_tax_jur_scope,
                                    "sectors": mex_qt_tax_ipcc_scope,
                                    "fuels": mex_qt_tax_fuel_scope},
                      "mex_yu_tax":{"jurisdictions":mex_yu_tax_jur_scope,
                                    "sectors":mex_yu_tax_ipcc_scope,
                                    "fuels":mex_yu_tax_fuel_scope},
                      "mex_tm_tax":{"jurisdictions":mex_tm_tax_jur_scope,
                                    "sectors":mex_tm_tax_ipcc_scope,
                                    "fuels":mex_tm_tax_fuel_scope},
                      "mex_za_tax":{"jurisdictions":mex_za_tax_jur_scope,
                                    "sectors":mex_za_tax_ipcc_scope,
                                    "fuels":mex_za_tax_fuel_scope}}                      
    
    taxes_scope_sources = {"arg_tax":arg_tax_scope_sources,
                              "aus_tax":aus_tax_scope_sources,
                              "che_tax":che_tax_scope_sources,
                              "chl_tax":chl_tax_scope_sources,
                              "col_tax":col_tax_scope_sources,
                              "dnk_tax":dnk_tax_scope_sources,
                              "est_tax":est_tax_scope_sources,
                              "fin_tax":fin_tax_scope_sources,
                              "fra_tax":fra_tax_scope_sources,
                              "hun_tax":hun_tax_scope_sources,
                              "isl_tax":isl_tax_scope_sources,
                              "irl_tax":irl_tax_scope_sources,
                              "jpn_tax":jpn_tax_scope_sources,
                              "lie_tax":lie_tax_scope_sources,
                              "lva_tax":lva_tax_scope_sources,
                              "lux_tax":lux_tax_scope_sources,                              
                              "mex_tax":mex_tax_scope_sources,
                              "nld_tax":nld_tax_scope_sources,
                              "nld_tax_II":nld_tax_II_scope_sources,                             
                              "nor_tax_I":nor_tax_I_scope_sources,
                              "nor_tax_II":nor_tax_II_scope_sources,
                              "prt_tax":prt_tax_scope_sources,
                              "pol_tax":pol_tax_scope_sources,
                              "sgp_tax":sgp_tax_scope_sources,
                              "slo_tax":slo_tax_scope_sources,
                              "zaf_tax":zaf_tax_scope_sources,
                              "swe_tax":swe_tax_scope_sources,
                              "ukr_tax":ukr_tax_scope_sources,
                              "gbr_tax":gbr_tax_scope_sources,
                              "ury_tax":ury_tax_scope_sources,
                              "can_tax_I":can_tax_I_scope_sources,
                              "can_tax_II":can_tax_II_scope_sources,
                              "can_ab_tax":can_ab_tax_scope_sources,
                              "can_bc_tax":can_bc_tax_scope_sources,
                              "can_nb_tax":can_nb_tax_scope_sources,
                              "can_pe_tax":can_pe_tax_scope_sources,
                              "can_nl_tax":can_nl_tax_scope_sources,
                              "can_nt_tax":can_nt_tax_scope_sources,
                              "mex_bc_tax":mex_bc_tax_scope_sources,
                              "mex_dg_tax":mex_dg_tax_scope_sources,
                              "mex_em_tax": mex_em_tax_scope_sources, 
                              "mex_gj_tax":mex_gj_tax_scope_sources,
                              "mex_qt_tax":mex_qt_tax_scope_sources,
                              "mex_tm_tax":mex_tm_tax_scope_sources,
                              "mex_yu_tax":mex_yu_tax_scope_sources,
                              "mex_za_tax":mex_za_tax_scope_sources}
    
    
    data_and_sources = {"data":taxes_scope, "sources":taxes_scope_sources}
    
    
    return data_and_sources
    