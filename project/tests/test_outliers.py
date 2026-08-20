import importlib

import numpy as np
import pandas as pd
import pytest


def outliers():
    return importlib.import_module("src.outliers")


def test_detect_outliers_iqr_flags_extreme_value_and_preserves_nan_as_unflagged():
    source = pd.Series([10.0, 11.0, 12.0, 13.0, 100.0, np.nan])

    result = outliers().detect_outliers_iqr(source, k=1.5)

    assert result.tolist() == [False, False, False, False, True, False]


def test_detect_outliers_zscore_uses_population_scale_and_flags_extreme_value():
    source = pd.Series([0.0, 0.0, 0.0, 10.0])

    result = outliers().detect_outliers_zscore(source, threshold=1.5)

    assert result.tolist() == [False, False, False, True]


@pytest.mark.parametrize(
    ("function_name", "parameter"),
    [("detect_outliers_iqr", {"k": 0}), ("detect_outliers_zscore", {"threshold": -1})],
)
def test_outlier_detectors_reject_nonpositive_thresholds(function_name, parameter):
    function = getattr(outliers(), function_name)

    with pytest.raises(ValueError, match="positive"):
        function(pd.Series([1.0, 2.0, 3.0]), **parameter)


def test_outlier_detectors_reject_empty_series():
    with pytest.raises(ValueError, match="non-empty"):
        outliers().detect_outliers_iqr(pd.Series([], dtype=float))


def test_winsorize_series_clips_to_declared_quantiles():
    source = pd.Series([0.0, 1.0, 2.0, 100.0])

    result = outliers().winsorize_series(source, lower=0.25, upper=0.75)

    assert result.tolist() == [0.75, 1.0, 2.0, 26.5]


def test_winsorize_series_rejects_reversed_quantiles():
    with pytest.raises(ValueError, match="lower < upper"):
        outliers().winsorize_series(
            pd.Series([1.0, 2.0, 3.0]), lower=0.9, upper=0.1
        )


def test_flag_outliers_returns_copy_with_boolean_flag():
    source = pd.DataFrame({"return": [10.0, 11.0, 12.0, 13.0, 100.0]})

    result = outliers().flag_outliers(source, "return", method="iqr", k=1.5)

    assert result["is_outlier"].tolist() == [False, False, False, False, True]
    assert "is_outlier" not in source.columns


def test_sensitivity_summary_compares_all_filtered_and_winsorized_treatments():
    source = pd.Series([10.0, 11.0, 12.0, 13.0, 100.0], name="return")
    mask = pd.Series([False, False, False, False, True])

    result = outliers().sensitivity_summary(source, mask, lower=0.2, upper=0.8)

    assert result.index.tolist() == ["all", "filtered_iqr", "winsorized"]
    assert result["count"].tolist() == [5, 4, 5]
    assert result.loc["all", "mean"] == 29.2
    assert result.loc["filtered_iqr", "mean"] == 11.5
