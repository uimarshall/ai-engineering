# Weekly SQL Challenge 05

## Overview

**Data:** `grocery_db` schema data tables  
**Tables used:** `grocery_db.transactions`, `grocery_db.product_areas`

---

## The Task

Write a query that returns, for **each customer**, their:

- **Total spend within the Fruit product area**
- **Total spend within the Meat product area**

**Expected Output:** One row per customer with three columns:

| customer_id | total_fruit_spend | total_meat_spend |
| ----------- | ----------------- | ---------------- |
| 1001        | 45.20             | 112.80           |
| 1002        | 0.00              | 67.50            |
| ...         | ...               | ...              |

---

## Business Context & Why This Matters

You are a data analyst at a grocery retail chain. The **Category Management** team wants to understand how customers split their spend across the **Fruit** and **Meat** departments — two of the highest-margin product areas in the store.

Why does this matter competitively?

- **Product area spend analysis is the foundation of basket analysis.** Knowing that a customer spends heavily on Meat but nothing on Fruit reveals a cross-sell opportunity — a targeted promotion could shift some of their weekly shop into the Fruit aisle, increasing basket size and overall revenue.
- **Competitor intelligence:** If a large segment of customers spend on Meat but not Fruit, it could indicate that the Fruit range, pricing, or placement is weak — and customers are buying their Fruit elsewhere (a competitor). Fixing this retains spend that is currently leaking.
- **Personalised marketing:** Customers with high `total_fruit_spend` are prime candidates for a "fresh produce loyalty" campaign. Customers with high `total_meat_spend` could be targeted with a butcher counter premium promotion. Segmented campaigns consistently outperform blanket promotions in ROI.
- **Range planning:** If `total_fruit_spend` is consistently low across a store's catchment, the buying team can use this to rationalise the range — reducing waste and improving gross margin, a direct profitability lever.
- **Pricing strategy:** Comparing spend profiles before and after a price change in either category shows the business whether the change attracted or repelled spending, informing competitive pricing decisions.

This query enables the business to move from _"we sell fruit and meat"_ to _"here is exactly how much each of our customers values each category, and here is what we can do about it."_

---

## The SQL Query (Fully Annotated)

```sql
SELECT
    a.customer_id,                                             -- Line 1
    SUM(CASE WHEN b.product_area_name = 'Fruit'               -- Line 2
             THEN a.sales_cost ELSE 0 END) AS total_fruit_spend,
    SUM(CASE WHEN b.product_area_name = 'Meat'                -- Line 3
             THEN a.sales_cost ELSE 0 END) AS total_meat_spend

FROM
    grocery_db.transactions a                                  -- Line 4
    INNER JOIN grocery_db.product_areas b                      -- Line 5
        ON a.product_area_id = b.product_area_id               -- Line 6

GROUP BY
    a.customer_id                                              -- Line 7

ORDER BY
    a.customer_id;                                             -- Line 8
```

---

## Line-by-Line Explanation

---

### Line 1 — `a.customer_id`

```sql
a.customer_id,
```

- `SELECT` opens the query and `a.customer_id` is the first column we want to return.
- `a` is the **table alias** for `grocery_db.transactions` (defined on Line 4). Using a short alias avoids typing the full table name every time you reference a column.
- `customer_id` is the **unique identifier for each customer** — the column that links transaction records back to a specific person.
- Because the final query uses `GROUP BY a.customer_id` (Line 7), this column becomes the **grouping key** — one row in the output per unique customer.
- **Beginner tip:** Any column that appears in `SELECT` and is _not_ inside an aggregate function (`SUM`, `COUNT`, `AVG`, etc.) **must also appear in `GROUP BY`**. Here `customer_id` is the only non-aggregated column, so it is the only one in `GROUP BY`.
- **Business purpose:** Identifies _which_ customer each spend figure belongs to, enabling individual customer-level targeting and analysis.

---

### Line 2 — `SUM(CASE WHEN b.product_area_name = 'Fruit' THEN a.sales_cost ELSE 0 END) AS total_fruit_spend`

```sql
SUM(
    CASE WHEN b.product_area_name = 'Fruit'
         THEN a.sales_cost
         ELSE 0
    END
) AS total_fruit_spend,
```

This is the most important and most powerful line in the query. It uses a technique called **conditional aggregation** — summing values only when a specific condition is true. Unpack it layer by layer:

#### The `CASE WHEN` expression (inner layer)

