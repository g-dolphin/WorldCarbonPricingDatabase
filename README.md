# World Carbon Pricing Database

The present dataset constitutes an extension of a dataset initially developed while pursuing my PhD within the Energy Policy Research Group at the University of Cambridge. Its existence owes much to its support as well as that of the Cambridge Judge Business School and the UK Economic and Social Research Council. Its most recent update was supported by Resources for the Future.

This dataset contains information on carbon pricing mechanisms (carbon taxes or cap-and-trade) introduced around the world since 1990. To date, it is the most comprehensive attempt at providing a consistent-across-jurisdiction description of carbon pricing mechanisms in terms of their sectoral (and fuel) coverage as well as the associated price signal.

## Dataset 
### Description

The database records information on the sectoral scope and price associated with carbon pricing mechanisms, i.e. mechanisms creating an explicit price on CO2 emissions. This information is recorded **at the sector-fuel level**. The sectoral disaggregation of the economy follows the [IPCC 2006 guidelines for national greenhouse gas emission inventories](https://www.ipcc-nggip.iges.or.jp/public/2006gl/). 

A key feature of this dataset is that it provides information structured by territorial jurisdiction, not carbon pricing mechanism. This is achieved by mapping information available for each carbon pricing mechanism onto jurisdictions. This mapping accounts for the possibility that multiple schemes apply to the same emissions sectors and, in such instances, presents information separately for each scheme. It also covers a long period of time (1990-2020) and, hence, allows to (re)construct time series of prices applied to emissions in the jurisdictions where such prices were in place. In addition, its disaggregation by IPCC 2006 sectors  allows for a straightforward integration with several other data sources following the same sectoral disaggregation. 

More details about the methodology supporting the construction of the dataset and the variables included in it are provided in the associated technical note available at [xxx].

### Scope

- Jurisdictions: The dataset currently covers 198 national jurisdictions and 98 sub-national jurisdictions (50 US States, 13 Canadian Provinces and Territories, 3 Japanese Municipalities, 32 Chinese Provinces and Municipalities). It records their institutional development (sectoral and fuel coverage as well as price) from 1990 (year of introduction of the first carbon pricing mechanism in Finland) to this day (currently, 2018 is the last year for which data has been collected).

- Sectors: A table summarising sectoral coverage can be found in the file [IPCC_coverage](https://github.com/gd1989/WorldCarbonPricingDatabase/blob/master/IPCC_coverage.md). In addtion, the file [IPCC2006-IEA-category-codes](https://github.com/g-dolphin/WorldCarbonPricingDatabase/blob/master/IPCC2006-IEA-codes.md) provides a mapping between IPCC sector names, their associated code and the corresponding International Energy Agency sector code. This latter file is particularly useful to the update of the dataset, since its `.csv` files only include sector codes.

- Greenhouse gases: the information currently in the dataset pertains exclusively to policy instruments targeting CO2 emissions. A future iteration will expand the dataset to other Kyoto gases that are subject to pricing mechanisms.

## Repository files

The repository is organised around three main folders:
1. `_data`, which contains the `.csv` files constituting the dataset.
2. `_sources`, which contains the `.csv` files recording the data sources as well as `.csv` files linking every data source citation to their full reference. These 'mapping' files are available in the folder [references](https://github.com/gd1989/WorldCarbonPricingDatabase/tree/master/Sources/references).
3. `_code`, which contains short Python scripts for basic manipulation of the original files.

## Citation

If you use the dataset in scientific publication, we would appreciate a reference to the following paper:

``Dolphin, G., Pollitt, M. and Newbery, D. 2020. The political economy of carbon pricing: a panel analysis. Oxford Economic Papers 72(2): 472-500.``

## License

MIT License

Copyright (c) 2021 g-dolphin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contribution

The dataset is under continuous development. While every precaution has been taken to accurately record coverage and price information, the size of the undertaking has been such that some inaccuracies might remain. Contributions to its development and improvement as well as to update of existing records are welcome (and encouraged).

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
  - Continuing with the above example, suppose you want to update the record(s) for the carbon tax on coal in the power sector in 2018. Then you would update the values of columns `tax`, `tax_rate_excl_ex_clcu`, `tax_ex_rate`, `tax_rate_incl_ex_clcu` corresponding to the (row) entry "Argentina"|"2018"|"1A1A1"|"ABFLOW003"|"Coal/peat" in `CP_Argentina.csv` and the values of the columns `tax`, `tax_rate_excl_ex_clc`, `tax_ex_rate` corresponding to that same entry in the `CP_sources_Argentina.csv` file.
  - **For references, please note (and follow) the citation structure**: "Source_type(Reference_tag[Year]); comment". For instance, if the information was taken from a (country) Report from the OECD published in 2019, you could assign the tag "OECD" to this source and the reference would look like "Report(OECD[2019]); current scheme excludes thermal plants rated <10Mw)".
5. Open the relevant sources mapping file and add the full reference to your source to it
  - For example, in our case, we would open the file `_Reports` and add our reference to the list, providing the required information.
6. Save your files and commit your changes.
7. Push your branch to the remote repository.
  
  
