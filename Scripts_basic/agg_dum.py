#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:40:49 2020

@author: GD
"""


# Assign values to aggregate categories if values in all subcategories is identical (UNDER DEVELOPMENT)
# Disaggregation levels

# Extract disaggregation levels
level_6 = [x for x in list(ipcc_iea.IPCC_CODE.unique()) if len(x) == 6]
level_5 = [x for x in list(ipcc_iea.IPCC_CODE.unique()) if len(x) == 5]
level_4 = [x for x in list(ipcc_iea.IPCC_CODE.unique()) if len(x) == 4]
level_3 = [x for x in list(ipcc_iea.IPCC_CODE.unique()) if len(x) == 3]
level_2 = [x for x in list(ipcc_iea.IPCC_CODE.unique()) if len(x) == 2]
level_1 = [x for x in list(ipcc_iea.IPCC_CODE.unique()) if len(x) == 1]

# For each level, check whether all values for lower disaggregation level are equal to 1
for ctry in ecp_v3.Jurisdiction.unique():
    for yr in ecp_v3.Year.unique():
        for 