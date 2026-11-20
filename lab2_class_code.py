# %% 1. Import Libraries and connect to bazaarbd.db
import sqlite3, pandas as pd
conn = sqlite3.connect("bazaarbd.db")      # Lab 2: "bazaarbd.db"

# %% 2  Run a query and return a DataFrame
def run_query(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)

run_query("SELECT status, COUNT(*) AS n FROM orders GROUP BY status")
# %%
