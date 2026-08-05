from pathlib import Path

import pandas as pd


BRONZE_FILE = Path(
    "data/bronze/bronze_sales.parquet"
)

SILVER_FOLDER = Path(
    "data/silver"
)

SILVER_FILE = (
    SILVER_FOLDER / "silver_sales.parquet"
)


def standardize_column_names(
    df: pd.DataFrame,
) -> pd.DataFrame:

    standardized_df = df.copy()

    standardized_df.columns = (
        standardized_df.columns
        .str.strip()
        .str.lower()
        .str.replace(
            " ",
            "_",
            regex=False,
        )
        .str.replace(
            "-",
            "_",
            regex=False,
        )
    )

    return standardized_df


def create_silver_layer() -> pd.DataFrame:

    if not BRONZE_FILE.exists():
        raise FileNotFoundError(
            f"Bronze file not found: {BRONZE_FILE}"
        )

    df = pd.read_parquet(
        BRONZE_FILE
    )

    print("\nCreating Silver layer...")

    initial_rows = len(df)

    df = standardize_column_names(df)

    # Use the generated hash for reliable deduplication
    if "record_hash" in df.columns:
        df = df.drop_duplicates(
            subset=["record_hash"],
            keep="first",
        )
    else:
        df = df.drop_duplicates()

    duplicates_removed = (
        initial_rows - len(df)
    )

    text_columns = [
        "ship_mode",
        "segment",
        "country",
        "city",
        "state",
        "region",
        "category",
        "sub_category",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

    if "postal_code" in df.columns:
        df["postal_code"] = (
            pd.to_numeric(
                df["postal_code"],
                errors="coerce",
            )
            .fillna(0)
            .astype(int)
        )

    numeric_columns = [
        "sales",
        "quantity",
        "discount",
        "profit",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    required_numeric_columns = [
        column
        for column in [
            "sales",
            "quantity",
            "profit",
        ]
        if column in df.columns
    ]

    if required_numeric_columns:
        df = df.dropna(
            subset=required_numeric_columns
        )

    SILVER_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        SILVER_FILE,
        index=False,
    )

    print(
        f"Duplicates removed: "
        f"{duplicates_removed}"
    )

    print(
        f"Silver rows: {len(df)}"
    )

    print(
        "Silver layer created successfully."
    )

    return df