import pandas as pd
import numpy as np

# Load files - this assumes that the repository has been cloned locally,
# that jurisdiction-level files have been concatenated (using the Python script
# in `extract.py`) and saved locally.

path_dependencies = '/Users/gd/GitHub/ECP/_code/compilation/dependencies'
exec(open(path_dependencies+'/pkgs_and_directories.py').read())
exec(open("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/jurisdictions.py").read())

path_wcpd = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_dataset/data"

gas = "CO2"

wcpd_ctry = ecp_general.concatenate(path_wcpd+"/"+gas+"/national")
wcpd_subnat = ecp_general.concatenate(path_wcpd+"/"+gas+"/subnational")

dataNat_yearSel = wcpd_ctry.loc[wcpd_ctry.year== 2021, ['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax', 'ets']]
dataSubnat_yearSel = wcpd_subnat.loc[wcpd_subnat.year== 2021, ['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax', 'ets']]

# jurisdiction-level summary statistics

sumstat = {}

dfs = {"national":dataNat_yearSel, "subnational":dataSubnat_yearSel}

for df in dfs.keys():
    temp = dfs[df].copy()
    temp.drop(["year"], axis=1, inplace=True)

    temp["pricing"] = temp["tax"]+temp["ets"]
    temp = temp.groupby(["jurisdiction"]).sum()
    temp.reset_index(inplace=True)

    for col in ["tax", "ets", "pricing"]:
        temp.loc[temp[col]>0, col] = 1

    sumstat[df] = {"tax":sum(temp.tax), "ets":sum(temp.ets), "pricing":sum(temp.pricing)}

# sector-level summary statistics