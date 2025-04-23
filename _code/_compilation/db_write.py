
#------------------------------Writing files----------------------------------#
## Main dataset

# Breaking up dataframe into single jurisdiction .csv files
std_country_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in ctry_list]
countries_dic = dict(zip(ctry_list, std_country_names))

std_subnat_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in subnat_list]
subnat_dic = dict(zip(subnat_list, std_subnat_names))


for jur in countries_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("_dataset/data/"+gas+"/national/wcpd_"+gas.lower()+"_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    wcpd_all_jur.loc[wcpd_all_jur.jurisdiction==jur, :].to_csv("_dataset/data/"+gas+"/subnational/wcpd_"+gas.lower()+"_"+subnat_dic[jur]+".csv", index=None)

for jur in countries_dic:
    wcpd_all_jur_sources.loc[wcpd_all_jur_sources.jurisdiction==jur, :].to_csv("_dataset/sources/"+gas+"/national/wcpd_"+gas.lower()+"_"+countries_dic[jur]+".csv", index=None)
for jur in subnat_dic:
    wcpd_all_jur_sources.loc[wcpd_all_jur_sources.jurisdiction==jur, :].to_csv("_dataset/sources/"+gas+"/subnational/wcpd_"+gas.lower()+"_"+subnat_dic[jur]+".csv", index=None)
    
    
## Coverage factors

for scheme in taxes_1_list+ets_1_list+ets_2_list:
    cf.loc[cf.scheme_id==scheme, :].to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverageFactor/"+scheme+"_cf.csv", index=None)

## Scheme overlap files

overlap.to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/overlap/overlap_CO2.csv", index=None)