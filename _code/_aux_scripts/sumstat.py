import pandas as pd
import numpy as np

# Load files - this assumes that the repository has been cloned locally,
# that jurisdiction-level files have been concatenated (using the Python script
# in `extract.py`) and saved locally.

path_dependencies = '/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp'
exec(open(path_dependencies+'/pkgs_and_directories.py').read())
exec(open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/jurisdictions.py").read())

path_wcpd = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data"

gas = "CO2"

wcpd_ctry = ecp_general.concatenate(path_wcpd+"/"+gas+"/national")
wcpd_subnat = ecp_general.concatenate(path_wcpd+"/"+gas+"/subnational")

def summaryStatistics(year):

    dataNat_yearSel = wcpd_ctry.loc[wcpd_ctry.year == year, ['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax', 'ets']]
    dataSubnat_yearSel = wcpd_subnat.loc[wcpd_subnat.year == year, ['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax', 'ets']]

    sumstat_jurisdictions = {}
    sumstat_sectors = {}

    dfs = {"national":dataNat_yearSel, "subnational":dataSubnat_yearSel}

    # jurisdiction-level summary statistics

    for df in dfs.keys():
        temp = dfs[df].copy()
        temp.drop(["year"], axis=1, inplace=True)

        temp["pricing"] = temp["tax"]+temp["ets"]
        temp = temp.groupby(["jurisdiction"]).sum().reset_index()

        # create jurisdiction-level binary value by assigning value 1 if value of sum is > 0
        for col in ["tax", "ets", "pricing"]:
            temp.loc[temp[col]>0, col] = 1

        sumstat_jurisdictions[df] = {"tax":sum(temp.tax), "ets":sum(temp.ets), "pricing":sum(temp.pricing)}

    # ipcc category-level summary statistics
    for df in dfs.keys():
        temp = dfs[df].copy()
        temp.drop(["year"], axis=1, inplace=True)

        temp["pricing"] = temp["tax"]+temp["ets"]
        temp = temp.groupby(["jurisdiction", "ipcc_code"]).sum().reset_index()

        # assign value 1 to 
        for col in ["tax", "ets", "pricing"]:
            temp.loc[temp[col]>0, col] = 1

        temp = temp.groupby(["ipcc_code"]).sum().reset_index()

        # drop sectors that are not covered by any single carbon price
        temp = temp[temp.pricing!=0]

        sumstat_sectors[df] = {"tax":sum(temp.tax), "ets":sum(temp.ets), "pricing":sum(temp.pricing)}

    return sumstat_jurisdictions, sumstat_sectors

test = summaryStatistics(2021)