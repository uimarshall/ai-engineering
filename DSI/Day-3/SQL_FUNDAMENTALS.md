Updated todo list

Read [](file:///c%3A/Users/uimar/code/Githubfiles/ai-engineering/DSI/Day-3/QUERY.md#1-1), lines 1 to 200

Read [](file:///c%3A/Users/uimar/code/Githubfiles/ai-engineering/DSI/Day-3/QUERY.md#201-201), lines 201 to 260

Read [](file:///c%3A/Users/uimar/code/Githubfiles/ai-engineering/DSI/Day-3/QUERY.md#261-261), lines 261 to 315

Here is a comprehensive, beginner-friendly breakdown of every SQL keyword, clause, function, and concept used in this file — with sample tables throughout.

---

## The Sample Tables We'll Use Throughout

```
customers
+-------------+----------+-------------------+---------+
| customer_id | name     | email             | country |
+-------------+----------+-------------------+---------+
| 1           | Alice    | alice@email.com   | UK      |
| 2           | Bob      | bob@email.com     | US      |
| 3           | Carol    | carol@email.com   | UK      |
+-------------+----------+-------------------+---------+

orders
+----------+-------------+------------+-----------+--------------+
| order_id | customer_id | order_date | status    | total_amount |
+----------+-------------+------------+-----------+--------------+
| 101      | 1           | 2024-01-15 | completed | 120.00       |
| 102      | 2           | 2024-01-20 | completed |  85.00       |
| 103      | 1           | 2024-02-05 | cancelled |  50.00       |
| 104      | 3           | 2024-02-10 | completed | 200.00       |
| 105      | 2           | 2024-03-01 | completed |  95.00       |
+----------+-------------+------------+-----------+--------------+

products
+------------+--------------+-------------+-------+-----------+
| product_id | name         | category    | price | stock_qty |
+------------+--------------+-------------+-------+-----------+
| 1          | Laptop       | Electronics | 999   | 5         |
| 2          | T-Shirt      | Clothing    | 25    | 200       |
| 3          | Headphones   | Electronics | 79    | 15        |
| 4          | Coffee Mug   | Kitchen     | 12    | 3         |
+------------+--------------+-------------+-------+-----------+

order_items
+---------------+----------+------------+----------+------------+
| order_item_id | order_id | product_id | quantity | unit_price |
+---------------+----------+------------+----------+------------+
| 1             | 101      | 1          | 1        | 999        |
| 2             | 102      | 2          | 3        | 25         |
| 3             | 104      | 3          | 2        | 79         |
| 4             | 105      | 2          | 1        | 25         |
+---------------+----------+------------+----------+------------+

reviews
+-----------+------------+-------------+--------+
| review_id | product_id | customer_id | rating |
+-----------+------------+-------------+--------+
| 1         | 1          | 1           | 5      |
| 2         | 2          | 2           | 3      |
| 3         | 3          | 3           | 4      |
| 4         | 2          | 3           | 4      |
+-----------+------------+-------------+--------+
```

---

## 1. `SELECT`

**What it does:** Picks which columns (or computed values) you want to see in your results.

```sql
SELECT name, email
FROM customers;
```

**Result:**

```
+-------+-------------------+
| name  | email             |
+-------+-------------------+
| Alice | alice@email.com   |
| Bob   | bob@email.com     |
| Carol | carol@email.com   |
+-------+-------------------+
```

Think of `SELECT` as saying: _"Show me these columns."_

---

## 2. `FROM`

**What it does:** Tells SQL which table to read data from.

```sql
SELECT name
FROM customers;   -- <-- tells SQL to look in the 'customers' table
```

Every query needs a `FROM` unless you are computing something with no table involved (e.g., `SELECT 1 + 1`).

---

## 3. `AS` (Alias)

**What it does:** Renames a column or table in the output. It is purely for readability — it does not change the actual table.

```sql
SELECT name AS customer_name, email AS contact_email
FROM customers;
```

**Result:**

```
+---------------+-------------------+
| customer_name | contact_email     |
+---------------+-------------------+
| Alice         | alice@email.com   |
| Bob           | bob@email.com     |
+---------------+-------------------+
```

You also alias tables (short names) to avoid typing the full table name repeatedly:

```sql
SELECT c.name, o.total_amount
FROM customers c   -- 'c' is the alias for customers
JOIN orders o      -- 'o' is the alias for orders
  ON c.customer_id = o.customer_id;
```

---

## 4. `WHERE`

**What it does:** Filters rows **before** any grouping or aggregation. Only rows that match the condition are kept.

```sql
SELECT order_id, total_amount
FROM orders
WHERE status = 'completed';
```

**Result** (cancelled row 103 is excluded):

```
+----------+--------------+
| order_id | total_amount |
+----------+--------------+
| 101      | 120.00       |
| 102      |  85.00       |
| 104      | 200.00       |
| 105      |  95.00       |
+----------+--------------+
```

Think of `WHERE` as a gate: _"Only let through rows that pass this test."_

Common `WHERE` operators:
| Operator | Meaning |
|----------|---------|
| `=` | Equal to |
| `<>` or `!=` | Not equal |
| `>`, `<`, `>=`, `<=` | Comparisons |
| `AND` | Both conditions must be true |
| `OR` | Either condition must be true |
| `IS NULL` | Value is missing/empty |
| `BETWEEN a AND b` | Value is in a range |
| `IN (a, b, c)` | Value matches one of a list |
| `LIKE '%text%'` | Pattern matching |

---

## 5. `GROUP BY`

**What it does:** Collapses many rows that share the same value in a column into a single summary row. It is always used with **aggregate functions** (SUM, COUNT, AVG, etc.).

```sql
SELECT status, COUNT(order_id) AS order_count
FROM orders
GROUP BY status;
```

**Before GROUP BY** (all 5 rows):

```
completed, completed, cancelled, completed, completed
```

**After GROUP BY status** (collapsed into 2 groups):

```
+-----------+-------------+
| status    | order_count |
+-----------+-------------+
| completed | 4           |
| cancelled | 1           |
+-----------+-------------+
```

Think of `GROUP BY` as sorting people into buckets by a label, then counting (or summing) what's in each bucket.

**Important rule:** Every column in `SELECT` must either be:

- The column you are grouping by, **OR**
- Inside an aggregate function like `SUM()`, `COUNT()`, etc.

---

## 6. `ORDER BY`

**What it does:** Sorts the result rows. Default is ascending (`ASC`). Use `DESC` for largest-first (descending).

```sql
SELECT name, total_amount
FROM orders
ORDER BY total_amount DESC;   -- most expensive first
```

**Result:**

```
+----------+--------------+
| order_id | total_amount |
+----------+--------------+
| 104      | 200.00       |
| 101      | 120.00       |
| 105      |  95.00       |
| 102      |  85.00       |
| 103      |  50.00       |
+----------+--------------+
```

You can sort by multiple columns: `ORDER BY country ASC, total_amount DESC`.

---

## 7. `LIMIT`

**What it does:** Caps how many rows come back. Useful when you only want the "top N" results.

```sql
SELECT name, total_amount
FROM orders
ORDER BY total_amount DESC
LIMIT 2;   -- only the top 2 rows
```

**Result:**

```
+----------+--------------+
| order_id | total_amount |
+----------+--------------+
| 104      | 200.00       |
| 101      | 120.00       |
+----------+--------------+
```

---

## 8. `JOIN` (INNER JOIN)

**What it does:** Combines rows from two tables where a matching value exists in both. Rows that do not match are excluded from the result.

```sql
SELECT c.name, o.order_id, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

SQL looks at every row in `customers`, finds matching rows in `orders` (where `customer_id` matches), and stitches them together.

**Result:**

```
+-------+----------+--------------+
| name  | order_id | total_amount |
+-------+----------+--------------+
| Alice | 101      | 120.00       |
| Bob   | 102      |  85.00       |
| Alice | 103      |  50.00       |
| Carol | 104      | 200.00       |
| Bob   | 105      |  95.00       |
+-------+----------+--------------+
```

`ON c.customer_id = o.customer_id` is the **join condition** — it tells SQL how the two tables relate to each other.

---

## 9. `LEFT JOIN`

**What it does:** Like `JOIN`, but keeps **all rows from the left table** even if there is no match in the right table. The right-table columns will be `NULL` for unmatched rows.

This file uses it in Query 12 to find products that have **never been ordered**:

```sql
SELECT p.name, oi.order_item_id
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id;
```

**Result:**

```
+------------+---------------+
| name       | order_item_id |
+------------+---------------+
| Laptop     | 1             |
| T-Shirt    | 2             |
| Headphones | 3             |
| Coffee Mug | NULL          |  <-- never ordered!
+------------+---------------+
```

Adding `WHERE oi.product_id IS NULL` then isolates only the unmatched products (Coffee Mug).

---

## 10. `HAVING`

**What it does:** Filters **after** grouping — it is like `WHERE` but for groups. You must use `HAVING` (not `WHERE`) when filtering on the result of an aggregate function.

```sql
-- Find customers whose last order was more than 90 days ago
SELECT customer_id, MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id
HAVING DATEDIFF(CURRENT_DATE, MAX(order_date)) > 90;
```

**Rule of thumb:**

- `WHERE` filters individual rows → runs **before** `GROUP BY`
- `HAVING` filters groups → runs **after** `GROUP BY`

```
Execution order:
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

---

## 11. `CASE WHEN ... THEN ... ELSE ... END`

**What it does:** Conditional logic inside SQL — it is SQL's version of `if / else if / else`. It returns a value based on which condition is true first.

```sql
SELECT
    customer_id,
    order_count,
    CASE
        WHEN order_count = 1 THEN 'One-Time Buyer'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Occasional Buyer'
        ELSE 'Loyal Customer'
    END AS customer_segment
FROM (some subquery);
```

**Example:**

```
order_count = 1   → 'One-Time Buyer'
order_count = 3   → 'Occasional Buyer'
order_count = 10  → 'Loyal Customer'
```

---

## 12. Subquery (Query Inside a Query)

**What it does:** A full SQL query nested inside another query. The inner query runs first and its result is treated as a temporary table.

```sql
SELECT customer_segment, COUNT(*) AS customer_count
FROM (
    -- inner subquery runs first:
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
) AS order_summary   -- give the temporary table a name with AS
GROUP BY customer_segment;
```

Think of it as building a small temporary table, then running another query on top of it.

---

## 13. Aggregate Functions

These functions collapse multiple rows into a single number.

### `COUNT()`

Counts the number of rows.

```sql
SELECT COUNT(order_id) AS total_orders FROM orders;
-- Result: 5
```

### `COUNT(DISTINCT ...)`

Counts only unique values (duplicates are ignored).

```sql
SELECT COUNT(DISTINCT customer_id) AS unique_customers FROM orders;
-- Result: 3  (Alice, Bob, Carol — even though Alice/Bob appear twice)
```

### `SUM()`

Adds up all values in a column.

```sql
SELECT SUM(total_amount) AS total_revenue FROM orders WHERE status = 'completed';
-- Result: 120 + 85 + 200 + 95 = 500
```

### `AVG()`

Calculates the average.

```sql
SELECT AVG(total_amount) AS avg_order FROM orders WHERE status = 'completed';
-- Result: 500 / 4 = 125.00
```

### `MAX()`

Returns the largest value.

```sql
SELECT MAX(order_date) AS last_order FROM orders;
-- Result: 2024-03-01
```

### `MIN()`

Returns the smallest value (not in the file but worth knowing).

```sql
SELECT MIN(price) AS cheapest FROM products;
-- Result: 12
```

---

## 14. `ROUND()`

**What it does:** Rounds a number to a given number of decimal places.

```sql
SELECT ROUND(AVG(rating), 2) AS avg_rating FROM reviews;
-- AVG might be 4.0000... → ROUND gives 4.00
```

```
ROUND(4.5678, 2) → 4.57
ROUND(4.5678, 0) → 5
```

---

## 15. Date & Time Functions

### `DATE_FORMAT(date, format)`

Formats a date into a string pattern.

```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month FROM orders;
-- 2024-01-15 → '2024-01'
-- 2024-02-05 → '2024-02'
```

Common format codes:

| Code | Meaning               |
| ---- | --------------------- |
| `%Y` | 4-digit year (2024)   |
| `%m` | 2-digit month (01–12) |
| `%d` | 2-digit day (01–31)   |

---

### `DATE(datetime)`

Strips the time part from a datetime, leaving just the date.

```sql
SELECT DATE('2024-01-15 14:32:00');
-- Result: 2024-01-15
```

---

### `DATEDIFF(date1, date2)`

Returns the number of days between two dates.

```sql
SELECT DATEDIFF('2024-04-15', '2024-01-15');
-- Result: 91  (91 days apart)
```

---

### `CURRENT_DATE`

Returns today's date (no time component).

```sql
SELECT CURRENT_DATE;
-- Result: 2026-07-16  (today)
```

---

### `HOUR(datetime)`

Extracts just the hour (0–23) from a datetime value.

```sql
SELECT HOUR('2024-01-15 14:32:00');
-- Result: 14  (2 PM)
```

Useful for finding peak shopping hours:

```sql
SELECT HOUR(order_date) AS hour_of_day, COUNT(*) AS orders
FROM orders
GROUP BY hour_of_day;
```

---

## 16. Window Functions with `OVER()`

**What it does:** Performs a calculation **across all rows** of the result set without collapsing them into a single row (unlike `GROUP BY`). The `OVER()` clause defines the "window" of rows to calculate over.

This file uses it for percentage of revenue per category:

```sql
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue,
    ROUND(
        SUM(oi.quantity * oi.unit_price) * 100.0
        / SUM(SUM(oi.quantity * oi.unit_price)) OVER ()  -- grand total of all categories
        , 2
    ) AS revenue_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category;
```

Without `OVER()`, the inner `SUM()` would only know about one category at a time. `OVER()` with nothing inside it means _"look at all rows"_, so SQL can compute what percentage each category is of the total.

**Simplified example:**

```
category_revenue per category = 800, 150, 50
total = 1000

Electronics: 800/1000 * 100 = 80.00%
Clothing:    150/1000 * 100 = 15.00%
Kitchen:      50/1000 * 100 =  5.00%
```

Other common window functions (good to know):
| Function | What it does |
|----------|-------------|
| `ROW_NUMBER() OVER(ORDER BY ...)` | Assign a row number 1, 2, 3... |
| `RANK() OVER(ORDER BY ...)` | Rank with gaps on ties |
| `SUM(col) OVER(ORDER BY ...)` | Running total |
| `LAG(col) OVER(ORDER BY ...)` | Get the previous row's value |

---

## 17. Arithmetic Expressions

SQL can do maths directly inside `SELECT`:

```sql
SELECT quantity * unit_price AS line_total
FROM order_items;
-- 1 * 999 = 999
-- 3 *  25 = 75
```

Also used for percentages:

```sql
SUM(oi.quantity * oi.unit_price) * 100.0 / grand_total
```

The `100.0` (with a decimal) forces decimal division instead of integer division.

---

## Complete Execution Order

This is the order SQL actually runs the clauses (not the order you write them):

```
1. FROM          → which table(s) to read
2. JOIN          → merge tables
3. WHERE         → filter individual rows
4. GROUP BY      → collapse rows into groups
5. HAVING        → filter groups
6. SELECT        → compute what to display
7. ORDER BY      → sort results
8. LIMIT         → take only the first N rows
```

This matters because it explains why you **cannot** use a `SELECT` alias in a `WHERE` clause (WHERE runs before SELECT computes the alias), but you **can** use it in `ORDER BY` (ORDER BY runs after SELECT).

---

## Quick Cheat Sheet

| Keyword / Function | Purpose                                     |
| ------------------ | ------------------------------------------- |
| `SELECT`           | Choose columns to display                   |
| `FROM`             | Source table                                |
| `AS`               | Rename a column or table                    |
| `WHERE`            | Filter rows (before grouping)               |
| `GROUP BY`         | Summarise rows into groups                  |
| `HAVING`           | Filter groups (after grouping)              |
| `ORDER BY`         | Sort output (ASC / DESC)                    |
| `LIMIT`            | Return only N rows                          |
| `JOIN`             | Combine tables (matching rows only)         |
| `LEFT JOIN`        | Combine tables (keep all left rows)         |
| `CASE WHEN`        | If/else logic                               |
| Subquery           | Nested query used as a temporary table      |
| `COUNT()`          | Number of rows                              |
| `COUNT(DISTINCT)`  | Number of unique values                     |
| `SUM()`            | Total of a column                           |
| `AVG()`            | Average of a column                         |
| `MAX()`            | Largest value                               |
| `MIN()`            | Smallest value                              |
| `ROUND()`          | Round to N decimal places                   |
| `DATE_FORMAT()`    | Format a date as a string                   |
| `DATE()`           | Extract date (strip time)                   |
| `DATEDIFF()`       | Days between two dates                      |
| `CURRENT_DATE`     | Today's date                                |
| `HOUR()`           | Extract hour from a datetime                |
| `OVER()`           | Window function — calculate across all rows |
