"""Main entry point for the Streamlit Business Dashboard."""

import streamlit as st

from src.config import DATA_MODE, DEPLOYMENT_MODE


st.set_page_config(
    page_title="Business Dashboard",
    layout="wide",
)

st.title("Streamlit Business Dashboard")
st.write(
    "Minimal multipage dashboard structure for e-commerce and business data."
)

st.warning(
    "Real company data must never be committed to GitHub. Use only sample or "
    "anonymized data in demo mode."
)

st.info(f"Current data mode: `{DATA_MODE}` | deployment mode: `{DEPLOYMENT_MODE}`")
