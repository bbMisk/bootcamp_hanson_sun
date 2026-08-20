import importlib

import numpy as np
import pandas as pd
import pytest


def cleaning():
    return importlib.import_module("src.cleaning")


def test_fill_missing_median_fills_declared_numeric_columns_without_mutating_input():
    source = pd.DataFrame({"value": [1.0, np.nan, 5.0], "label": ["a", "b", "c"]})

    result = cleaning().fill_missing_median(source, ["value"])

    assert result["value"].tolist() == [1.0, 3.0, 5.0]
    assert source["value"].isna().tolist() == [False, True, False]


def test_fill_missing_median_rejects_all_missing_column():
    source = pd.DataFrame({"value": [np.nan, np.nan]})

    with pytest.raises(ValueError, match="no finite median"):
        cleaning().fill_missing_median(source, ["value"])


def test_drop_missing_removes_columns_above_missingness_threshold():
    source = pd.DataFrame(
        {"keep": [1.0, 2.0, 3.0], "mostly_missing": [1.0, np.nan, np.nan]}
    )

    result = cleaning().drop_missing(source, threshold=0.5)

    assert result.columns.tolist() == ["keep"]
    assert len(result) == 3


def test_normalize_data_minmax_scales_and_handles_constant_column():
    source = pd.DataFrame({"value": [10.0, 20.0, 30.0], "constant": [4.0] * 3})

    result = cleaning().normalize_data(source, ["value", "constant"])

    assert result["value"].tolist() == [0.0, 0.5, 1.0]
    assert result["constant"].tolist() == [0.0, 0.0, 0.0]


def test_preprocess_market_data_sorts_filters_and_creates_finite_log_returns():
    source = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-01-05", "2026-01-02", "2026-01-06"]),
            "open": [102.0, 100.0, 103.0],
            "high": [103.0, 101.0, 104.0],
            "low": [101.0, 99.0, 102.0],
            "close": [102.0, 100.0, -1.0],
            "volume": [1_100.0, np.nan, 1_200.0],
        }
    )

    result = cleaning().preprocess_market_data(source)

    assert result["date"].dt.strftime("%Y-%m-%d").tolist() == ["2026-01-05"]
    assert result.columns.tolist() == [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "log_return",
    ]
    assert np.isclose(result.loc[0, "log_return"], np.log(102.0 / 100.0))
    assert not result.isna().any().any()
