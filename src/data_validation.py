"""Basic dataframe inspection helpers."""


def get_dataframe_summary(df):
    """Return a technical summary for a pandas dataframe."""
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
    }
