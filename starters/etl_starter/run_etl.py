"""Run the BazaarBD ETL pipeline.

  python -m etl.run_etl --mode full          # rebuild warehouse from data/raw
  python -m etl.run_etl --mode incremental   # add the new batch from data/incoming
Run from the project root (the folder that contains the `etl` package).
"""
import argparse
import logging
import sqlite3
import time

import pandas as pd

from . import config as cfg
from . import extract, load, transform, validate


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s",
                        handlers=[logging.FileHandler(cfg.LOG_FILE, encoding="utf-8"), logging.StreamHandler()])


def run_full(conn):
    customers = transform.clean_customers(extract.read_csv(cfg.RAW_DIR / "customers_raw.csv", dtype={"phone": str}))
    products = transform.clean_products(extract.read_csv(cfg.RAW_DIR / "products_raw.csv"))
    raw_orders = extract.read_csv(cfg.RAW_DIR / "orders_raw.csv")
    orders = transform.clean_orders(raw_orders, customers)
    raw_items = extract.read_csv(cfg.RAW_DIR / "order_items_raw.csv")
    items = transform.clean_items(raw_items, orders, products)
    return customers, products, orders, items, raw_orders["order_id"].nunique(), raw_items["order_item_id"].nunique()


def run_incremental(conn):
    # reference data already in the warehouse
    customers = pd.read_sql_query("SELECT * FROM customers", conn)
    products = pd.read_sql_query("SELECT * FROM products", conn)
    raw_orders = extract.read_csv(cfg.INCOMING_DIR / "orders_2026-11.csv")
    orders = transform.clean_orders(raw_orders, customers)
    raw_items = extract.read_csv(cfg.INCOMING_DIR / "order_items_2026-11.csv")
    items = transform.clean_items(raw_items, orders, products)
    return None, None, orders, items, raw_orders["order_id"].nunique(), raw_items["order_item_id"].nunique()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["full", "incremental"], default="full")
    args = ap.parse_args()
    setup_logging()
    log = logging.getLogger("etl")
    t0 = time.time()
    log.info("=== ETL start | mode=%s ===", args.mode)

    conn = load.init_db(cfg.WAREHOUSE_DB, cfg.SCHEMA_FILE, reset=(args.mode == "full"))
    try:
        customers, products, orders, items, n_raw_o, n_raw_i = (run_full if args.mode == "full" else run_incremental)(conn)

        # ---- validate (stop before anything is written)
        validate.check_drop_ratio(n_raw_o, len(orders), "orders")
        validate.check_drop_ratio(n_raw_i, len(items), "order_items")
        validate.validate_orders(orders)
        validate.validate_items(items)

        # ---- load (parents before children)
        if customers is not None:
            load.load_table(conn, customers, "customers")
            load.load_table(conn, products, "products")
        load.load_table(conn, orders, "orders")
        load.load_table(conn, items, "order_items")
        log.info("foreign key check: %s", conn.execute("PRAGMA foreign_key_check").fetchall() or "OK")
        log.info("=== ETL finished OK in %.2fs ===", time.time() - t0)
    except validate.DataQualityError as e:
        log.error("PIPELINE STOPPED - data quality failure: %s", e)
        raise SystemExit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
