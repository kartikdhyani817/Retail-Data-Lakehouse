from scripts.ingest import load_raw_data
from scripts.bronze import save_bronze


def main():

    print("=" * 50)
    print("Retail Data Lakehouse")
    print("=" * 50)

    df = load_raw_data()

    print("\nRows :", len(df))
    print("Columns :", len(df.columns))

    save_bronze(df)

    print("\nDay 2 completed successfully.")


if __name__ == "__main__":
    main()