import os
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from importlib.machinery import SourceFileLoader

#----------------------------- Setup -----------------------------#
def find_project_root(markers=("pyproject.toml","setup.cfg","requirements.txt",".git",".project-root")):
    p = Path.cwd().resolve()
    for parent in (p, *p.parents):
        if any((parent / m).exists() for m in markers):
            return parent
    return p

# Constants
GAS = "CH4"  # Change to CO2 / CH4 / F-GASES / SF6 as needed
ROOT_DIR = find_project_root()
CODE_DIR = ROOT_DIR / "_code/_compilation/_utils"
RAW_DIR = ROOT_DIR / "_raw"
WCPD_STRUCTURE_PATH = "_raw/_aux_files/wcpd_structure/wcpd_structure_CO2.csv"

# ---------------- Utilities ----------------

def load_module(name, relative_path):
    path = os.path.join(ROOT_DIR, relative_path)
    if not os.path.exists(path):
        logging.error(f"Module not found: {path}")
        raise FileNotFoundError(path)
    return SourceFileLoader(name, path).load_module()

def load_structure() -> pd.DataFrame:
    path = WCPD_STRUCTURE_PATH
    full_path = os.path.join(ROOT_DIR, path)
    return pd.read_csv(full_path)

def create_jurisdiction_frame(wcpd_structure: pd.DataFrame, jurisdictions: list) -> pd.DataFrame:
    records = []
    for jur in jurisdictions:
        temp = wcpd_structure.copy()
        temp["jurisdiction"] = jur
        records.append(temp)
    return pd.concat(records, axis=0)
# ---------------- Main Logic ----------------

logging.info(f"Starting WCPD build for GHG: {GAS}")

gen_func = load_module("general", "/Users/geoffroydolphin/GitHub/ECP/_code/compilation/_dependencies/dep_ecp/ecp_v3_gen_func.py")
jurisdictions_module = load_module("jurisdictions", CODE_DIR / "jurisdictions.py")
ets_prices_module = load_module("ets_prices", CODE_DIR / "ets_prices.py")
tax_rates_module = load_module("tax_rates", CODE_DIR / "tax_rates.py")
ets_scope_module = load_module("ets_scope", RAW_DIR / f"scope/ets/ets_scope_{GAS}.py")
tax_scope_module = load_module("taxes_scope", RAW_DIR / f"scope/tax/taxes_scope_{GAS}.py")

#---------------------- Load WCPD Structure ----------------------#

# Load structure and jurisdiction lists
wcpd_structure = load_structure() # Note: the function currently loads the CO2 structure for all gases.
ctries = jurisdictions_module.jurisdictions["countries"]
subnats = jurisdictions_module.jurisdictions["subnationals"]["Canada"] + jurisdictions_module.jurisdictions["subnationals"]["China"] + jurisdictions_module.jurisdictions["subnationals"]["Japan"] + jurisdictions_module.jurisdictions["subnationals"]["United States"] + jurisdictions_module.jurisdictions["subnationals"]["Mexico"]
all_jurisdictions = ctries + subnats

# Build jurisdiction-level dataframe
wcpd_all_jur = create_jurisdiction_frame(wcpd_structure, all_jurisdictions)
wcpd_all_jur_sources = create_jurisdiction_frame(wcpd_structure, all_jurisdictions)

logging.info(f"Constructed base data for {len(all_jurisdictions)} jurisdictions")

#------------------- Load Price and Scope Data ------------------#

ets_prices = ets_prices_module.load_ets_prices(RAW_DIR / "price")
tax_rates = tax_rates_module.load_tax_rates(RAW_DIR / "price", gas=GAS)
tax_rates.rename(columns={"product": "em_type"}, inplace=True)

ets_scope = ets_scope_module.scope()
ets_scope_data, ets_scope_sources = ets_scope["data"], ets_scope["sources"]
taxes_scope = tax_scope_module.scope()
taxes_scope_data, taxes_scope_sources = taxes_scope["data"], taxes_scope["sources"]

#-------------------- Helper Functions --------------------#

