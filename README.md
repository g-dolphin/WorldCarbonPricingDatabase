# World Carbon Pricing Database

The present dataset constitutes an extension of a dataset initially developed while pursuing my PhD within the Energy Policy Research Group at the University of Cambridge. Its existence owes much to its support as well as that of the Cambridge Judge Business School and the UK Economic and Social Research Council.

This dataset contains information on carbon pricing mechanisms (carbon taxes or cap-and-trade) introduced around the world since 1990.
To date, it is the most comprehensive attempt at providing a systematic description of carbon pricing mechanisms in terms of their sectoral (and fuel) coverage as well as the associated price signal.

## Dataset 
### Description

The database records information on the coverage and price associated with mechanisms creating an explicit price on CO2 emissions **at the sector-fuel level**. It records separately information about carbon taxes and cap-and-trade mechanisms. The sectoral disaggregation of the economy follows the [IPCC 2006 guidelines for national greenhouse gas emission inventories](https://www.ipcc-nggip.iges.or.jp/public/2006gl/). 

- Coverage of a given sector-fuel level is recorded as binary 0/1 variable.
- Prices are recorded in current local currency units and expressed per tonne of CO_2. 
  - For taxes, the recorded value is the administratively set rate of the tax.
  - For emission trading systems (cap-and-trade), the recorded value is the yearly average of (daily) allowance prices.

For carbon taxes, the dataset also records separately 'price-based', sector-fuel specific, exemptions. That is, it records whether a given carbon tax regulation contains provisions for some sectors and/or fuels to be faced with a different tax rate. In practice, exemptions implying a different price of CO2 across fuels are rare (though not inexistant); more common are exemptions set at the sector level and implying a different price of CO2 across sectors.

The dataset does not, however, account for 'quantity-based' exemptions. This category includes all exemptions that allow firms in specified sectors and/or meeting certain conditions within those sectors to exempt part of their emissions from the tax or to waive their obligation to surrender allowances for these emissions. For instance, the dataset currently does not contain information on the emissions thresholds above which firms (or plants) become liable for the carbon tax or have to surrender emissions allowances. Similarly, it does not have data on the 'offset mechanisms' by which firms can waive their tax or allowance surrendering obligation on a share of their total emissions.

### Scope

The dataset currently covers 198 national jurisdictions and 98 sub-national jurisdictions (50 US States, 13 Canadian Provinces and Territories, 3 Japanese Municipalities, 32 Chinese Provinces and Municipalities). It records their institutional development (sectoral and fuel coverage as well as price) from 1990 (year of introduction of the first carbon pricing mechanism in Finland) to this day (currently, 2018 is the last year for which data has been collected).

A table summarising sectoral coverage can be found in the file [IPCC_coverage](https://github.com/gd1989/WorldCarbonPricingDatabase/blob/master/IPCC_coverage.md). In addtion, the file [IPCC2006-IEA-category-codes]() provides a mapping between IPCC sector names, their associated code and the corresponding International Energy Agency sector code. This latter file is particularly useful to the update of the dataset, since its `.csv` files only include sector codes.

## Repository files

The repository is organised around three main folders:
1. `Data`, which contains the `.csv` files constituting the dataset
2. `Sources`, which contains the `.csv` files recording the data sources as well as `.csv` files linking every data source citation to their full reference. These 'mapping' files are available in the folder [references](https://github.com/gd1989/WorldCarbonPricingDatabase/tree/master/Sources/references)
3. `Scripts_basic`, which contains short Python scripts for basic manipulation of the original files

## Contribution

The dataset is under continuous development. While every precaution has been taken to accurately record coverage and price information for each carbon pricing mechanism, the size of the undertaking has been such that some inaccuracies might remain. Contributions to its development and improvement as well as to update of existing records are welcome (and encouraged).

The initial dataset development focused on IPCC sectors (and sub-sectors therein) 1. Energy and 2. Industrial Processes and Product Use. More specifically, I recorded information on sub-sectors of category 1A (Fuel Combustion Activities), 1B2 (Fugitive Emissions from Fuels - Oil and Natural Gas) and 2A1 (Cement Production). Information on carbon pricing mechanisms in other sectors has, so far, not been systematically recorded. This focus is the result of a decision criterion: availability of comprehensive standardized international CO_2 emissions data for a given IPCC sector. An extension of records to other IPCC sectors would be a welcome addition to the dataset and will be pursued as time and resources allow.

### Contributing to the dataset: step-by-step guidance

Contributions to the dataset are greatly appreciated. Please bear in mind the following principles:
1. Updates to the dataset should be accurate and traceable. All proposed updates must provide a complete reference to the source of information.
2. Manual entries should be made at the lowest level of (IPCC) sectoral(-fuel) disaggregation:
    - Records at higher levels of aggregation will be the result of aggregation of lower-level entries (which will be calculated at later stage, following a set of yet-to-define aggregation rules)
3. No source of information is excluded from the set of admissible sources *a priori*. However:
    - pulicly available sources are preferred to sources subject to access restrictions;
    - 'higher quality' sources are preferred to 'lower quality' ones. For instance, official government legislation published in a jurisdiction's official journal will be prioritised over a third party report on the jurisdiction's policy.
    - to enhance the consistency of the dataset, sources offering standardized information on a larger set of jurisdictions are preferred to jurisdiction-specific sources.
    
If you wish to contribute to the development of the dataset, please follow these steps:
1. Clone the repository to your local machine
2. Create a new (local) branch on which you will execute the files update(s)
3. Open the `Data`and `Sources` `.csv` files corresponding to the jurisdiction(s) whose records you intend to update.
  - For example, if you want to update a record for Argentina, you open the files `CP_Argentina.csv` and `CP_sources_Argentina.csv` that will be available at `[...]/GitHub/WorldCarbonPricingDatabase/Data/national_jur/` and `[...]/GitHub/WorldCarbonPricingDatabase/Data/national_jur/`respectively.  
4. Update the relevant records in both the `Data`and `Sources` files.
  - Continuing with the above example, suppose you want to update the record(s) for the carbon tax on coal in the power sector in 2018. Then you would update the values of columns `Tax_dummy`, `Tax_rate_excl_ex_clc`, `Tax_ex_rate`, `Tax_rate_incl_ex_clc` corresponding to the (row) entry "Argentina"|"2018"|"1A1A1"|"ABFLOW003"|"Coal/peat" in `CP_Argentina.csv` and the values of the columns `Tax_dummy`, `Tax_rate_excl_ex_clc`, `Tax_ex_rate` corresponding to that same entry in the `CP_sources_Argentina.csv` file.
  - **For references, please note (and follow) the citation structure**: "Source_type(Reference_tag[Year]); comment". For instance, if the information was taken from a (country) Report from the OECD published in 2019, you could assign the tag "OECD" to this source and the reference would look like "Report(OECD[2019]); current scheme excludes thermal plants rated <10Mw)".
5. Open the relevant sources mapping file and add the full reference to your source to it
  - For example, in our case, we would open the file `_Reports` and add our reference to the list, providing the required information.
6. Save your files and commit your changes.
7. Push your branch to the remote repository.
  
  
