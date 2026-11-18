# Lab 1 starter: Taming a messy dataset
# Run each "# %%" cell with Shift+Enter (VS Code Interactive Window) or run the whole file.
# %% 0. Setup
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
CLEAN = Path("data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)
pd.set_option("display.width", 140)

# %% 1. Load and inspect the customers file
customers = pd.read_csv(RAW / "customers_raw.csv", dtype={"phone": str})
print(customers.shape)
# TODO: use .head(), .info(), .describe(include="all"), .isna().sum()

# %% 2. Duplicates
# TODO: how many fully duplicated rows? how many duplicated customer_id?
# TODO: drop duplicates by customer_id

# %% 3. Text cleaning: names, email, city
# TODO: strip + title-case full_name; lower-case email
# TODO: strip + title-case city, then map Dacca->Dhaka, Chittagong->Chattogram, Comilla->Cumilla

# %% 4. Phone numbers (target: 11 digits starting with 01)
# TODO: keep digits only (str.replace(r"\D", "", regex=True)), then keep the last 11 characters

# %% 5. Dates (two formats: 2025-03-14 and 14/03/2025)
# TODO: write parse_mixed_dates(series) using two pd.to_datetime(..., format=..., errors="coerce") + fillna

# %% 6. Products: price strings, categories, missing values
products = pd.read_csv(RAW / "products_raw.csv")
# TODO: remove "৳", "Tk." and "," from unit_price, convert with pd.to_numeric
# TODO: standardise category; fill brand with "Unknown"; fill stock_qty with 0 and make it int

# %% 7. Orders: status, payment, dates, orphans, missing city
orders = pd.read_csv(RAW / "orders_raw.csv")
# TODO: drop duplicate order_id; parse dates; standardise status (canceled -> Cancelled) and payment_method
# TODO: drop orders whose customer_id is not in customers (isin)
# TODO: fill missing delivery_city from the customer's city (map)

# %% 8. Order items: invalid quantities and missing prices
items = pd.read_csv(RAW / "order_items_raw.csv")
# TODO: keep only rows with 0 < quantity <= 50 and order_id in cleaned orders
# TODO: fill missing unit_price from the product catalogue

# %% 9. Analysis: merge + groupby
# TODO: merge items + orders + products; revenue = quantity * unit_price
# TODO: revenue by category (exclude Cancelled / Returned); orders per city

# %% 10. Save
# TODO: write customers_clean.csv, products_clean.csv, orders_clean.csv, order_items_clean.csv to CLEAN (index=False)
