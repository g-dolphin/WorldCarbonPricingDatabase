# Carbon pricing mechanisms dataset [TEST]

The .csv files in the above folders contain the carbon pricing schemes' institutional variables for [xx] national and [xx] sub-national jurisdictions. For each jurisdiction and each year between 1989 and 2018, these variables are recorded at the sector or sector-fuel level.  

The first five columns of each dataframe (.csv file) record the `keys` of each entry. The corresponding column titles are: Jurisdiction, Year, IPCC_cat_code, IEA_CODE, Product. 

The remaining columns record the variables' value. The following variables are included. 
- `Tax_dummy`: a binary variable indicating coverage (1) or not (0) by a carbon tax
- `ETS_dummy`: a binary variable indicating coverage (1) or not (0) by an emission trading system
- `Tax_rate_excl_ex_clc`: tax rate in current local currency unit per tonne of CO2
- `Tax_ex_rate`: rate of exemption applicable (e.g. 0.1 if a 10% reduction on full rate is granted)
- `Tax_rate_incl_ex_clc`: net tax rate (accounting for exemption) in current local currency unit per tonne of CO2
- `Tax_curr_code`: ISO code of the currency in which the tax rate is recorded (e.g. EUR for euro)
- `ETS_price`: price of an emissions allowance in current local currency unit per tonne of CO2
- `ETS_curr_code`: ISO code of the currency in which the allowance price is recorded (e.g. EUR for euro)

## Different tax rates (in LCU/tCO2) applicable to different fuels

It may be the case that different tax rates are applied to different fuels within the the main fuel categories (i.e. Coal/peat, Natural Gas, Oil). This comes in the form of differentiated applicable tax rates or varying exemption rates. This the case for Mexico and Argentina, for instance. 

In such cases, the value recorded in the dataset is the highest rate applicable to the fuel category. The fuel- and/or sector-fuel-specific rates are recorded in the *country notes* associated with each country.

## "NA" and empty values

- **“NA” values** should not be interpreted as either ‘missing’ or ‘zero’. Rather they indicate that the column is ‘not applicable’ for the particular row you are looking at. There are several types of instances in which "NA" is used:
    1. In `keys` columns: for instance, in the column “IEA_CODE”, there is only such a code for IPCC Energy sector, not the others. 
    2. In `variables` columns:
        - For the columns recording price level and exemptions, there will be an “NA” entry if there is no such scheme in place, i.e. if the value of the corresponding coverage dummy column is set to 0.
    
- **Empty cells** are cells that ought to be filled in future. But here again, there are different types of instances which would lead to an empty cell:
    1. For IPCC sectors above the lowest level of disaggregation: currently empty as aggregate level records have not been determined/calculated yet.
    2. For disaggregated levels: no data has been recorded yet! ==> feel free to contribute :) 
        - The sectors for which data has so far been recorded are listed [here](https://github.com/g-dolphin/WorldCarbonPricingDatabase/blob/master/IPCC_coverage.md). Hence, in general, data is missing for all sectors other than these ones (AND in which some CO2 emissions occur; otherwise it would be a 'Not Applicable' case). 
