import os
import pandas as pd

# Directory containing price data
# price_dir = os.path.join(repo_dir, "_raw", "price")
price_dir = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price"

# Ensure the directory exists
if not os.path.exists(price_dir):
    print(f"Error: Directory {price_dir} does not exist.")
    exit()

# List CSV files in the directory
csv_files = [f for f in os.listdir(price_dir) if f.endswith(".csv")]
csv_files.remove('_ICAP_allowance_prices.csv')

# required_years
start_year = 2023
last_year = 2025

required_years = set(range(start_year, last_year))  # 2023 to 2024

# Process each file
for file in csv_files:
    file_path = os.path.join(price_dir, file)
    try:
        df = pd.read_csv(file_path)

        if "year" not in df.columns:
            print(f"Skipping {file} (No 'year' column found)")
            continue

        available_years = set(df["year"].dropna().astype(int))
        missing_years = required_years - available_years

        if missing_years:
            print(f"Updating {file} - Adding missing years: {', '.join(map(str, missing_years))}")

            if "tax" in file.lower():
                # Ensure required columns exist
                required_cols = {"scheme_id", "ghg", "product", "rate", "year"}
                if not required_cols.issubset(df.columns):
                    print(f"Skipping {file}: Missing required columns")
                    continue

                # Get last available year data
                last_year_data = df[df["year"] == df["year"].max()]

                # Get value in cells for last year of data
                scheme_id = last_year_data["scheme_id"]
                curr_code = last_year_data["currency_code"]

                # Generate new rows for each missing year
                new_rows = []
                for year in missing_years:
                    for _, row in last_year_data.iterrows():
                        new_row = row.copy()
                        new_row["scheme_id"] = scheme_id
                        new_row["year"] = year
                        new_row["rate"] = None  # Leave rate blank
                        new_row["currency_code"] = curr_code
                        new_rows.append(new_row)

                new_df = pd.DataFrame(new_rows)
                df = pd.concat([df, new_df], ignore_index=True).sort_values(by="year")

            elif any(x in file.lower() for x in ["ets", "obps", "rggi"]):
                # Just add a single row per missing year, copying structure
                new_rows = []
                for year in missing_years:
                    new_row = {col: None for col in df.columns}  # Blank row
                    new_row["year"] = year
                    new_rows.append(new_row)

                new_df = pd.DataFrame(new_rows)
                df = pd.concat([df, new_df], ignore_index=True).sort_values(by="year")

            # Save updated file
            df.to_csv(file_path, index=False)
            print(f"Updated {file} saved successfully.")

    except Exception as e:
        print(f"Error processing {file}: {e}")

print("Missing years added where necessary. All files updated.")
