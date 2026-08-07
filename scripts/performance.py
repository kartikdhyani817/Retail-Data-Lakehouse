from datetime import datetime
from pathlib import Path


REPORT_FILE = Path(
    "reports/performance_report.txt"
)


def generate_performance_report(
    stage_times,
    total_time,
):

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        file.write("=" * 60 + "\n")
        file.write(
            "RETAIL DATA LAKEHOUSE PERFORMANCE REPORT\n"
        )
        file.write("=" * 60 + "\n\n")

        file.write(
            f"Generated: "
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n\n"
        )

        file.write(
            f"Total Pipeline Time: "
            f"{total_time:.4f} seconds\n\n"
        )

        file.write(
            "STAGE PERFORMANCE\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for stage, execution_time in stage_times.items():

            percentage = (
                execution_time / total_time * 100
                if total_time > 0
                else 0
            )

            file.write(
                f"{stage}\n"
            )

            file.write(
                f"  Time       : "
                f"{execution_time:.4f} seconds\n"
            )

            file.write(
                f"  Percentage : "
                f"{percentage:.2f}%\n\n"
            )

        if stage_times:

            slowest_stage = max(
                stage_times,
                key=stage_times.get,
            )

            file.write(
                "-" * 60 + "\n"
            )

            file.write(
                f"Slowest Stage: {slowest_stage}\n"
            )

            file.write(
                f"Slowest Stage Time: "
                f"{stage_times[slowest_stage]:.4f} seconds\n"
            )

    print(
        "\nPerformance report generated."
    )