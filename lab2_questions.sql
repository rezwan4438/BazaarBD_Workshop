-- Lab 2: write one query under each question. Revenue = quantity * unit_price on Delivered orders.

-- Q1  The 10 most recent orders (order_id, customer_id, order_date, status)
SELECT order_id, customer_id, order_date, status
FROM orders
ORDER BY order_date DESC
LIMIT 10;

-- Q2  Customers living in Sylhet, alphabetically

-- Q3  Number of orders per status, most common first

-- Q4  Total revenue from delivered orders

-- Q5  Revenue by product category, highest first

-- Q6  Top 5 products by units sold (delivered orders)

-- Q7  Customers who have never placed an order

-- Q8  Average order value by payment method (delivered orders)

-- Q9  Number of orders per month in 2026

-- Q10 Delivery cities with more than 200 orders

-- Q11 Products priced above the average price of their own category

-- Q12 Customers with 10 or more orders
