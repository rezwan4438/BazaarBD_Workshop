"""TRANSFORM: pure functions. DataFrame in -> DataFrame out. No file or database access."""
import logging

import pandas as pd

from . import config as cfg

log = logging.getLogger(__name__)


def parse_mixed_dates(s: pd.Series) -> pd.Series:
    iso = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
    return iso.fillna(dmy)


def clean_city(s: pd.Series) -> pd.Series:
    return s.str.strip().str.title().replace(cfg.CITY_FIX)


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset="customer_id").copy()
    df["full_name"] = df["full_name"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()
    df["phone"] = df["phone"].str.replace(r"\D", "", regex=True).str[-11:]
    df["city"] = clean_city(df["city"])
    df["signup_date"] = parse_mixed_dates(df["signup_date"]).dt.strftime("%Y-%m-%d")
    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    price = (df["unit_price"].astype(str).str.replace("৳", "", regex=False)
             .str.replace("Tk.", "", regex=False).str.replace(",", "", regex=False).str.strip())
    df["unit_price"] = pd.to_numeric(price, errors="coerce")
    df["category"] = df["category"].str.strip().str.title()
    df["brand"] = df["brand"].fillna("Unknown")
    df["stock_qty"] = df["stock_qty"].fillna(0).astype(int)
    return df


def clean_orders(df: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """`customers` must already be clean (used for orphan check and city fill)."""
    df = df.drop_duplicates(subset="order_id").copy()
    df["order_date"] = parse_mixed_dates(df["order_date"]).dt.strftime("%Y-%m-%d")
    df["status"] = df["status"].str.strip().str.lower().replace(cfg.STATUS_FIX).str.title()
    df["payment_method"] = df["payment_method"].str.strip().str.lower().map(cfg.PAYMENT_MAP)
    known = df["customer_id"].isin(customers["customer_id"])
    log.info("orders: %d orphan rows rejected", int((~known).sum()))
    df = df[known].copy()
    home = customers.set_index("customer_id")["city"]
    df["delivery_city"] = clean_city(df["delivery_city"]).fillna(df["customer_id"].map(home))
    return df


def clean_items(df: pd.DataFrame, orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset="order_item_id")
    df = df[df["order_id"].isin(orders["order_id"])]
    ok = (df["quantity"] > 0) & (df["quantity"] <= cfg.MAX_VALID_QUANTITY)
    log.info("order_items: %d rows with invalid quantity rejected", int((~ok).sum()))
    df = df[ok].copy()
    df["unit_price"] = df["unit_price"].fillna(df["product_id"].map(products.set_index("product_id")["unit_price"]))
    return df
