"""Main entry point for the Streamlit Business Dashboard."""

import streamlit as st


def render_home() -> None:
    """Render the dashboard landing page."""
    st.title("Streamlit Business Dashboard")
    st.write(
        "Portfolio-ready multipage dashboard for e-commerce sales, orders, "
        "stock, and data quality analysis."
    )

    st.info("Demo mode · Sample e-commerce data")

    st.warning(
        "Real company data must never be committed to GitHub. Use only sample or "
        "anonymized data in demo mode."
    )


navigation = st.navigation(
    [
        st.Page(render_home, title="Home", default=True),
        st.Page("pages/01_Overview.py", title="Overview"),
        st.Page("pages/02_Sales.py", title="Sales"),
        st.Page("pages/03_Stock.py", title="Stock"),
        st.Page("pages/04_Orders.py", title="Orders"),
        st.Page("pages/05_Data_Preview.py", title="Data Preview"),
        st.Page("pages/06_Methodology.py", title="Methodology"),
    ]
)
navigation.run()
