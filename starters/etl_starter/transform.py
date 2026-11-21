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
    # TODO: drop duplicate order_id; parse order_date to 'YYYY-MM-DD' strings (use parse_mixed_dates(...).dt.strftime)
    # TODO: standardise status (strip, lower, cfg.STATUS_FIX, title) and payment_method (strip, lower, map cfg.PAYMENT_MAP)
    # TODO: reject orphan orders (customer_id not in customers) and log how many
    # TODO: fill missing delivery_city from the customer's home city
    raise NotImplementedError


def clean_items(df: pd.DataFrame, orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    # TODO: drop duplicate order_item_id; keep items of valid orders only
    # TODO: keep 0 < quantity <= cfg.MAX_VALID_QUANTITY and log rejected rows
    # TODO: fill missing unit_price from the product catalogue
    raise NotImplementedError
