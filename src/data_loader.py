"""Data loading helpers for local CSV and Excel files.

The loader only works inside the configured sample or private data directory.
"""

from pathlib import Path

import pandas as pd

from src.config import DATA_MODE, PRIVATE_DATA_DIR, SAMPLE_DATA_DIR


SUPPORTED_DATA_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def get_active_data_dir():
    """Return the active data directory based on DATA_MODE."""
    if DATA_MODE == "sample":
        return SAMPLE_DATA_DIR
    if DATA_MODE == "private":
        return PRIVATE_DATA_DIR

    raise ValueError(
        f"Unknown DATA_MODE '{DATA_MODE}'. Expected 'sample' or 'private'."
    )


def list_data_files():
    """List supported CSV and Excel files in the active data directory."""
    data_dir = get_active_data_dir()

    if not data_dir.exists():
        return []

    return sorted(
        file_path
        for file_path in data_dir.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in SUPPORTED_DATA_EXTENSIONS
    )


def load_data_file(file_path):
    """Load one supported data file without transforming its contents."""
    path = _resolve_safe_data_path(file_path)
    suffix = path.suffix.lower()

    try:
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(path)
    except Exception as exc:
        raise ValueError(f"Could not load data file '{path.name}': {exc}") from exc

    raise ValueError(
        f"Unsupported data file type '{suffix}'. Supported types are CSV, XLSX, XLS."
    )


def load_all_data_files():
    """Load all supported files from the active data directory."""
    return {file_path.name: load_data_file(file_path) for file_path in list_data_files()}


def _resolve_safe_data_path(file_path):
    """Resolve a path and ensure it stays inside the active data directory."""
    active_dir = get_active_data_dir().resolve()
    path = Path(file_path)

    if not path.is_absolute():
        path = active_dir / path

    resolved_path = path.resolve()

    if resolved_path.parent != active_dir:
        raise ValueError(
            "Data files can only be loaded directly from the active data directory."
        )

    if resolved_path.suffix.lower() not in SUPPORTED_DATA_EXTENSIONS:
        raise ValueError(
            "Unsupported data file type. Supported types are CSV, XLSX, XLS."
        )

    return resolved_path
