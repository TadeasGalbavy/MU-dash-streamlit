"""Technical data preview page."""

import pandas as pd
import streamlit as st

from src.data_loader import list_data_files, load_data_file
from src.data_validation import get_dataframe_summary


st.set_page_config(page_title="Data Preview", layout="wide")

st.title("Data Preview")

try:
    data_files = list_data_files()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.info("Active dataset: Sample e-commerce data")
st.caption(
    "Raw exports contain sample data in demo mode. Handle raw exports carefully "
    "when using internal or private data."
)

if not data_files:
    st.info(
        "No CSV or Excel files were found in the active data directory. "
        "Add a `.csv`, `.xlsx`, or `.xls` file to preview its structure."
    )
    st.stop()

st.write("Found data files:")
st.dataframe(
    pd.DataFrame({"file_name": [file_path.name for file_path in data_files]}),
    width="stretch",
    hide_index=True,
)

for file_path in data_files:
    with st.expander(file_path.name):
        try:
            df = load_data_file(file_path)
            summary = get_dataframe_summary(df)
        except ValueError as exc:
            st.error(str(exc))
            continue

        st.write(
            f"Rows: `{summary['row_count']}` | "
            f"Columns: `{summary['column_count']}`"
        )

        if not df.empty:
            download_file_name = file_path.with_suffix(".csv").name
            st.download_button(
                "Download raw CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=download_file_name,
                mime="text/csv",
                key=f"download-{file_path.name}",
            )

        st.write("Data types")
        st.dataframe(
            pd.DataFrame(
                {
                    "column": summary["columns"],
                    "dtype": [
                        summary["dtypes"][column] for column in summary["columns"]
                    ],
                }
            ),
            width="stretch",
            hide_index=True,
        )

        st.write("Missing values")
        st.dataframe(
            pd.DataFrame(
                {
                    "column": summary["columns"],
                    "missing_values": [
                        summary["missing_values"][column]
                        for column in summary["columns"]
                    ],
                }
            ),
            width="stretch",
            hide_index=True,
        )

        st.write("First 10 rows")
        st.dataframe(df.head(10), width="stretch")
