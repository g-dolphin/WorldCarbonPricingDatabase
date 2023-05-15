The file `ipcc2006Full_isic_map` conttains an ISIC/IPCC concordance matrix. Three types of concordances exist:
- 1 to 1
-  1 to N
- N to 1

Concordances typically require the calculation of distribution weights (or keys) to accurately map the target quantity (e.g, emissions) from one classification to another.
1 to 1 and N to 1 concordances do not pose problem as they allocate one or several emission categories to a single ISIC industry. In that case, the distribution key can be calculated from the original data.

1 to many concordances require either (i) aggregation of ISIC categories into 1 or (ii) calculation of distribution keys relying on auxiliary data.

For instance, one can construct distribution keys based on national accounts data. This is the approach followed for the construction of (FIGARO)[https://ec.europa.eu/eurostat/web/esa-supply-use-input-tables/figaro]. The methodology is as follows:
- Assume that the emission intensity (emissions/unit of monetary output) is equal to that of the EU27 average
- Multiply by monetary output of country C
- Sum estimated emissions over all N categories
- Calculate shares of emissions of each category in calculated total
- Use these distribution keys to allocate emissions to these N ISIC sectors (NB: use country-specific emissions data)
