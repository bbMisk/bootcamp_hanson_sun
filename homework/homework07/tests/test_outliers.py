import pandas as pd
import pytest

from src.outliers import (
    detect_outliers_iqr,
    detect_outliers_zscore,
    sensitivity_summary,
    winsorize_series,
)


def test_iqr_and_zscore_return_aligned_boolean_masks():
    values = pd.Series([0.0] * 20 + [1.0], index=range(10, 31))

    iqr = detect_outliers_iqr(values)
    zscore = detect_outliers_zscore(values, threshold=3.0)

    assert iqr.index.equals(values.index) and iqr.dtype == bool
    assert zscore.index.equals(values.index) and zscore.dtype == bool
    assert iqr.iloc[-1] and zscore.iloc[-1]


def test_winsorization_and_sensitivity_preserve_the_raw_series():
    raw = pd.Series([1.0, 2.0, 3.0, 100.0])
    snapshot = raw.copy()
    mask = detect_outliers_iqr(raw)

    clipped = winsorize_series(raw, lower=0.25, upper=0.75)
    summary = sensitivity_summary(raw, mask, lower=0.25, upper=0.75)

    pd.testing.assert_series_equal(raw, snapshot)
    assert clipped.max() == pytest.approx(27.25)
    assert list(summary.index) == ["all", "filtered_iqr", "winsorized"]
    assert summary.loc["filtered_iqr", "count"] == 3


def test_reversed_quantiles_fail_loudly():
    with pytest.raises(ValueError, match="lower < upper"):
        winsorize_series(pd.Series([1.0, 2.0]), lower=0.9, upper=0.1)
