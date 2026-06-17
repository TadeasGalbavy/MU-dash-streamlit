# Project Brief

This project is a Streamlit Business Dashboard for e-commerce and business
reporting workflows.

## Purpose

The dashboard will provide a structured place for future sales, stock, order,
and data quality views. The current version is intentionally minimal and does
not calculate KPIs, render charts, or load real files.

## Planned Pages

- Overview
- Sales
- Stock
- Orders
- Data Preview
- Methodology

## Dual-Mode Architecture

The project is designed around two operating modes:

- Demo mode uses only sample or anonymized data suitable for GitHub and public
  previews.
- Internal mode uses real company data stored locally in `data/private/` or,
  later, in an external source.

## Data Protection

Real company data must never be committed to GitHub. The `data/private/`
directory and `.streamlit/secrets.toml` are ignored by Git so private files and
secrets stay local.
