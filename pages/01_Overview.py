"""High-level business overview page."""

import streamlit as st

from src.charts import (
    create_monthly_revenue_chart,
    create_orders_by_status_chart,
    create_revenue_by_country_choropleth_chart,
)
from src.data_loader import load_all_data_files
from src.metrics import (
    calculate_average_order_value,
    calculate_latest_stock_value,
    calculate_out_of_stock_products,
    calculate_total_orders,
    calculate_total_quantity,
    calculate_total_revenue,
)
from src.transformations import prepare_latest_stock_snapshot, prepare_orders_model


st.set_page_config(page_title="Overview", layout="wide")

st.title("Executive overview")
st.write("Managerial overview of sales, orders, and current stock position.")

try:
    data = load_all_data_files()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

if not data:
    st.warning("No data files were found in the active dataset.")
    st.stop()

try:
    orders_model = prepare_orders_model(data)
    latest_stock = prepare_latest_stock_snapshot(data)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

if orders_model.empty:
    st.warning("The order model is empty. Check the sample data files.")
    st.stop()

if latest_stock.empty:
    st.warning("The latest stock snapshot is empty. Check the sample data files.")
    st.stop()

total_revenue = calculate_total_revenue(orders_model)
total_orders = calculate_total_orders(orders_model)
average_order_value = calculate_average_order_value(orders_model)
total_quantity = calculate_total_quantity(orders_model)
latest_stock_value = calculate_latest_stock_value(latest_stock)
out_of_stock_products = calculate_out_of_stock_products(latest_stock)

st.caption("Active dataset: Sample e-commerce data")

first_row = st.columns(3)
first_row[0].metric("Total revenue", f"{total_revenue:,.2f} EUR")
first_row[1].metric("Orders", f"{total_orders:,}")
first_row[2].metric("Average order value", f"{average_order_value:,.2f} EUR")

second_row = st.columns(3)
second_row[0].metric("Items sold", f"{total_quantity:,}")
second_row[1].metric("Total stock value", f"{latest_stock_value:,.2f} EUR")
second_row[2].metric("Out of stock products", f"{out_of_stock_products:,}")

st.divider()

st.subheader("Monthly revenue")
st.plotly_chart(
    create_monthly_revenue_chart(orders_model),
    width="stretch",
)

st.subheader("Orders by status")
st.plotly_chart(
    create_orders_by_status_chart(orders_model),
    width="stretch",
)

st.subheader("Revenue by country")
st.plotly_chart(
    create_revenue_by_country_choropleth_chart(orders_model),
    width="stretch",
)
