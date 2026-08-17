"""Environment-driven, reconciled storage for project data snapshots."""

import os
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal


def resolve_data_dir(project_root: Path) -> Path:
    """Resolve DATA_DIR, keeping relative paths inside the project root."""
    configured = Path(os.getenv("DATA_DIR", "data")).expanduser()
    if configured.is_absolute():
        return configured.resolve()
    return (project_root / configured).resolve()


def save_raw_snapshot(
    frame: pd.DataFrame, symbol: str, data_dir: Path
) -> tuple[Path, Path]:
    """Write one stable raw snapshot as both CSV and Parquet."""
    raw_dir = Path(data_dir) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{symbol.lower()}_daily"
    csv_path = raw_dir / f"{stem}.csv"
    parquet_path = raw_dir / f"{stem}.parquet"
    frame.to_csv(csv_path, index=False)
    frame.to_parquet(parquet_path, index=False)
    return csv_path, parquet_path


def verify_storage_round_trip(
    source: pd.DataFrame, csv_path: Path, parquet_path: Path
) -> None:
    """Require both stored representations to reconcile with the source data."""
    missing = [str(path) for path in (csv_path, parquet_path) if not Path(path).is_file()]
    if missing:
        raise FileNotFoundError(f"missing stored data: {missing}")

    expected = source.reset_index(drop=True)
    csv_frame = pd.read_csv(csv_path, parse_dates=["date"])[expected.columns]
    parquet_frame = pd.read_parquet(parquet_path)[expected.columns]
    assert_frame_equal(
        expected,
        csv_frame,
        check_dtype=False,
        rtol=1e-10,
        atol=1e-12,
    )
    assert_frame_equal(
        expected,
        parquet_frame,
        check_dtype=False,
        rtol=1e-10,
        atol=1e-12,
    )
