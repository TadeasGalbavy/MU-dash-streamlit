"""Shared utility helpers."""

from datetime import date

import pandas as pd


def prepare_date_filter_bounds(
    df: pd.DataFrame,
    date_column: str,
) -> tuple[pd.DataFrame, date | None, date | None]:
    """Return a dataframe with parsed dates and safe date filter bounds."""
    if df is None or df.empty or date_column not in df.columns:
        return pd.DataFrame(), None, None

    filtered_df = df.copy()
    filtered_df[date_column] = pd.to_datetime(
        filtered_df[date_column],
        errors="coerce",
    )
    filtered_df = filtered_df.dropna(subset=[date_column])

    if filtered_df.empty:
        return filtered_df, None, None

    return (
        filtered_df,
        filtered_df[date_column].min().date(),
        filtered_df[date_column].max().date(),
    )


def filter_by_date_range(
    df: pd.DataFrame,
    date_column: str,
    date_range: tuple[date, date],
) -> pd.DataFrame:
    """Filter a dataframe by an inclusive date range."""
    if df is None or df.empty or date_column not in df.columns:
        return pd.DataFrame()

    start_date, end_date = date_range
    filtered_df = df.copy()
    filtered_df[date_column] = pd.to_datetime(
        filtered_df[date_column],
        errors="coerce",
    )
    filtered_df = filtered_df.dropna(subset=[date_column])
    order_dates = filtered_df[date_column].dt.date

    return filtered_df[
        (order_dates >= start_date)
        & (order_dates <= end_date)
    ]


def prepare_month_filter_options(
    df: pd.DataFrame,
    date_column: str,
) -> tuple[pd.DataFrame, list[str]]:
    """Return a dataframe with parsed dates and available YYYY-MM month options."""
    if df is None or df.empty or date_column not in df.columns:
        return pd.DataFrame(), []

    filtered_df = df.copy()
    filtered_df[date_column] = pd.to_datetime(
        filtered_df[date_column],
        errors="coerce",
    )
    filtered_df = filtered_df.dropna(subset=[date_column])

    if filtered_df.empty:
        return filtered_df, []

    months = (
        filtered_df[date_column]
        .dt.to_period("M")
        .drop_duplicates()
        .sort_values()
        .astype(str)
        .tolist()
    )

    return filtered_df, months


def filter_by_month_range(
    df: pd.DataFrame,
    date_column: str,
    start_month: str,
    end_month: str,
) -> pd.DataFrame:
    """Filter a dataframe by an inclusive YYYY-MM month range."""
    if df is None or df.empty or date_column not in df.columns:
        return pd.DataFrame()

    filtered_df = df.copy()
    filtered_df[date_column] = pd.to_datetime(
        filtered_df[date_column],
        errors="coerce",
    )
    filtered_df = filtered_df.dropna(subset=[date_column])

    start_period = pd.Period(start_month, freq="M")
    end_period = pd.Period(end_month, freq="M")
    order_months = filtered_df[date_column].dt.to_period("M")

    return filtered_df[
        (order_months >= start_period)
        & (order_months <= end_period)
    ]
