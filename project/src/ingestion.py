"""Validated market-data acquisition at the external network boundary."""

import pandas as pd
import yfinance as yf

from src.utils import clean_columns, parse_date_column


REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]
PRICE_COLUMNS = ["open", "high", "low", "close"]


def normalize_yfinance_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert a single-symbol yfinance response into the project data contract."""
    if frame.empty:
        raise ValueError("yfinance returned no rows")

    result = frame.copy()
    if isinstance(result.columns, pd.MultiIndex):
        tickers = result.columns.get_level_values(-1).unique()
        if len(tickers) != 1:
            raise ValueError("expected exactly one ticker in yfinance response")
        result.columns = result.columns.get_level_values(0)

    result = result.reset_index()
    result = clean_columns(result)
    if "date" not in result.columns:
        result = result.rename(columns={result.columns[0]: "date"})

    missing = [column for column in REQUIRED_COLUMNS if column not in result.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    result = result[REQUIRED_COLUMNS]
    result = parse_date_column(result, "date")
    for column in PRICE_COLUMNS + ["volume"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")
    return result.reset_index(drop=True)


def validate_market_data(frame: pd.DataFrame, min_rows: int = 20) -> None:
    """Raise a clear error unless market data satisfies the project invariant."""
    if frame.columns.tolist() != REQUIRED_COLUMNS:
        raise ValueError(f"expected columns {REQUIRED_COLUMNS}")
    if len(frame) < min_rows:
        raise ValueError(f"expected at least {min_rows} rows")
    if frame["date"].isna().any():
        raise ValueError("date contains missing values")
    if frame["date"].duplicated().any():
        raise ValueError("duplicate dates found")
    if not frame["date"].is_monotonic_increasing:
        raise ValueError("dates must be ordered")
    if frame[PRICE_COLUMNS].isna().any().any():
        raise ValueError("price columns contain missing or nonnumeric values")
    if not (frame[PRICE_COLUMNS] > 0).all().all():
        raise ValueError("prices must be positive")
    if frame["volume"].isna().any() or (frame["volume"] < 0).any():
        raise ValueError("volume must be nonnegative and nonmissing")


def download_daily_prices(symbol: str, start: str, end: str | None = None) -> pd.DataFrame:
    """Download and validate adjusted daily OHLCV history for one ticker."""
    raw = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        actions=False,
        threads=False,
    )
    normalized = normalize_yfinance_frame(raw)
    validate_market_data(normalized)
    return normalized
