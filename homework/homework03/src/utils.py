import pandas as pd


def get_summary_stats(frame: pd.DataFrame) -> pd.DataFrame:
    """Return transposed numeric summary statistics for readable export."""
    return frame.describe(include="number").T
