import os
import glob
import pandas as pd

# --- Configuration ---
PRICE_FOLDER = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price"  # Folder containing CSV files.

END_YEAR = 2024


# --- Get start year ---

start_year_file = pd.read_csv('/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/_aux_files/scheme_description.csv')
start_year = dict(zip(start_year_file.scheme_id, start_year_file.implementation_year))

# --- Helper Function ---
def get_price_column(columns):
    """Return 'rate' if present; otherwise return 'allowance_price' if present; else None."""
    if "rate" in columns:
        return "rate"
    elif "allowance_price" in columns:
        return "allowance_price"
    else:
        return None

# --- Reports Initialization ---
# Report 1: Missing rows (years) for each file.
# { filename: { scheme_id: [missing_years, ...] } }
missing_rows_report = {}

# Report 2: Rows with missing data in required columns.
# { filename: { scheme_id: [ { 'year': ..., 'missing_columns': [...] }, ... ] } }
missing_fields_report = {}

# --- Process Each CSV File in the Folder ---
file_list = glob.glob(os.path.join(PRICE_FOLDER, "*.csv"))
file_list.remove('/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price/_ICAP_allowance_prices.csv')

for filepath in file_list:
    filename = os.path.basename(filepath)
    
    try:
        # Read all columns as strings so we can easily test for emptiness.
        df = pd.read_csv(filepath, keep_default_na=False, na_values=[''])
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    # Retrieve the static scheme_id from the first row.
    scheme_id = df.loc[0, "scheme_id"] if "scheme_id" in df.columns else "Unknown scheme"
    
    # Convert the 'year' column to numeric (coerce errors).
    if "year" not in df.columns:
        print(f"File {filename} does not have a 'year' column; skipping.")
        continue
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    
    try:
        # Dynamically assign START_YEAR based on the corresponding scheme_id from the CSV
        START_YEAR = int(start_year[scheme_id])
        print(f"START_YEAR for scheme_id '{scheme_id}' is {START_YEAR}")

        YEARS_TO_CHECK = set(range(START_YEAR, END_YEAR + 1))

        # --- Missing Rows Check ---
        # Consider only rows with valid numeric years.
        valid_years = df.dropna(subset=["year"])
        years_present = set(valid_years["year"].dropna().astype(int).tolist()) & YEARS_TO_CHECK
        missing_years = sorted(YEARS_TO_CHECK - years_present)
        
        if missing_years:
            missing_rows_report.setdefault(filename, {})[scheme_id] = missing_years

        # --- Missing Data Check ---
        # Identify which price column to check.
        price_col = get_price_column(df.columns)
        # Build list of required columns.
        required_columns = ["comment", "source", "currency_code"]
        if price_col is not None:
            required_columns.append(price_col)
        else:
            # If neither expected price column exists, include a placeholder.
            required_columns.append("rate/allowance_price")
        
        # Process only rows with years in the specified time span.
        df_subset = df[df["year"].notna() & df["year"].astype(float).between(START_YEAR, END_YEAR)]
        
        for _, row in df_subset.iterrows():
            year_val = row["year"]
            missing_cols = []
            for col in required_columns:
                # If the expected column isn't in the DataFrame, mark it missing.
                if col not in df.columns:
                    missing_cols.append(col)
                else:
                    cell_val = row[col]
                    # Check for a missing value: either a pandas NA or an empty string (after stripping).
                    if pd.isna(cell_val) or (isinstance(cell_val, str) and cell_val.strip() == ""):
                        missing_cols.append(col)
            if missing_cols:
                try:
                    year_int = int(float(year_val))
                except Exception as e:
                    print(f"Error converting year {year_val}: {e}")
                    year_int = year_val  # Or handle it in another appropriate way

                if filename not in missing_fields_report:
                    missing_fields_report[filename] = {}

                if scheme_id not in missing_fields_report[filename]:
                    missing_fields_report[filename][scheme_id] = []

                missing_fields_report[filename][scheme_id].append({
                    "year": year_int,
                    "missing_columns": missing_cols
                })
    except Exception as e:
        print(f"Scheme id '{scheme_id}' not found in scheme_description.csv file")

# --- Output the Reports ---
# --- Flatten and Write Reports to CSV ---

# Flatten missing_rows_report: one row per (filename, scheme_id)
rows_list = []
for file, schemes in missing_rows_report.items():
    for scheme, years in schemes.items():
        rows_list.append({
            "filename": file,
            "scheme_id": scheme,
            "missing_years": ", ".join(map(str, years))
        })
df_missing_rows = pd.DataFrame(rows_list)
df_missing_rows.to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_update_management/missing_rows_report.csv", index=False)
print("Missing rows report written to missing_rows_report.csv")

# Flatten missing_fields_report: one row per (filename, scheme_id, year)
fields_list = []
for file, schemes in missing_fields_report.items():
    for scheme, issues in schemes.items():
        for issue in issues:
            fields_list.append({
                "filename": file,
                "scheme_id": scheme,
                "year": issue["year"],
                "missing_columns": ", ".join(issue["missing_columns"])
            })
df_missing_fields = pd.DataFrame(fields_list)
df_missing_fields.to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_update_management/missing_fields_report.csv", index=False)
print("Missing fields report written to missing_fields_report.csv")
