"""Business metric calculations for dashboard pages."""

import pandas as pd


def calculate_total_revenue(orders_model: pd.DataFrame) -> float:
    """Calculate total revenue from the prepared orders model."""
    return _sum_column(orders_model, "revenue")


def calculate_total_orders(orders_model: pd.DataFrame) -> int:
    """Calculate the number of unique orders."""
    if _is_empty_or_missing(orders_model, "order_id"):
        return 0

    return int(orders_model["order_id"].nunique())


def calculate_total_quantity(orders_model: pd.DataFrame) -> int:
    """Calculate the number of sold items."""
    return int(_sum_column(orders_model, "quantity"))


def calculate_average_order_value(orders_model: pd.DataFrame) -> float:
    """Calculate average order value from revenue and unique orders."""
    total_orders = calculate_total_orders(orders_model)

    if total_orders == 0:
        return 0.0

    return calculate_total_revenue(orders_model) / total_orders


def calculate_active_products(products_df: pd.DataFrame) -> int:
    """Calculate the number of active products."""
    if _is_empty_or_missing(products_df, "active"):
        return 0

    active = products_df["active"]

    if active.dtype == bool:
        return int(active.sum())

    return int(active.astype(str).str.lower().isin({"true", "1", "yes"}).sum())


def calculate_latest_stock_value(latest_stock_df: pd.DataFrame) -> float:
    """Calculate the latest stock value."""
    return _sum_column(latest_stock_df, "stock_value")


def _sum_column(df: pd.DataFrame, column: str) -> float:
    if _is_empty_or_missing(df, column):
        return 0.0

    return float(pd.to_numeric(df[column], errors="coerce").fillna(0).sum())


def _is_empty_or_missing(df: pd.DataFrame, column: str) -> bool:
    return df is None or df.empty or column not in df.columns
