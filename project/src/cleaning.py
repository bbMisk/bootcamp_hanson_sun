"""Reusable preprocessing functions for tabular and market data."""

from collections.abc import Iterable

import numpy as np
import pandas as pd


MARKET_COLUMNS = ["date", "open", "high", "low", "close", "volume"]
PRICE_COLUMNS = ["open", "high", "low", "close"]


def _require_columns(frame: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    requested = list(columns)
    missing = [column for column in requested if column not in frame.columns]
    if missing:
        raise KeyError(f"missing columns: {missing}")
    return requested


def _numeric_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if not pd.api.types.is_numeric_dtype(frame[column]):
        raise TypeError(f"{column} must be numeric")
    return frame[column].astype(float)


def fill_missing_median(
    frame: pd.DataFrame, columns: Iterable[str]
) -> pd.DataFrame:
    """Return a copy with missing values filled by each column's finite median."""
    result = frame.copy()
    for column in _require_columns(result, columns):
        numeric = _numeric_series(result, column)
        median = numeric.median(skipna=True)
        if pd.isna(median) or not np.isfinite(median):
            raise ValueError(f"{column} has no finite median")
        result[column] = numeric.fillna(float(median))
    return result


def drop_missing(frame: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Drop columns whose missing fraction is greater than *threshold*."""
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    result = frame.copy()
    missing_fraction = result.isna().mean()
    return result.drop(columns=missing_fraction[missing_fraction > threshold].index)


def normalize_data(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Return a copy with declared numeric columns min-max scaled to [0, 1]."""
    result = frame.copy()
    for column in _require_columns(result, columns):
        numeric = _numeric_series(result, column)
        minimum = numeric.min(skipna=True)
        maximum = numeric.max(skipna=True)
        if pd.isna(minimum) or pd.isna(maximum):
            raise ValueError(f"{column} has no finite range")
        span = maximum - minimum
        result[column] = 0.0 if span == 0 else (numeric - minimum) / span
    return result


def preprocess_market_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Clean OHLCV data and derive a same-day-safe close-to-close log return."""
    _require_columns(frame, MARKET_COLUMNS)
    result = frame[MARKET_COLUMNS].copy()
    result["date"] = pd.to_datetime(result["date"], errors="coerce")
    for column in PRICE_COLUMNS + ["volume"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    result = result.dropna(subset=["date"])
    result = result.sort_values("date").drop_duplicates("date", keep="last")
    result = fill_missing_median(result, ["volume"])
    result = result.dropna(subset=PRICE_COLUMNS + ["volume"])
    valid = (result[PRICE_COLUMNS] > 0).all(axis=1) & (result["volume"] >= 0)
    result = result.loc[valid].copy()
    result["log_return"] = np.log(result["close"] / result["close"].shift(1))
    result = result.replace([np.inf, -np.inf], np.nan).dropna(subset=["log_return"])
    return result.reset_index(drop=True)
