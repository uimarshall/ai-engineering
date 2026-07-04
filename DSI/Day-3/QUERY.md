# SELECT Statement — E-Commerce Data Analysis

Real-world use cases for analysing e-commerce data using SQL SELECT statements.

---

## Schema Reference (assumed tables)

```
customers(customer_id, name, email, country, signup_date)
products(product_id, name, category, price, stock_qty)
orders(order_id, customer_id, order_date, status, total_amount)
order_items(order_item_id, order_id, product_id, quantity, unit_price)
reviews(review_id, product_id, customer_id, rating, review_date)
```

---

## 1. Total Revenue by Month

Track monthly revenue trends to spot seasonal peaks.

```sql
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(total_amount)               AS total_revenue,
    COUNT(order_id)                 AS total_orders
FROM orders
WHERE status = 'completed'
GROUP BY month
ORDER BY month;
```

---

## 2. Top 10 Best-Selling Products

Identify which products drive the most sales volume.

```sql
SELECT
    p.product_id,
    p.name                      AS product_name,
    p.category,
    SUM(oi.quantity)            AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY units_sold DESC
LIMIT 10;
```

---

## 3. Customer Lifetime Value (CLV)

Find the highest-spending customers to target for loyalty programmes.

```sql
SELECT
    c.customer_id,
    c.name,
    c.email,
    COUNT(DISTINCT o.order_id)  AS total_orders,
    SUM(o.total_amount)         AS lifetime_value,
    AVG(o.total_amount)         AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name, c.email
ORDER BY lifetime_value DESC
LIMIT 20;
```

---

## 4. Products with Low Stock (Inventory Alert)

Flag items that need restocking before they run out.

```sql
SELECT
    product_id,
    name        AS product_name,
    category,
    stock_qty,
    price
FROM products
WHERE stock_qty < 20
ORDER BY stock_qty ASC;
```

---

## 5. Orders by Status Breakdown

Get a snapshot of the order pipeline (pending, shipped, completed, cancelled).

```sql
SELECT
    status,
    COUNT(order_id)     AS order_count,
    SUM(total_amount)   AS total_value
FROM orders
GROUP BY status
ORDER BY order_count DESC;
```

---

## 6. Average Product Rating per Category

Understand which product categories customers rate highest.

```sql
SELECT
    p.category,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.review_id)      AS review_count
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.category
ORDER BY avg_rating DESC;
```

---

## 7. Customers Who Have Not Ordered in 90 Days (Churn Risk)

Identify inactive customers for re-engagement campaigns.

```sql
SELECT
    c.customer_id,
    c.name,
    c.email,
    MAX(o.order_date) AS last_order_date,
    DATEDIFF(CURRENT_DATE, MAX(o.order_date)) AS days_since_last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email
HAVING days_since_last_order > 90
ORDER BY days_since_last_order DESC;
```

---

## 8. Revenue by Product Category

Determine which categories generate the most revenue.

```sql
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue,
    ROUND(
        SUM(oi.quantity * oi.unit_price) * 100.0 /
        SUM(SUM(oi.quantity * oi.unit_price)) OVER (), 2
    ) AS revenue_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o   ON oi.order_id   = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY category_revenue DESC;
```

---

## 9. Repeat vs. One-Time Customers

Measure customer retention — how many buyers return?

```sql
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-Time Buyer'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Occasional Buyer'
        ELSE 'Loyal Customer'
    END AS customer_segment,
    COUNT(*) AS customer_count
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
) AS order_summary
GROUP BY customer_segment
ORDER BY customer_count DESC;
```

---

## 10. Daily New Customer Sign-Ups

Monitor acquisition rates to evaluate marketing campaign effectiveness.

```sql
SELECT
    DATE(signup_date)   AS signup_day,
    COUNT(customer_id)  AS new_customers
FROM customers
GROUP BY signup_day
ORDER BY signup_day DESC
LIMIT 30;
```

---

## 11. Cancelled Orders — Loss Analysis

Quantify revenue lost to cancellations by month.

```sql
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(order_id)                  AS cancelled_orders,
    SUM(total_amount)                AS lost_revenue
FROM orders
WHERE status = 'cancelled'
GROUP BY month
ORDER BY month;
```

---

## 12. Products Never Ordered (Dead Stock)

Find products sitting in the catalogue with zero sales.

```sql
SELECT
    p.product_id,
    p.name      AS product_name,
    p.category,
    p.price,
    p.stock_qty
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.product_id IS NULL
ORDER BY p.stock_qty DESC;
```

---

## 13. Average Order Value (AOV) by Country

Compare purchasing power across different markets.

```sql
SELECT
    c.country,
    COUNT(DISTINCT o.order_id)  AS total_orders,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value,
    SUM(o.total_amount)           AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.country
ORDER BY total_revenue DESC;
```

---

## 14. Hourly Order Distribution

Find peak shopping hours to optimise server capacity and ad scheduling.

```sql
SELECT
    HOUR(order_date)    AS hour_of_day,
    COUNT(order_id)     AS order_count
FROM orders
GROUP BY hour_of_day
ORDER BY hour_of_day;
```

---

## 15. Customers Who Ordered a Specific Product

Useful for targeted promotions (e.g., accessories for a product).

```sql
SELECT
    c.customer_id,
    c.name,
    c.email,
    o.order_date
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
WHERE oi.product_id = 42          -- replace with target product_id
  AND o.status      = 'completed'
ORDER BY o.order_date DESC;
```

---

## Key Clauses Summary

| Clause        | Purpose                               |
| ------------- | ------------------------------------- |
| `WHERE`       | Filter rows before aggregation        |
| `GROUP BY`    | Aggregate data into buckets           |
| `HAVING`      | Filter groups after aggregation       |
| `ORDER BY`    | Sort results                          |
| `LIMIT`       | Cap the number of rows returned       |
| `JOIN`        | Combine data from multiple tables     |
| `CASE WHEN`   | Conditional logic inside a query      |
| Window `OVER` | Running totals, percentages, rankings |
