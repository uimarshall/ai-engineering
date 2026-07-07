# AGGREGATING DATA

Aggregating data in SQL means summarising many rows of data into a single (or fewer) result(s).
This is essential for reporting, dashboards, and business intelligence tasks where raw row-level
data needs to be condensed into meaningful metrics.

---

## AGGREGATION FUNCTIONS

Aggregation functions operate on a set of values and return a single computed value.
They are typically used in the `SELECT` clause and can be combined with `GROUP BY` to
break results down by a category.

### Common Aggregation Functions

| Function              | Description                                 |
| --------------------- | ------------------------------------------- |
| `SUM()`               | Adds up all numeric values in a column      |
| `AVG()`               | Calculates the arithmetic mean of a column  |
| `MIN()`               | Returns the smallest value in a column      |
| `MAX()`               | Returns the largest value in a column       |
| `COUNT(*)`            | Counts all rows, including those with NULLs |
| `COUNT(DISTINCT col)` | Counts only unique non-NULL values          |

---

### Example 1 — Inspect a Single Customer's Transactions

Before aggregating, it is good practice to inspect raw row-level data first.
Here we pull all transactions for customer 642 to understand what the data looks like.

**Use case:** A customer service agent wants to review the purchase history of a specific
customer who raised a complaint.

```sql
SELECT * FROM grocery_db.transactions WHERE customer_id = 642;
```

---

### Example 2 — Overall Aggregated Sales Metrics

This query collapses the entire `transactions` table into a single summary row.
It tells us the total revenue, average transaction value, the cheapest and most
expensive sales, the total row count, and the number of distinct transactions.

**Use case:** An executive dashboard needs a high-level snapshot of all-time store
performance — total revenue, average basket size, and transaction volume.

```sql
SELECT
    SUM(sales_cost)                    AS total_sales,
    AVG(sales_cost)                    AS avg_sales,
    MIN(sales_cost)                    AS min_sales,
    MAX(sales_cost)                    AS max_sales,
    COUNT(*)                           AS num_rows,
    COUNT(DISTINCT transaction_id)     AS num_transactions
FROM grocery_db.transactions;
```

> **Note:** `COUNT(*)` counts every row in the result set, whereas
> `COUNT(DISTINCT transaction_id)` counts only unique transaction IDs.
> These will differ if a single transaction spans multiple product lines (rows).

---

## THE GROUP BY STATEMENT

`GROUP BY` splits the data into groups based on one or more columns and then applies
the aggregation function **within each group** rather than across the whole table.

**Rules to remember:**

- Every column in `SELECT` that is **not** inside an aggregation function **must** appear in `GROUP BY`.
- `ORDER BY` can be used alongside `GROUP BY` to sort the grouped results.

---

### Example 3 — Daily Sales Summary

This query breaks down sales, item counts, and transaction volumes **per day**.
The results are sorted chronologically so trends over time are easy to spot.

**Use case:** A store manager wants to review daily trading performance for the last
month to identify the busiest days and plan staffing accordingly.

```sql
SELECT
    transaction_date,
    SUM(sales_cost)                AS total_sales,
    SUM(num_items)                 AS total_items,
    COUNT(DISTINCT transaction_id) AS num_transactions
FROM grocery_db.transactions
GROUP BY transaction_date
ORDER BY transaction_date;
```

---

## GROUPING BY MULTIPLE VARIABLES

You can group by more than one column at a time. SQL will create a unique group for
every combination of values across all the listed columns.

---

### Example 4 — Daily Sales Broken Down by Product Area

Adding `product_area_id` to the grouping gives us a cross-tab view — sales per product
area per day. This is more granular and useful for category-level analysis.

**Use case:** A category manager wants to compare how different product areas (e.g.
Dairy, Bakery, Produce) perform on each day of the week to optimise promotions and
stock replenishment schedules.

```sql
SELECT
    product_area_id,
    transaction_date,
    SUM(sales_cost)                AS total_sales,
    SUM(num_items)                 AS total_items,
    COUNT(DISTINCT transaction_id) AS num_transactions
FROM grocery_db.transactions
GROUP BY product_area_id, transaction_date
ORDER BY product_area_id, transaction_date;
```

---

## THE HAVING CLAUSE

`WHERE` filters **rows before** grouping. `HAVING` filters **groups after** aggregation.
You cannot use an aggregate function (e.g. `SUM`, `COUNT`) inside a `WHERE` clause —
this is exactly the problem that `HAVING` solves.

**Key distinction:**

| Clause   | Runs            | Can use aggregates? |
| -------- | --------------- | ------------------- |
| `WHERE`  | Before GROUP BY | No                  |
| `HAVING` | After GROUP BY  | Yes                 |

---

### Example 5 — High-Revenue Product Areas Only

This query returns only the product areas that have generated more than £200,000 in
total sales, filtering out low-volume categories from the results.

**Use case:** A finance team wants to identify which product areas are the major
revenue drivers so they can focus investment and promotional budgets effectively.

