# Data Schema

This project includes fictional sample data for the demo e-commerce dashboard.
The files are safe to keep in GitHub and do not contain real company,
customer, product, order, or price data.

## Sample CSV Files

The sample data lives in `data/sample/` and can be regenerated with:

```bash
python scripts/generate_sample_data.py
```

### `products.csv`

Purpose: product master data used to describe items sold in the demo store.

Columns:

- `product_id`: stable fictional product identifier.
- `sku`: fictional stock keeping unit.
- `product_name`: generated fictional product name.
- `category`: product category.
- `supplier`: fictional supplier name.
- `brand`: fictional brand name.
- `cost_price`: generated unit cost price.
- `sales_price`: generated list sales price.
- `active`: whether the product is currently active in the catalog.

### `orders.csv`

Purpose: order header data with order-level commercial and operational
attributes.

Columns:

- `order_id`: stable fictional order identifier.
- `order_date`: order date in ISO format.
- `country`: destination country code.
- `customer_type`: customer segment, such as new, returning, or business.
- `order_status`: order state, such as completed, cancelled, returned, or pending.
- `payment_method`: payment method used for the order.
- `shipping_method`: delivery or shipping method.

### `order_items.csv`

Purpose: line-level order data connecting orders to purchased products.

Columns:

- `order_id`: order identifier matching `orders.order_id`.
- `product_id`: product identifier matching `products.product_id`.
- `quantity`: ordered quantity.
- `unit_price`: generated line unit price.
- `discount_pct`: generated discount rate applied to the line.
- `revenue`: line revenue calculated from quantity, unit price, and discount.

### `stock_snapshots.csv`

Purpose: monthly stock snapshots for each product over the demo reporting
period.

Columns:

- `snapshot_date`: monthly snapshot date in ISO format.
- `product_id`: product identifier matching `products.product_id`.
- `stock_qty`: generated stock quantity on the snapshot date.
- `stock_value`: stock value calculated from stock quantity and product cost price.

## Relationships

- `orders.order_id` -> `order_items.order_id`
- `products.product_id` -> `order_items.product_id`
- `products.product_id` -> `stock_snapshots.product_id`

## Safety Note

These are fully fictional sample datasets intended for GitHub, local demos, and
the Streamlit demo dashboard. Real operational data belongs outside GitHub,
for example in `data/private/` or in an approved external data source.
