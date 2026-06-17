"""High-level business overview page."""

import streamlit as st

from src.charts import (
    create_orders_over_time_chart,
    create_revenue_by_category_chart,
    create_revenue_by_country_chart,
    create_revenue_over_time_chart,
)
from src.data_loader import get_active_data_dir, load_all_data_files
from src.metrics import (
    calculate_active_products,
    calculate_average_order_value,
    calculate_latest_stock_value,
    calculate_total_orders,
    calculate_total_quantity,
    calculate_total_revenue,
)
from src.transformations import prepare_latest_stock_snapshot, prepare_orders_model


st.set_page_config(page_title="Overview", layout="wide")

st.title("Overview")

try:
    active_data_dir = get_active_data_dir()
    data = load_all_data_files()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

if not data:
    st.warning(f"No data files were found in `{active_data_dir}`.")
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

products_df = data.get("products.csv")

total_revenue = calculate_total_revenue(orders_model)
total_orders = calculate_total_orders(orders_model)
total_quantity = calculate_total_quantity(orders_model)
average_order_value = calculate_average_order_value(orders_model)
active_products = calculate_active_products(products_df)
latest_stock_value = calculate_latest_stock_value(latest_stock)

st.caption(f"Data source: `{active_data_dir}`")

first_row = st.columns(3)
first_row[0].metric("Total revenue", f"{total_revenue:,.2f}")
first_row[1].metric("Orders", f"{total_orders:,}")
first_row[2].metric("Items sold", f"{total_quantity:,}")

second_row = st.columns(3)
second_row[0].metric("Average order value", f"{average_order_value:,.2f}")
second_row[1].metric("Active products", f"{active_products:,}")
second_row[2].metric("Latest stock value", f"{latest_stock_value:,.2f}")

st.plotly_chart(
    create_revenue_over_time_chart(orders_model),
    use_container_width=True,
)
st.plotly_chart(
    create_orders_over_time_chart(orders_model),
    use_container_width=True,
)

chart_columns = st.columns(2)
chart_columns[0].plotly_chart(
    create_revenue_by_country_chart(orders_model),
    use_container_width=True,
)
chart_columns[1].plotly_chart(
    create_revenue_by_category_chart(orders_model),
    use_container_width=True,
)
