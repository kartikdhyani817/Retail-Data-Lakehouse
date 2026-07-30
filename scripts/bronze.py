from pathlib import Path


def save_bronze(df):

    bronze_folder = Path("data/bronze")

    bronze_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = bronze_folder / "bronze_sales.parquet"

    df.to_parquet(
        output_file,
        index=False,
    )

    print("\nBronze layer created successfully.")
    print(output_file)