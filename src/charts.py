"""Plotly chart builders for dashboard pages."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_revenue_over_time_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a monthly revenue trend chart."""
    if _is_empty_or_missing(orders_model, {"order_date", "revenue"}):
        return _empty_chart("Revenue over time")

    chart_data = _with_month(orders_model).groupby("month", as_index=False)[
        "revenue"
    ].sum()

    return px.line(
        chart_data,
        x="month",
        y="revenue",
        markers=True,
        title="Revenue over time",
        labels={"month": "Month", "revenue": "Revenue"},
    )


def create_monthly_revenue_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a revenue by month chart."""
    if _is_empty_or_missing(orders_model, {"order_date", "revenue"}):
        return _empty_chart("Revenue by month")

    chart_data = _with_month(orders_model).groupby("month", as_index=False)[
        "revenue"
    ].sum()

    if chart_data.empty:
        return _empty_chart("Revenue by month")

    return px.bar(
        chart_data,
        x="month",
        y="revenue",
        title="Revenue by month",
        labels={"month": "Month", "revenue": "Revenue"},
    )


def create_orders_over_time_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a monthly order count trend chart."""
    if _is_empty_or_missing(orders_model, {"order_date", "order_id"}):
        return _empty_chart("Orders over time")

    chart_data = (
        _with_month(orders_model)
        .groupby("month", as_index=False)["order_id"]
        .nunique()
        .rename(columns={"order_id": "orders"})
    )

    return px.bar(
        chart_data,
        x="month",
        y="orders",
        title="Orders over time",
        labels={"month": "Month", "orders": "Orders"},
    )


def create_revenue_by_country_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a revenue by country chart."""
    if _is_empty_or_missing(orders_model, {"country", "revenue"}):
        return _empty_chart("Revenue by country")

    chart_data = (
        orders_model.groupby("country", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    return px.bar(
        chart_data,
        x="country",
        y="revenue",
        title="Revenue by country",
        labels={"country": "Country", "revenue": "Revenue"},
    )


def create_revenue_by_category_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a revenue by product category chart."""
    if _is_empty_or_missing(orders_model, {"category", "revenue"}):
        return _empty_chart("Revenue by category")

    chart_data = (
        orders_model.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=True)
    )

    return px.bar(
        chart_data,
        x="revenue",
        y="category",
        orientation="h",
        title="Revenue by category",
        labels={"category": "Category", "revenue": "Revenue"},
    )


def _with_month(df: pd.DataFrame) -> pd.DataFrame:
    chart_df = df.copy()
    chart_df["order_date"] = pd.to_datetime(chart_df["order_date"], errors="coerce")
    chart_df = chart_df.dropna(subset=["order_date"])
    chart_df["month"] = chart_df["order_date"].dt.to_period("M").dt.to_timestamp()
    return chart_df


def _is_empty_or_missing(df: pd.DataFrame, columns: set[str]) -> bool:
    return df is None or df.empty or not columns.issubset(df.columns)


def _empty_chart(title: str) -> go.Figure:
    figure = go.Figure()
    figure.update_layout(title=title)
    return figure
