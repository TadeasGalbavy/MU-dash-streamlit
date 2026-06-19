"""High-level business overview page."""

import streamlit as st

from src.charts import (
    create_monthly_revenue_chart,
    create_orders_by_status_chart,
    create_orders_by_shipping_method_pie_chart,
    create_revenue_by_country_choropleth_chart,
)
from src.config import get_data_mode_label
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
    st.warning("The order model is empty. Check the active data files.")
    st.stop()

if latest_stock.empty:
    st.warning("The latest stock snapshot is empty. Check the active data files.")
    st.stop()

total_revenue = calculate_total_revenue(orders_model)
total_orders = calculate_total_orders(orders_model)
average_order_value = calculate_average_order_value(orders_model)
total_quantity = calculate_total_quantity(orders_model)
latest_stock_value = calculate_latest_stock_value(latest_stock)
out_of_stock_products = calculate_out_of_stock_products(latest_stock)

st.caption(f"Active dataset: {get_data_mode_label()}")

first_row = st.columns(3)
first_row[0].metric("Total revenue", f"{total_revenue:,.2f} EUR")
first_row[1].metric("Orders", f"{total_orders:,}")
first_row[2].metric("Average order value", f"{average_order_value:,.2f} EUR")

second_row = st.columns(3)
second_row[0].metric("Items sold", f"{total_quantity:,}")
second_row[1].metric("Total stock value", f"{latest_stock_value:,.2f} EUR")
second_row[2].metric("Out of stock products", f"{out_of_stock_products:,}")

st.divider()

monthly_revenue_chart = create_monthly_revenue_chart(orders_model)
orders_by_status_chart = create_orders_by_status_chart(orders_model)
revenue_by_country_chart = create_revenue_by_country_choropleth_chart(orders_model)
orders_by_shipping_method_chart = create_orders_by_shipping_method_pie_chart(
    orders_model
)

for figure in (
    monthly_revenue_chart,
    orders_by_status_chart,
    revenue_by_country_chart,
    orders_by_shipping_method_chart,
):
    figure.update_layout(height=440)

vertical_divider = (
    "<div style='height: 500px; border-left: 1px solid #2a2a2a; "
    "margin: 0 auto;'></div>"
)
horizontal_divider = (
    "<div style='border-top: 1px solid #2a2a2a; "
    "margin: 1rem 0 1.25rem 0;'></div>"
)

top_chart_columns = st.columns([1, 0.03, 1], gap="medium")
with top_chart_columns[0]:
    st.subheader("Monthly revenue")
    st.plotly_chart(
        monthly_revenue_chart,
        use_container_width=True,
    )

with top_chart_columns[1]:
    st.markdown(vertical_divider, unsafe_allow_html=True)

with top_chart_columns[2]:
    st.subheader("Orders by status")
    st.plotly_chart(
        orders_by_status_chart,
        use_container_width=True,
    )

st.markdown(horizontal_divider, unsafe_allow_html=True)

bottom_chart_columns = st.columns([1, 0.03, 1], gap="medium")
with bottom_chart_columns[0]:
    st.subheader("Revenue by country")
    st.plotly_chart(
        revenue_by_country_chart,
        use_container_width=True,
    )

with bottom_chart_columns[1]:
    st.markdown(vertical_divider, unsafe_allow_html=True)

with bottom_chart_columns[2]:
    st.subheader("Orders by shipping method")
    st.plotly_chart(
        orders_by_shipping_method_chart,
        use_container_width=True,
    )
