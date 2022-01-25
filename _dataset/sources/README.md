# Sources
The present folder contains a 'master' file, which contains all citations referring to the sources of recorded data, and a series of references files, which contain the full reference of the cited sources.

The structure of the 'master' file mimicks that of the dataset. That is, there is one entry (one row) for each *jurisdiction-year-sector* or, when applicable, *jurisdiction-year-sector-fuel* combination.

A reference is provided for every single data point recorded. The referencing structure is as follows: DocumentType(Tag[Year]). For instance, the `Sweden 	1997 	1A4C1 	ABFLOW036 	Coal/peat` entry of the `tax` variable contains the citation `report(SMF-CT[2011])`. 

The cell might also include a comment, seperated from the reference by a semicolon. In our example, it is `; underlying principle of the Swedish CO2 tax is that it applies to motor and heating fuels`. 

The full reference corresponding to this citation can then be looked up in the relevant .csv file. The reference of the 'Report(WB[2014])' citation can be found in the `reports.csv` file.
