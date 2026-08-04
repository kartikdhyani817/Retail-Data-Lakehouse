import pandas as pd
from pathlib import Path


def validate_data(df: pd.DataFrame):

    report = {}

    report["Total Rows"] = len(df)
    report["Total Columns"] = len(df.columns)

    report["Duplicate Rows"] = int(df.duplicated().sum())

    report["Missing Values"] = (
        df.isnull().sum().sum()
    )

    if "sales" in df.columns:
        report["Negative Sales"] = int(
            (df["sales"] < 0).sum()
        )

    if "profit" in df.columns:
        report["Negative Profit"] = int(
            (df["profit"] < 0).sum()
        )

    if "quantity" in df.columns:
        report["Zero Quantity"] = int(
            (df["quantity"] <= 0).sum()
        )

    return report