import pandas as pd
import pytest

from src.cleaning import drop_missing, fill_missing_median, normalize_data


def test_cleaning_workflow_is_copy_safe_and_complete():
    original = pd.DataFrame(
        {
            "age": [20.0, None, 40.0],
            "score": [5.0, 10.0, 15.0],
            "mostly_missing": [None, None, 1.0],
        }
    )

    filled = fill_missing_median(original, ["age"])
    reduced = drop_missing(filled, threshold=0.5)
    cleaned = normalize_data(reduced, ["age", "score"])

    assert pd.isna(original.loc[1, "age"])
    assert "mostly_missing" not in cleaned
    assert cleaned["age"].tolist() == [0.0, 0.5, 1.0]
    assert cleaned["score"].tolist() == [0.0, 0.5, 1.0]


def test_invalid_threshold_fails_loudly():
    with pytest.raises(ValueError, match="between 0 and 1"):
        drop_missing(pd.DataFrame({"x": [1]}), threshold=1.1)
