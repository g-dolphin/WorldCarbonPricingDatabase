import os
import pandas as pd

# Directory containing price data
#price_dir = os.path.join(repo_dir, "_raw", "price")
price_dir = "/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/price"


# Ensure the directory exists
if not os.path.exists(price_dir):
    print(f"Error: Directory {price_dir} does not exist.")
    exit()

# List CSV files in the directory
csv_files = [f for f in os.listdir(price_dir) if f.endswith(".csv")]
csv_files.remove('_ICAP_allowance_prices.csv')

missing_data_report = []

# required_years
start_year = 2023
last_year = 2025

required_years = set(range(start_year, last_year))  # 2023 to 2024

# Check for missing rows and data
for file in csv_files:
    file_path = os.path.join(price_dir, file)
    try:
        df = pd.read_csv(file_path, dtype={"rate": str}, na_values=[""])

        if "year" not in df.columns:
            print(f"Skipping {file} (No 'year' column found)")
            continue

        # Identify missing years
        available_years = set(df["year"].dropna().astype(int))
        missing_years = required_years - available_years

        if missing_years:
            missing_data_report.append({"File": file, "Issue": f"Missing years: {', '.join(map(str, missing_years))}"})

        # Check for missing values in required years
        df_filtered = df[df["year"].isin(required_years)]
        missing_values = df_filtered.isnull().sum()

        if missing_values.sum() > 0:
            missing_cols = missing_values[missing_values > 0].index.tolist()
            missing_data_report.append(
                {"File": file, "Issue": f"Missing values in columns for 2020-2024: {', '.join(missing_cols)}"}
            )

    except Exception as e:
        print(f"Error processing {file}: {e}")

# Output report
if missing_data_report:
    report_df = pd.DataFrame(missing_data_report)
    report_df.to_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_update_management/update_report.csv")

else:
    print("All files contain complete data for 2020-2024.")