```sql
CASE WHEN b.product_area_name = 'Fruit'
     THEN a.sales_cost
     ELSE 0
END
```

- `CASE WHEN ... THEN ... ELSE ... END` is SQL's **if/else logic**, applied row by row.
- For each individual row in the joined data:
  - **If** the product area name is `'Fruit'` → return the value in `a.sales_cost` (the actual spend amount for that line item).
  - **Otherwise (Meat, Bakery, Dairy, etc.)** → return `0` (contribute nothing to the Fruit total).
- The result is a column that contains the real spend value for Fruit rows and `0` for everything else.
- **Beginner tip:** Think of it as a filter that doesn't remove rows — instead it replaces the non-qualifying values with `0` so the `SUM` outside ignores them mathematically.

#### The `SUM(...)` (outer layer)

- `SUM()` adds up the values produced by the `CASE WHEN` expression across all rows that belong to the same customer (the `GROUP BY` group).
- Because non-Fruit rows contribute `0`, the total equals exactly the customer's Fruit spend.
- `AS total_fruit_spend` names the output column clearly and descriptively.

#### Why `ELSE 0` instead of `ELSE NULL`?

- Using `ELSE NULL` would still work with `SUM` because SQL's `SUM` ignores `NULL` values. However, `ELSE 0` makes intent explicit and prevents potential confusion if the expression is used outside an aggregate.
- A customer who bought no Fruit would show `0.00` rather than `NULL` — cleaner for reporting dashboards that may treat NULL as "missing data" rather than "zero spend."

- **Business purpose:** This column tells the business exactly how much each customer is worth to the Fruit category. It can drive personalised Fruit promotions, identify Fruit non-buyers, or feed into a product recommendation engine.

---

### Line 3 — `SUM(CASE WHEN b.product_area_name = 'Meat' THEN a.sales_cost ELSE 0 END) AS total_meat_spend`

```sql
SUM(
    CASE WHEN b.product_area_name = 'Meat'
         THEN a.sales_cost
         ELSE 0
    END
) AS total_meat_spend
```

- Identical structure to Line 2, but the condition now checks for `'Meat'` instead of `'Fruit'`.
- The same `CASE WHEN` logic applies row by row: Meat rows contribute their `sales_cost` value; all other rows contribute `0`.
- `SUM()` totals the Meat-only spend per customer group.
- `AS total_meat_spend` labels the column.
- **Key insight:** Both conditional aggregations run over **the same joined dataset at the same time** — the database does not scan the table twice. This makes conditional aggregation far more efficient than writing two separate subqueries and joining them together.
- **Beginner tip:** You can add as many `SUM(CASE WHEN ...)` columns as you need — one per product area, one per month, one per region — all in a single query pass. This is sometimes called a **"pivot"** because you are rotating category rows into category columns.
- **Business purpose:** Paired with `total_fruit_spend`, this column allows the business to compare how each customer allocates spend between two key categories — enabling **cross-category basket analysis** and revealing whether customers are single-category shoppers or broad-basket shoppers.

---

### Line 4 — `FROM grocery_db.transactions a`

```sql
FROM grocery_db.transactions a
```

- Specifies `grocery_db.transactions` as the **primary (left) table** — the main data source for this query.
- `a` is the **table alias** for `transactions`. It is short, unambiguous, and used throughout the query to prefix column names from this table (`a.customer_id`, `a.sales_cost`, `a.product_area_id`).
- The `transactions` table holds one row per **line item** per transaction — e.g., a customer who bought bananas, steak, and bread in one visit would have three rows, one for each product.
- **Beginner tip:** Table aliases are optional but strongly recommended in multi-table queries. They prevent errors when two tables share column names (both tables here have `product_area_id`), and they make queries shorter and easier to scan.
- **Business purpose:** This is the transactional heartbeat of the business — every sale recorded. All spend analysis originates from this table.

---

### Line 5–6 — `INNER JOIN grocery_db.product_areas b ON a.product_area_id = b.product_area_id`

```sql
INNER JOIN grocery_db.product_areas b
    ON a.product_area_id = b.product_area_id
```

#### Why is this JOIN needed?

The `transactions` table records which `product_area_id` each item belongs to (a number like `3` or `7`). But the `CASE WHEN` on Lines 2 and 3 needs the human-readable **name** (`'Fruit'`, `'Meat'`). That name lives in the `product_areas` table.

The JOIN bridges these two tables so that each transaction row gains the `product_area_name` column it needs.

