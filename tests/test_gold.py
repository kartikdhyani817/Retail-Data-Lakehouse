import pandas as pd

from config import GOLD_DIR


def test_gold_directory_exists():

    assert GOLD_DIR.exists()


def test_category_dataset_exists():

    file_path = (
        GOLD_DIR
        / "sales_by_category.parquet"
    )

    assert file_path.exists()


def test_region_dataset_exists():

    file_path = (
        GOLD_DIR
        / "sales_by_region.parquet"
    )

    assert file_path.exists()


def test_kpi_dataset_exists():

    file_path = (
        GOLD_DIR
        / "overall_kpis.parquet"
    )

    assert file_path.exists()


def test_category_dataset_not_empty():

    file_path = (
        GOLD_DIR
        / "sales_by_category.parquet"
    )

    df = pd.read_parquet(
        file_path
    )

    assert not df.empty


def test_kpi_values():

    file_path = (
        GOLD_DIR
        / "overall_kpis.parquet"
    )

    df = pd.read_parquet(
        file_path
    )

    assert not df.empty

    assert (
        df.iloc[0]["total_sales"]
        > 0
    )


def test_expected_gold_files():

    expected_files = [
        "sales_by_category.parquet",
        "sales_by_region.parquet",
        "sales_by_subcategory.parquet",
        "top_cities.parquet",
        "segment_performance.parquet",
        "overall_kpis.parquet",
    ]

    for file_name in expected_files:

        assert (
            GOLD_DIR / file_name
        ).exists()