def assign_price_and_currency(df, selection, scheme_df, scheme, yr, columns, fuel=None, source_df=None):
    row_sel = (scheme_df.scheme_id == scheme) & (scheme_df.year == yr) if any(x in scheme for x in ["ets", "obps", "cat", "rggi"]) else (scheme_df.scheme_id == scheme) & (scheme_df.year == yr) & (scheme_df.em_type==fuel)
    try:
        row = scheme_df.loc[row_sel].squeeze()
        price_col = "price" if any(x in scheme for x in ["ets", "obps", "cat", "rggi"]) else "rate"
        df.loc[selection, columns[price_col]] = row["rate"] if "rate" in row else row["allowance_price"]
        df.loc[selection, columns["curr_code"]] = row["currency_code"]
        if source_df is not None:
            source = f"{row['source']}; {row['comment']}"
            source_df.loc[selection, columns[price_col]] = source
    except Exception as e:
        print(f"{scheme} {yr}: {e}")

def ets_db_values(schemes, scheme_no):
    columns = {
        "scheme_1": {"id": "ets_id", "binary": "ets", "price": "ets_price", "curr_code": "ets_curr_code"},
        "scheme_2": {"id": "ets_2_id", "binary": "ets_2", "price": "ets_2_price", "curr_code": "ets_2_curr_code"}
    }[scheme_no]

    for scheme in schemes:
        print(scheme)
        print("Available years for scheme:", list(ets_scope_data[scheme]["jurisdictions"].keys()))
        for yr in ets_scope_data[scheme]["jurisdictions"]:
            print("Processing year:", yr)
            selection = (
                (wcpd_all_jur.year == yr) &
                (wcpd_all_jur.jurisdiction.isin(ets_scope_data[scheme]["jurisdictions"][yr])) &
                (wcpd_all_jur.ipcc_code.isin(ets_scope_data[scheme]["sectors"][yr]))
            )
            selection_src = (
                (wcpd_all_jur_sources.year == yr) &
                (wcpd_all_jur_sources.jurisdiction.isin(ets_scope_data[scheme]["jurisdictions"][yr])) &
                (wcpd_all_jur_sources.ipcc_code.isin(ets_scope_data[scheme]["sectors"][yr]))
            )
            wcpd_all_jur.loc[selection, columns["binary"]] = 1
            wcpd_all_jur.loc[selection, columns["id"]] = scheme
            wcpd_all_jur_sources.loc[selection_src, columns["binary"]] = ets_scope_sources[scheme][yr]
            assign_price_and_currency(wcpd_all_jur, selection, ets_prices, scheme, yr, columns, source_df=wcpd_all_jur_sources)

def tax_db_values(schemes, scheme_no):
    columns = {
        "scheme_1": {"id": "tax_id", "binary": "tax", "rate": "tax_rate_excl_ex_clcu", "curr_code": "tax_curr_code"},
        "scheme_2": {"id": "tax_2_id", "binary": "tax_2", "rate": "tax_2_rate_excl_ex_clcu", "curr_code": "tax_2_curr_code"}
    }[scheme_no]

    for scheme in schemes:
        print(scheme)
        print("Available years for scheme:", list(taxes_scope_data[scheme]["jurisdictions"].keys()))
        for yr in taxes_scope_data[scheme]["jurisdictions"]:
            print("Processing year:", yr)
            juris = taxes_scope_data[scheme]["jurisdictions"][yr]
            sectors = taxes_scope_data[scheme]["sectors"][yr]
            fuels = taxes_scope_data[scheme].get("fuels", {}).get(yr, [None])

            # if GAS == "CO2":
            for fuel in fuels:
            #         sel = (
            #             (wcpd_all_jur.year == yr) &
            #             (wcpd_all_jur.jurisdiction.isin(juris)) &
            #             (wcpd_all_jur.ipcc_code.isin(sectors)) &
            #             (wcpd_all_jur.Product == fuel)
            #         )
            #         sel_src = (
            #             (wcpd_all_jur_sources.year == yr) &
            #             (wcpd_all_jur_sources.jurisdiction.isin(juris)) &
            #             (wcpd_all_jur_sources.ipcc_code.isin(sectors)) &
            #             (wcpd_all_jur_sources.Product == fuel)
            #         )
            #         wcpd_all_jur.loc[sel, columns["binary"]] = 1
            #         wcpd_all_jur.loc[sel, columns["id"]] = scheme
            #         wcpd_all_jur_sources.loc[sel_src, columns["binary"]] = taxes_scope_sources[scheme][yr]
            #         assign_price_and_currency(wcpd_all_jur, sel, tax_rates, scheme, yr, columns, fuel, wcpd_all_jur_sources)
            # else:
                sel = (
                        (wcpd_all_jur.year == yr) &
                        (wcpd_all_jur.jurisdiction.isin(juris)) &
                        (wcpd_all_jur.ipcc_code.isin(sectors))
                    )
                sel_src = (
                        (wcpd_all_jur_sources.year == yr) &
                        (wcpd_all_jur_sources.jurisdiction.isin(juris)) &
                        (wcpd_all_jur_sources.ipcc_code.isin(sectors))
                    )
                wcpd_all_jur.loc[sel, columns["binary"]] = 1
                wcpd_all_jur.loc[sel, columns["id"]] = scheme
                wcpd_all_jur_sources.loc[sel_src, columns["binary"]] = taxes_scope_sources[scheme][yr]
                assign_price_and_currency(wcpd_all_jur, sel, tax_rates, scheme, yr, columns, fuel, wcpd_all_jur_sources)
                
