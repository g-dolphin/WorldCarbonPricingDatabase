# This script contains commands to calculate basic summary
# statistics on the dataset

import MLJ: schema, std, mean, median, coerce, coerce!, scitype
using DataFrames
using CSV
using UrlDownload
using PyPlot

# Load files - this assumes that the repository has been cloned locally,
# that jurisdiction-level files have been concatenated (using the Python script
# in `extract.py`) and saved locally.

path_nat = "/Users/GD/Desktop/wcpdb_nat.csv"
path_subnat = "/Users/GD/Desktop/wcpdb_subnat.csv"

data_nat = CSV.read(path_nat, DataFrame)
data_subnat = CSV.read(path_subnat, DataFrame)

data_nat_2018 = data_nat[data_nat[:Year] .== 2018, :]
data_subnat_2018 = data_subnat[data_subnat[:Year] .== 2018, :]

dropmissing!(data_nat_2018, [:Tax_dummy, :ETS_dummy])
dropmissing!(data_subnat_2018, [:Tax_dummy, :ETS_dummy])

gdf_nat = groupby(data_nat_2018, [:Jurisdiction, :Year])
gdf_subnat = groupby(data_subnat_2018, [:Jurisdiction, :Year])

# Total number of schemes
#temp = combine(gdf_subnat, :Tax_dummy => sum => :Sum_tax, :ETS_dummy => sum => :Sum_ets)
temp = combine(gdf_subnat, :Tax_dummy => sum => :Sum_tax, :ETS_dummy => sum => :Sum_ets)

temp.Sum_tax_bin = [x > 0 ? 1 : 0 for x in temp.Sum_tax]
temp.Sum_tax_ets = [x > 0 ? 1 : 0 for x in temp.Sum_ets]

gtemp = groupby(temp, :Year)
gtemp = combine(gtemp, :Sum_tax_bin => sum => :tax_tot,
                :Sum_tax_ets => sum => :ets_tot)

# Sector level stats
sectors = r"ABFLOW003|ABFLOW012|ABFLOW028|ABFLOW029|ABFLOW034|ABFLOW035"

data_2018 = vcat(data_nat_2018, data_subnat_2018)
dropmissing!(data_2018, :IEA_CODE)
data_2018_sec = data_2018[occursin.(sectors, data_2018.IEA_CODE), :]

gdata_2018_sec = groupby(data_2018_sec, [:Jurisdiction, :Year, :IEA_CODE])

gsec_temp = combine(gdata_2018_sec, :Tax_dummy => sum => :Sum_tax, :ETS_dummy => sum => :Sum_ets)

gsec_temp.Sum_tax_bin = [x > 0 ? 1 : 0 for x in gsec_temp.Sum_tax]
gsec_temp.Sum_tax_ets = [x > 0 ? 1 : 0 for x in gsec_temp.Sum_ets]

ggsec_temp = groupby(gsec_temp, [:Year, :IEA_CODE])
ggsec_temp = combine(ggsec_temp, :Sum_tax_bin => sum => :tax_tot,
                :Sum_tax_ets => sum => :ets_tot)
