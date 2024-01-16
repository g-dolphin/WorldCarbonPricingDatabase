# World Carbon Pricing Database

The present dataset constitutes an extension of a dataset initially developed while pursuing my PhD within the Energy Policy Research Group at the University of Cambridge. Its existence owes much to its support as well as that of the Cambridge Judge Business School and the UK Economic and Social Research Council. Its most recent update was supported by Resources for the Future.

This dataset contains information on carbon pricing mechanisms (carbon taxes or cap-and-trade) introduced around the world since 1990. To date, it is the most comprehensive attempt at providing a consistent-across-jurisdiction description of carbon pricing mechanisms in terms of their sectoral (and fuel) coverage as well as the associated price signal.

In a separate project, it is used in combination with greenhouse gas emissions data to calculate an emissions-weighted average carbon price. This project is hosted here: [https://github.com/g-dolphin/ECP](https://github.com/g-dolphin/ECP).

If this dataset has been useful to you or simply think it's cool, feel free to give it a ⭐!

## Dataset 
### Description

The database records information on the sectoral scope and price associated with carbon pricing mechanisms, i.e. mechanisms creating an explicit price on CO2 emissions. This information is recorded **at the sector-fuel level**. The sectoral disaggregation of the economy follows the [IPCC 2006 guidelines for national greenhouse gas emission inventories](https://www.ipcc-nggip.iges.or.jp/public/2006gl/). 

A key feature of this dataset is that it provides information structured by territorial jurisdiction, not carbon pricing mechanism. This is achieved by mapping information available for each carbon pricing mechanism onto jurisdictions. This mapping accounts for the possibility that multiple schemes apply to the same emissions sectors and, in such instances, presents information separately for each scheme. It also covers a long period of time (1990-2020) and, hence, allows to (re)construct time series of prices applied to emissions in the jurisdictions where such prices were in place. In addition, its disaggregation by IPCC 2006 sectors  allows for a straightforward integration with several other data sources following the same sectoral disaggregation. 

More details about the methodology supporting the construction of the dataset and the variables included in it are provided in the associated Data Descriptor available at [https://doi.org/10.1038/s41597-022-01659-x](https://doi.org/10.1038/s41597-022-01659-x).

### Scope

- Jurisdictions: The dataset currently covers 198 national jurisdictions and 98 sub-national jurisdictions (50 US States, 13 Canadian Provinces and Territories, 3 Japanese Municipalities, 32 Chinese Provinces and Municipalities). It records their institutional development (sectoral and fuel coverage as well as price) from 1990 (year of introduction of the first carbon pricing mechanism in Finland) to this day (currently, 2018 is the last year for which data has been collected).

- Sectors: The dataset covers all IPCC source categories. In addition, the file [IPCC2006-IEA-category-codes]([https://github.com/g-dolphin/WorldCarbonPricingDatabase/blob/master/_raw/_aux_files](https://github.com/g-dolphin/ECP/blob/master/_raw/_aux_files/ipcc2006_iea_category_codes.csv)) provides a mapping between IPCC sector names, their associated code and the corresponding International Energy Agency sector code. This latter file is particularly useful to the update of the dataset, since its `.csv` files only include sector codes.

- Greenhouse gases: the information currently in the dataset pertains exclusively to policy instruments targeting CO2 emissions. A future iteration will expand the dataset to other Kyoto gases that are subject to pricing mechanisms.

## Repository files

The repository is organised around three main directories:
1. `_dataset`, which contains the `.csv` files constituting the dataset. Wihtin that directory, the actual data files can be found under the `data` directory and files with references to the data source under the `sources` directory. The full details of cited references are available in separate files in the [references](https://github.com/g-dolphin/WorldCarbonPricingDatabase/tree/master/_dataset/sources/references) directory.
2. `_raw`, which contains the files recording or coding the pricing mechanisms' design features.
3. `_code`, which contains scripts for the compilation of the dataset as well as short Python scripts for basic manipulation of the dataset files.

**Note** The files located at the ``_raw`` directory contain empty cells. These cells indicate that no relevant information has been recorded.

## Citation

If you use the dataset in scientific publication, please reference the following paper:

``Dolphin, G., Xiahou, Q. World carbon pricing database: sources and methods. Sci Data 9, 573 (2022)``. The article is available in Open Access at [https://doi.org/10.1038/s41597-022-01659-x](https://doi.org/10.1038/s41597-022-01659-x).

## License

This work is licensed under a [Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/) 

## Contribution

The dataset is under continuous development. While every precaution has been taken to accurately record coverage and price information, the size of the undertaking has been such that some inaccuracies might remain. Contributions to its development and improvement as well as to update of existing records are welcome (and encouraged).

### Principles for the selection of sources of information

Contributions to the dataset are greatly appreciated. Please bear in mind the following principles:
1. Updates to the dataset should be accurate and traceable. All proposed updates must provide a complete reference to the source of information.
2. Information is recorded at the lowest level of (IPCC) sectoral(-fuel) disaggregation:
    - Records at higher levels of aggregation are the result of aggregation of lower-level entries
3. No source of information is excluded from the set of admissible sources *a priori*. However:
    - pulicly available sources are preferred to sources subject to access restrictions;
    - 'higher quality' sources are preferred to 'lower quality' ones. For instance, official government legislation published in a jurisdiction's official journal will be prioritised over a third party report on the jurisdiction's policy.
    - to enhance the consistency of the dataset, sources offering standardized information on a larger set of jurisdictions are preferred to jurisdiction-specific sources.
    
### Step-by-step guidance   

! All files under the `_data` directory are the final dataset files and are not the ones to be updated !

The files to be modified to update the dataset are found under the `_raw` and `_compilation` directories, respectively.

If you wish to contribute to the development of the dataset, please follow these steps:
1. Clone the repository to your local machine
2. Create a new (local) branch on which you will execute the files update(s)
3. Save your files and commit your changes.
4. Push your branch to the remote repository.
  
To update the scope of one of the carbon pricing mechanisms, update either `ets_coverage.py` or `taxes_coverage.py` in the directory `_raw/coverage`. To update the price associated with a mechanism, update the corresponding `csv` file in the directory `_raw/price`.
