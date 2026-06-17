"""Generate deterministic fictional sample data for the demo dashboard."""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample"

RANDOM_SEED = 42
PRODUCT_COUNT = 120
ORDER_COUNT = 1000
DEMO_START_DATE = date(2025, 7, 1)
DEMO_END_DATE = date(2026, 6, 17)


CATEGORIES = {
    "Home Essentials": {
        "nouns": ["Organizer", "Storage Box", "Cleaning Kit", "Shelf Insert"],
        "cost_range": (4.5, 28.0),
        "markup_range": (1.45, 2.35),
    },
    "Kitchen": {
        "nouns": ["Prep Bowl", "Spice Rack", "Lunch Jar", "Serving Tray"],
        "cost_range": (5.0, 34.0),
        "markup_range": (1.5, 2.4),
    },
    "Office Gear": {
        "nouns": ["Desk Pad", "Cable Dock", "Notebook Set", "Task Lamp"],
        "cost_range": (3.5, 42.0),
        "markup_range": (1.55, 2.5),
    },
    "Travel": {
        "nouns": ["Packing Cube", "Travel Pouch", "Bottle Sleeve", "Luggage Tag"],
        "cost_range": (4.0, 38.0),
        "markup_range": (1.5, 2.45),
    },
    "Personal Care": {
        "nouns": ["Care Pouch", "Mirror Case", "Brush Stand", "Towel Wrap"],
        "cost_range": (3.0, 26.0),
        "markup_range": (1.6, 2.6),
    },
    "Pet Supplies": {
        "nouns": ["Snack Tin", "Toy Basket", "Feeding Mat", "Travel Bowl"],
        "cost_range": (2.5, 24.0),
        "markup_range": (1.55, 2.55),
    },
    "Fitness": {
        "nouns": ["Grip Band", "Yoga Strap", "Training Towel", "Hydration Clip"],
        "cost_range": (3.0, 32.0),
        "markup_range": (1.55, 2.5),
    },
    "Electronics Accessories": {
        "nouns": ["Cable Set", "Charging Stand", "Tablet Sleeve", "Adapter Pouch"],
        "cost_range": (5.5, 48.0),
        "markup_range": (1.45, 2.3),
    },
}

ADJECTIVES = [
    "Aero",
    "Bright",
    "Clear",
    "Compact",
    "Flex",
    "Fresh",
    "Metro",
    "Nord",
    "Prime",
    "Urban",
]
BRANDS = ["Auralen", "Brixo", "Cavaro", "Doventa", "Elvara", "Fintoro"]
SUPPLIERS = [
    "Demo Supply One",
    "Fictional Trade Co",
    "Sample Goods Hub",
    "Northbridge Demo Ltd",
    "Central Test Supply",
]
COUNTRIES = ["SK", "CZ", "PL", "HU", "RO"]
CUSTOMER_TYPES = ["new", "returning", "business"]
ORDER_STATUSES = ["completed", "cancelled", "returned", "pending"]
PAYMENT_METHODS = ["card", "bank_transfer", "cash_on_delivery", "digital_wallet"]
SHIPPING_METHODS = ["standard", "express", "pickup_point", "courier"]


def money(value: float) -> float:
    """Round monetary values consistently for CSV output."""
    return round(value + 1e-9, 2)


def weighted_choice(options: list[str], weights: list[float]) -> str:
    return random.choices(options, weights=weights, k=1)[0]


def random_date(start: date, end: date) -> date:
    day_offset = random.randint(0, (end - start).days)
    return start + timedelta(days=day_offset)


def generate_products() -> pd.DataFrame:
    rows = []
    category_names = list(CATEGORIES)

    for index in range(1, PRODUCT_COUNT + 1):
        category = category_names[(index - 1) % len(category_names)]
        category_config = CATEGORIES[category]
        noun = random.choice(category_config["nouns"])
        adjective = random.choice(ADJECTIVES)
        variant = random.randint(10, 99)
        cost_min, cost_max = category_config["cost_range"]
        markup_min, markup_max = category_config["markup_range"]
        cost_price = money(random.uniform(cost_min, cost_max))
        sales_price = money(cost_price * random.uniform(markup_min, markup_max))

        rows.append(
            {
                "product_id": f"P{index:04d}",
                "sku": f"DEMO-{category[:3].upper().replace(' ', '')}-{index:04d}",
                "product_name": f"{adjective} {noun} {variant}",
                "category": category,
                "supplier": random.choice(SUPPLIERS),
                "brand": random.choice(BRANDS),
                "cost_price": cost_price,
                "sales_price": sales_price,
                "active": random.random() >= 0.08,
            }
        )

    return pd.DataFrame(rows)


