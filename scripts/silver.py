import pandas as pd
from pathlib import Path


BRONZE_FILE = Path("data/bronze/bronze_sales.parquet")


def create_silver_layer():

    df = pd.read_parquet(BRONZE_FILE)

    print("\nCleaning data...")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
    )

    # Fill missing values
    if "postal_code" in df.columns:
        df["postal_code"] = df["postal_code"].fillna(0)

    if "ship_mode" in df.columns:
        df["ship_mode"] = df["ship_mode"].fillna("Unknown")

    # Convert dates
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"])

    if "ship_date" in df.columns:
        df["ship_date"] = pd.to_datetime(df["ship_date"])

    silver_folder = Path("data/silver")
    silver_folder.mkdir(parents=True, exist_ok=True)

    output_file = silver_folder / "silver_sales.parquet"

    df.to_parquet(output_file, index=False)

    print(f"Duplicates Removed : {duplicates}")
    print(f"Final Rows : {len(df)}")
    print("Silver layer created successfully.")

    return df