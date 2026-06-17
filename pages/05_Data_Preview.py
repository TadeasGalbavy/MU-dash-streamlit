"""Technical data preview page."""

import pandas as pd
import streamlit as st

from src.config import DATA_MODE
from src.data_loader import get_active_data_dir, list_data_files, load_data_file
from src.data_validation import get_dataframe_summary


st.set_page_config(page_title="Data Preview", layout="wide")

st.title("Data Preview")

try:
    active_data_dir = get_active_data_dir()
    data_files = list_data_files()
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.info(f"Current data mode: `{DATA_MODE}`")
st.write(f"Active data directory: `{active_data_dir}`")

if not data_files:
    st.info(
        "No CSV or Excel files were found in the active data directory. "
        "Add a `.csv`, `.xlsx`, or `.xls` file to preview its structure."
    )
    st.stop()

st.write("Found data files:")
st.dataframe(
    pd.DataFrame({"file_name": [file_path.name for file_path in data_files]}),
    use_container_width=True,
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
            use_container_width=True,
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
            use_container_width=True,
            hide_index=True,
        )

        st.write("First 10 rows")
        st.dataframe(df.head(10), use_container_width=True)
