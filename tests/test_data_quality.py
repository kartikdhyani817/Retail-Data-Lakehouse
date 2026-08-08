import pandas as pd

from scripts.data_quality import validate_data


def create_sample_data():

    return pd.DataFrame(
        {
            "category": [
                "Technology",
                "Furniture",
                "Office Supplies",
            ],
            "sales": [
                1000.0,
                500.0,
                250.0,
            ],
            "quantity": [
                2,
                1,
                4,
            ],
            "profit": [
                200.0,
                -50.0,
                40.0,
            ],
        }
    )


def test_total_rows():

    df = create_sample_data()

    report = validate_data(df)

    assert report["Total Rows"] == 3


def test_total_columns():

    df = create_sample_data()

    report = validate_data(df)

    assert report["Total Columns"] == 4


def test_duplicate_detection():

    df = create_sample_data()

    df = pd.concat(
        [df, df.iloc[[0]]],
        ignore_index=True,
    )

    report = validate_data(df)

    assert report["Duplicate Rows"] == 1


def test_negative_sales():

    df = create_sample_data()

    report = validate_data(df)

    assert report["Negative Sales"] == 0


def test_negative_profit_detection():

    df = create_sample_data()

    report = validate_data(df)

    assert report["Negative Profit"] == 1


def test_zero_quantity():

    df = create_sample_data()

    report = validate_data(df)

    assert report["Zero Quantity"] == 0