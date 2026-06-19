"""Project configuration constants."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_MODE = "sample"
DEPLOYMENT_MODE = "demo"

SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample"
PRIVATE_DATA_DIR = PROJECT_ROOT / "data" / "private"


def get_data_mode_label():
    """Return a user-facing label for the current data mode."""
    if DATA_MODE == "sample":
        return "Demo / sample data"
    if DATA_MODE == "private":
        return "Internal / private data"

    raise ValueError(
        f"Unknown DATA_MODE '{DATA_MODE}'. Expected 'sample' or 'private'."
    )


def get_configured_data_dir():
    """Return the configured data directory for the current data mode."""
    if DATA_MODE == "sample":
        return SAMPLE_DATA_DIR
    if DATA_MODE == "private":
        return PRIVATE_DATA_DIR

    raise ValueError(
        f"Unknown DATA_MODE '{DATA_MODE}'. Expected 'sample' or 'private'."
    )
