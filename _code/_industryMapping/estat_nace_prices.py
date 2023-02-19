# Script implementing calculation of carbon prices for NACE industries
#

# Load air emissions account

# Load national accounts


# Mapping between IEA ans ISIC/NACE categories
# 1-1 and 1-N mapping

# Approach: 
# 1. Match IEA with ISIC sector at relevant level of aggregation
# 2. For emission categories that have a 1-N mapping, calculate distribution keys as per FIGARO methodology
# 3. Use distribution keys to associate emissions with industries
# 4. Associate carbon prices with IEA/IPCC categories
# 5. Calculate emissions-weighted average at industry level.

# For sub-industries, apply the price of the higher industry aggregate