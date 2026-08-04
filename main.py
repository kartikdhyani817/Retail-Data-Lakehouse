from scripts.ingest import load_raw_data
from scripts.data_quality import validate_data
from scripts.quality_report import save_quality_report

from scripts.bronze import save_bronze
from scripts.silver import create_silver_layer
from scripts.gold import create_gold_layer
from scripts.analytics import run_analytics
from scripts.report import generate_report


def main():

    print("=" * 50)
    print("Retail Data Lakehouse")
    print("=" * 50)

    raw_df = load_raw_data()

   
    quality_report = validate_data(raw_df)

    save_quality_report(quality_report)

    
    print("\nData Quality Summary\n")

    for key, value in quality_report.items():
        print(f"{key}: {value}")

    
    save_bronze(raw_df)

    create_silver_layer()

    create_gold_layer()

    connection = run_analytics()

    generate_report(connection)

    print("\nDay 7 completed successfully.")


if __name__ == "__main__":
    main()
