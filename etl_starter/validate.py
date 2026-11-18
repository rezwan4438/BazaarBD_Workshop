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
    # TODO: raise DataQualityError if df[col] contains values outside `allowed`
    raise NotImplementedError


def check_drop_ratio(before: int, after: int, name: str) -> None:
    # TODO: log kept/rejected counts; raise DataQualityError if more than cfg.MAX_DROP_RATIO was rejected
    raise NotImplementedError


def validate_orders(df: pd.DataFrame) -> None:
    check_unique(df, "order_id", "orders")
    # TODO: required columns not null; status in the 5 allowed values; payment_method in the 4 allowed values


def validate_items(df: pd.DataFrame) -> None:
    check_unique(df, "order_item_id", "order_items")
    check_not_null(df, ["order_id", "product_id", "quantity", "unit_price"], "order_items")