#### Breaking it down:

- `INNER JOIN` — combines rows from both tables, keeping only rows where a **matching value exists in both tables**. Any transaction row whose `product_area_id` has no match in `product_areas` is silently dropped. In a well-maintained database this should never happen (it would indicate a data integrity problem).
- `grocery_db.product_areas b` — the second table, aliased as `b`. This is a **lookup / reference table** that maps IDs to names (e.g., `product_area_id = 3` → `product_area_name = 'Fruit'`).
- `ON a.product_area_id = b.product_area_id` — the **join condition**: match each transaction row to the product area record that shares the same `product_area_id`. This is a standard **foreign key → primary key** join.
- **Beginner tip:** `INNER JOIN` is the most common join type. Think of it as: _"For each row in the left table, find the matching row in the right table — and only keep pairs where a match is found."_
- **Beginner tip:** Without this JOIN, `b.product_area_name` would not exist in the query and the `CASE WHEN` logic on Lines 2 and 3 would fail.
- **Business purpose:** Translates numeric product area IDs into meaningful category names — essential for the conditional logic that separates Fruit spend from Meat spend.

---

### Line 7 — `GROUP BY a.customer_id`

```sql
GROUP BY a.customer_id
```

- `GROUP BY` **collapses all rows for the same customer into a single output row**, applying the `SUM()` aggregate functions across all rows in each customer's group.
- Without `GROUP BY`, `SUM()` would add up all Fruit spend across _all_ customers into one single number — which is not what we want. `GROUP BY customer_id` makes `SUM()` calculate separately per customer.
- The number of rows in the output equals the number of distinct `customer_id` values in the joined data.
- **Beginner tip:** The rule is strict: every column in `SELECT` must either be (a) inside an aggregate function like `SUM()` or (b) listed in `GROUP BY`. `customer_id` is in `GROUP BY`; `total_fruit_spend` and `total_meat_spend` are inside `SUM()`. The query is valid.
- **Business purpose:** Produces one summary row per customer — the standard unit of analysis for CRM, personalisation, and segmentation work.

---

### Line 8 — `ORDER BY a.customer_id;`

```sql
ORDER BY a.customer_id;
```

- `ORDER BY` **sorts the final result set** before it is returned to the user.
- `a.customer_id` sorts rows in **ascending order** by customer ID (lowest number first) — `ASC` is the default and does not need to be written explicitly.
- Without `ORDER BY`, SQL databases do not guarantee the order of returned rows — results could appear in any sequence, varying between runs.
- The semicolon `;` terminates the entire SQL statement.
- **Beginner tip:** `ORDER BY` is purely cosmetic — it makes results easier to read and compare but has no effect on what data is returned. To sort highest spend first instead, you could write `ORDER BY total_fruit_spend DESC`.
- **Business purpose:** Presenting rows in a predictable, sorted order makes it easy to spot patterns at a glance, export to Excel, or join with another sorted dataset. When sharing results in a business meeting, ordered output looks professional and intentional.

---

## Full Query Logic Flow (Visual Summary)

```
grocery_db.transactions          grocery_db.product_areas
(one row per line item)          (one row per product area)
        │                                   │
        └─────────── INNER JOIN ────────────┘
                  ON product_area_id
                         │
                         ▼
              Enriched rows: each transaction now
              has the product_area_name attached
                         │
                         ▼
              GROUP BY customer_id
              Apply SUM(CASE WHEN 'Fruit' ...)  → total_fruit_spend
              Apply SUM(CASE WHEN 'Meat'  ...)  → total_meat_spend
                         │
                         ▼
              ORDER BY customer_id
                         │
                         ▼
          Final result: one row per customer
          with spend split by category
```

---

## Summary Table

| Line | SQL Element                                                | What It Does                                                      | Business Reason                                            |
| ---- | ---------------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------- |
| 1    | `a.customer_id`                                            | Identifies the customer; acts as the grouping key                 | One output row per customer for individual-level analysis  |
| 2    | `SUM(CASE WHEN 'Fruit' THEN sales_cost ELSE 0 END)`        | Sums only Fruit spend per customer; zero for all other categories | Measures each customer's Fruit category value              |
| 3    | `SUM(CASE WHEN 'Meat' THEN sales_cost ELSE 0 END)`         | Sums only Meat spend per customer; zero for all other categories  | Measures each customer's Meat category value               |
| 4    | `FROM grocery_db.transactions a`                           | Sources raw line-item sales data; aliases as `a`                  | The transaction record — every item ever sold              |
| 5–6  | `INNER JOIN grocery_db.product_areas b ON product_area_id` | Adds product area names to each transaction row                   | Enables `CASE WHEN` to check category by name, not just ID |
| 7    | `GROUP BY a.customer_id`                                   | Collapses all rows per customer into one summary row              | Produces the per-customer aggregation the business needs   |
| 8    | `ORDER BY a.customer_id;`                                  | Sorts output ascending by customer ID                             | Clean, predictable output for reporting and export         |

