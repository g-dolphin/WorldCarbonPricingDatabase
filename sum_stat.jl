
import Pkg

Pkg.add("MLJ")
Pkg.add("PyPlot")
Pkg.add("UrlDownload")
Pkg.add("DataFrames")
Pkg.add("CSV")

import MLJ: schema, std, mean, median, coerce, coerce!, scitype
using DataFrames
using UrlDownload
using PyPlot

raw_data = urldownload("https://raw.githubusercontent.com/gd1989/WorldCarbonPricingDatabase/master/Data/national_jur/CP_Afghanistan.csv")
data = DataFrame(raw_data)

count = groupby(data, [:Year, :IPCC_cat_code])
