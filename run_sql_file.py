"""Run every statement in a .sql file against bazaarbd.db and print the first rows of each result."""
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent / "bazaarbd.db"
sql = Path(sys.argv[1]).read_text(encoding="utf-8")
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6

conn = sqlite3.connect(DB)
for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
    title = next((l for l in stmt.splitlines() if l.startswith("--")), "").strip()
    cur = conn.execute(stmt)

    if cur.description is not None:
        rows = cur.fetchall()
        print(f"\n{title}\n  cols={[d[0] for d in cur.description]}  n_rows={len(rows)}")
        for r in rows[:limit]:
            print("  ", r)
    else:
        print(f"\n{title}\n  rows affected={cur.rowcount}")
