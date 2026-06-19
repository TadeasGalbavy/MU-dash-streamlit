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
from src.utils import filter_by_month_range, prepare_month_filter_options


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
        st.warning("No sales data match the selected month range.")
        st.stop()

    countries = sorted(month_filtered_orders_model["country"].dropna().unique())
    selected_countries = st.multiselect(
        "Country",
        options=countries,
        default=countries,
    )

filtered_orders_model = month_filtered_orders_model[
    month_filtered_orders_model["country"].isin(selected_countries)
]

if filtered_orders_model.empty:
    st.warning("No sales data match the selected month range and country filter.")
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
    use_container_width=True,
)

st.subheader("Revenue by category")
st.plotly_chart(
    create_revenue_by_category_donut_chart(filtered_orders_model),
    use_container_width=True,
)

st.subheader("Top products by revenue")
top_products = calculate_top_products_by_revenue(filtered_orders_model)

if top_products.empty:
    st.warning("No product revenue data are available for the selected country filter.")
else:
    st.dataframe(
        top_products,
        hide_index=True,
        use_container_width=True,
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
