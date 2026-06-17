# MU Dash Streamlit

Minimal Streamlit Business Dashboard for e-commerce and business data.

## Goal

The project provides a safe base structure for a multipage Streamlit dashboard.
It loads demo data, prepares analytical models, computes KPIs, and renders
Plotly charts while keeping private data outside version control.

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

The Overview page contains the first basic KPI cards and Plotly charts built
from the fictional sample data.

## Sample Data

Generate fictional demo data with:

```bash
python scripts/generate_sample_data.py
```

The generated files are written to `data/sample/` and are safe for GitHub demos.
Real company data must stay outside GitHub, for example in `data/private/`.

## Local setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

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

Start the app:

```bash
streamlit run app.py
```
