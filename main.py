import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from config import create_project_directories

from scripts.performance import (
    generate_performance_report,
)
from scripts.analytics import run_analytics
from scripts.bronze import save_bronze
from scripts.data_quality import validate_data
from scripts.gold import create_gold_layer
from scripts.incremental_report import save_incremental_report
from scripts.ingest import load_raw_data
from scripts.quality_report import save_quality_report
from scripts.report import generate_report
from scripts.silver import create_silver_layer
from utils.logger import logger


REPORTS_FOLDER = Path("reports")
PIPELINE_SUMMARY_FILE = REPORTS_FOLDER / "pipeline_summary.txt"


def run_stage(
    stage_name: str,
    stage_function: Callable,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, float]:
    """
    Run one pipeline stage and record its execution time.

    Returns:
        A tuple containing:
        - the result returned by the stage
        - execution time in seconds
    """

    logger.info("Stage started: %s", stage_name)

    stage_start_time = time.perf_counter()

    try:
        result = stage_function(*args, **kwargs)

        stage_execution_time = round(
            time.perf_counter() - stage_start_time,
            2,
        )

        logger.info(
            "Stage completed: %s | Execution time: %.2f seconds",
            stage_name,
            stage_execution_time,
        )

        return result, stage_execution_time

    except Exception:
        stage_execution_time = round(
            time.perf_counter() - stage_start_time,
            2,
        )

        logger.exception(
            "Stage failed: %s | Execution time: %.2f seconds",
            stage_name,
            stage_execution_time,
        )

        raise


def save_pipeline_summary(
    status: str,
    execution_time: float,
    stage_times: dict[str, float],
    error_message: str | None = None,
) -> None:
    """
    Save a summary of the latest pipeline execution.
    """

    REPORTS_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    with PIPELINE_SUMMARY_FILE.open(
        "w",
        encoding="utf-8",
    ) as report_file:

        report_file.write("=" * 60 + "\n")
        report_file.write("RETAIL DATA LAKEHOUSE PIPELINE SUMMARY\n")
        report_file.write("=" * 60 + "\n\n")

        report_file.write(
            f"Pipeline Run: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
        )

        report_file.write(
            f"Status: {status}\n"
        )

        report_file.write(
            f"Total Execution Time: {execution_time:.2f} seconds\n\n"
        )

        report_file.write("STAGE EXECUTION TIMES\n")
        report_file.write("-" * 60 + "\n")

        for stage_name, stage_time in stage_times.items():
            report_file.write(
                f"{stage_name}: {stage_time:.2f} seconds\n"
            )

        if error_message:
            report_file.write("\nERROR DETAILS\n")
            report_file.write("-" * 60 + "\n")
            report_file.write(error_message + "\n")


def print_quality_summary(
    quality_report: dict[str, Any],
) -> None:
    """
    Display the data-quality results in the terminal.
    """

    print("\nData Quality Summary")
    print("-" * 40)

    for key, value in quality_report.items():
        print(f"{key}: {value}")


def print_incremental_summary(
    incremental_report: dict[str, Any],
) -> None:
    """
    Display the incremental-loading results.
    """

    print("\nIncremental Loading Summary")
    print("-" * 40)

    for key, value in incremental_report.items():
        formatted_key = key.replace("_", " ").title()
        print(f"{formatted_key}: {value}")


