import duckdb
from pathlib import Path


DATABASE = "retail_lakehouse.duckdb"

GOLD_FOLDER = Path("data/gold")


def run_analytics():

    con = duckdb.connect(DATABASE)

    # Create views directly from Parquet files
    con.execute(f"""
        CREATE OR REPLACE VIEW sales_by_category AS
        SELECT *
        FROM read_parquet('{GOLD_FOLDER / "sales_by_category.parquet"}')
    """)

    con.execute(f"""
        CREATE OR REPLACE VIEW sales_by_region AS
        SELECT *
        FROM read_parquet('{GOLD_FOLDER / "sales_by_region.parquet"}')
    """)

    con.execute(f"""
        CREATE OR REPLACE VIEW top_cities AS
        SELECT *
        FROM read_parquet('{GOLD_FOLDER / "top_cities.parquet"}')
    """)

    con.execute(f"""
        CREATE OR REPLACE VIEW segment_performance AS
        SELECT *
        FROM read_parquet('{GOLD_FOLDER / "segment_performance.parquet"}')
    """)

    print("\nDuckDB Connected Successfully.")

    return con