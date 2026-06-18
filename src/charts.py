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
    """Create a monthly revenue line chart."""
    if _is_empty_or_missing(orders_model, {"order_date", "revenue"}):
        return _empty_chart("Monthly revenue")

    chart_df = _with_month(orders_model)
    chart_df["revenue"] = pd.to_numeric(chart_df["revenue"], errors="coerce").fillna(0)
    chart_data = chart_df.groupby("month", as_index=False)["revenue"].sum()

    if chart_data.empty:
        return _empty_chart("Monthly revenue")

    figure = px.line(
        chart_data,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly revenue",
        labels={"month": "Month", "revenue": "Revenue (€)"},
    )
    figure.update_traces(name="Revenue (€)", showlegend=True)

    return figure


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


def create_orders_by_status_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create an order count by status chart."""
    if _is_empty_or_missing(orders_model, {"order_status", "order_id"}):
        return _empty_chart("Orders by status")

    chart_data = (
        orders_model.groupby("order_status", as_index=False)["order_id"]
        .nunique()
        .rename(columns={"order_id": "orders"})
        .sort_values("orders", ascending=False)
    )

    if chart_data.empty:
        return _empty_chart("Orders by status")

    return px.bar(
        chart_data,
        x="order_status",
        y="orders",
        title="Orders by status",
        labels={"order_status": "Order status", "orders": "Orders"},
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


def create_revenue_by_category_donut_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a revenue by product category donut chart."""
    if _is_empty_or_missing(orders_model, {"category", "revenue"}):
        return _empty_chart("Revenue by category")

    chart_df = orders_model.copy()
    chart_df["revenue"] = pd.to_numeric(chart_df["revenue"], errors="coerce").fillna(0)
    chart_data = (
        chart_df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    if chart_data.empty:
        return _empty_chart("Revenue by category")

    return px.pie(
        chart_data,
        names="category",
        values="revenue",
        title="Revenue by category",
        hole=0.45,
    )


def create_stock_value_by_category_chart(stock_df: pd.DataFrame) -> go.Figure:
    """Create a stock value by category chart."""
    if _is_empty_or_missing(stock_df, {"category", "stock_value"}):
        return _empty_chart("Stock value by category")

    chart_df = stock_df.copy()
    chart_df["stock_value"] = pd.to_numeric(
        chart_df["stock_value"],
        errors="coerce",
    ).fillna(0)
    chart_data = (
        chart_df.groupby("category", as_index=False)["stock_value"]
        .sum()
        .sort_values("stock_value", ascending=False)
    )

    if chart_data.empty:
        return _empty_chart("Stock value by category")

    return px.bar(
        chart_data,
        x="category",
        y="stock_value",
        title="Stock value by category",
        labels={"category": "Category", "stock_value": "Stock value"},
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
