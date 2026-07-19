# Weekly SQL Challenge 04a

## Overview

**Data:** `grocery_db` schema data tables  
**Tables used:** `grocery_db.transactions`, `grocery_db.customer_details`

---

## The Task

Write a query that returns the **customer details** (`customer_id`, `distance_from_store`, `gender`, `credit_score`) and the **sales cost of their first transaction**, but only for customers whose **first transaction exceeded $100**.

**Requirements:**
- Use **Common Table Expressions (CTEs)** instead of nested subqueries
- Use a **window function**
- Use an **INNER JOIN**

---

## Business Context & Why This Matters

You are a data analyst at a grocery retail chain. The commercial leadership team wants to identify **high-value customers from the moment they first walked through the door** — customers whose very first purchase exceeded $100.

Why does this matter competitively?

- A customer who spends big on their **first visit** has already demonstrated **high purchase intent**. These customers are significantly more likely to become high-lifetime-value regulars.
- Knowing *who* these customers are — their distance from the store, gender, and credit score — allows the business to build a **profile of the ideal high-value customer** and use that profile to:
  - Target similar prospects in acquisition campaigns.
  - Design a premium onboarding experience for first-time big spenders (e.g., a personalised thank-you voucher after their first visit).
  - Feed this segment into a predictive model to **forecast future revenue** from new sign-ups.
- Understanding distance helps decide whether to expand delivery zones or open new locations.
- Credit score data, combined with first-transaction spend, can inform whether to offer **store credit products** early in the customer relationship.

This query is the foundation of a **first-purchase analytics pipeline** — a tool that lets the business act on early customer signals before a competitor wins them over.

---

## The SQL Query (Fully Annotated)

```sql
-- STEP 1: CTE 1 — Aggregate transactions to get spend per visit
WITH cust_orders AS (
    SELECT
        customer_id,          -- Line A1
        transaction_id,       -- Line A2
        transaction_date,     -- Line A3
        SUM(sales_cost) AS sales_cost  -- Line A4

    FROM
        grocery_db.transactions t  -- Line A5

    GROUP BY
        customer_id,          -- Line A6
        transaction_id,       -- Line A6
        transaction_date      -- Line A6
),

-- STEP 2: CTE 2 — Rank each customer's transactions by date to find the first one
firstorders AS (
    SELECT
        customer_id,          -- Line B1
        transaction_id,       -- Line B2
        transaction_date,     -- Line B3
        sales_cost,           -- Line B4
        ROW_NUMBER() OVER (   -- Line B5
            PARTITION BY customer_id
            ORDER BY transaction_date ASC, transaction_id ASC
        ) AS row_num

    FROM
        cust_orders t         -- Line B6
),

-- STEP 3: Final SELECT — Join customer details to first orders and filter
SELECT
    cd.customer_id,           -- Line C1
    cd.distance_from_store,   -- Line C2
    cd.gender,                -- Line C3
    cd.credit_score,          -- Line C4
    fo.sales_cost             -- Line C5

FROM
    grocery_db.customer_details cd        -- Line C6
    INNER JOIN firstorders fo             -- Line C7
        ON cd.customer_id = fo.customer_id -- Line C8

WHERE
    fo.sales_cost > 100   -- Line C9
    AND fo.row_num = 1;   -- Line C10
```

---

## Section-by-Section Breakdown

---

### `WITH cust_orders AS (...)` — CTE 1: Aggregate spend per transaction

A **CTE (Common Table Expression)** is a named, temporary result set defined at the top of the query using the `WITH` keyword. It behaves like a virtual table that exists only for the duration of the query. CTEs make complex queries easier to read, test, and maintain — like breaking a big problem into labelled steps.

---

#### Line A1 — `customer_id`

```sql
customer_id,
```

- Selects the `customer_id` column from `grocery_db.transactions`.
- This is the **unique identifier** for each customer — the link that allows us to connect transaction records back to customer profile data later.
- **Why include it here:** We need to group spending by customer, so `customer_id` must appear in both the `SELECT` and `GROUP BY` clauses.

---

#### Line A2 — `transaction_id`

```sql
transaction_id,
```

- Selects the `transaction_id` — a unique identifier for each individual shopping visit or order.
- One transaction may span many rows in `grocery_db.transactions` (one row per product bought). `transaction_id` groups all those product rows back into a single visit.
- **Why include it here:** We need to sum the cost of all items within a single transaction, so `transaction_id` is part of our grouping key.

