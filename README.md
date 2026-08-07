# 🏗️ Retail Data Lakehouse

A hands-on end-to-end **Data Engineering project** where I built a retail data pipeline from raw CSV files to analytics-ready datasets and an interactive dashboard.

The main idea behind this project was to understand how data moves through a real pipeline — from ingestion and cleaning to transformation, storage, SQL analytics, monitoring, and reporting. Instead of keeping everything in one script, I gradually structured the project into different layers and reusable components.

The project follows the **Bronze → Silver → Gold (Medallion) architecture** and currently includes incremental loading, data quality checks, DuckDB analytics, pipeline logging, performance monitoring, automated reports, and a Streamlit dashboard.

---

## 🚀 What Does This Project Do?

The pipeline takes raw retail data and processes it through several stages:

```text
Raw Retail CSV
      │
      ▼
Data Quality Checks
      │
      ▼
Incremental Loading
      │
      ▼
┌─────────────────┐
│  BRONZE LAYER   │
│    Raw Data     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SILVER LAYER   │
│  Cleaned Data   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   GOLD LAYER    │
│ Business Tables │
└────────┬────────┘
         │
         ▼
     DuckDB SQL
         │
    ┌────┴────┐
    ▼         ▼
 Reports   Streamlit
    │
    ▼
Logging & Monitoring
    │
    ▼
Performance Tracking
```

The goal is to convert raw data into reliable, structured information that can easily be queried, analyzed, and visualized.

---

# 🥉 Bronze Layer

The Bronze layer stores the ingested data in **Parquet format**.

Instead of repeatedly working directly with the CSV file, the pipeline creates a structured storage layer that acts as the starting point for downstream processing.

From Day 8 onwards, the Bronze layer also supports **incremental loading**.

### Features

- Raw CSV ingestion
- CSV → Parquet conversion
- Row-level hashing
- Duplicate detection
- Incremental record detection
- Idempotent pipeline runs

---

# 🥈 Silver Layer

The Silver layer is where the raw data becomes cleaner and more reliable.

The pipeline performs operations such as:

- Removing duplicate records
- Standardizing column names
- Handling missing values
- Converting numeric fields
- Cleaning text columns
- Preparing data for analytics

The result is stored as:

```text
data/silver/silver_sales.parquet
```

This becomes the main cleaned dataset used to create the Gold layer.

---

# 🥇 Gold Layer

The Gold layer contains business-ready aggregated datasets.

Instead of making the dashboard repeatedly process thousands of raw rows, commonly required analytics are calculated beforehand.

The pipeline currently generates:

```text
sales_by_category.parquet

sales_by_region.parquet

sales_by_subcategory.parquet

top_cities.parquet

segment_performance.parquet

overall_kpis.parquet
```

These datasets provide insights into sales, profit, quantity, regions, customer segments, cities, and product categories.

---

# 🔄 Incremental Data Loading

One of the most useful additions to the project was **incremental ingestion**.

Initially, the pipeline recreated the Bronze dataset every time it ran. I later changed this so the pipeline can identify records that have already been processed.

Each incoming record receives a SHA-256 based `record_hash`.

The pipeline then compares incoming hashes against existing Bronze records.

```text
Incoming Data
      │
      ▼
Generate Record Hash
      │
      ▼
Compare with Bronze
      │
      ├── Existing → Skip
      │
      └── New → Load
```

This means running the pipeline multiple times with unchanged data does not keep inserting the same records.

The pipeline also generates:

```text
reports/incremental_load_report.txt
```

---

# 🔍 Data Quality Framework

Before data moves through the Lakehouse, the pipeline performs automated quality checks.

Current checks include:

- Total records
- Total columns
- Missing values
- Duplicate rows
- Negative sales
- Negative profit
- Invalid/zero quantity

A report is automatically created at:

```text
reports/data_quality_report.txt
```

This helped turn the project from a simple transformation script into a more reliable pipeline where data quality can be inspected before using the results.

> Negative profit is reported as a business condition rather than automatically removed, since a loss-making sale can still be a valid transaction.

---

# 🦆 DuckDB Analytics

The project uses **DuckDB** as its local analytical SQL engine.

DuckDB can query the generated Parquet datasets directly, which allowed me to combine SQL analytics with the Lakehouse architecture without requiring a paid cloud database.

Example:

```sql
SELECT *
FROM sales_by_category
ORDER BY total_sales DESC;
```

DuckDB views are created over the Gold datasets and used for reporting.

---

# 📊 Streamlit Dashboard

The processed data is presented through an interactive **Streamlit dashboard**.

The dashboard includes:

### Executive KPIs

- Total Sales
- Total Profit
- Total Quantity
- Profit Margin
- Average Discount

### Business Analytics

- Sales by Category
- Sales by Region
- Sub-Category Performance
- Top Cities
- Customer Segment Performance

### Engineering Monitoring

The dashboard also provides access to:

- Data Quality Report
- Incremental Loading Report
- Pipeline Logs
- Pipeline Performance
- Business Report

This means the application isn't only a sales dashboard — it also gives visibility into the underlying data pipeline.

---

# 📑 Automated Reporting

The pipeline automatically generates multiple reports during execution.

```text
reports/
│
├── business_report.txt
├── data_quality_report.txt
├── incremental_load_report.txt
├── pipeline_summary.txt
└── performance_report.txt
```

