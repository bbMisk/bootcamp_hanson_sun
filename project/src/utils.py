"""Small, reusable data-cleaning utilities."""

import re

import pandas as pd


def clean_column_name(name: str) -> str:
    """Return a lowercase snake-case representation of a column name."""
    normalized = re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower())
    return normalized.strip("_")


def clean_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of *frame* with normalized column names."""
    result = frame.copy()
    result.columns = [clean_column_name(column) for column in result.columns]
    return result


def parse_date_column(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """Parse and chronologically sort a date column without mutating input."""
    result = frame.copy()
    parsed = pd.to_datetime(result[column], errors="coerce")
    if parsed.isna().any():
        raise ValueError(f"{column} contains invalid dates")
    result[column] = parsed
    return result.sort_values(column).reset_index(drop=True)
