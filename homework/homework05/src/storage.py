from pathlib import Path
from typing import Union

import pandas as pd


PathLike = Union[str, Path]


def detect_format(path: PathLike) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix in {".parquet", ".pq", ".parq"}:
        return "parquet"
    raise ValueError(f"Unsupported format: {suffix or '<none>'}")


def write_df(frame: pd.DataFrame, path: PathLike) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if detect_format(output) == "csv":
        frame.to_csv(output, index=False)
    else:
        try:
            frame.to_parquet(output, index=False)
        except ImportError as error:
            raise RuntimeError(
                "Parquet engine not available. Install pyarrow or fastparquet."
            ) from error
    return output


def read_df(path: PathLike) -> pd.DataFrame:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(source)
    if detect_format(source) == "csv":
        frame = pd.read_csv(source)
        if "date" in frame.columns:
            frame["date"] = pd.to_datetime(frame["date"], errors="raise")
        return frame
    try:
        return pd.read_parquet(source)
    except ImportError as error:
        raise RuntimeError(
            "Parquet engine not available. Install pyarrow or fastparquet."
        ) from error
