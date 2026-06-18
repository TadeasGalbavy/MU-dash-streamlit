"""Dashboard methodology page."""

import streamlit as st


st.set_page_config(page_title="Methodology", layout="wide")

st.title("Methodology")

st.markdown(
    """
    This dashboard provides a concise view of sales performance, order activity,
    and current stock position. It is designed to work both as a portfolio-ready
    demo with safe sample data and as an internal analytics tool when connected
    to private business data.
    """
)

st.subheader("Demo and internal modes")

st.markdown(
    """
    **Demo mode** uses committed sample datasets from `data/sample/`. These files
    are fictional or anonymized and are safe for GitHub, demos, and portfolio
    presentations.

    **Internal mode** is intended for real company data used locally or through an
    approved private data source. Real exports, customer data, credentials, and
    operational files must stay outside version control.
    """
)

st.info(
    "The same dashboard logic should work in both modes; only the data source changes."
)

st.subheader("Data model")

st.markdown(
    """
    The dashboard is built from four core datasets:

    - `orders.csv`: order headers with order date, country, customer type,
      order status, payment method, and shipping method.
    - `order_items.csv`: order line items with purchased product, quantity,
      unit price, discount, and line revenue.
    - `products.csv`: product master data with SKU, product name, category,
      supplier, brand, prices, and active flag.
    - `stock_snapshots.csv`: monthly inventory snapshots with stock quantity
      and stock value by product.

    Main relationships:

    - `orders.order_id` -> `order_items.order_id`
    - `products.product_id` -> `order_items.product_id`
    - `products.product_id` -> `stock_snapshots.product_id`
    """
)

st.subheader("KPI definitions")

st.markdown(
    """
    - **Total revenue** = sum of `revenue`.
    - **Orders** = count of unique `order_id`.
    - **Average order value** = total revenue divided by the number of orders.
    - **Items sold** = sum of `quantity`.
    - **Total stock value** = sum of `stock_value` from the latest stock snapshot.
    - **Out of stock products** = count of products where `stock_qty == 0`.
    """
)

st.subheader("Data safety")

st.markdown(
    """
    Sample data in this repository is fictional or anonymized. Real business
    data, customer data, credentials, API keys, exports, and local environment
    files must never be committed.

    The following paths are reserved for local/private use and should remain out
    of version control:

    - `data/private/`
    - `.env`
    - `.streamlit/secrets.toml`
    """
)