#-------------------- Execution Section --------------------#

if GAS == "CO2":
    ets_1_list = list(ets_scope_data.keys())
    ets_1_list.remove("usa_ma_ets")
    taxes_1_list = list(taxes_scope_data.keys())
    
    ets_db_values(ets_1_list, "scheme_1")
    tax_db_values(taxes_1_list, "scheme_1")
    ets_db_values(["usa_ma_ets"], "scheme_2")
    tax_db_values([], "scheme_2")
    
if GAS == "N2O":
    ets_1_list = list(ets_scope_data.keys())
    taxes_1_list = list(taxes_scope_data.keys())
    taxes_1_list.remove("nld_tax_II")

    ets_db_values(ets_1_list, "scheme_1")
    tax_db_values(taxes_1_list, "scheme_1")
    ets_db_values([], "scheme_2")
    tax_db_values(["nld_tax_II"], "scheme_2")  # Special case for Netherlands tax II
    
else:
    ets_1_list = list(ets_scope_data.keys())
    taxes_1_list = list(taxes_scope_data.keys())

    ets_db_values(ets_1_list, "scheme_1")
    tax_db_values(taxes_1_list, "scheme_1")
    ets_db_values([], "scheme_2")
    tax_db_values([], "scheme_2")
    
#-------------------- Post-processing --------------------#

# Blank cells filling
wcpd_all_jur.loc[wcpd_all_jur.tax!=1, "tax"] = 0
wcpd_all_jur.loc[wcpd_all_jur.ets!=1, "ets"] = 0

# Prepare wcpd_all_jur frame for tax exemptions
## Filling "tax_ex_rate" column with NaN if no tax scheme
wcpd_all_jur.loc[wcpd_all_jur.tax!=1, "tax_ex_rate"] = np.nan
wcpd_all_jur_sources.loc[wcpd_all_jur.tax!=1, "tax_ex_rate"] = np.nan
#all_jur.loc[(all_jur.tax==1) & (all_jur.tax_ex_rate==""), :] #checking whether we've missed any exemptions

wcpd_all_jur_sources.rename(columns={"tax_ex_rate_sources":"tax_ex_rate"}, inplace=True)

## Set default non-"NA" values to 0
wcpd_all_jur.loc[wcpd_all_jur.tax==1, "tax_ex_rate"] = 0
wcpd_all_jur_sources.loc[wcpd_all_jur.tax==1, "tax_ex_rate"] = "NA"

