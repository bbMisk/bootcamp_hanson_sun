"""Reusable outlier detection and sensitivity functions for Homework 07."""

import pandas as pd


def _numeric(series: pd.Series) -> pd.Series:
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a pandas Series")
    if series.empty or series.dropna().empty:
        raise ValueError("series must contain numeric data")
    if not pd.api.types.is_numeric_dtype(series):
        raise TypeError("series must be numeric")
    return series.astype(float)


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """Return an aligned IQR-rule outlier mask."""
    if k <= 0:
        raise ValueError("k must be positive")
    numeric = _numeric(series)
    q1, q3 = numeric.quantile([0.25, 0.75])
    spread = q3 - q1
    return ((numeric < q1 - k * spread) | (numeric > q3 + k * spread)).fillna(
        False
    )


def detect_outliers_zscore(
    series: pd.Series, threshold: float = 3.0
) -> pd.Series:
    """Return an aligned population-Z-score outlier mask."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    numeric = _numeric(series)
    sigma = numeric.std(ddof=0, skipna=True)
    if sigma == 0 or pd.isna(sigma):
        return pd.Series(False, index=numeric.index, dtype=bool)
    return (((numeric - numeric.mean()) / sigma).abs() > threshold).fillna(False)


def winsorize_series(
    series: pd.Series, lower: float = 0.05, upper: float = 0.95
) -> pd.Series:
    """Clip a numeric series to declared lower and upper quantiles."""
    if not 0 <= lower < upper <= 1:
        raise ValueError("quantiles must satisfy 0 <= lower < upper <= 1")
    numeric = _numeric(series)
    return numeric.clip(numeric.quantile(lower), numeric.quantile(upper))


def sensitivity_summary(
    series: pd.Series,
    outlier_mask: pd.Series,
    *,
    lower: float = 0.05,
    upper: float = 0.95,
) -> pd.DataFrame:
    """Compare raw, IQR-filtered, and winsorized distribution summaries."""
    numeric = _numeric(series)
    mask = outlier_mask.reindex(numeric.index).fillna(False).astype(bool)
    treatments = {
        "all": numeric,
        "filtered_iqr": numeric.loc[~mask],
        "winsorized": winsorize_series(numeric, lower=lower, upper=upper),
    }
    return pd.DataFrame.from_dict(
        {
            name: {
                "count": int(values.count()),
                "mean": float(values.mean()),
                "median": float(values.median()),
                "std": float(values.std(ddof=1)),
            }
            for name, values in treatments.items()
        },
        orient="index",
    )
