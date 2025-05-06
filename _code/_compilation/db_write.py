import os

#----------------------------- Helper Functions -----------------------------#

def standardize_name(name):
    return name.replace(".", "").replace(",", "").replace(" ", "_")

def save_jurisdiction_files(df, jurisdictions, std_names, gas, level, base_dir):
    for jur, std_name in zip(jurisdictions, std_names):
        subset = df[df.jurisdiction == jur]
        filename = f"wcpd_{gas.lower()}_{std_name}.csv"
        out_path = os.path.join(base_dir, gas, level, filename)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        subset.to_csv(out_path, index=False)

#------------------------------- File Writing -------------------------------#

# Standardized names
std_country_names = [standardize_name(x) for x in ctry_list]
std_subnat_names = [standardize_name(x) for x in subnat_list]

# Save national and subnational data files
save_jurisdiction_files(wcpd_all_jur, ctry_list, std_country_names, gas, "national", "_dataset/data")
save_jurisdiction_files(wcpd_all_jur, subnat_list, std_subnat_names, gas, "subnational", "_dataset/data")
save_jurisdiction_files(wcpd_all_jur_sources, ctry_list, std_country_names, gas, "national", "_dataset/sources")
save_jurisdiction_files(wcpd_all_jur_sources, subnat_list, std_subnat_names, gas, "subnational", "_dataset/sources")

#---------------------------- Coverage Factors -----------------------------#

coverage_dir = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverageFactor"
os.makedirs(coverage_dir, exist_ok=True)

for scheme in taxes_1_list + ets_1_list + ets_2_list:
    cf[cf.scheme_id == scheme].to_csv(os.path.join(coverage_dir, f"{scheme}_cf.csv"), index=False)

#---------------------------- Scheme Overlap -------------------------------#

overlap_path = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/overlap/overlap_CO2.csv"
os.makedirs(os.path.dirname(overlap_path), exist_ok=True)
overlap.to_csv(overlap_path, index=False)
