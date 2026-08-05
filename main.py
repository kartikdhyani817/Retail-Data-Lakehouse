from scripts.analytics import run_analytics
from scripts.bronze import save_bronze
from scripts.data_quality import validate_data
from scripts.gold import create_gold_layer
from scripts.incremental_report import (
    save_incremental_report,
)
from scripts.ingest import load_raw_data
from scripts.quality_report import (
    save_quality_report,
)
from scripts.report import generate_report
from scripts.silver import create_silver_layer


def main() -> None:

    print("=" * 60)
    print("Retail Data Lakehouse")
    print("=" * 60)

    # Extract
    raw_df = load_raw_data()

    # Data-quality validation
    quality_report = validate_data(
        raw_df
    )

    save_quality_report(
        quality_report
    )

    print("\nData Quality Summary\n")

    for key, value in quality_report.items():
        print(f"{key}: {value}")

    # Incremental Bronze loading
    incremental_report = save_bronze(
        raw_df
    )

    save_incremental_report(
        incremental_report
    )

    # Silver transformation
    create_silver_layer()

    # Gold aggregations
    create_gold_layer()

    # DuckDB analytics and reporting
    connection = run_analytics()

    try:
        generate_report(connection)
    finally:
        connection.close()

    print(
        "\nDay 8 completed successfully."
    )


if __name__ == "__main__":
    main()