from pathlib import Path


# =========================================================
# PROJECT
# =========================================================

PROJECT_NAME = "Retail Data Lakehouse"

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# DATA DIRECTORIES
# =========================================================

DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"


# =========================================================
# FILE PATHS
# =========================================================

RAW_FILE = RAW_DIR / "superstore.csv"

BRONZE_FILE = (
    BRONZE_DIR / "bronze_sales.parquet"
)

SILVER_FILE = (
    SILVER_DIR / "silver_sales.parquet"
)


# =========================================================
# DATABASE
# =========================================================

DUCKDB_FILE = (
    BASE_DIR / "retail_lakehouse.duckdb"
)


# =========================================================
# REPORTS
# =========================================================

REPORTS_DIR = BASE_DIR / "reports"

BUSINESS_REPORT = (
    REPORTS_DIR / "business_report.txt"
)

QUALITY_REPORT = (
    REPORTS_DIR / "data_quality_report.txt"
)

INCREMENTAL_REPORT = (
    REPORTS_DIR / "incremental_load_report.txt"
)

PIPELINE_SUMMARY = (
    REPORTS_DIR / "pipeline_summary.txt"
)

PERFORMANCE_REPORT = (
    REPORTS_DIR / "performance_report.txt"
)


# =========================================================
# LOGGING
# =========================================================

LOGS_DIR = BASE_DIR / "logs"

PIPELINE_LOG = (
    LOGS_DIR / "pipeline.log"
)


# =========================================================
# CREATE DIRECTORIES
# =========================================================

def create_project_directories():

    directories = [
        RAW_DIR,
        BRONZE_DIR,
        SILVER_DIR,
        GOLD_DIR,
        REPORTS_DIR,
        LOGS_DIR,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )