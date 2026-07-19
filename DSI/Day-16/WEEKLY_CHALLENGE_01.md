# Weekly SQL Challenge 01

## Data: grocery_db schema data tables

Task: Identify customers who have a credit score over 0.5 and who spent more than $100 in September 2020.

Expected Output: Return data with 3 columns:

customer_id
credit_score
total_sales (the customer's spend in September 2020)

**Database:** `grocery_db` schema

---

## Business Context

You work as a data analyst for a mid-sized grocery chain that wants to stay ahead of its competitors. The marketing and finance teams need to identify their most valuable, financially reliable customers so they can:

- Target high-value customers with exclusive loyalty rewards **before a rival chain does**, reducing churn
- Prioritise promotional spend on customers most likely to convert, protecting profit margins
- Build a credit-risk-aware customer segment for a new **Buy Now, Pay Later (BNPL)** scheme, driving incremental revenue

---

## Task

Identify customers who have a **credit score above 0.5** AND who **spent more than $100** during September 2020 — a month that included a major promotional event.

### Why This Matters

Combining credit score with actual spend behaviour gives the business a two-dimensional view of a customer:

| Dimension     | What it tells us                       |
| ------------- | -------------------------------------- |
| Credit score  | Financial reliability and risk profile |
| Monthly spend | Actual value to the business right now |

Customers who score well on **both** dimensions are prime candidates for premium loyalty tiers, personalised offers, and higher credit limits — all of which drive repeat business and increase **customer lifetime value (CLV)**.

---

## Expected Output

| Column         | Description                                           |
| -------------- | ----------------------------------------------------- |
| `customer_id`  | Unique identifier for the customer                    |
| `credit_score` | Credit reliability score (0–1 scale, higher = better) |
| `total_sales`  | Total amount the customer spent in September 2020     |

---

## Step 1 — Inspect the Raw Tables

> **Always do this before writing your main query.**
> It lets you confirm column names, data types, and see a sample of the data. This prevents typos and wrong assumptions in the final query.

```sql
-- Returns every column and every row from the customer_details table.
-- Look for: customer_id, credit_score, name, address, and any other profile columns.
SELECT * FROM grocery_db.customer_details;

-- Returns every column and every row from the transactions table.
-- Look for: transaction_id, customer_id, transaction_date, sales_cost.
SELECT * FROM grocery_db.transactions;
```

---

## Step 2 — The Main Analytical Query

```sql
SELECT
    a.customer_id,    -- The unique ID that identifies each customer
    a.credit_score,   -- Their financial reliability score (0 to 1)
    SUM(b.sales_cost) AS total_spend  -- Total money spent in the filtered period
FROM
    grocery_db.customer_details a
    INNER JOIN grocery_db.transactions b ON a.customer_id = b.customer_id
WHERE
    a.credit_score > 0.5
    AND b.transaction_date BETWEEN '2020-09-01' AND '2020-09-30'
GROUP BY
    a.customer_id,
    a.credit_score
HAVING
    SUM(b.sales_cost) > 100;
```

---

## Line-by-Line Explanation

### SELECT — Choosing the Output Columns

```sql
SELECT
    a.customer_id,
    a.credit_score,
    SUM(b.sales_cost) AS total_spend
```

| Line                               | What it does                                                                                                                                                                                      |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `a.customer_id`                    | Pulls the unique customer ID from the `customer_details` table. The `a.` prefix tells SQL which table to read from (using the alias defined in `FROM`).                                           |
| `a.credit_score`                   | Returns the customer's credit score. Including it in `SELECT` lets analysts rank or segment the results without needing a second query.                                                           |
| `SUM(b.sales_cost) AS total_spend` | `SUM()` is an **aggregate function** — it adds up every `sales_cost` value for each customer group. `AS total_spend` gives the result a readable column name instead of showing the raw function. |

---

### FROM and INNER JOIN — Combining the Two Tables

```sql
FROM
    grocery_db.customer_details a
    INNER JOIN grocery_db.transactions b ON a.customer_id = b.customer_id
```

| Concept                            | Explanation                                                                                                                                                                                           |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grocery_db.customer_details a`    | The primary table. `a` is a **table alias** — a short nickname so you do not repeat the full table name on every column reference.                                                                    |
| `INNER JOIN`                       | Returns only rows that have a matching record in **both** tables (like the overlap of a Venn diagram). Customers with no transactions and orphaned transaction records are both excluded.             |
| `ON a.customer_id = b.customer_id` | The **join condition** — the rule that links the two tables. Without it, the database would pair every customer with every transaction, producing millions of meaningless rows (a cartesian product). |

---

### WHERE — Filtering Individual Rows

```sql
WHERE
    a.credit_score > 0.5
    AND b.transaction_date BETWEEN '2020-09-01' AND '2020-09-30'
```

> `WHERE` runs **before** any grouping or aggregation. Both conditions must be `TRUE` for a row to pass through (`AND` logic).

| Filter                                  | What it removes                     | Business rationale                                                                                                                                                                         |
| --------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `a.credit_score > 0.5`                  | Customers at 0.5 or below           | Extending premium offers to financially unreliable customers increases bad debt risk. Removing them early also makes the query faster. Use `>=` if you want to include the boundary value. |
| `BETWEEN '2020-09-01' AND '2020-09-30'` | Transactions outside September 2020 | Restricting to one month enables like-for-like performance comparison, isolates the September promotion's impact, and pinpoints which high-credit customers responded to it.               |

---

### GROUP BY — Collapsing Rows into Summaries

```sql
GROUP BY
    a.customer_id,
    a.credit_score
```

`GROUP BY` collapses all the individual transaction rows that belong to the same customer into **one summary row**. This is what makes `SUM()` meaningful — without it, `SUM()` would add up every transaction across every customer and return a single grand total.

> **Rule:** every column in `SELECT` that is **not** inside an aggregate function (`SUM`, `COUNT`, `AVG`, etc.) **must** appear in `GROUP BY`. Both `customer_id` and `credit_score` are plain columns, so both must be listed.

---

### HAVING — Filtering the Aggregated Results

```sql
HAVING
    SUM(b.sales_cost) > 100
```

| Keyword  | Runs              | Filters                      |
| -------- | ----------------- | ---------------------------- |
| `WHERE`  | Before `GROUP BY` | Individual rows              |
| `HAVING` | After `GROUP BY`  | Grouped / aggregated results |

You **cannot** use `WHERE` to filter on `SUM()` because `SUM()` does not exist at the `WHERE` stage — that is exactly why `HAVING` exists.

**Business insight:** a customer with a great credit score who spends $5 a month is far less valuable than one who spends $150. The $150 customer is where marketing budget delivers the highest ROI.

---

## Query Execution Order

Understanding the order in which the database processes each clause helps you write correct filters and debug unexpected results.

| Step | Clause     | What happens                                                         |
| ---- | ---------- | -------------------------------------------------------------------- |
| 1    | `FROM`     | Load the `customer_details` table                                    |
| 2    | `JOIN`     | Combine with `transactions` on matching `customer_id`                |
| 3    | `WHERE`    | Discard rows where `credit_score <= 0.5` or date is outside Sep 2020 |
| 4    | `GROUP BY` | Collapse remaining rows into one row per customer                    |
| 5    | `HAVING`   | Discard customer groups where total spend `<= $100`                  |
| 6    | `SELECT`   | Pick the three output columns and calculate the `SUM` alias          |
| 7    | `ORDER BY` | _(not used here, but would run last if included)_                    |

> **Common beginner mistake:** filtering on `total_spend` inside `WHERE`. This fails because `WHERE` runs at step 3 — before `SUM()` is calculated at step 6. Always use `HAVING` to filter on aggregated values.

---

## Business Decisions This Query Enables

The result set is a shortlist of customers who are financially reliable **and** actively spending at a meaningful level.

### Marketing Team

- Send targeted vouchers or loyalty tier upgrades **before a competitor does**
- Build lookalike audiences to acquire similar new customers
- Feed results into a churn model — if a customer on this list stops spending, that is an early warning sign worth acting on immediately

### Finance Team

- Approve higher credit limits for BNPL schemes, increasing basket size and revenue per visit
- Forecast monthly revenue from the high-value customer segment
- Measure whether the September promotion moved the needle on spend for the most profitable cohort, and decide whether to repeat or scale it — directly linking SQL analysis to profitability