def generate_orders() -> pd.DataFrame:
    rows = []

    for index in range(1, ORDER_COUNT + 1):
        order_date = random_date(DEMO_START_DATE, DEMO_END_DATE)
        rows.append(
            {
                "order_id": f"ORD-{index:06d}",
                "order_date": order_date.isoformat(),
                "country": weighted_choice(COUNTRIES, [0.32, 0.25, 0.18, 0.14, 0.11]),
                "customer_type": weighted_choice(
                    CUSTOMER_TYPES, [0.34, 0.56, 0.10]
                ),
                "order_status": weighted_choice(
                    ORDER_STATUSES, [0.78, 0.08, 0.07, 0.07]
                ),
                "payment_method": weighted_choice(
                    PAYMENT_METHODS, [0.58, 0.18, 0.14, 0.10]
                ),
                "shipping_method": weighted_choice(
                    SHIPPING_METHODS, [0.48, 0.18, 0.22, 0.12]
                ),
            }
        )

    return pd.DataFrame(rows).sort_values("order_date").reset_index(drop=True)


def generate_order_items(products: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    rows = []
    product_records = products.to_dict("records")

    for order_id in orders["order_id"]:
        item_count = weighted_choice(["1", "2", "3", "4"], [0.46, 0.31, 0.16, 0.07])
        selected_products = random.sample(product_records, int(item_count))

        for product in selected_products:
            quantity = weighted_choice(
                ["1", "2", "3", "4", "5"],
                [0.58, 0.24, 0.10, 0.05, 0.03],
            )
            unit_price = money(
                product["sales_price"] * random.uniform(0.96, 1.04)
            )
            discount_pct = weighted_choice(
                ["0.00", "0.05", "0.10", "0.15", "0.20"],
                [0.58, 0.18, 0.14, 0.07, 0.03],
            )

            rows.append(
                {
                    "order_id": order_id,
                    "product_id": product["product_id"],
                    "quantity": int(quantity),
                    "unit_price": unit_price,
                    "discount_pct": float(discount_pct),
                }
            )

    order_items = pd.DataFrame(rows)
    order_items["revenue"] = (
        order_items["quantity"]
        * order_items["unit_price"]
        * (1 - order_items["discount_pct"])
    ).round(2)

    return order_items


def month_starts(start: date, months: int) -> list[date]:
    dates = []
    year = start.year
    month = start.month

    for _ in range(months):
        dates.append(date(year, month, 1))
        month += 1
        if month == 13:
            month = 1
            year += 1

    return dates


def generate_stock_snapshots(products: pd.DataFrame) -> pd.DataFrame:
    rows = []
    snapshots = month_starts(DEMO_START_DATE, 12)

    for product in products.to_dict("records"):
        base_stock = random.randint(20, 240)

        for snapshot_index, snapshot_date in enumerate(snapshots):
            seasonal_change = random.randint(-25, 30)
            stock_qty = max(0, base_stock + seasonal_change - snapshot_index * random.randint(0, 5))
            stock_value = money(stock_qty * product["cost_price"])

            rows.append(
                {
                    "snapshot_date": snapshot_date.isoformat(),
                    "product_id": product["product_id"],
                    "stock_qty": stock_qty,
                    "stock_value": stock_value,
                }
            )

    return pd.DataFrame(rows)


def write_csv(df: pd.DataFrame, file_name: str) -> None:
    output_path = SAMPLE_DATA_DIR / file_name
    df.to_csv(output_path, index=False)


def main() -> None:
    random.seed(RANDOM_SEED)
    SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    products = generate_products()
    orders = generate_orders()
    order_items = generate_order_items(products, orders)
    stock_snapshots = generate_stock_snapshots(products)

    write_csv(products, "products.csv")
    write_csv(orders, "orders.csv")
    write_csv(order_items, "order_items.csv")
    write_csv(stock_snapshots, "stock_snapshots.csv")

    print(f"Generated sample data in {SAMPLE_DATA_DIR}")
    print(f"products.csv: {len(products)} rows")
    print(f"orders.csv: {len(orders)} rows")
    print(f"order_items.csv: {len(order_items)} rows")
    print(f"stock_snapshots.csv: {len(stock_snapshots)} rows")


if __name__ == "__main__":
    main()
