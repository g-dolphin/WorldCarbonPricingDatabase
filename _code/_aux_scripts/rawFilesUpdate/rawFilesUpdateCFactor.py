import os
import pandas as pd

# Path to the uploaded file
dir_path = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverageFactor"

# List CSV files in the directory
csv_files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]

# required_years
start_year = 2023
last_year = 2025

required_years = set(range(start_year, last_year))  # 2023 to 2024

# Process each file
for file in csv_files:
    file_path = os.path.join(dir_path, file)
    try:
        df = pd.read_csv(file_path)

        # Check if required columns exist
        required_cols = {"scheme_id", "jurisdiction", "ipcc_code", "cf_CO2", "year"}
        if not required_cols.issubset(df.columns):
            print(f"Skipping {file_path}: Missing required columns.")
        else:
            available_years = set(df["year"].dropna().astype(int))
            missing_years = required_years - available_years

            if missing_years:
                print(f"Updating {file_path} - Adding missing years: {', '.join(map(str, missing_years))}")

                # Get the last available year data
                last_year_data = df[df["year"] == df["year"].max()]

                # Generate new rows for each missing year
                new_rows = []
                for year in missing_years:
                    for _, row in last_year_data.iterrows():
                        new_row = row.copy()
                        new_row["year"] = year
                        new_row["cf_CO2"] = None  # Leave cf_CO2 blank
                        new_rows.append(new_row)

                new_df = pd.DataFrame(new_rows)
                df = pd.concat([df, new_df], ignore_index=True).sort_values(by=["scheme_id", "jurisdiction", "ipcc_code", "year"])

                # Save updated file (overwrite)
                df.to_csv(file_path, index=False)
                print(f"Updated {file_path} saved successfully.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
