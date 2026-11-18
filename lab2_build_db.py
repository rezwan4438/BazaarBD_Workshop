"""Lab 2 helper: create bazaarbd.db from schema.sql and load the clean CSVs.

Usage:  python lab2_build_db.py [path/to/schema.sql]
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
# use your own Lab 1 output if it exists, otherwise the reference copy
CLEAN = ROOT / "data" / "clean"
if not (CLEAN / "orders_clean.csv").exists():
    CLEAN = ROOT / "reference_clean"
DB = ROOT / "bazaarbd.db"
schema_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "schema.sql"

# load order matters because of foreign keys: parents first
TABLES = [("customers", "customers_clean.csv"),
          ("products", "products_clean.csv"),
          ("orders", "orders_clean.csv"),
          ("order_items", "order_items_clean.csv")]

conn = sqlite3.connect(DB)
conn.executescript(schema_path.read_text(encoding="utf-8"))
conn.execute("PRAGMA foreign_keys = ON")

for table, csv in TABLES:
    df = pd.read_csv(CLEAN / csv, dtype={"phone": str})
    df.to_sql(table, conn, if_exists="append", index=False)   # append keeps YOUR schema
    print(f"{table:12s} {len(df):5d} rows loaded")

conn.commit()
print("integrity:", conn.execute("PRAGMA foreign_key_check").fetchall() or "OK")
conn.close()
print("Created", DB)
