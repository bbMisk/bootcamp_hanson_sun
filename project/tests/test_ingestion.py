import pandas as pd
import pytest

from src.ingestion import normalize_yfinance_frame, validate_market_data


def sample_frame(rows: int = 25) -> pd.DataFrame:
    dates = pd.date_range("2026-01-01", periods=rows, freq="B")
    return pd.DataFrame(
        {
            "Open": range(100, 100 + rows),
            "High": range(101, 101 + rows),
            "Low": range(99, 99 + rows),
            "Close": range(100, 100 + rows),
            "Volume": [1_000] * rows,
        },
        index=dates,
    )


def test_normalize_yfinance_frame_creates_stable_schema():
    result = normalize_yfinance_frame(sample_frame())

    assert result.columns.tolist() == ["date", "open", "high", "low", "close", "volume"]
    assert result["date"].is_monotonic_increasing


def test_normalize_yfinance_frame_flattens_single_ticker_multiindex():
    source = sample_frame()
    source.columns = pd.MultiIndex.from_product([source.columns, ["SPY"]])

    result = normalize_yfinance_frame(source)

    assert result.columns.tolist() == ["date", "open", "high", "low", "close", "volume"]


def test_validate_market_data_accepts_valid_frame():
    validate_market_data(normalize_yfinance_frame(sample_frame()))


def test_validate_market_data_rejects_small_response():
    with pytest.raises(ValueError, match="at least 20 rows"):
        validate_market_data(normalize_yfinance_frame(sample_frame(3)))


def test_validate_market_data_rejects_duplicate_dates():
    frame = normalize_yfinance_frame(sample_frame())
    frame.loc[1, "date"] = frame.loc[0, "date"]

    with pytest.raises(ValueError, match="duplicate dates"):
        validate_market_data(frame)


def test_validate_market_data_rejects_nonpositive_prices():
    frame = normalize_yfinance_frame(sample_frame())
    frame.loc[0, "close"] = 0

    with pytest.raises(ValueError, match="positive"):
        validate_market_data(frame)
