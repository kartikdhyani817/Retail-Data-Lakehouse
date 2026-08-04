from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


GOLD_FOLDER = Path("data/gold")
REPORT_FILE = Path("reports/business_report.txt")


st.set_page_config(
    page_title="Retail Data Lakehouse",
    page_icon="🏗️",
    layout="wide",
)


@st.cache_data
def load_parquet(file_name: str) -> pd.DataFrame:
    file_path = GOLD_FOLDER / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Gold layer file not found: {file_path}"
        )

    return pd.read_parquet(file_path)


@st.cache_data
def load_gold_data() -> dict[str, pd.DataFrame]:
    return {
        "kpis": load_parquet("overall_kpis.parquet"),
        "category": load_parquet("sales_by_category.parquet"),
        "region": load_parquet("sales_by_region.parquet"),
        "subcategory": load_parquet(
            "sales_by_subcategory.parquet"
        ),
        "cities": load_parquet("top_cities.parquet"),
        "segments": load_parquet(
            "segment_performance.parquet"
        ),
    }


@st.cache_data
def load_business_report() -> str:
    if not REPORT_FILE.exists():
        return (
            "Business report not found. "
            "Run `python main.py` first."
        )

    return REPORT_FILE.read_text(encoding="utf-8")


st.title("🏗️ Retail Data Lakehouse")

st.caption(
    "Bronze, Silver and Gold data architecture "
    "with DuckDB analytics"
)

with st.sidebar:
    st.header("Navigation")

    page = st.radio(
        "Choose a page",
        [
            "Dashboard",
            "Category Analytics",
            "Regional Analytics",
            "Customer Segments",
            "Business Report",
        ],
    )

    st.divider()

    if st.button(
        "Refresh Data",
        use_container_width=True,
    ):
        st.cache_data.clear()
        st.rerun()

    st.caption(
        "Run `python main.py` whenever the raw dataset changes."
    )


try:
    data = load_gold_data()

except FileNotFoundError as error:
    st.error(str(error))

    st.info(
        "Run the pipeline first using `python main.py`."
    )

    st.stop()


kpi_df = data["kpis"]

if kpi_df.empty:
    st.error("The KPI dataset is empty.")
    st.stop()


kpi_row = kpi_df.iloc[0]

total_sales = float(kpi_row["total_sales"])
total_profit = float(kpi_row["total_profit"])
total_quantity = int(kpi_row["total_quantity"])
profit_margin = float(
    kpi_row["profit_margin_percent"]
)
average_discount = float(
    kpi_row["average_discount"]
)


if page == "Dashboard":

    st.subheader("Executive Dashboard")

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Total Sales",
        f"${total_sales:,.2f}",
    )

    metric_2.metric(
        "Total Profit",
        f"${total_profit:,.2f}",
    )

    metric_3.metric(
        "Total Quantity",
        f"{total_quantity:,}",
    )

    metric_4.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%",
    )

    st.caption(
        f"Average discount: {average_discount:.2%}"
    )

    st.divider()

    chart_1, chart_2 = st.columns(2)

    with chart_1:
        st.subheader("Sales by Category")

        category_df = data["category"]

        category_chart = px.bar(
            category_df,
            x="category",
            y="total_sales",
            color="category",
            title="Category Revenue",
            labels={
                "category": "Category",
                "total_sales": "Sales",
            },
        )

        st.plotly_chart(
            category_chart,
            use_container_width=True,
        )

    with chart_2:
        st.subheader("Sales by Region")

        region_df = data["region"]

        region_chart = px.pie(
            region_df,
            names="region",
            values="total_sales",
            title="Regional Sales Distribution",
        )

        st.plotly_chart(
            region_chart,
            use_container_width=True,
        )

    st.divider()

    st.subheader("Top Cities")

    city_df = data["cities"]

    city_chart = px.bar(
        city_df,
        x="total_sales",
        y="city",
        orientation="h",
        title="Top Cities by Sales",
        labels={
            "city": "City",
            "total_sales": "Sales",
        },
    )

    st.plotly_chart(
        city_chart,
        use_container_width=True,
    )


elif page == "Category Analytics":

    st.subheader("Category and Sub-Category Analytics")

    category_df = data["category"].copy()
    subcategory_df = data["subcategory"].copy()

    selected_metric = st.selectbox(
        "Choose metric",
        [
            "total_sales",
            "total_profit",
            "total_quantity",
        ],
    )

    category_chart = px.bar(
        category_df,
        x="category",
        y=selected_metric,
        color="category",
        title=f"Category Performance: {selected_metric}",
    )

    st.plotly_chart(
        category_chart,
        use_container_width=True,
    )

    st.subheader("Sub-Category Performance")

    subcategory_chart = px.bar(
        subcategory_df.sort_values(
            selected_metric,
            ascending=True,
        ),
        x=selected_metric,
        y="sub-category",
        orientation="h",
        title=f"Sub-Category Performance: {selected_metric}",
    )

    st.plotly_chart(
        subcategory_chart,
        use_container_width=True,
    )

    st.dataframe(
        subcategory_df,
        use_container_width=True,
        hide_index=True,
    )


elif page == "Regional Analytics":

    st.subheader("Regional Analytics")

    region_df = data["region"].copy()
    city_df = data["cities"].copy()

    selected_regions = st.multiselect(
        "Select regions",
        options=region_df["region"].tolist(),
        default=region_df["region"].tolist(),
    )

    filtered_regions = region_df[
        region_df["region"].isin(selected_regions)
    ]

    region_chart = px.bar(
        filtered_regions,
        x="region",
        y="total_sales",
        color="region",
        title="Sales by Region",
    )

    st.plotly_chart(
        region_chart,
        use_container_width=True,
    )

    st.subheader("Top City Performance")

    st.dataframe(
        city_df,
        use_container_width=True,
        hide_index=True,
    )


elif page == "Customer Segments":

    st.subheader("Customer Segment Performance")

    segment_df = data["segments"].copy()

    segment_chart = px.bar(
        segment_df,
        x="segment",
        y="total_sales",
        color="segment",
        title="Sales by Customer Segment",
    )

    st.plotly_chart(
        segment_chart,
        use_container_width=True,
    )

    profit_chart = px.bar(
        segment_df,
        x="segment",
        y="total_profit",
        color="segment",
        title="Profit by Customer Segment",
    )

    st.plotly_chart(
        profit_chart,
        use_container_width=True,
    )

    st.dataframe(
        segment_df,
        use_container_width=True,
        hide_index=True,
    )


elif page == "Business Report":

    st.subheader("Automated Business Report")

    report_text = load_business_report()

    st.text_area(
        "Report",
        report_text,
        height=500,
        disabled=True,
    )

    st.download_button(
        label="Download Business Report",
        data=report_text,
        file_name="business_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

elif page == "Data Quality":

    st.subheader("Data Quality Report")

    report_file = Path(
        "reports/data_quality_report.txt"
    )

    if report_file.exists():

        report = report_file.read_text(
            encoding="utf-8"
        )

        st.text(report)

        st.download_button(
            "Download Report",
            report,
            "data_quality_report.txt"
        )

    else:

        st.warning(
            "Run the pipeline first."
        )
