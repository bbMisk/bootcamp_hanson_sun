import pandas as pd
import pytest

from src.utils import clean_column_name, clean_columns, parse_date_column


def test_clean_column_name_normalizes_spacing_and_symbols():
    assert clean_column_name(" Adj Close ($) ") == "adj_close"


def test_clean_columns_returns_copy_with_normalized_columns():
    source = pd.DataFrame({"Trade Date": ["2026-01-02"], "Adj Close": [100.0]})

    result = clean_columns(source)

    assert result.columns.tolist() == ["trade_date", "adj_close"]
    assert source.columns.tolist() == ["Trade Date", "Adj Close"]


def test_parse_date_column_parses_and_sorts_dates():
    source = pd.DataFrame({"date": ["2026-01-03", "2026-01-02"]})

    result = parse_date_column(source, "date")

    assert result["date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2026-01-02",
        "2026-01-03",
    ]


def test_parse_date_column_rejects_invalid_values():
    with pytest.raises(ValueError, match="invalid dates"):
        parse_date_column(pd.DataFrame({"date": ["not-a-date"]}), "date")
