-- BazaarBD schema (SQLite). Complete the TODOs, then run:  python lab2_build_db.py schema.sql
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

-- Worked example
CREATE TABLE customers (
    customer_id  TEXT PRIMARY KEY,
    full_name    TEXT NOT NULL,
    email        TEXT UNIQUE,
    phone        TEXT,
    city         TEXT,
    signup_date  TEXT NOT NULL
);

-- TODO: products (product_id PK, product_name, category, brand DEFAULT 'Unknown',
--        unit_price > 0, stock_qty >= 0)

-- TODO: orders (order_id PK, customer_id FK -> customers, order_date, status in
--        ('Delivered','Shipped','Processing','Cancelled','Returned'),
--        payment_method in ('bKash','Nagad','COD','Card'), delivery_city)

-- TODO: order_items (order_item_id INTEGER PK, order_id FK, product_id FK, quantity > 0, unit_price > 0)

-- TODO: indexes on orders(customer_id), orders(order_date), order_items(order_id), order_items(product_id)
