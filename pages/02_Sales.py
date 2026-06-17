"""Sales analysis page."""

import streamlit as st

from src.charts import create_monthly_revenue_chart
from src.data_loader import load_all_data_files
from src.transformations import prepare_orders_model


st.set_page_config(page_title="Sales", layout="wide")

st.title("Sales")
st.write("Monthly revenue view based on the prepared orders model.")

try:
    data = load_all_data_files()
    orders_model = prepare_orders_model(data)
except ValueError as exc:
    st.warning(f"Sales data could not be prepared: {exc}")
    st.stop()

if orders_model.empty:
    st.warning("The orders model is empty. Check the source data files.")
    st.stop()

st.write(f"Rows in orders model: `{len(orders_model):,}`")

st.plotly_chart(
    create_monthly_revenue_chart(orders_model),
    use_container_width=True,
)
