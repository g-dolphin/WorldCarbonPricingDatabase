# Carbon pricing mechanisms dataset

The .csv files in the above folders contain the carbon pricing schemes' institutional variables for [xx] national and [xx] sub-national jurisdictions. For each jurisdiction and each year between 1989 and 2020, these variables are recorded at the sector or sector-fuel level.  

The first five columns of each dataframe (.csv file) record the `keys` of each entry. The corresponding column titles are: jurisdiction, year, ipcc_code, iea_code, Product. 

The remaining columns record the variables' value. The following variables are included. 
- `tax`: a binary variable indicating coverage (1) or not (0) by a carbon tax
- `ets`: a binary variable indicating coverage (1) or not (0) by an emission trading system
- `tax_rate_excl_ex_clc`: tax rate in current local currency unit per tonne of CO2
- `tax_ex_rate`: rate of exemption applicable (e.g. 0.1 if a 10% reduction on full rate is granted)
- `tax_rate_incl_ex_clc`: net tax rate (accounting for exemption) in current local currency unit per tonne of CO2
- `tax_curr_code`: ISO code of the currency in which the tax rate is recorded (e.g. EUR for euro)
- `ets_price`: price of an emissions allowance in current local currency unit per tonne of CO2
- `ets_curr_code`: ISO code of the currency in which the allowance price is recorded (e.g. EUR for euro)

## Different tax rates (in LCU/tCO2) applicable to different fuels

It may be the case that different tax rates are applied to different fuels within the the main fuel categories (i.e. Coal/peat, Natural Gas, Oil). This comes in the form of differentiated applicable tax rates or varying exemption rates. This the case for Mexico and Argentina, for instance. 

In such cases, the value recorded in the dataset is the highest rate applicable to the fuel category. The fuel- and/or sector-fuel-specific rates are recorded in the *country notes* associated with each country.

## "NA" and empty values

- **“NA” values** should not be interpreted as either ‘missing’ or ‘zero’. Rather they indicate that the column is ‘not applicable’ for the particular row you are looking at. There are several types of instances in which "NA" is used:
    1. In `keys` columns: for instance, in the column “iea_code”, there is only such a code for IPCC Energy sectors, not the others. 
    2. In `variables` columns:
        - For the columns recording price level and exemptions, there will be an “NA” entry if there is no such scheme in place, i.e. if the value of the corresponding coverage binary column is set to 0.
