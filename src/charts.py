"""Plotly chart builders for dashboard pages."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


BACKGROUND_COLOR = "#0d0d0d"
SURFACE_COLOR = "#141414"
BORDER_COLOR = "#222"
TEXT_COLOR = "#f0ede8"
SOFT_TEXT_COLOR = "#a8a49e"
DATA_ACCENT_COLOR = "#c8f060"
SECONDARY_ACCENT_COLOR = "#FFBBFF"
CHART_COLOR_SEQUENCE = [
    DATA_ACCENT_COLOR,
    SECONDARY_ACCENT_COLOR,
    "#8bd3ff",
    "#f6d365",
    "#b8a7ff",
    "#7ee0c6",
]


def create_revenue_over_time_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a monthly revenue trend chart."""
    if _is_empty_or_missing(orders_model, {"order_date", "revenue"}):
        return _empty_chart("Revenue over time")

    chart_data = _with_month(orders_model).groupby("month", as_index=False)[
        "revenue"
    ].sum()

    figure = px.line(
        chart_data,
        x="month",
        y="revenue",
        markers=True,
        title="Revenue over time",
        labels={"month": "Month", "revenue": "Revenue"},
    )

    return _apply_dark_chart_theme(figure)


def create_monthly_revenue_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a monthly revenue line chart."""
    if _is_empty_or_missing(orders_model, {"order_date", "revenue"}):
        return _empty_chart("Monthly revenue")

    chart_df = _with_month(orders_model)
    chart_df["revenue"] = pd.to_numeric(chart_df["revenue"], errors="coerce").fillna(0)
    chart_data = chart_df.groupby("month", as_index=False)["revenue"].sum()

    if chart_data.empty:
        return _empty_chart("Monthly revenue")

    chart_data["revenue_label"] = chart_data["revenue"].round(0)
    figure = px.line(
        chart_data,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly revenue",
        labels={"month": "Month", "revenue": "Revenue (€)"},
    )
    figure.update_traces(name="Revenue (€)", showlegend=True)

    if len(chart_data) <= 12:
        figure.update_traces(
            mode="lines+markers+text",
            text=chart_data["revenue_label"],
            texttemplate="%{text:,.0f}",
            textposition="top center",
        )

    return _apply_dark_chart_theme(figure)


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

    figure = px.bar(
        chart_data,
        x="month",
        y="orders",
        text="orders",
        title="Orders over time",
        labels={"month": "Month", "orders": "Orders"},
    )

    return _apply_dark_chart_theme(_apply_bar_value_labels(figure, "%{text:,.0f}"))


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

    figure = px.bar(
        chart_data,
        x="order_status",
        y="orders",
        text="orders",
        title="Orders by status",
        labels={"order_status": "Order status", "orders": "Orders"},
    )

    return _apply_dark_chart_theme(_apply_bar_value_labels(figure, "%{text:,.0f}"))


def create_revenue_by_country_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a revenue by country chart."""
    if _is_empty_or_missing(orders_model, {"country", "revenue"}):
        return _empty_chart("Revenue by country")

    chart_data = (
        orders_model.groupby("country", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    chart_data["revenue_label"] = chart_data["revenue"].round(0)

    figure = px.bar(
        chart_data,
        x="country",
        y="revenue",
        text="revenue_label",
        title="Revenue by country",
        labels={"country": "Country", "revenue": "Revenue"},
    )

    return _apply_dark_chart_theme(_apply_bar_value_labels(figure, "%{text:,.0f}"))


def create_revenue_by_category_chart(orders_model: pd.DataFrame) -> go.Figure:
    """Create a revenue by product category chart."""
    if _is_empty_or_missing(orders_model, {"category", "revenue"}):
        return _empty_chart("Revenue by category")

    chart_data = (
        orders_model.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=True)
    )
    chart_data["revenue_label"] = chart_data["revenue"].round(0)

    figure = px.bar(
        chart_data,
        x="revenue",
        y="category",
        text="revenue_label",
        orientation="h",
        title="Revenue by category",
        labels={"category": "Category", "revenue": "Revenue"},
    )

    return _apply_dark_chart_theme(_apply_bar_value_labels(figure, "%{text:,.0f}"))


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

    figure = px.pie(
        chart_data,
        names="category",
        values="revenue",
        title="Revenue by category",
        hole=0.45,
        color_discrete_sequence=CHART_COLOR_SEQUENCE,
    )
    figure.update_traces(
        textinfo="label+percent",
        textposition="inside",
        insidetextorientation="radial",
    )

    return _apply_dark_chart_theme(figure)


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
    chart_data["stock_value_label"] = chart_data["stock_value"].round(0)

    if chart_data.empty:
        return _empty_chart("Stock value by category")

    figure = px.bar(
        chart_data,
        x="category",
        y="stock_value",
        text="stock_value_label",
        title="Stock value by category",
        labels={"category": "Category", "stock_value": "Stock value"},
    )

    return _apply_dark_chart_theme(_apply_bar_value_labels(figure, "%{text:,.0f}"))


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
    return _apply_dark_chart_theme(figure)


def _apply_bar_value_labels(figure: go.Figure, texttemplate: str) -> go.Figure:
    figure.update_traces(
        texttemplate=texttemplate,
        textposition="auto",
        cliponaxis=False,
        textfont={"color": TEXT_COLOR},
    )
    return figure


def _apply_dark_chart_theme(figure: go.Figure) -> go.Figure:
    figure.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=SURFACE_COLOR,
        font={"color": TEXT_COLOR},
        title={"font": {"color": TEXT_COLOR}},
        legend={
            "font": {"color": SOFT_TEXT_COLOR},
            "bgcolor": "rgba(0,0,0,0)",
        },
        margin={"l": 40, "r": 24, "t": 56, "b": 40},
        uniformtext={"mode": "show", "minsize": 10},
    )
    figure.update_xaxes(
        gridcolor=BORDER_COLOR,
        linecolor=BORDER_COLOR,
        tickfont={"color": SOFT_TEXT_COLOR},
        title_font={"color": TEXT_COLOR},
        zerolinecolor=BORDER_COLOR,
    )
    figure.update_yaxes(
        gridcolor=BORDER_COLOR,
        linecolor=BORDER_COLOR,
        tickfont={"color": SOFT_TEXT_COLOR},
        title_font={"color": TEXT_COLOR},
        zerolinecolor=BORDER_COLOR,
    )

    for trace in figure.data:
        if trace.type == "scatter":
            trace.update(
                line={"color": DATA_ACCENT_COLOR},
                marker={"color": DATA_ACCENT_COLOR},
                textfont={"color": TEXT_COLOR},
            )
        elif trace.type == "bar":
            trace.update(
                marker={"color": DATA_ACCENT_COLOR},
                textfont={"color": TEXT_COLOR},
            )
        elif trace.type == "pie":
            trace.update(
                textfont={"color": TEXT_COLOR},
                marker={"line": {"color": BACKGROUND_COLOR, "width": 2}},
            )

    return figure
