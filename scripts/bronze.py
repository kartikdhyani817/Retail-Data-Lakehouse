from pathlib import Path
import hashlib

import pandas as pd


BRONZE_FOLDER = Path("data/bronze")
BRONZE_FILE = BRONZE_FOLDER / "bronze_sales.parquet"


def create_row_hash(row: pd.Series) -> str:
    """
    Create a stable unique hash from all values in a row.
    """

    row_text = "|".join(
        str(value).strip()
        for value in row.values
    )

    return hashlib.sha256(
        row_text.encode("utf-8")
    ).hexdigest()


def add_record_hash(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a record_hash column for duplicate and incremental detection.
    """

    hashed_df = df.copy()

    source_columns = [
        column
        for column in hashed_df.columns
        if column != "record_hash"
    ]

    hashed_df["record_hash"] = hashed_df[
        source_columns
    ].apply(
        create_row_hash,
        axis=1,
    )

    return hashed_df


def save_bronze(df: pd.DataFrame) -> dict:
    """
    Incrementally load only new records into the Bronze layer.
    """

    BRONZE_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    incoming_df = add_record_hash(df)

    incoming_rows = len(incoming_df)

    # Remove duplicates inside the new source file
    incoming_df = incoming_df.drop_duplicates(
        subset=["record_hash"]
    )

    source_duplicates = (
        incoming_rows - len(incoming_df)
    )

    # First pipeline execution
    if not BRONZE_FILE.exists():

        incoming_df.to_parquet(
            BRONZE_FILE,
            index=False,
        )

        report = {
            "incoming_rows": incoming_rows,
            "source_duplicates": source_duplicates,
            "existing_bronze_rows": 0,
            "new_rows_loaded": len(incoming_df),
            "final_bronze_rows": len(incoming_df),
        }

        print("\nInitial Bronze load completed.")
        print(f"New rows loaded: {len(incoming_df)}")
        print(f"Bronze rows: {len(incoming_df)}")

        return report

    # Incremental pipeline execution
    existing_df = pd.read_parquet(
        BRONZE_FILE
    )

    # Compatibility with an old Bronze file created before Day 8
    if "record_hash" not in existing_df.columns:
        existing_df = add_record_hash(existing_df)

    existing_rows = len(existing_df)

    existing_hashes = set(
        existing_df["record_hash"].astype(str)
    )

    new_records = incoming_df[
        ~incoming_df["record_hash"]
        .astype(str)
        .isin(existing_hashes)
    ].copy()

    combined_df = pd.concat(
        [
            existing_df,
            new_records,
        ],
        ignore_index=True,
    )

    combined_df = combined_df.drop_duplicates(
        subset=["record_hash"],
        keep="first",
    )

    combined_df.to_parquet(
        BRONZE_FILE,
        index=False,
    )

    report = {
        "incoming_rows": incoming_rows,
        "source_duplicates": source_duplicates,
        "existing_bronze_rows": existing_rows,
        "new_rows_loaded": len(new_records),
        "final_bronze_rows": len(combined_df),
    }

    print("\nIncremental Bronze load completed.")
    print(f"Incoming rows: {incoming_rows}")
    print(f"Source duplicates: {source_duplicates}")
    print(f"Existing Bronze rows: {existing_rows}")
    print(f"New rows loaded: {len(new_records)}")
    print(f"Final Bronze rows: {len(combined_df)}")

    return report