def tax_exemptions(gas): 
        ## Load tax exemptions
        rebate_module = load_module("tax_rebates", RAW_DIR / f"priceRebates/tax/_price_exemptions_tax_{GAS}.py")

        if not rebate_module.tax_exemptions or rebate_module.tax_exemptions == [""]:
            # No exemptions, just fill columns as needed and return
            wcpd_all_jur["tax_rate_incl_ex_clcu"] = "NA"
            
        else:
            i = 0
            for exemption in rebate_module.tax_exemptions:
                for yr in exemption["jurisdiction"].keys():
                    row_selection = (wcpd_all_jur.jurisdiction.isin(exemption["jurisdiction"][yr])) & (wcpd_all_jur.year==yr) & (wcpd_all_jur.ipcc_code.isin(exemption["ipcc"][yr])) & (wcpd_all_jur.Product.isin(exemption["fuel"][yr]))
                    wcpd_all_jur.loc[row_selection, "tax_ex_rate"] = exemption["value"][yr]
                    wcpd_all_jur_sources.loc[row_selection, "tax_ex_rate"] = rebate_module.tax_exemptions_sources[i][yr]

                i+=1
            # Calculate tax rate including rebate
            wcpd_all_jur["tax_rate_incl_ex_clcu"] = wcpd_all_jur["tax_rate_excl_ex_clcu"] * (1 - wcpd_all_jur["tax_ex_rate"])

        # Fill NAs for Product
        wcpd_all_jur["Product"] = wcpd_all_jur["Product"].fillna("NA")
        wcpd_all_jur_sources["Product"] = wcpd_all_jur_sources["Product"].fillna("NA")

        # Replace NA values in columns
        tax_cols = ['tax_id', 'tax_rate_excl_ex_clcu', 'tax_curr_code', 'tax_ex_rate', 'tax_rate_incl_ex_clcu']
        ets_1_cols = ['ets_id', 'ets_price', 'ets_curr_code']
        ets_2_cols = ['ets_2_id', 'ets_2_price', 'ets_2_curr_code']

        wcpd_all_jur.loc[wcpd_all_jur.tax != 1, tax_cols] = "NA"
        wcpd_all_jur.loc[wcpd_all_jur.ets != 1, ets_1_cols + ets_2_cols] = "NA"
        wcpd_all_jur_sources.fillna("NA", inplace=True)
        wcpd_all_jur.fillna("NA", inplace = True)

        # Reorder columns
        final_columns = [
            "jurisdiction", "year", "ipcc_code", "Product", "tax", "ets", "tax_id",
            "tax_rate_excl_ex_clcu", "tax_ex_rate", "tax_rate_incl_ex_clcu", "tax_curr_code",
            "ets_id", "ets_price", "ets_curr_code", "ets_2_id", "ets_2_price", "ets_2_curr_code"
        ]

        source_columns = [
            "jurisdiction", "year", "ipcc_code", "Product", "tax", "ets",
            "tax_rate_excl_ex_clcu", "tax_ex_rate", "ets_price"
        ]

        wcpd_all_jur.loc[:, :] = wcpd_all_jur[final_columns]
        wcpd_all_jur_sources.loc[:, :] = wcpd_all_jur_sources[source_columns]
        
#Run Tax Exemption 
tax_exemptions(GAS)

#-------------------- Coverage Factors --------------------#

stream = open("/Users/geoffroydolphin/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_preprocessing/_coverageFactors.py")
read_file = stream.read()
exec(read_file)

#-------------------- Validation Checks --------------------#

def validate_output(df):
    print("\nRunning validation checks...")

    missing_prices = df[(df["ets"] == 1) & (df["ets_price"] == "NA")]
    if not missing_prices.empty:
        print(f"Warning: {len(missing_prices)} ETS-covered rows have missing prices.")

    missing_tax_rates = df[(df["tax"] == 1) & (df["tax_rate_excl_ex_clcu"] == "NA")]
    if not missing_tax_rates.empty:
        print(f"Warning: {len(missing_tax_rates)} tax-covered rows have missing tax rates.")

    overlapping_schemes = df[(df["ets"] == 1) & (df["ets_2"] == 1)]
    if not overlapping_schemes.empty:
        print(f"Note: {len(overlapping_schemes)} rows have overlapping ETS schemes.")

    print("Validation checks complete.\n")

# Run validation
validate_output(wcpd_all_jur)