---

## Key SQL Concepts Used

| Concept                                   | Description                                                                                              |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Conditional aggregation**               | `SUM(CASE WHEN condition THEN value ELSE 0 END)` — aggregate only rows matching a condition              |
| **`CASE WHEN ... THEN ... ELSE ... END`** | Row-level if/else logic; evaluates a condition and returns different values based on the result          |
| **`SUM()`**                               | Aggregate function — adds up numeric values within a group                                               |
| **`GROUP BY`**                            | Collapses multiple rows into one per grouping key; required when mixing `SELECT` columns with aggregates |
| **`INNER JOIN ... ON`**                   | Merges two tables, keeping only rows with matching values in both                                        |
| **Table alias (`a`, `b`)**                | Shorthand for a table name; prevents ambiguity when column names overlap across tables                   |
| **`ORDER BY`**                            | Sorts the final result set; ascending by default, use `DESC` to reverse                                  |
| **Column alias (`AS`)**                   | Renames a computed column to a human-readable label                                                      |
| **`;`**                                   | Statement terminator — ends the SQL query                                                                |

---

## The Power of Conditional Aggregation (vs Alternatives)

Many beginners would try to solve this with two separate queries and a JOIN:

```sql
-- Approach 1: Subquery approach (verbose, slower)
SELECT f.customer_id, f.fruit_spend, m.meat_spend
FROM (SELECT customer_id, SUM(sales_cost) AS fruit_spend FROM ... WHERE product_area = 'Fruit' GROUP BY customer_id) f
JOIN (SELECT customer_id, SUM(sales_cost) AS meat_spend  FROM ... WHERE product_area = 'Meat'  GROUP BY customer_id) m
ON f.customer_id = m.customer_id;
```

The conditional aggregation approach (Lines 2–3) is **better** because:

1. **One table scan** — the database reads `transactions` once and computes both category totals simultaneously, rather than scanning the table twice.
2. **Handles zero-spend customers correctly** — customers who bought no Fruit still appear with `0.00`. The subquery approach with an `INNER JOIN` would silently drop them.
3. **Scales easily** — add a third category (e.g., `total_bakery_spend`) with one extra line. The subquery approach requires adding another entire subquery and another JOIN.
4. **Cleaner, more readable code** — the business logic (what defines Fruit vs Meat spend) is visible in one place.

---

## Extended Business Use Cases

The **conditional aggregation** pattern is one of the most versatile in business SQL. It solves any "split one metric across categories in columns" problem:

| Industry           | Business Question                                                                   | Columns Produced                                         |
| ------------------ | ----------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Grocery retail** | How much does each customer spend on Fruit vs Meat?                                 | `total_fruit_spend`, `total_meat_spend`                  |
| **E-commerce**     | How much does each customer spend on Electronics vs Clothing vs Books?              | `electronics_spend`, `clothing_spend`, `books_spend`     |
| **Banking**        | How many transactions did each customer make via mobile vs branch vs ATM?           | `mobile_txn_count`, `branch_txn_count`, `atm_txn_count`  |
| **Marketing**      | How many emails did each customer open vs click vs ignore last month?               | `emails_opened`, `emails_clicked`, `emails_ignored`      |
| **HR / Workforce** | How many hours did each employee log on billable vs non-billable vs training tasks? | `billable_hours`, `non_billable_hours`, `training_hours` |
| **SaaS**           | How many times did each user use Feature A vs Feature B vs Feature C this week?     | `feature_a_uses`, `feature_b_uses`, `feature_c_uses`     |

In every case the competitive advantage is the same: **turning rows of raw events into a clean, wide, customer-level summary table** — the standard input format for segmentation models, personalisation engines, churn predictors, and executive dashboards. Businesses that do this well can act on customer behaviour in near-real-time; those that cannot are always reacting to last quarter's trends.
