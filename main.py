from scripts.ingest import load_raw_data
from scripts.bronze import save_bronze
from scripts.silver import create_silver_layer
from scripts.gold import create_gold_layer


def main():

    print("=" * 50)
    print("Retail Data Lakehouse")
    print("=" * 50)

    raw_df = load_raw_data()

    save_bronze(raw_df)

    create_silver_layer()

    create_gold_layer()

    print("\nDay 4 completed successfully.")


if __name__ == "__main__":
    main()
