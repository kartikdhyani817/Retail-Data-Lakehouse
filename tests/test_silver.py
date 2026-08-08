import pandas as pd

from config import SILVER_FILE


def test_silver_file_exists():

    assert SILVER_FILE.exists()


def test_silver_not_empty():

    df = pd.read_parquet(
        SILVER_FILE
    )

    assert not df.empty


def test_silver_has_no_duplicates():

    df = pd.read_parquet(
        SILVER_FILE
    )

    if "record_hash" in df.columns:

        duplicate_count = (
            df["record_hash"]
            .duplicated()
            .sum()
        )

    else:

        duplicate_count = (
            df.duplicated().sum()
        )

    assert duplicate_count == 0


def test_required_columns_exist():

    df = pd.read_parquet(
        SILVER_FILE
    )

    required_columns = [
        "category",
        "sales",
        "quantity",
        "profit",
        "region",
    ]

    for column in required_columns:

        assert column in df.columns


def test_sales_is_numeric():

    df = pd.read_parquet(
        SILVER_FILE
    )

    assert pd.api.types.is_numeric_dtype(
        df["sales"]
    )


def test_quantity_is_numeric():

    df = pd.read_parquet(
        SILVER_FILE
    )

    assert pd.api.types.is_numeric_dtype(
        df["quantity"]
    )