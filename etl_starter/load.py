"""LOAD: write clean data into SQLite. INSERT OR IGNORE makes every load safe to repeat."""
import logging
import sqlite3
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def init_db(db_path: Path, schema_file: Path, reset: bool) -> sqlite3.Connection:
    fresh = reset or not db_path.exists()
    if reset and db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    if fresh:
        conn.executescript(schema_file.read_text(encoding="utf-8"))
        log.info("created schema in %s", db_path.name)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def load_table(conn: sqlite3.Connection, df: pd.DataFrame, table: str) -> int:
    """Insert rows that are not already present (by primary key). Returns rows actually added."""
    df = df.astype(object).where(df.notna(), None)          # NaN -> NULL
    cols = list(df.columns)
    sql = f"INSERT OR IGNORE INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})"
    before = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.executemany(sql, df.itertuples(index=False, name=None))
    conn.commit()
    added = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] - before
    log.info("loaded %-12s offered=%d added=%d skipped(existing)=%d", table, len(df), added, len(df) - added)
    return added