---

#### Line A3 — `transaction_date`

```sql
transaction_date,
```

- Selects the date of the transaction.
- **Why include it here:** We need this to rank transactions chronologically in the next CTE so we can identify which one was the *first*. It must also appear in `GROUP BY` for SQL to allow it in the `SELECT` list.

---

#### Line A4 — `SUM(sales_cost) AS sales_cost`

```sql
SUM(sales_cost) AS sales_cost
```

- `SUM(sales_cost)` is an **aggregate function** that adds up the `sales_cost` values across all rows that share the same `customer_id`, `transaction_id`, and `transaction_date`.
- In plain terms: it totals up how much a customer spent in a single transaction (visit), across all the individual items they bought.
- `AS sales_cost` renames the computed column so it keeps the readable name `sales_cost` for use in the next step.
- **Beginner tip:** Without `SUM`, if a customer bought 5 items in one visit, you'd see 5 separate rows instead of one consolidated total per visit.
- **Business purpose:** Converts raw line-item transaction data into a per-visit spend figure — the actual business-meaningful unit of measurement.

---

#### Line A5 — `FROM grocery_db.transactions t`

```sql
FROM grocery_db.transactions t
```

- Specifies the **source table**: `grocery_db.transactions`, which holds one row per item per transaction (the raw till receipt data).
- `t` is a **table alias** — a shorthand name for the table within this CTE. It is not used within this CTE but is declared here and could be referenced if needed.
- **Business purpose:** This is the company's core transactional data — every item scanned at the checkout.

---

#### Line A6 — `GROUP BY customer_id, transaction_id, transaction_date`

```sql
GROUP BY
    customer_id,
    transaction_id,
    transaction_date
```

- `GROUP BY` collapses multiple rows into one row per unique combination of the listed columns.
- Here it creates **one row per transaction per customer**, collapsing all the individual line items within a visit into a single total (the `SUM` on Line A4).
- Every column in `SELECT` that is *not* inside an aggregate function (`SUM`, `COUNT`, `AVG`, etc.) **must appear in `GROUP BY`** — this is a fundamental SQL rule.
- **Beginner tip:** Think of `GROUP BY` as a "bundle by" instruction: bundle all rows that share the same `customer_id` + `transaction_id` + `transaction_date` into one row and apply the `SUM` to everything in the bundle.

---

### `firstorders AS (...)` — CTE 2: Rank each customer's transactions

This second CTE takes the output of `cust_orders` (one row per transaction per customer) and **assigns a rank to each transaction** ordered by date, so we can identify the very first one.

---

#### Lines B1–B4 — `customer_id`, `transaction_id`, `transaction_date`, `sales_cost`

```sql
customer_id,
transaction_id,
transaction_date,
sales_cost,
```

- These four columns are passed through from `cust_orders` unchanged.
- They carry the customer identifier, visit identifier, date, and total spend-per-visit forward into this CTE so they are available in the final `SELECT`.

---

#### Line B5 — `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date ASC, transaction_id ASC) AS row_num`

```sql
ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY transaction_date ASC, transaction_id ASC
) AS row_num
```

This is the **window function** — the most technically significant line in the query. Break it down part by part:

- `ROW_NUMBER()` — assigns a sequential integer (1, 2, 3, …) to each row within a defined group (the "window"). The first row in the group gets 1, the second gets 2, and so on.
- `OVER (...)` — this keyword turns `ROW_NUMBER()` into a **window function**. It tells SQL to apply the numbering within a defined "window" of rows rather than across the entire table.
- `PARTITION BY customer_id` — **restarts the numbering at 1 for every new customer**. So customer 101 gets rows numbered 1, 2, 3… and customer 102 independently gets rows numbered 1, 2, 3… This is the "partition" — separate windows per customer.
- `ORDER BY transaction_date ASC, transaction_id ASC` — within each customer's window, rows are sorted **oldest transaction first** (`ASC` = ascending = earliest date first). `transaction_id ASC` is a tiebreaker in case two transactions share the same date — the lower ID is treated as earlier.
- `AS row_num` — names the computed column `row_num`.
- **The result:** For each customer, their oldest transaction gets `row_num = 1`, their second oldest gets `row_num = 2`, and so on.
- **Beginner tip:** Window functions are powerful because they add computed values to rows *without collapsing them* like `GROUP BY` does. Every row stays; each row just gains a new computed column.
- **Business purpose:** `row_num = 1` is how we identify each customer's first-ever purchase, which is the core business question of this query.

---

#### Line B6 — `FROM cust_orders t`

```sql
FROM cust_orders t
```

- Instead of a real table, this references **the first CTE** `cust_orders` as if it were a table.
- This is the power of CTEs: each one builds on the last, letting you write complex logic as a clear sequence of named steps rather than a deeply nested subquery.

---

### Final `SELECT` — Join and Filter

---

#### Lines C1–C5 — Selected columns

```sql
cd.customer_id,
cd.distance_from_store,
cd.gender,
cd.credit_score,
fo.sales_cost
```

- These are the five columns returned to the user in the final result.
- `cd.` prefix means the column comes from `customer_details` (aliased as `cd`).
- `fo.` prefix means the column comes from `firstorders` (aliased as `fo`).
- Using table prefixes is essential here to avoid ambiguity — both tables contain a `customer_id` column, so without the prefix SQL would not know which one to use.
- **Business purpose:** The output gives the business a customer-level table with profile attributes (distance, gender, credit score) alongside first-visit spend — everything needed to profile the "high first-purchase value" customer segment.

---

#### Line C6 — `FROM grocery_db.customer_details cd`

```sql
FROM grocery_db.customer_details cd
```

- Sets `customer_details` as the **left (primary) table** in the join.
- `cd` is a short **table alias** used throughout the `SELECT` and `WHERE` clauses.
- `customer_details` holds the customer profile attributes: `customer_id`, `gender`, `distance_from_store`, `credit_score`, etc.

---

#### Lines C7–C8 — `INNER JOIN firstorders fo ON cd.customer_id = fo.customer_id`

```sql
INNER JOIN firstorders fo
    ON cd.customer_id = fo.customer_id
```

