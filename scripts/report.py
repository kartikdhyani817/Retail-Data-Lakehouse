from pathlib import Path


def generate_report(con):

    report_folder = Path("reports")
    report_folder.mkdir(exist_ok=True)

    report_file = report_folder / "business_report.txt"

    with open(report_file, "w", encoding="utf-8") as file:

        file.write("=" * 50 + "\n")
        file.write("Retail Data Lakehouse Report\n")
        file.write("=" * 50 + "\n\n")

        # Category Sales
        file.write("Top Categories\n")
        file.write("----------------------\n")

        result = con.execute("""
            SELECT *
            FROM sales_by_category
            LIMIT 5
        """).fetchdf()

        file.write(result.to_string(index=False))

        file.write("\n\n")

        # Region Sales
        file.write("Region Performance\n")
        file.write("----------------------\n")

        result = con.execute("""
            SELECT *
            FROM sales_by_region
        """).fetchdf()

        file.write(result.to_string(index=False))

        file.write("\n\n")

        # Top Cities
        file.write("Top Cities\n")
        file.write("----------------------\n")

        result = con.execute("""
            SELECT *
            FROM top_cities
            LIMIT 10
        """).fetchdf()

        file.write(result.to_string(index=False))

    print("\nBusiness report generated.")