-- BazaarBD reference schema (SQLite) -- Lab 2 solution
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id  TEXT PRIMARY KEY,
    full_name    TEXT NOT NULL,
    email        TEXT UNIQUE,                 -- NULLs allowed (several are missing)
    phone        TEXT,
    city         TEXT,
    signup_date  TEXT NOT NULL                -- ISO date: YYYY-MM-DD
);

CREATE TABLE products (
    product_id   TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    brand        TEXT NOT NULL DEFAULT 'Unknown',
    unit_price   REAL NOT NULL CHECK (unit_price > 0),
    stock_qty    INTEGER NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
);

CREATE TABLE orders (
    order_id       TEXT PRIMARY KEY,
    customer_id    TEXT NOT NULL,
    order_date     TEXT NOT NULL,
    status         TEXT NOT NULL CHECK (status IN
                   ('Delivered','Shipped','Processing','Cancelled','Returned')),
    payment_method TEXT NOT NULL CHECK (payment_method IN ('bKash','Nagad','COD','Card')),
    delivery_city  TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      TEXT NOT NULL,
    product_id    TEXT NOT NULL,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL NOT NULL CHECK (unit_price > 0),
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date     ON orders(order_date);
CREATE INDEX idx_items_order     ON order_items(order_id);
CREATE INDEX idx_items_product   ON order_items(product_id);
