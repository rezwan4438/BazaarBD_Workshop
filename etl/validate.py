"""VALIDATE: data-quality gates that run BEFORE loading."""
import logging

import pandas as pd

from . import config as cfg

log = logging.getLogger(__name__)


class DataQualityError(Exception):
    """Raised when a critical data-quality rule fails: the pipeline must stop."""


def check_unique(df: pd.DataFrame, col: str, name: str) -> None:
    n = int(df[col].duplicated().sum())
    if n:
        raise DataQualityError(f"{name}: {n} duplicate values in {col}")


def check_not_null(df: pd.DataFrame, cols: list, name: str) -> None:
    for c in cols:
        n = int(df[c].isna().sum())
        if n:
            raise DataQualityError(f"{name}: {n} NULLs in required column {c}")


def check_allowed(df: pd.DataFrame, col: str, allowed: set, name: str) -> None:
    bad = set(df[col].dropna().unique()) - allowed
    if bad:
        raise DataQualityError(f"{name}: unexpected values in {col}: {sorted(bad)}")


def check_drop_ratio(before: int, after: int, name: str) -> None:
    ratio = 1 - after / before if before else 0
    log.info("%s: kept %d of %d rows (%.1f%% rejected)", name, after, before, 100 * ratio)
    if ratio > cfg.MAX_DROP_RATIO:
        raise DataQualityError(f"{name}: {ratio:.1%} of rows rejected (limit {cfg.MAX_DROP_RATIO:.0%})")


def validate_orders(df: pd.DataFrame) -> None:
    check_unique(df, "order_id", "orders")
    check_not_null(df, ["order_id", "customer_id", "order_date", "status", "payment_method"], "orders")
    check_allowed(df, "status", {"Delivered", "Shipped", "Processing", "Cancelled", "Returned"}, "orders")
    check_allowed(df, "payment_method", {"bKash", "Nagad", "COD", "Card"}, "orders")


def validate_items(df: pd.DataFrame) -> None:
    check_unique(df, "order_item_id", "order_items")
    check_not_null(df, ["order_id", "product_id", "quantity", "unit_price"], "order_items")
