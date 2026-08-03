# 🏗️ Retail Data Lakehouse

A modern end-to-end Data Engineering project that implements a Retail Data Lakehouse using the Bronze, Silver, and Gold architecture. The project processes raw retail sales data, performs transformations, generates analytics-ready datasets, executes SQL-based business analysis with DuckDB, and provides an interactive Streamlit dashboard for business insights.

> 🚀 Built using Python, Pandas, DuckDB, Parquet, Plotly, and Streamlit.

---

# 🚀 Features

## Day 1
- Project initialization
- Folder structure setup
- Virtual environment
- Dependency management

---

## Day 2
- Raw retail data ingestion
- Bronze Layer creation
- CSV to Parquet conversion

---

## Day 3
- Silver Layer implementation
- Data cleaning
- Duplicate removal
- Missing value handling
- Data standardization

---

## Day 4
- Gold Layer creation
- Business-ready aggregated datasets
- Category analysis
- Region analysis
- Sub-category analysis
- Top city analysis
- Segment performance
- Overall KPI generation

---

## Day 5
- DuckDB integration
- SQL analytics engine
- Automated business report generation
- Parquet querying using SQL
- Analytics views

---

## Day 6
- Interactive Streamlit dashboard
- Executive KPI cards
- Category analytics
- Regional analytics
- Customer segment analysis
- Business report viewer
- Interactive charts using Plotly
- Downloadable reports
- Automatic data refresh

---

# 🏗️ Lakehouse Architecture

```
                 RAW CSV
                    │
                    ▼
            Bronze Layer
        (Raw Parquet Storage)
                    │
                    ▼
            Silver Layer
      (Clean & Standardized Data)
                    │
                    ▼
             Gold Layer
    (Business Ready Datasets)
                    │
                    ▼
              DuckDB SQL
          Analytics Engine
                    │
                    ▼
        Business Reports
                    │
                    ▼
      Streamlit Dashboard
```

---

# 📂 Project Structure

```text
Retail_Data_Lakehouse/

│
├── app.py
├── main.py
├── retail_lakehouse.duckdb
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── reports/
│   └── business_report.txt
│
├── scripts/
│   ├── ingest.py
│   ├── bronze.py
│   ├── silver.py
│   ├── gold.py
│   ├── analytics.py
│   └── report.py
```

---

# 📊 Dashboard Features

### Executive Dashboard
- Total Sales
- Total Profit
- Total Quantity
- Profit Margin
- Average Discount

### Analytics
- Sales by Category
- Sales by Region
- Sales by Sub-Category
- Top Cities
- Customer Segment Performance

### Business Report
- Automatically generated report
- Download option
- SQL-based analytics

---

# 🛠️ Tech Stack

- Python
- Pandas
- DuckDB
- Parquet
- Plotly
- Streamlit

---

# ▶️ How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the complete pipeline:

```bash
python main.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

---

# 📈 Business Analytics

The project generates:

- Sales by Category
- Sales by Region
- Sales by Sub-Category
- Top Cities
- Customer Segment Performance
- Total Sales
- Total Profit
- Profit Margin
- Overall Business KPIs

---

# 📌 Future Enhancements

- Data Quality Dashboard
- Data Validation Rules
- Logging Framework
- Incremental Data Loading
- Apache Spark Integration
- Apache Airflow Scheduling
- Docker Support
- CI/CD Pipeline
- Cloud Deployment
- Azure Data Lake Integration

---

# 👨‍💻 Author

**Kartik Dhyani**

Aspiring Data Engineer | Python | SQL | ETL | Data Lakehouse | Streamlit

GitHub: https://github.com/kartikdhyani817

---

# ⭐ Project Status

✅ Day 1 – Project Setup

✅ Day 2 – Bronze Layer

✅ Day 3 – Silver Layer

✅ Day 4 – Gold Layer

✅ Day 5 – DuckDB Analytics

✅ Day 6 – Streamlit Dashboard

🚧 Day 7 – Data Quality Framework

🚧 Day 8 – Incremental Data Loading

🚧 Day 9 – Logging & Monitoring

🚧 Day 10 – Performance Optimization

🚧 Day 11 – Production Enhancements

🚧 Day 12 – Final Deployment & Documentation