- `INNER JOIN` connects two tables and returns **only rows where a match exists in both tables**.
- `firstorders` is the second CTE being joined; `fo` is its alias.
- `ON cd.customer_id = fo.customer_id` is the **join condition** — it specifies which column links the two tables. A customer in `customer_details` is matched to their transaction record in `firstorders` using the shared `customer_id` value.
- **What INNER JOIN does NOT return:** Customers in `customer_details` who have *no* transactions (they'd appear in a `LEFT JOIN` but not here), and transactions in `firstorders` with no matching customer profile.
- **Beginner tip:** Think of `INNER JOIN` as a Venn diagram — only the overlapping middle section is kept.
- **Business purpose:** Links the "what they spent" data (transactions) to the "who they are" data (customer profile) so both dimensions are available in one result row.

---

#### Line C9 — `WHERE fo.sales_cost > 100`

```sql
WHERE fo.sales_cost > 100
```

- Filters the joined result to keep only rows where the `sales_cost` column from `firstorders` is **strictly greater than 100**.
- This targets customers whose first-ever transaction total exceeded $100 — the high-value first-purchase threshold set by the business.
- `> 100` is a **strict inequality** — a customer who spent exactly $100.00 would be excluded. Use `>= 100` to include the boundary.
- **Business purpose:** The $100 threshold is a proxy for "high purchase intent on first visit." The business has determined that customers crossing this threshold have a significantly higher probability of becoming top-quartile lifetime-value customers.

---

#### Line C10 — `AND fo.row_num = 1;`

```sql
AND fo.row_num = 1;
```

- `AND` adds the second filter condition — both must be true.
- `fo.row_num = 1` keeps only the row for each customer that was assigned `row_num = 1` in the window function — i.e., **their very first transaction chronologically**.
- Without this filter, the query would return results for *all* transactions where spend exceeded $100, not just the first one. A customer who spent $50 on their first visit and $150 on their third would incorrectly appear in the results.
- The semicolon `;` terminates the entire SQL statement.
- **Business purpose:** This is the precision filter that makes the query answer the exact business question: *"Who spent big on their first visit?"* — not just *"Who has ever spent big?"*

---

## Full Query Logic Flow (Visual Summary)

```
grocery_db.transactions (raw line items)
        │
        ▼
  CTE 1: cust_orders
  → GROUP BY customer + transaction
  → SUM(sales_cost) per visit
  → Result: one row per transaction per customer
        │
        ▼
  CTE 2: firstorders
  → ROW_NUMBER() per customer, oldest date first
  → Result: one row per transaction per customer + row_num column
        │
        ▼
  Final SELECT
  → INNER JOIN with customer_details on customer_id
  → WHERE sales_cost > 100 AND row_num = 1
  → Result: profile + first-visit spend for high-value first-purchasers
```

---

## Summary Table

| Line | SQL Element | What It Does | Business Reason |
|------|-------------|--------------|-----------------|
| A1–A3 | `SELECT customer_id, transaction_id, transaction_date` | Carries identifiers and date into CTE 1 | Needed for grouping and later chronological ranking |
| A4 | `SUM(sales_cost) AS sales_cost` | Totals item costs into a per-visit spend figure | Converts raw receipt rows into a meaningful spend metric |
| A5 | `FROM grocery_db.transactions t` | Sources raw till data | The company's record of every item sold |
| A6 | `GROUP BY customer_id, transaction_id, transaction_date` | Collapses item rows into one row per visit | Required by SQL when mixing `SELECT` columns with aggregates |
| B5 | `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_date ASC...)` | Numbers each customer's transactions oldest-first | Enables identification of the very first purchase per customer |
| B6 | `FROM cust_orders t` | References CTE 1 as input | Chains the two CTEs together in a readable pipeline |
| C1–C5 | Final column list | Selects the five output columns | Delivers the profile + spend data the business team needs |
| C6 | `FROM grocery_db.customer_details cd` | Brings in customer profile attributes | Links spend behaviour to demographic information |
| C7–C8 | `INNER JOIN firstorders fo ON customer_id` | Merges profile and transaction data | Combines "who they are" with "what they spent" |
| C9 | `WHERE fo.sales_cost > 100` | Keeps only first visits exceeding $100 | Isolates the high-value first-purchase segment |
| C10 | `AND fo.row_num = 1;` | Restricts to first transaction only | Ensures we analyse first-purchase behaviour, not repeat visits |

---

## Key SQL Concepts Used

| Concept | Description |
|---------|-------------|
| **CTE (`WITH ... AS`)** | Named temporary result set; makes complex logic readable and reusable within a query |
| **`SUM()`** | Aggregate function — adds up numeric values within a group |
| **`GROUP BY`** | Collapses multiple rows into one per unique combination of grouping columns |
| **`ROW_NUMBER()`** | Window function — assigns a sequential rank to rows within a partition |
| **`OVER (PARTITION BY ... ORDER BY ...)`** | Defines the window: which rows to include and how to order them for ranking |
| **`INNER JOIN ... ON`** | Combines two tables, keeping only rows with matching values in both |
| **Table aliases (`cd`, `fo`, `t`)** | Shorthand names for tables; essential when the same column name exists in multiple tables |
| **`WHERE`** | Filters rows after all joins are resolved |
| **`>`** | Strict greater-than; excludes the boundary value |
| **`;`** | Statement terminator |

---

## Extended Business Use Cases

This **CTE + Window Function + JOIN** pattern is one of the most powerful and widely used patterns in business analytics. The same structure solves a broad class of "first event" and "most recent event" problems:

| Industry | Business Question | How the Pattern Applies |
|----------|------------------|------------------------|
| **Grocery retail** | Which customers spent >$100 on their first visit? | Identify high-intent new customers for premium loyalty onboarding |
| **E-commerce** | Which customers placed their first order within 24 hours of signing up? | Measure campaign urgency effectiveness; fast first-purchase = higher LTV |
| **Banking** | Which new current-account holders made a deposit >£500 within 7 days of opening? | Flag high-value new customers for a relationship manager call |
| **SaaS** | Which trial users triggered a key feature on their first session? | Identify "aha moment" users — they convert to paid at 3× the normal rate |
| **Telecom** | Which customers called support within 30 days of signing a new contract? | Early dissatisfaction signal — intervene before they churn to a competitor |
| **Insurance** | Which policyholders made a claim within 6 months of their first policy? | Flag for risk review; adjust pricing models to improve margin |

In each case the **competitive advantage** is the same: by understanding what high-value or high-risk customers look like at the *very beginning* of their relationship with the business, you can act faster and more precisely than competitors who wait for behaviour to accumulate over months.