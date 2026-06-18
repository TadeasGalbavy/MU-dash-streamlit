# MU Dash Streamlit

MU Dash Streamlit is a multipage Streamlit dashboard for e-commerce and
business analytics. It brings together sales, orders, stock, and data quality
views into a single lightweight reporting app built with Python, Pandas, and
Plotly.

The project is designed for two use cases:

- **Demo mode** uses committed fictional or anonymized sample data from
  `data/sample/`. This mode is safe for GitHub, portfolio presentation, and
  local demos.
- **Internal mode** is intended for real business data stored outside GitHub,
  for example in `data/private/` or a future private data source.

## Dashboard pages

- **Executive Overview**: management summary with key sales, order, and stock
  KPIs plus high-level revenue and order status charts.
- **Sales**: country-filtered sales performance with revenue KPIs, monthly
  revenue, category revenue, and top products by revenue.
- **Orders**: order status overview with status-filtered KPIs, orders by
  status, and latest order-level activity.
- **Stock**: current inventory snapshot with category filtering, stock value
  KPIs, stock value by category, and top stock value products.
- **Data Preview**: technical inspection of loaded files, columns, data types,
  missing values, and sample rows.
- **Methodology**: documentation of the data model, KPI definitions, demo vs.
  internal mode, and data safety rules.

## Data model

The demo dashboard uses four core CSV datasets:

- `orders.csv`: order header data such as order date, country, customer type,
  order status, payment method, and shipping method.
- `order_items.csv`: order line data with purchased product, quantity, unit
  price, discount, and line revenue.
- `products.csv`: product master data with product name, category, supplier,
  brand, cost price, sales price, and active flag.
- `stock_snapshots.csv`: monthly product-level stock snapshots with stock
  quantity and stock value.

Main relationships:

- `orders.order_id` -> `order_items.order_id`
- `products.product_id` -> `order_items.product_id`
- `products.product_id` -> `stock_snapshots.product_id`

## Local setup

Clone the repository:

```bash
git clone <repository-url>
cd MU-dash-streamlit
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate sample data if `data/sample/` is empty or missing demo CSV files:

```bash
python scripts/generate_sample_data.py
```

Run the app:

```bash
python -m streamlit run app.py
```

## Data safety

Real business data, customer data, credentials, API keys, production exports,
and local environment files must not be committed to GitHub.

- `data/sample/` contains fictional or anonymized sample data suitable for demos.
- `data/private/` is reserved for local/private data and is ignored by Git.
- `.env` is ignored and should be used only for local environment settings.
- `.streamlit/secrets.toml` is ignored and should be used only for local
  Streamlit secrets.

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly

## Future improvements

- Connect to a cloud data source.
- Add a SQL backend for larger datasets.
- Add authentication and private deployment support.
- Extend advanced filtering across pages.
- Add more KPI pages for finance, customer behavior, and operational quality.
