from pathlib import Path

import pandas as pd
import pytest

from src.storage import resolve_data_dir, save_raw_snapshot, verify_storage_round_trip


def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=3, freq="B"),
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 100.0, 101.0],
            "close": [100.5, 101.5, 102.5],
            "volume": [1000, 1100, 1200],
        }
    )


def test_resolve_data_dir_defaults_inside_project(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.delenv("DATA_DIR", raising=False)

    assert resolve_data_dir(tmp_path) == tmp_path / "data"


def test_resolve_data_dir_uses_environment_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setenv("DATA_DIR", "custom_data")

    assert resolve_data_dir(tmp_path) == tmp_path / "custom_data"


def test_save_and_verify_round_trip(tmp_path: Path):
    csv_path, parquet_path = save_raw_snapshot(sample_frame(), "SPY", tmp_path)

    assert csv_path.name == "spy_daily.csv"
    assert parquet_path.name == "spy_daily.parquet"
    verify_storage_round_trip(sample_frame(), csv_path, parquet_path)


def test_verify_round_trip_requires_both_files(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="missing stored data"):
        verify_storage_round_trip(
            sample_frame(), tmp_path / "missing.csv", tmp_path / "missing.parquet"
        )
