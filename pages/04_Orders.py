"""Orders analysis page."""

import streamlit as st

from src.charts import create_orders_by_status_chart
from src.data_loader import load_all_data_files
from src.metrics import calculate_orders_by_status, calculate_total_orders
from src.transformations import prepare_latest_orders_table, prepare_orders_model
from src.utils import filter_by_month_range, prepare_month_filter_options


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

orders_model, order_months = prepare_month_filter_options(
    orders_model,
    "order_date",
)

if not order_months:
    st.warning(
        "Month filter cannot be shown because the orders model "
        "has no valid order_date values."
    )
    st.stop()

with st.expander("Filters", expanded=True):
    selected_start_month = st.selectbox(
        "Start month",
        options=order_months,
        index=0,
    )
    selected_end_month = st.selectbox(
        "End month",
        options=order_months,
        index=len(order_months) - 1,
    )

    if selected_start_month > selected_end_month:
        st.warning("Start month must be earlier than or equal to End month.")
        st.stop()

    month_filtered_orders_model = filter_by_month_range(
        orders_model,
        "order_date",
        selected_start_month,
        selected_end_month,
    )

    if month_filtered_orders_model.empty:
        st.warning("No orders match the selected month range.")
        st.stop()

    order_statuses = sorted(
        month_filtered_orders_model["order_status"].dropna().unique()
    )
    selected_order_statuses = st.multiselect(
        "Order status",
        options=order_statuses,
        default=order_statuses,
    )

filtered_orders_model = month_filtered_orders_model[
    month_filtered_orders_model["order_status"].isin(selected_order_statuses)
]

if filtered_orders_model.empty:
    st.warning(
        "No orders match the selected month range and order status filter."
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

st.subheader("Orders by status")
st.plotly_chart(
    create_orders_by_status_chart(filtered_orders_model),
    use_container_width=True,
)

st.subheader("Latest orders")
latest_orders = prepare_latest_orders_table(filtered_orders_model)

if latest_orders.empty:
    st.warning("No latest order data are available for the selected order status filter.")
else:
    st.dataframe(
        latest_orders,
        hide_index=True,
        use_container_width=True,
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
