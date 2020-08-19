# World Carbon Pricing Database

The present dataset constitutes an extension of a dataset initially developed while pursuing my PhD within the Energy Policy Research Group at the University of Cambridge. Its existence owes much to its support as well as that of the Cambridge Judge Business School and of the UK Economic and Social Research Council.

This dataset contains information on carbon pricing mechanisms (carbon taxes or cap-and-trade) introduced around the world since 1990.
To date, it is the most comprehensive attempt at providing a systematic description of carbon pricing mechanisms in terms of their sectoral (and fuel) coverage and associated price signal.

## Dataset description
### Dataset scope

The dataset currently covers [xx] national jurisdictions and [xx] sub-national jurisdictions (50 US States, 13 Canadian Provinces and Territories, [yy] Japanese Municipalities, [xx] Chinese Provinces). It records their institutional development (sectoral and fuel coverage as well as price) from 1990 (year of introduction of the first carbon pricing mechanism in Finland) to this day (currently, 2018 is the last year for which data has been collected).

The database records information on the coverage and price associated with mechanisms placing a price on CO2 emissions **at the sector-fuel level**. It records separately information about carbon taxes and cap-and-trade mechanisms.

- The sectoral disaggregation of the economy follows the [IPCC 2006 guidelines for national greenhouse gas emission inventories](https://www.ipcc-nggip.iges.or.jp/public/2006gl/). 
- Coverage of a given at the sector-fuel level is recorded as binary 0/1 variable.
- Prices are recorded in current local currency units per tonne of CO_2.

A table summarising sectoral coverage can be found in the file [IPCC_coverage](https://github.com/gd1989/WorldCarbonPricingDatabase/blob/master/IPCC_coverage.md).

## Repository files

The repository is organised around three main folders:
1. Carbon pricing mechanisms dataset
2. Meta-data: .csv files linking every data entry to their original source
3. Data sources: original documents and files from which the data was obtained / scraped.

## Contribution

The dataset is under continuous development. While every precaution has been taken to accurately record coverage and price information for each carbon pricing mechanism, the size of the undertaking has been such that some inaccuracies might remain. Contributions to its development and improvement as well as to update of existing records are welcome (and encouraged).

The initial dataset development focused on IPCC sectors (and sub-sectors therein) 1. Energy and 2. Industrial Processes and Product Use. More specifically, I recorded information on sub-sectors of category 1A (Fuel Combustion Activities), 1B2 (Fugitive Emissions from Fuels - Oil and Natural Gas) and 2A1 (Cement Production). Information on carbon pricing mechanisms in other sectors has, so far, not been systematically recorded. This focus is the result of a decision criterion: availability of comprehensive standardized international CO_2 emissions data for a given IPCC sector. An extension of records to other IPCC sectors would be a welcome addition to the dataset and will be pursued as time and resources allow.

