"""Outlier detection, handling, and sensitivity helpers."""

import numpy as np
import pandas as pd


def _validated_numeric(series: pd.Series) -> pd.Series:
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a pandas Series")
    if series.empty or series.dropna().empty:
        raise ValueError("series must contain non-empty numeric data")
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError("series must be numeric")
    return series.astype(float)


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Return an aligned mask for points outside Q1 - k*IQR and Q3 + k*IQR."""
    if k <= 0:
        raise ValueError("k must be positive")
    numeric = _validated_numeric(series)
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    mask = (numeric < q1 - k * iqr) | (numeric > q3 + k * iqr)
    return mask.fillna(False).astype(bool)


def detect_outliers_zscore(
    series: pd.Series, threshold: float = 3.0
) -> pd.Series:
    """Return an aligned population-Z-score mask; missing values are unflagged."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    numeric = _validated_numeric(series)
    sigma = numeric.std(ddof=0, skipna=True)
    if sigma == 0 or pd.isna(sigma):
        return pd.Series(False, index=numeric.index, dtype=bool)
    zscore = (numeric - numeric.mean(skipna=True)) / sigma
    return zscore.abs().gt(threshold).fillna(False).astype(bool)


def winsorize_series(
    series: pd.Series, lower: float = 0.05, upper: float = 0.95
) -> pd.Series:
    """Clip values to declared quantiles while preserving index and missing values."""
    if not 0 <= lower < upper <= 1:
        raise ValueError("quantiles must satisfy 0 <= lower < upper <= 1")
    numeric = _validated_numeric(series)
    return numeric.clip(
        lower=numeric.quantile(lower), upper=numeric.quantile(upper)
    )


def flag_outliers(
    frame: pd.DataFrame,
    column: str,
    *,
    method: str = "iqr",
    flag_column: str = "is_outlier",
    k: float = 1.5,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """Return a copy with a boolean outlier flag for one numeric column."""
    if column not in frame.columns:
        raise KeyError(f"missing column: {column}")
    result = frame.copy()
    if method == "iqr":
        result[flag_column] = detect_outliers_iqr(result[column], k=k)
    elif method == "zscore":
        result[flag_column] = detect_outliers_zscore(
            result[column], threshold=threshold
        )
    else:
        raise ValueError("method must be 'iqr' or 'zscore'")
    return result


def sensitivity_summary(
    series: pd.Series,
    outlier_mask: pd.Series,
    *,
    lower: float = 0.05,
    upper: float = 0.95,
) -> pd.DataFrame:
    """Compare distribution summaries for all, filtered, and winsorized values."""
    numeric = _validated_numeric(series)
    mask = outlier_mask.reindex(numeric.index).fillna(False).astype(bool)
    treatments = {
        "all": numeric,
        "filtered_iqr": numeric.loc[~mask],
        "winsorized": winsorize_series(numeric, lower=lower, upper=upper),
    }
    rows = {}
    for name, values in treatments.items():
        rows[name] = {
            "count": int(values.count()),
            "mean": float(values.mean()),
            "median": float(values.median()),
            "std": float(values.std(ddof=1)),
        }
    return pd.DataFrame.from_dict(rows, orient="index")
