"""Reusable cleaning functions for Homework 06."""

from collections.abc import Iterable

import pandas as pd


def _columns(frame: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    selected = list(columns)
    missing = [column for column in selected if column not in frame.columns]
    if missing:
        raise KeyError(f"missing columns: {missing}")
    return selected


def fill_missing_median(
    frame: pd.DataFrame, columns: Iterable[str]
) -> pd.DataFrame:
    """Return a copy with missing numeric values replaced by column medians."""
    result = frame.copy()
    for column in _columns(result, columns):
        numeric = pd.to_numeric(result[column], errors="raise").astype(float)
        median = numeric.median(skipna=True)
        if pd.isna(median):
            raise ValueError(f"{column} has no usable median")
        result[column] = numeric.fillna(median)
    return result


def drop_missing(frame: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Drop columns with a missing fraction greater than ``threshold``."""
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    missing_fraction = frame.isna().mean()
    return frame.drop(
        columns=missing_fraction[missing_fraction > threshold].index
    ).copy()


def normalize_data(
    frame: pd.DataFrame, columns: Iterable[str]
) -> pd.DataFrame:
    """Return a copy with selected numeric columns min-max scaled to [0, 1]."""
    result = frame.copy()
    for column in _columns(result, columns):
        numeric = pd.to_numeric(result[column], errors="raise").astype(float)
        minimum, maximum = numeric.min(), numeric.max()
        if pd.isna(minimum) or pd.isna(maximum):
            raise ValueError(f"{column} has no usable range")
        span = maximum - minimum
        result[column] = 0.0 if span == 0 else (numeric - minimum) / span
    return result
