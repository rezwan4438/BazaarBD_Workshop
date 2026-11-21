"""Central configuration for the BazaarBD ETL pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
INCOMING_DIR = ROOT / "data" / "incoming"
SCHEMA_FILE = Path(__file__).with_name("schema.sql")
WAREHOUSE_DB = ROOT / "warehouse.db"
LOG_FILE = ROOT / "etl.log"

# Business rules
MAX_VALID_QUANTITY = 50
MAX_DROP_RATIO = 0.05          # abort if more than 5% of rows are rejected in one step

CITY_FIX = {"Dacca": "Dhaka", "Ctg": "Chattogram", "Chittagong": "Chattogram", "Comilla": "Cumilla"}
PAYMENT_MAP = {"bkash": "bKash", "nagad": "Nagad", "card": "Card", "cod": "COD", "cash on delivery": "COD"}
STATUS_FIX = {"canceled": "cancelled"}
