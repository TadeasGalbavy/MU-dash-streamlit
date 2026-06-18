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
    """Calculate average order value from order-level revenue."""
    if (
        orders_model is None
        or orders_model.empty
        or not {"order_id", "revenue"}.issubset(orders_model.columns)
    ):
        return 0.0

    order_revenue = (
        orders_model.assign(
            revenue=pd.to_numeric(orders_model["revenue"], errors="coerce").fillna(0)
        )
        .groupby("order_id", as_index=False)["revenue"]
        .sum()
    )

    if order_revenue.empty:
        return 0.0

    return float(order_revenue["revenue"].mean())


def calculate_top_products_by_revenue(
    orders_model: pd.DataFrame,
    limit: int = 10,
) -> pd.DataFrame:
    """Return top products aggregated by revenue."""
    required_columns = {
        "product_name",
        "category",
        "revenue",
        "quantity",
        "order_id",
    }
    output_columns = ["Product", "Category", "Revenue", "Items sold", "Orders"]

    if (
        orders_model is None
        or orders_model.empty
        or not required_columns.issubset(orders_model.columns)
    ):
        return pd.DataFrame(columns=output_columns)

    top_products = (
        orders_model.assign(
            revenue=pd.to_numeric(orders_model["revenue"], errors="coerce").fillna(0),
            quantity=pd.to_numeric(orders_model["quantity"], errors="coerce").fillna(0),
        )
        .groupby(["product_name", "category"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            order_id=("order_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
        .head(limit)
        .rename(
            columns={
                "product_name": "Product",
                "category": "Category",
                "revenue": "Revenue",
                "quantity": "Items sold",
                "order_id": "Orders",
            }
        )
    )

    top_products["Items sold"] = top_products["Items sold"].astype(int)
    top_products["Orders"] = top_products["Orders"].astype(int)

    return top_products[output_columns]


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
