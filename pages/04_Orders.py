"""Orders analysis page."""

from datetime import date

import streamlit as st

from src.charts import (
    create_orders_by_status_chart,
    create_orders_over_time_chart,
)
from src.data_loader import load_all_data_files
from src.metrics import calculate_orders_by_status, calculate_total_orders
from src.transformations import prepare_latest_orders_table, prepare_orders_model
from src.utils import filter_by_date_range, prepare_date_filter_bounds


st.set_page_config(page_title="Orders", layout="wide")

st.title("Orders")
st.write("Review order status performance and the latest order activity.")

try:
    data = load_all_data_files()
    orders_model = prepare_orders_model(data)
except ValueError as exc:
    st.warning(f"Orders data could not be prepared: {exc}")
    st.stop()

if orders_model.empty:
    st.warning("The orders model is empty. Check the source data files.")
    st.stop()

if "order_status" not in orders_model.columns:
    st.warning(
        "Order status filter cannot be shown because the orders model "
        "has no order_status column."
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

date_picker_min = date(min_order_date.year, 1, 1)
date_picker_max = date(max_order_date.year, 12, 31)

with st.expander("Filters", expanded=False):
    date_columns = st.columns(2)
    selected_start_date = date_columns[0].date_input(
        "Start date",
        value=min_order_date,
        min_value=date_picker_min,
        max_value=date_picker_max,
    )
    selected_end_date = date_columns[1].date_input(
        "End date",
        value=max_order_date,
        min_value=date_picker_min,
        max_value=date_picker_max,
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
        st.warning("No orders match the selected date range.")
        st.stop()

    order_statuses = sorted(
        date_filtered_orders_model["order_status"].dropna().unique()
    )
    selected_order_statuses = st.multiselect(
        "Order status",
        options=order_statuses,
        default=order_statuses,
    )

filtered_orders_model = date_filtered_orders_model[
    date_filtered_orders_model["order_status"].isin(selected_order_statuses)
]

if filtered_orders_model.empty:
    st.warning(
        "No orders match the selected date range and order status filter."
    )
    st.stop()

st.divider()

st.subheader("Key metrics")
total_orders = calculate_total_orders(filtered_orders_model)
completed_orders = calculate_orders_by_status(filtered_orders_model, "completed")
cancelled_orders = calculate_orders_by_status(filtered_orders_model, "cancelled")
returned_orders = calculate_orders_by_status(filtered_orders_model, "returned")

metric_columns = st.columns(4)
metric_columns[0].metric("Total orders", f"{total_orders:,}")
metric_columns[1].metric("Completed orders", f"{completed_orders:,}")
metric_columns[2].metric("Cancelled orders", f"{cancelled_orders:,}")
metric_columns[3].metric("Returned orders", f"{returned_orders:,}")

st.divider()

st.subheader("Orders over time")
st.plotly_chart(
    create_orders_over_time_chart(filtered_orders_model),
    use_container_width=True,
)

latest_orders = prepare_latest_orders_table(filtered_orders_model)
bottom_columns = st.columns(2, gap="large")
with bottom_columns[0]:
    st.subheader("Orders by status")
    st.plotly_chart(
        create_orders_by_status_chart(filtered_orders_model),
        use_container_width=True,
    )

with bottom_columns[1]:
    divider_columns = st.columns([0.03, 1], gap="small")
    with divider_columns[0]:
        st.markdown(
            "<div style='height: 500px; border-left: 1px solid #2a2a2a; "
            "margin: 0 auto;'></div>",
            unsafe_allow_html=True,
        )

    with divider_columns[1]:
        st.subheader("Latest orders")

        if latest_orders.empty:
            st.warning(
                "No latest order data are available for the selected order status filter."
            )
        else:
            st.dataframe(
                latest_orders,
                hide_index=True,
                width="stretch",
                column_config={
                    "order_date": st.column_config.DateColumn(
                        "order_date",
                        format="YYYY-MM-DD",
                    ),
                    "revenue": st.column_config.NumberColumn(
                        "revenue",
                        format="%.2f EUR",
                    ),
                },
            )
