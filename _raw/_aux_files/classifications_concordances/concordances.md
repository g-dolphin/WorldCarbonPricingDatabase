The file `ipcc2006Full_isic_map` conttains an ISIC/IPCC concordance matrix. Three types of concordances exist:
[1] 1 to 1
[2] 1 to N
[3] N to 1

Concordances typically require the calculation of distribution weights (or keys) to accurately map the target quanitity (e.g, emissions) from one classification to another.
1 to 1 and N to 1 concordances do not pose problem as they allocate one or several emission categories to a single ISIC industry. In that case, the distribution key can be calculated from the original data.
1 to many concordances, require calculation of distribution keys relying on auxiliary data.

