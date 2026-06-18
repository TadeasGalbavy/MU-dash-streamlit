"""Stock analysis page."""

import streamlit as st

from src.charts import create_stock_value_by_category_chart
from src.data_loader import load_all_data_files
from src.metrics import (
    calculate_latest_stock_value,
    calculate_out_of_stock_products,
    calculate_products_in_stock,
    calculate_total_stock_quantity,
)
from src.transformations import (
    prepare_latest_stock_snapshot,
    prepare_top_stock_value_products,
)


st.set_page_config(page_title="Stock", layout="wide")

st.title("Stock")
st.write("Review current inventory value, stock availability, and top stocked products.")

try:
    data = load_all_data_files()
    latest_stock_df = prepare_latest_stock_snapshot(data)
except ValueError as exc:
    st.warning(f"Stock data could not be prepared: {exc}")
    st.stop()

if latest_stock_df.empty:
    st.warning("The latest stock snapshot is empty. Check the source data files.")
    st.stop()

if "category" not in latest_stock_df.columns:
    st.warning(
        "Category filter cannot be shown because the latest stock snapshot "
        "has no category column."
    )
    st.stop()

categories = sorted(latest_stock_df["category"].dropna().unique())
with st.expander("Filters", expanded=True):
    selected_categories = st.multiselect(
        "Category",
        options=categories,
        default=categories,
    )

filtered_stock_df = latest_stock_df[
    latest_stock_df["category"].isin(selected_categories)
]

if filtered_stock_df.empty:
    st.warning(
        "No stock data match the selected category filter. Select at least one category."
    )
    st.stop()

st.divider()

st.subheader("Key metrics")
total_stock_value = calculate_latest_stock_value(filtered_stock_df)
total_stock_quantity = calculate_total_stock_quantity(filtered_stock_df)
products_in_stock = calculate_products_in_stock(filtered_stock_df)
out_of_stock_products = calculate_out_of_stock_products(filtered_stock_df)

metric_columns = st.columns(4)
metric_columns[0].metric("Total stock value", f"{total_stock_value:,.2f} EUR")
metric_columns[1].metric("Total stock quantity", f"{total_stock_quantity:,}")
metric_columns[2].metric("Products in stock", f"{products_in_stock:,}")
metric_columns[3].metric("Out of stock products", f"{out_of_stock_products:,}")

st.divider()

st.subheader("Stock value by category")
st.plotly_chart(
    create_stock_value_by_category_chart(filtered_stock_df),
    use_container_width=True,
)

st.subheader("Top stock value products")
top_stock_products = prepare_top_stock_value_products(filtered_stock_df)

if top_stock_products.empty:
    st.warning(
        "No stock value product data are available for the selected category filter."
    )
else:
    st.dataframe(
        top_stock_products,
        hide_index=True,
        use_container_width=True,
        column_config={
            "stock_qty": st.column_config.NumberColumn(
                "stock_qty",
                format="%d",
            ),
            "stock_value": st.column_config.NumberColumn(
                "stock_value",
                format="%.2f EUR",
            ),
        },
    )