```sql
SELECT
    product_area_id,
    SUM(sales_cost) AS total_sales
FROM grocery_db.transactions
GROUP BY product_area_id
HAVING SUM(sales_cost) > 200000;
```

> **Tip:** You can combine `WHERE` and `HAVING` in the same query. Use `WHERE` to
> pre-filter rows (e.g. a specific date range) before grouping, and `HAVING` to
> filter the resulting groups.

---

### Example 6 — Combining WHERE, GROUP BY, and HAVING

This example shows all three filtering stages working together in a single query.
`WHERE` narrows the rows to a specific date range **before** grouping, and `HAVING`
then drops any product areas that still have fewer than 500 transactions **after**
grouping. This is more efficient than filtering after aggregation alone.

**Use case:** A seasonal trading report needs to show only the high-volume product
areas during the Christmas period (December) to highlight where the store should
increase staffing and stock levels.

```sql
SELECT
    product_area_id,
    COUNT(DISTINCT transaction_id) AS num_transactions,
    SUM(sales_cost)                AS total_sales
FROM grocery_db.transactions
WHERE transaction_date BETWEEN '2021-12-01' AND '2021-12-31'
GROUP BY product_area_id
HAVING COUNT(DISTINCT transaction_id) >= 500
ORDER BY total_sales DESC;
```

---

### Example 7 — Top N Groups with ORDER BY and LIMIT

Sorting aggregated results by a metric descending and then limiting the output
is a classic pattern for finding the best- or worst-performing groups.

**Use case:** A merchandising team wants to quickly identify the top 5 best-selling
product areas to decide where to expand shelf space.

```sql
SELECT
    product_area_id,
    SUM(sales_cost)  AS total_sales,
    SUM(num_items)   AS total_items
FROM grocery_db.transactions
GROUP BY product_area_id
ORDER BY total_sales DESC
LIMIT 5;
```

> **Note:** `LIMIT` is MySQL / PostgreSQL syntax. In SQL Server use `TOP 5` in the
> `SELECT` clause; in Oracle use `FETCH FIRST 5 ROWS ONLY`.

---

### Example 8 — COUNT(\*) vs COUNT(column) — Handling NULLs

`COUNT(*)` counts **every row**, including rows where a column value is `NULL`.
`COUNT(column_name)` counts only the rows where that column is **not NULL**.
The difference matters when a column is sparsely populated.

**Use case:** The data team wants to audit how many transactions are missing a
`loyalty_card_id` (i.e. the customer did not scan their loyalty card) versus the
total number of transactions.

```sql
SELECT
    COUNT(*)                AS total_rows,
    COUNT(loyalty_card_id)  AS rows_with_loyalty_card,
    COUNT(*) - COUNT(loyalty_card_id) AS rows_missing_loyalty_card
FROM grocery_db.transactions;
```

> **Tip:** The difference `COUNT(*) - COUNT(col)` gives you a quick NULL audit for
> any column — useful for data quality checks before analysis.

---

### Example 9 — Derived Metrics and Percentage of Total

Sometimes you need to compute a ratio or percentage within the same query.
A subquery (or CTE) can supply the overall total so each group's share can be
calculated directly in the `SELECT`.

**Use case:** The finance team wants to see each product area's contribution to
overall revenue as a percentage, so they can build a pie-chart for the board report.

```sql
SELECT
    product_area_id,
    SUM(sales_cost)                                      AS area_sales,
    ROUND(
        SUM(sales_cost) * 100.0
        / (SELECT SUM(sales_cost) FROM grocery_db.transactions),
        2
    )                                                    AS pct_of_total_sales
FROM grocery_db.transactions
GROUP BY product_area_id
ORDER BY area_sales DESC;
```

> **Note:** Multiplying by `100.0` (not `100`) forces floating-point division
> in databases that would otherwise perform integer division.

---

## PRACTICE EXERCISE

**Task:** You've been asked to return data that shows, for each transaction date,
the number of **unique customers** that transacted in-store.

To make it easy for stakeholders to review, ensure the output is ordered by
transaction date from earliest to latest.

**Required output columns:**

- `transaction_date` — ordered ascending
- `customer_count` — the number of distinct customers on that date

**Use case:** The marketing team wants to understand footfall patterns across the
calendar — specifically on which dates the most individual customers visited the store.
This helps them time promotional campaigns and loyalty reward pushes.

```sql
SELECT
    transaction_date,
    COUNT(DISTINCT customer_id) AS customer_count
FROM grocery_db.transactions
GROUP BY transaction_date
ORDER BY transaction_date ASC;
```

---

## SUMMARY

| Concept                         | Purpose                                        |
| ------------------------------- | ---------------------------------------------- |
| `SUM / AVG / MIN / MAX / COUNT` | Collapse many rows into a single metric        |
| `GROUP BY`                      | Segment aggregations by one or more categories |
| `HAVING`                        | Filter groups based on an aggregated value     |
| `ORDER BY` (with GROUP BY)      | Sort the grouped results for readability       |
| `COUNT(DISTINCT ...)`           | Count unique values, ignoring duplicates       |
