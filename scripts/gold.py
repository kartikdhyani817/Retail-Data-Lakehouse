import pandas as pd
from pathlib import Path


SILVER_FILE = Path("data/silver/silver_sales.parquet")


def create_gold_layer():

    if not SILVER_FILE.exists():
        raise FileNotFoundError(
            f"Silver file not found: {SILVER_FILE}"
        )

    df = pd.read_parquet(SILVER_FILE)

    gold_folder = Path("data/gold")
    gold_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------
    # Sales by Category
    # --------------------------------------------------

    category_sales = (
        df.groupby(
            "category",
            as_index=False
        )
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    category_sales.to_parquet(
        gold_folder / "sales_by_category.parquet",
        index=False
    )

    # --------------------------------------------------
    # Sales by Region
    # --------------------------------------------------

    region_sales = (
        df.groupby(
            "region",
            as_index=False
        )
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    region_sales.to_parquet(
        gold_folder / "sales_by_region.parquet",
        index=False
    )

    # --------------------------------------------------
    # Sales by Sub-Category
    # --------------------------------------------------

    subcategory_sales = (
        df.groupby(
            "sub-category",
            as_index=False
        )
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    subcategory_sales.to_parquet(
        gold_folder / "sales_by_subcategory.parquet",
        index=False
    )

    # --------------------------------------------------
    # Top Cities
    # --------------------------------------------------

    top_cities = (
        df.groupby(
            "city",
            as_index=False
        )
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
        .head(10)
    )

    top_cities.to_parquet(
        gold_folder / "top_cities.parquet",
        index=False
    )

    # --------------------------------------------------
    # Segment Performance
    # --------------------------------------------------

    segment_performance = (
        df.groupby(
            "segment",
            as_index=False
        )
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum"),
            average_discount=("discount", "mean")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    segment_performance.to_parquet(
        gold_folder / "segment_performance.parquet",
        index=False
    )

    # --------------------------------------------------
    # Overall KPIs
    # --------------------------------------------------

    total_sales = float(df["sales"].sum())
    total_profit = float(df["profit"].sum())
    total_quantity = int(df["quantity"].sum())
    average_discount = float(df["discount"].mean())

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0
        else 0
    )

    overall_kpis = pd.DataFrame(
        [
            {
                "total_sales": round(total_sales, 2),
                "total_profit": round(total_profit, 2),
                "total_quantity": total_quantity,
                "average_discount": round(
                    average_discount,
                    4
                ),
                "profit_margin_percent": round(
                    profit_margin,
                    2
                ),
                "total_records": len(df)
            }
        ]
    )

    overall_kpis.to_parquet(
        gold_folder / "overall_kpis.parquet",
        index=False
    )

    print("\nGold layer created successfully.")

    print("\nBusiness tables created:")
    print("- sales_by_category.parquet")
    print("- sales_by_region.parquet")
    print("- sales_by_subcategory.parquet")
    print("- top_cities.parquet")
    print("- segment_performance.parquet")
    print("- overall_kpis.parquet")

    return {
        "category_sales": category_sales,
        "region_sales": region_sales,
        "subcategory_sales": subcategory_sales,
        "top_cities": top_cities,
        "segment_performance": segment_performance,
        "overall_kpis": overall_kpis
    }