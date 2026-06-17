# AGENTS.md

Project instructions for AI coding agents working in this repository.

## Project Purpose

MU Dash Streamlit is a Streamlit dashboard for sales, orders, stock, and data quality analysis. The app is intended to be useful both as a demo dashboard with sample data and as an internal analytics tool when connected to real business data.

## Demo vs. Internal Mode

- Demo mode should use only safe sample data from committed demo files.
- Internal mode may use real or private data locally, but those files must stay out of git.
- Do not mix demo data assumptions into reusable transformation, metric, or chart logic unless the behavior is explicitly sample-only.

## Data Safety

- Never commit real data, private data, customer data, secrets, API keys, credentials, exports, or local environment files.
- Never commit anything under `data/private/`.
- Keep `.env`, credentials, downloaded production exports, and ad hoc analysis files out of version control.
- If a task touches data loading or file paths, check whether the change could expose private data before editing.

## Architecture

Follow the existing flow:

`data_loader -> transformations -> metrics -> charts -> pages`

- `src/data_loader.py`: reading source files and basic loading concerns.
- `src/transformations.py`: preparing clean analytical models.
- `src/metrics.py`: reusable KPI and numeric calculations.
- `src/charts.py`: reusable Plotly figure builders.
- `pages/*.py`: Streamlit page layout, filters, and rendering.

Keep page files thin. Put reusable data logic, metrics, and charts in the appropriate `src/` module.

## Change Discipline

- Work in small, focused steps.
- Diagnose before fixing: inspect the current implementation, imports, call sites, data columns, and rendered behavior before editing.
- Do not perform broad refactors unless explicitly requested.
- Do not change unrelated files.
- Preserve existing behavior outside the requested scope.
- Prefer the repository's current patterns over introducing new abstractions.

## Plotly and Charts

- Standard dashboard charts should use Plotly Express unless there is a clear reason to use lower-level Plotly APIs.
- Import Plotly Express as `import plotly.express as px`.
- Chart builder functions in `src/charts.py` should return valid Plotly `Figure` objects.
- Streamlit pages should render Plotly figures with `st.plotly_chart(..., use_container_width=True)`.
- Handle empty dataframes and missing required columns by returning an empty Plotly figure with a useful title.
- Do not use matplotlib, seaborn, or Altair for normal dashboard charts unless explicitly requested.

## Git Rules

- Do not commit or push unless the user explicitly asks for it.
- Before reporting completion, check `git status --short`.
- Mention unrelated pre-existing changes instead of reverting them.
- Never discard user changes without explicit permission.

## Checklist After Changes

- Confirm only intended files changed.
- Run focused syntax or behavior checks when practical.
- Verify Streamlit pages still import correctly when page code changed.
- Check that filters still feed the correct filtered dataframe into metrics and charts.
- Check that charts use expected columns and render through `st.plotly_chart`.
- Summarize changed files and verification results.
