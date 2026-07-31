from scripts.ingest import load_raw_data
from scripts.bronze import save_bronze
from scripts.silver import create_silver_layer


def main():

    print("=" * 50)
    print("Retail Data Lakehouse")
    print("=" * 50)

    df = load_raw_data()

    save_bronze(df)

    silver_df = create_silver_layer()

    print("\nSilver Layer Shape")
    print(silver_df.shape)

    print("\nDay 3 completed successfully.")


if __name__ == "__main__":
    main()
