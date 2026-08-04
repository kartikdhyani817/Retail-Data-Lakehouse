from pathlib import Path


def save_quality_report(report):

    report_folder = Path("reports")
    report_folder.mkdir(
        exist_ok=True
    )

    report_file = report_folder / "data_quality_report.txt"

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("=" * 60 + "\n")
        file.write("DATA QUALITY REPORT\n")
        file.write("=" * 60 + "\n\n")

        for key, value in report.items():

            file.write(
                f"{key}: {value}\n"
            )

    print(
        "\nData Quality Report Generated."
    )