### Business Report

Contains SQL-based business insights generated using DuckDB.

### Data Quality Report

Shows issues detected in the incoming dataset.

### Incremental Load Report

Shows:

- Incoming records
- Source duplicates
- Existing Bronze records
- New records loaded
- Final Bronze record count

### Pipeline Summary

Records the status and execution time of the latest pipeline run.

### Performance Report

Shows how much time each stage of the pipeline takes and identifies the slowest stage.

---

# 📝 Logging & Monitoring

The project contains centralized pipeline logging.

Logs are stored in:

```text
logs/pipeline.log
```

Important pipeline events are recorded, including:

```text
Pipeline Started
Stage Started
Stage Completed
Execution Time
Pipeline Completed
Pipeline Failed
Error Details
```

Python exception logging is also used so failures can be investigated instead of relying only on terminal output.

---

# ⚡ Performance Monitoring

Each major pipeline stage is timed separately.

For example:

```text
Raw Data Ingestion
Data Quality Validation
Incremental Bronze Loading
Silver Transformation
Gold Aggregation
DuckDB Analytics
Business Report Generation
```

A performance report is generated after a successful run.

This makes it possible to identify which stage is taking the most time and where future optimization may be useful.

---

# ⚙️ Centralized Configuration

Instead of spreading important paths throughout different scripts, the project now includes:

```text
config.py
```

It contains centralized configuration for:

- Raw data
- Bronze storage
- Silver storage
- Gold storage
- Reports
- Logs
- DuckDB database
- Project directories

This makes the codebase easier to maintain as the project grows.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core pipeline development |
| Pandas | Data processing |
| Parquet | Lakehouse data storage |
| PyArrow | Parquet support |
| DuckDB | SQL analytics |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| SHA-256 | Incremental record hashing |
| Git & GitHub | Version control |

The project was intentionally built using **free and locally available technologies**, without depending on paid cloud services.

---

# 📂 Project Structure

```text
Retail_Data_Lakehouse/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── superstore.csv
│   │
│   ├── bronze/
│   │   └── bronze_sales.parquet
│   │
│   ├── silver/
│   │   └── silver_sales.parquet
│   │
│   └── gold/
│       ├── overall_kpis.parquet
│       ├── sales_by_category.parquet
│       ├── sales_by_region.parquet
│       ├── sales_by_subcategory.parquet
│       ├── segment_performance.parquet
│       └── top_cities.parquet
│
├── scripts/
│   ├── ingest.py
│   ├── bronze.py
│   ├── silver.py
│   ├── gold.py
│   ├── data_quality.py
│   ├── quality_report.py
│   ├── incremental_report.py
│   ├── analytics.py
│   ├── report.py
│   └── performance.py
│
├── utils/
│   └── logger.py
│
├── logs/
│   └── pipeline.log
│
└── reports/
    ├── business_report.txt
    ├── data_quality_report.txt
    ├── incremental_load_report.txt
    ├── pipeline_summary.txt
    └── performance_report.txt
```

---

# ▶️ Running the Project

## 1. Clone the repository

```bash
git clone <your-repository-url>

cd Retail-Data-Lakehouse
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the complete data pipeline

```bash
python main.py
```

This executes:

```text
Ingestion
   ↓
Data Quality
   ↓
Incremental Bronze Load
   ↓
Silver Transformation
   ↓
Gold Aggregation
   ↓
DuckDB Analytics
   ↓
Reporting
   ↓
Logging & Performance Monitoring
```

## 5. Launch the dashboard

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

# 📅 Development Journey

I built this project step-by-step instead of trying to create everything at once.

| Day | Development |
|---|---|
| Day 1 | Project structure and environment setup |
| Day 2 | Raw ingestion and Bronze Layer |
| Day 3 | Cleaning and Silver Layer |
| Day 4 | Business transformations and Gold Layer |
| Day 5 | DuckDB SQL analytics and reporting |
| Day 6 | Interactive Streamlit dashboard |
| Day 7 | Data Quality Framework |
| Day 8 | Incremental Data Loading |
| Day 9 | Logging and Pipeline Monitoring |
| Day 10 | Configuration and Performance Monitoring |
| Day 11 | Automated Testing & Reliability |
| Day 12 | Final optimization, documentation & deployment |

---

# 💡 What I Learned

Building this project helped me understand that Data Engineering involves much more than simply cleaning a CSV file.

I worked with concepts such as:

- Medallion/Lakehouse architecture
- ETL pipeline development
- Parquet-based storage
- Incremental data ingestion
- Idempotent pipelines
- Data quality validation
- SQL analytics
- Automated reporting
- Pipeline logging
- Exception handling
- Performance monitoring
- Modular Python development

Most importantly, I learned how different pieces of a data pipeline connect together from **raw ingestion to the final analytics layer**.

---

# 🔮 Next Steps

The project is still being improved.

Planned additions include:

- Automated unit tests
- Pipeline reliability checks
- Better exception handling
- Final dashboard improvements
- Deployment
- Architecture documentation
- Final GitHub cleanup

---

# 👨‍💻 Author

**Kartik Dhyani**

Aspiring Data Engineer focused on building practical end-to-end data systems using Python, SQL, ETL and modern data engineering concepts.

GitHub: `kartikdhyani817`

---

## ⭐ Project Status

**Day 10/12 completed — actively developing.**
