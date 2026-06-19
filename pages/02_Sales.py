"""Sales analysis page."""

import streamlit as st

from src.charts import (
    create_monthly_revenue_chart,
    create_revenue_by_category_donut_chart,
)
from src.data_loader import load_all_data_files
from src.metrics import (
    calculate_average_order_value,
    calculate_top_products_by_revenue,
    calculate_total_orders,
    calculate_total_quantity,
    calculate_total_revenue,
)
from src.transformations import prepare_orders_model
from src.utils import filter_by_date_range, prepare_date_filter_bounds


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
    st.warning(
        "Country filter cannot be shown because the orders model has no country column."
    )
    st.stop()

orders_model, min_order_date, max_order_date = prepare_date_filter_bounds(
    orders_model,
    "order_date",
)

if min_order_date is None or max_order_date is None:
    st.warning(
        "Date filter cannot be shown because the orders model "
        "has no valid order_date values."
    )
    st.stop()

with st.expander("Filters", expanded=False):
    date_columns = st.columns(2)
    selected_start_date = date_columns[0].date_input(
        "Start date",
        value=min_order_date,
        min_value=min_order_date,
        max_value=max_order_date,
    )
    selected_end_date = date_columns[1].date_input(
        "End date",
        value=max_order_date,
        min_value=min_order_date,
        max_value=max_order_date,
    )

    if selected_start_date > selected_end_date:
        st.warning("Start date must be earlier than or equal to End date.")
        st.stop()

    date_filtered_orders_model = filter_by_date_range(
        orders_model,
        "order_date",
        (selected_start_date, selected_end_date),
    )

    if date_filtered_orders_model.empty:
        st.warning("No sales data match the selected date range.")
        st.stop()

    countries = sorted(date_filtered_orders_model["country"].dropna().unique())
    selected_countries = st.multiselect(
        "Country",
        options=countries,
        default=countries,
    )

filtered_orders_model = date_filtered_orders_model[
    date_filtered_orders_model["country"].isin(selected_countries)
]

if filtered_orders_model.empty:
    st.warning("No sales data match the selected date range and country filter.")
    st.stop()

st.divider()

st.subheader("Key metrics")
st.write(f"Filtered rows: `{len(filtered_orders_model):,}`")
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
    width="stretch",
)

st.subheader("Revenue by category")
st.plotly_chart(
    create_revenue_by_category_donut_chart(filtered_orders_model),
    width="stretch",
)

st.subheader("Top products by revenue")
top_products = calculate_top_products_by_revenue(filtered_orders_model)

if top_products.empty:
    st.warning("No product revenue data are available for the selected country filter.")
else:
    st.dataframe(
        top_products,
        hide_index=True,
        width="stretch",
        column_config={
            "Revenue": st.column_config.NumberColumn(
                "Revenue",
                format="%.2f EUR",
            ),
            "Items sold": st.column_config.NumberColumn(
                "Items sold",
                format="%d",
            ),
            "Orders": st.column_config.NumberColumn(
                "Orders",
                format="%d",
            ),
        },
    )