def main() -> None:
    
    create_project_directories()

    pipeline_start_time = time.perf_counter()

    stage_times: dict[str, float] = {}

    connection = None

    logger.info("=" * 60)
    logger.info("Retail Data Lakehouse pipeline started")
    logger.info("=" * 60)

    print("=" * 60)
    print("Retail Data Lakehouse")
    print("=" * 60)

    try:
        # ==================================================
        # STAGE 1: RAW DATA INGESTION
        # ==================================================

        raw_df, stage_time = run_stage(
            "Raw Data Ingestion",
            load_raw_data,
        )

        stage_times["Raw Data Ingestion"] = stage_time

        print(
            f"\nRaw records loaded: {len(raw_df):,}"
        )

        # ==================================================
        # STAGE 2: DATA QUALITY VALIDATION
        # ==================================================

        quality_report, stage_time = run_stage(
            "Data Quality Validation",
            validate_data,
            raw_df,
        )

        stage_times["Data Quality Validation"] = stage_time

        _, stage_time = run_stage(
            "Data Quality Report Generation",
            save_quality_report,
            quality_report,
        )

        stage_times[
            "Data Quality Report Generation"
        ] = stage_time

        print_quality_summary(
            quality_report
        )

        # ==================================================
        # STAGE 3: INCREMENTAL BRONZE LOAD
        # ==================================================

        incremental_report, stage_time = run_stage(
            "Incremental Bronze Loading",
            save_bronze,
            raw_df,
        )

        stage_times[
            "Incremental Bronze Loading"
        ] = stage_time

        _, stage_time = run_stage(
            "Incremental Report Generation",
            save_incremental_report,
            incremental_report,
        )

        stage_times[
            "Incremental Report Generation"
        ] = stage_time

        print_incremental_summary(
            incremental_report
        )

        # ==================================================
        # STAGE 4: SILVER LAYER
        # ==================================================

        silver_df, stage_time = run_stage(
            "Silver Layer Transformation",
            create_silver_layer,
        )

        stage_times[
            "Silver Layer Transformation"
        ] = stage_time

        print(
            f"\nSilver records available: {len(silver_df):,}"
        )

        # ==================================================
        # STAGE 5: GOLD LAYER
        # ==================================================

        gold_result, stage_time = run_stage(
            "Gold Layer Aggregation",
            create_gold_layer,
        )

        stage_times[
            "Gold Layer Aggregation"
        ] = stage_time

        if isinstance(gold_result, dict):
            print(
                f"\nGold datasets created: {len(gold_result)}"
            )

        # ==================================================
        # STAGE 6: DUCKDB ANALYTICS
        # ==================================================

        connection, stage_time = run_stage(
            "DuckDB Analytics Setup",
            run_analytics,
        )

        stage_times[
            "DuckDB Analytics Setup"
        ] = stage_time

        # ==================================================
        # STAGE 7: BUSINESS REPORT
        # ==================================================

        _, stage_time = run_stage(
            "Business Report Generation",
            generate_report,
            connection,
        )

        stage_times[
            "Business Report Generation"
        ] = stage_time

        # ==================================================
        # PIPELINE SUCCESS
        # ==================================================

        total_execution_time = round(
            time.perf_counter() - pipeline_start_time,
            2,
        )
        generate_performance_report(
            stage_times,
            total_execution_time,
        )

        save_pipeline_summary(
            status="SUCCESS",
            execution_time=total_execution_time,
            stage_times=stage_times,
        )

        logger.info(
            "Pipeline completed successfully in %.2f seconds",
            total_execution_time,
        )

        print("\n" + "=" * 60)
        print("Pipeline completed successfully.")
        print(
            f"Total execution time: "
            f"{total_execution_time:.2f} seconds"
        )
        print(
            f"Pipeline summary: {PIPELINE_SUMMARY_FILE}"
        )
        print("=" * 60)

    except Exception as error:
        total_execution_time = round(
            time.perf_counter() - pipeline_start_time,
            2,
        )

        error_message = (
            f"{type(error).__name__}: {error}"
        )

        save_pipeline_summary(
            status="FAILED",
            execution_time=total_execution_time,
            stage_times=stage_times,
            error_message=error_message,
        )

        logger.exception(
            "Pipeline failed after %.2f seconds",
            total_execution_time,
        )

        print("\n" + "=" * 60)
        print("Pipeline failed.")
        print(f"Error: {error_message}")
        print(
            f"Failure summary: {PIPELINE_SUMMARY_FILE}"
        )
        print("=" * 60)

        raise

    finally:
        if connection is not None:
            try:
                connection.close()

                logger.info(
                    "DuckDB connection closed"
                )

            except Exception:
                logger.exception(
                    "Failed to close DuckDB connection"
                )


if __name__ == "__main__":
    main()