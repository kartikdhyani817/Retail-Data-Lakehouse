from datetime import datetime
from pathlib import Path


REPORT_FOLDER = Path("reports")

REPORT_FILE = (
    REPORT_FOLDER
    / "incremental_load_report.txt"
)


def save_incremental_report(
    report: dict,
) -> None:

    REPORT_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    with REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "=" * 60 + "\n"
        )

        file.write(
            "INCREMENTAL LOAD REPORT\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            "Pipeline Run: "
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
        )

        file.write(
            f"Incoming Rows: "
            f"{report['incoming_rows']}\n"
        )

        file.write(
            f"Source Duplicates: "
            f"{report['source_duplicates']}\n"
        )

        file.write(
            f"Existing Bronze Rows: "
            f"{report['existing_bronze_rows']}\n"
        )

        file.write(
            f"New Rows Loaded: "
            f"{report['new_rows_loaded']}\n"
        )

        file.write(
            f"Final Bronze Rows: "
            f"{report['final_bronze_rows']}\n"
        )

    print(
        "Incremental load report generated."
    )