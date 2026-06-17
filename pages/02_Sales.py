"""Sales analysis page."""

import streamlit as st

from src.charts import (
    create_monthly_revenue_chart,
    create_revenue_by_category_donut_chart,
)
from src.data_loader import load_all_data_files
from src.metrics import (
    calculate_average_order_value,
    calculate_total_orders,
    calculate_total_quantity,
    calculate_total_revenue,
)
from src.transformations import prepare_orders_model


st.set_page_config(page_title="Sales", layout="wide")

st.title("Sales")
st.write("Track sales performance by country with core KPIs and monthly revenue.")

try:
    data = load_all_data_files()
    orders_model = prepare_orders_model(data)
except ValueError as exc:
    st.warning(f"Sales data could not be prepared: {exc}")
    st.stop()

if orders_model.empty:
    st.warning("The orders model is empty. Check the source data files.")
    st.stop()

if "country" not in orders_model.columns:
    st.warning("Country filter cannot be shown because the orders model has no country column.")
    st.stop()

countries = sorted(orders_model["country"].dropna().unique())
with st.expander("Filters", expanded=True):
    selected_countries = st.multiselect(
        "Country",
        options=countries,
        default=countries,
    )

filtered_orders_model = orders_model[
    orders_model["country"].isin(selected_countries)
]

if filtered_orders_model.empty:
    st.warning("No sales data match the selected country filter. Select at least one country.")
    st.stop()

st.divider()

st.subheader("Key metrics")
st.write(f"Rows in orders model: `{len(filtered_orders_model):,}`")
total_revenue = calculate_total_revenue(filtered_orders_model)
total_orders = calculate_total_orders(filtered_orders_model)
average_order_value = calculate_average_order_value(filtered_orders_model)
total_quantity = calculate_total_quantity(filtered_orders_model)

metric_columns = st.columns(4)
metric_columns[0].metric("Total revenue", f"{total_revenue:,.2f} EUR")
metric_columns[1].metric("Orders", f"{total_orders:,}")
metric_columns[2].metric("Average order value", f"{average_order_value:,.2f} EUR")
metric_columns[3].metric("Items sold", f"{total_quantity:,}")

st.divider()

st.subheader("Monthly revenue")
st.plotly_chart(
    create_monthly_revenue_chart(filtered_orders_model),
    use_container_width=True,
)

st.subheader("Revenue by category")
st.plotly_chart(
    create_revenue_by_category_donut_chart(filtered_orders_model),
    use_container_width=True,
)
