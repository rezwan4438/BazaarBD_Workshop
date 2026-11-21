"""EXTRACT: read raw CSV files into DataFrames (no cleaning here)."""
import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def read_csv(path: Path, **kwargs) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    df = pd.read_csv(path, **kwargs)
    log.info("extracted %-28s rows=%d cols=%d", path.name, len(df), df.shape[1])
    return df
