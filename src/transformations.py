"""Data transformation helpers for dashboard-ready data models."""

import pandas as pd


REQUIRED_ORDER_FILES = {"orders.csv", "order_items.csv", "products.csv"}
REQUIRED_STOCK_FILES = {"stock_snapshots.csv", "products.csv"}

ORDERS_MODEL_COLUMNS = [
    "order_id",
    "order_date",
    "country",
    "customer_type",
    "order_status",
    "payment_method",
    "shipping_method",
    "product_id",
    "sku",
    "product_name",
    "category",
    "supplier",
    "brand",
    "quantity",
    "unit_price",
    "discount_pct",
    "revenue",
    "cost_price",
    "sales_price",
]


def prepare_orders_model(data: dict) -> pd.DataFrame:
    """Return an item-level analytical order model."""
    _require_files(data, REQUIRED_ORDER_FILES)

    orders = data["orders.csv"].copy()
    order_items = data["order_items.csv"].copy()
    products = data["products.csv"].copy()

    if orders.empty or order_items.empty or products.empty:
        return pd.DataFrame(columns=ORDERS_MODEL_COLUMNS)

    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")

    orders_model = order_items.merge(
        orders,
        on="order_id",
        how="left",
        validate="many_to_one",
    ).merge(
        products,
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    return orders_model[ORDERS_MODEL_COLUMNS]


def prepare_latest_stock_snapshot(data: dict) -> pd.DataFrame:
    """Return the newest stock snapshot enriched with product attributes."""
    _require_files(data, REQUIRED_STOCK_FILES)

    stock_snapshots = data["stock_snapshots.csv"].copy()
    products = data["products.csv"].copy()

    if stock_snapshots.empty or products.empty:
        return pd.DataFrame()

    stock_snapshots["snapshot_date"] = pd.to_datetime(
        stock_snapshots["snapshot_date"],
        errors="coerce",
    )
    latest_snapshot_date = stock_snapshots["snapshot_date"].max()

    if pd.isna(latest_snapshot_date):
        return pd.DataFrame()

    latest_stock = stock_snapshots[
        stock_snapshots["snapshot_date"] == latest_snapshot_date
    ].merge(
        products,
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    return latest_stock


def prepare_latest_orders_table(
    orders_model: pd.DataFrame,
    limit: int = 10,
) -> pd.DataFrame:
    """Return the latest unique orders with order-level revenue."""
    output_columns = [
        "order_id",
        "order_date",
        "country",
        "customer_type",
        "order_status",
        "payment_method",
        "shipping_method",
        "revenue",
    ]
    required_columns = set(output_columns)

    if (
        orders_model is None
        or orders_model.empty
        or not required_columns.issubset(orders_model.columns)
    ):
        return pd.DataFrame(columns=output_columns)

    orders_table = orders_model.copy()
    orders_table["order_date"] = pd.to_datetime(
        orders_table["order_date"],
        errors="coerce",
    )
    orders_table["revenue"] = pd.to_numeric(
        orders_table["revenue"],
        errors="coerce",
    ).fillna(0)

    latest_orders = (
        orders_table.groupby("order_id", as_index=False)
        .agg(
            order_date=("order_date", "max"),
            country=("country", "first"),
            customer_type=("customer_type", "first"),
            order_status=("order_status", "first"),
            payment_method=("payment_method", "first"),
            shipping_method=("shipping_method", "first"),
            revenue=("revenue", "sum"),
        )
        .sort_values("order_date", ascending=False)
        .head(limit)
    )

    return latest_orders[output_columns]


def _require_files(data: dict, required_files: set[str]) -> None:
    """Raise a clear error when expected source files are missing."""
    missing_files = sorted(required_files - set(data))

    if missing_files:
        raise ValueError(f"Missing required data files: {', '.join(missing_files)}")
