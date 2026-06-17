# MU Dash Streamlit

Minimal Streamlit Business Dashboard for e-commerce and business data.

## Goal

The project provides a safe base structure for a future multipage dashboard.
This initial version contains only placeholders and does not load data, compute
KPIs, or render charts.

## Demo vs. Internal Mode

- Demo mode uses only sample or anonymized data and is suitable for GitHub or
  public previews.
- Internal mode is reserved for real company data stored locally in
  `data/private/` or later in an external source.

Real company data must never be committed to GitHub. Keep private datasets in
`data/private/` and secrets in `.streamlit/secrets.toml`; both paths are ignored
by Git.

## Data Preview

The Data Preview page provides a technical check of files loaded from the active
data directory. It supports CSV, XLSX, and XLS files and displays row counts,
column counts, data types, missing values, and the first 10 rows.

## Sample Data

Generate fictional demo data with:

```bash
python scripts/generate_sample_data.py
```

The generated files are written to `data/sample/` and are safe for GitHub demos.
Real company data must stay outside GitHub, for example in `data/private/`.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run app.py
```
