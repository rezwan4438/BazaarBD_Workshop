# %% 1. Import Libraries and connect to bazaarbd.db
import sqlite3, pandas as pd
conn = sqlite3.connect("bazaarbd.db")      # Lab 2: "bazaarbd.db"

# %% 2  Run a query and return a DataFrame
def run_query(sql, params=()):
    return pd.read_sql_query(sql, conn, params=params)

run_query("SELECT customer_id, full_name, email FROM customers WHERE city = 'Dhaka'")
# %%
statement = """ SELECT customer_id, full_name, email 
            FROM customers 
            WHERE city = 'Dhaka' """

run_query(statement)

# %%
statement = """ SELECT customer_id, full_name, email, phone
            FROM customers 
            WHERE city = 'Dhaka' AND phone LIKE '017%' """

run_query(statement)



# %%
statement = """ SELECT COUNT(*) AS n_customers
FROM customers""" 

run_query(statement)

# %%
statement = """ SELECT COUNT(*) AS n_products
FROM products
WHERE category = 'Electronics' """

run_query(statement)
# %%

statement = """ SELECT category, COUNT(*) AS n_products
FROM products
GROUP BY category
HAVING COUNT(*) >= 15
ORDER BY n_products DESC 
LIMIT 5"""
run_query(statement)

# %% Find average, minimum, and maximum price for each category
statement = """ SELECT category, AVG(unit_price) AS avg_price, MIN(unit_price) AS min_price, MAX(unit_price) AS max_price
FROM products
GROUP BY category """

run_query(statement)


# %%
statement = """ SELECT category, AVG(unit_price) AS avg_price, MIN(unit_price) AS min_price, MAX(unit_price) AS max_price
FROM products
GROUP BY category 
HAVING AVG(unit_price) > 1000 """

run_query(statement)

# %%
statement = """ SELECT *
FROM products
ORDER BY unit_price 
LIMIT 5 """
run_query(statement)
# %%

statement = """ SELECT order_id, full_name
FROM customers c JOIN orders o ON c.customer_id = o.customer_id"""

run_query(statement)

# %%
statement = """ SELECT c.customer_id, c.full_name
FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL"""

run_query(statement)

# %%

statement = """ SELECT c.customer_id, c.full_name
FROM orders o RIGHT JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL"""

run_query(statement)

# %% 
statement = """
SELECT full_name, city
FROM customers c JOIN orders o ON c.customer_id = o.customer_id
WHERE payment_method = 'bKash'
"""
run_query(statement)

# %%
