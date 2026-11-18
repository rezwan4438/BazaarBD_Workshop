# Lab 3 starter: SQL + Python together.  Run cell by cell (Shift+Enter).
# %% Setup
import sqlite3
from pathlib import Path
import pandas as pd

pd.set_option("display.width", 140)
DB = Path("bazaarbd_lab3.db")
CLEAN = Path("data/clean")           # use reference_clean/ if your Lab 1 output is incomplete
RAW = Path("data/raw")

# %% Task 1: helper + load
def run_query(conn, sql, params=()):
    """Run a SELECT and return a DataFrame."""
    return pd.read_sql_query(sql, conn, params=params)

# TODO 1a: connect to DB; for each of customers, products, orders, order_items read the *_clean.csv
#          (phone as str) and write it with df.to_sql(table, conn, index=False)
# TODO 1b: run_query(conn, "SELECT COUNT(*) AS n FROM orders WHERE status = ?", ("Delivered",))

# %% Task 2: advanced SQL (paste each query in a triple-quoted string and call run_query)
# 2a  CTE + CASE: customer segments by lifetime spend (VIP >= 50000, Regular >= 20000, else Occasional)
# 2b  RANK() window: top 3 products by revenue in each category
# 2c  Monthly revenue with running total (SUM OVER) and month-over-month growth (LAG)
# 2d  ROW_NUMBER(): average days between each customer's 1st and 2nd order (julianday)
# 2e  Best customer (highest spend) in each delivery city

# %% Task 3: data-quality checks
# TODO: write dq_duplicates(conn, table, key), dq_orphans(conn, child, fk, parent, pk),
#       dq_not_positive(conn, table, col), dq_distinct(conn, table, col)
# TODO: write run_checks(conn, label) that prints a small report
# TODO: run it on (a) your clean database and (b) the RAW files loaded into an in-memory database
