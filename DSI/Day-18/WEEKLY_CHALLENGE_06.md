# Weekly SQL Challenge 06

## Overview

**Data:** `grocery_db` schema data tables  
**Table used:** `grocery_db.transactions`

---

## The Task

Return a list of **customers that have shopped in all 5 product areas**.

**Expected Output:** Two columns:

| customer_id | product_id_count |
|-------------|-----------------|
| 1004 | 5 |
| 1017 | 5 |
| ... | ... |

- `customer_id` — identifies the customer
- `product_id_count` — the count of distinct product areas that customer has purchased from (only customers with a count of 5 appear)

---

## Business Context & Why This Matters

You are a data analyst at a grocery retail chain competing in a highly contested local market. The **Head of Loyalty & Retention** has asked a critical strategic question:

> *"Which customers are truly engaged with our full store offering — not just one or two aisles?"*

A customer who shops across **all 5 product areas** (e.g., Fruit, Meat, Bakery, Dairy, Frozen) is fundamentally different from a customer who only ever buys Meat:

- **Full-basket customers** are the business's most valuable segment. They have a higher average transaction value, visit more frequently, and are significantly harder for a competitor to poach — because switching would mean finding a single alternative store that matches the quality of *all* departments, not just one.
- **Churn risk is lowest** in this segment. A customer who only buys Fruit could easily switch to a farmers' market or a discount competitor. A customer who depends on five departments has deeply integrated the store into their weekly routine.
- **Profitability is highest** here — each department they use adds margin, and multi-category customers are more likely to respond positively to cross-category promotions (e.g., "Buy Meat + Fruit and save 10%").
- **Strategic insight:** If the count of full-basket customers is declining quarter-on-quarter, it may indicate that one or more product areas is losing quality or competitiveness — an early warning signal before revenue starts to drop.

Finding these customers enables the business to:

1. **Reward and retain** them with exclusive VIP loyalty perks — the cost of retention is far lower than the cost of acquiring a replacement.
2. **Study their behaviour** to build a profile of the "ideal customer" and use that profile in acquisition targeting.
3. **Benchmark performance** — track whether the number of all-5-area customers grows after a store refresh, price investment, or new product range launch.

---

## The SQL Query (Fully Annotated)

```sql
SELECT
    customer_id,                                        -- Line 1
    COUNT(DISTINCT product_area_id) AS product_id_count -- Line 2

FROM
    grocery_db.transactions                             -- Line 3

GROUP BY
    customer_id                                         -- Line 4

HAVING
    COUNT(DISTINCT product_area_id) = 5;                -- Line 5
```

---

## Line-by-Line Explanation

---

### Line 1 — `customer_id`

```sql
customer_id,
```

- `SELECT` opens the query. `customer_id` is the first column to return — it identifies *who* the customer is.
- Unlike previous challenges, there is **no table alias prefix** here (e.g., no `a.customer_id`). This is fine because only one table is used in the query — there is no ambiguity about which table `customer_id` comes from.
- `customer_id` is also the column named in `GROUP BY` (Line 4), making it the **grouping key** — one output row per unique customer.
- **Beginner tip:** In a single-table query, table aliases are optional. In a multi-table query (with JOINs), always use aliases to avoid column name conflicts.
- **Business purpose:** Tells us *which* customers have shopped across all five areas — so the business can look them up in CRM, send them targeted rewards, or feed them into a loyalty tier model.

---

### Line 2 — `COUNT(DISTINCT product_area_id) AS product_id_count`

```sql
COUNT(DISTINCT product_area_id) AS product_id_count
```

This line does two things simultaneously — it **deduplicates** and **counts**. Break it down:

#### `DISTINCT product_area_id` (inner operation)

- `DISTINCT` removes duplicates *within the group* before counting.
- A customer who bought Fruit items on 10 separate transactions still has only **one** Fruit product area, not 10. `DISTINCT` ensures each product area is counted only once per customer, regardless of how many times they shopped there.
- **Beginner tip:** Without `DISTINCT`, `COUNT(product_area_id)` would count every transaction row — a customer with 50 Fruit transactions would contribute 50 to the count instead of 1. The result would be meaningless for this business question.

#### `COUNT(...)` (outer operation)

- `COUNT()` tallies how many unique `product_area_id` values exist within each customer's group.
- The possible result per customer ranges from 1 (shopped in only one area) up to 5 (shopped in all five areas).
- Combined with the `HAVING` filter on Line 5, only customers where this count equals exactly 5 will appear in the output.

#### `AS product_id_count`

- Renames the column from the default `COUNT(DISTINCT product_area_id)` to the clean, readable label `product_id_count`.
- **Note:** The task description names this column `unique_product_areas` — either alias is valid; what matters is that the business understands what the number represents.

- **Business purpose:** Measures the **breadth of engagement** for each customer — a proxy for how deeply embedded they are in the store's full offering.

---

### Line 3 — `FROM grocery_db.transactions`

```sql
FROM grocery_db.transactions
```

- `FROM` specifies `grocery_db.transactions` as the **sole data source**.
- This table holds one row per **line item** per transaction — one row per product bought per visit.
- Because a customer may have hundreds of rows (many visits, many items), the `GROUP BY` and `COUNT(DISTINCT)` on Lines 4 and 2 do the work of collapsing all those rows into one meaningful summary row per customer.
- **Beginner tip:** Notice that we do *not* need to join to `grocery_db.product_areas` here — we only need the `product_area_id` number (the integer key), not the human-readable name. We are counting distinct IDs, not filtering by name. This keeps the query simpler and faster.
- **Business purpose:** Transactions is the most granular, complete record of customer behaviour. Everything the business knows about what customers buy originates here.

---

### Line 4 — `GROUP BY customer_id`

```sql
GROUP BY customer_id
```

- `GROUP BY` **bundles all transaction rows for the same customer together** so that the `COUNT(DISTINCT ...)` on Line 2 can be computed per customer rather than across the entire table.
- Without `GROUP BY`, `COUNT(DISTINCT product_area_id)` would return a single number — the total count of distinct product areas across all customers combined (which would always be 5, and would not identify any individual customer).
- The number of groups equals the number of distinct customers in the transactions table.
- **Beginner tip:** `GROUP BY` is the engine of aggregation. It answers the question: *"Apply this calculation separately for each unique value of this column."*
- **Business purpose:** Produces an individual summary for every customer — the building block for all customer-level analytics, segmentation, and targeting.

---

### Line 5 — `HAVING COUNT(DISTINCT product_area_id) = 5;`

```sql
HAVING
    COUNT(DISTINCT product_area_id) = 5;
```

This is the most nuanced line in the query — and the one beginners most commonly confuse with `WHERE`.

#### `HAVING` vs `WHERE` — a critical distinction

| | `WHERE` | `HAVING` |
|--|---------|---------|
| **When it filters** | Before `GROUP BY` — filters individual rows | After `GROUP BY` — filters entire groups (aggregated results) |
| **What it can reference** | Raw column values | Aggregate function results like `COUNT()`, `SUM()`, `AVG()` |
| **Example** | `WHERE product_area_id = 3` (keep only Fruit rows) | `HAVING COUNT(...) = 5` (keep only customers with 5 areas) |

- **Why you cannot use `WHERE` here:** At the point `WHERE` runs, `GROUP BY` hasn't happened yet — `COUNT(DISTINCT product_area_id)` doesn't exist as a value yet. You would get a SQL error if you tried `WHERE COUNT(DISTINCT product_area_id) = 5`.
- `HAVING` runs **after** `GROUP BY`, so the aggregated count already exists as a value that can be compared.
- `COUNT(DISTINCT product_area_id) = 5` keeps only customer groups where the count of distinct product areas equals exactly **5** — the total number of product areas in the store.
- **Beginner tip:** The rule of thumb: use `WHERE` to filter rows before aggregation; use `HAVING` to filter groups after aggregation.
- The semicolon `;` at the end terminates the SQL statement.
- **Business purpose:** This is the precision filter that identifies the **all-5-area customer segment** — the store's most engaged, highest-value, most loyal customers.

---

## Full Query Logic Flow (Visual Summary)

```
grocery_db.transactions
(many rows per customer — one per item per visit)
        │
        ▼
  GROUP BY customer_id
  → Bundle all rows per customer into one group
        │
        ▼
  COUNT(DISTINCT product_area_id) per group
  → How many unique areas has this customer visited?
  Customer 1001: 2 areas   Customer 1004: 5 areas
  Customer 1002: 3 areas   Customer 1017: 5 areas
  Customer 1003: 1 area    ...
        │
        ▼
  HAVING COUNT(DISTINCT product_area_id) = 5
  → Keep only customers with exactly 5 distinct areas
        │
        ▼
  Final result:
  customer_id | product_id_count
  1004        | 5
  1017        | 5
  ...
```

---

## Summary Table

| Line | SQL Element | What It Does | Business Reason |
|------|-------------|--------------|-----------------|
| 1 | `customer_id` | Identifies the customer; acts as the grouping key | Shows *who* qualifies for the full-basket segment |
| 2 | `COUNT(DISTINCT product_area_id) AS product_id_count` | Counts how many unique product areas each customer has bought from | Measures breadth of engagement across the store |
| 3 | `FROM grocery_db.transactions` | Sources all raw transaction line items | The complete record of every product every customer has ever bought |
| 4 | `GROUP BY customer_id` | Creates one summary row per customer | Enables per-customer aggregation |
| 5 | `HAVING COUNT(DISTINCT product_area_id) = 5;` | Keeps only customers who have shopped in all 5 areas | Identifies the highest-value, most-engaged customer segment |

---

## Key SQL Concepts Used

| Concept | Description |
|---------|-------------|
| **`COUNT(DISTINCT column)`** | Counts only unique (non-duplicate) values within a group |
| **`DISTINCT`** | Removes duplicates before counting or selecting |
| **`GROUP BY`** | Collapses rows into one per group; required when using aggregate functions |
| **`HAVING`** | Filters groups after `GROUP BY`; the only way to filter on aggregate results |
| **`WHERE` vs `HAVING`** | `WHERE` filters rows before grouping; `HAVING` filters groups after aggregation |
| **Column alias (`AS`)** | Renames a computed column to a readable label |
| **`;`** | Statement terminator |

---

## Common Beginner Mistakes to Avoid

### Mistake 1: Using `WHERE` instead of `HAVING`

```sql
-- WRONG — this causes a SQL error
WHERE COUNT(DISTINCT product_area_id) = 5

-- CORRECT — HAVING filters after aggregation
HAVING COUNT(DISTINCT product_area_id) = 5
```

`WHERE` cannot reference aggregate functions because aggregation hasn't happened yet at that stage of execution.

---

### Mistake 2: Forgetting `DISTINCT` inside `COUNT`

```sql
-- WITHOUT DISTINCT — counts every row, not every unique area
COUNT(product_area_id)  -- could return 50 for a customer with 50 transactions

-- WITH DISTINCT — counts each area only once
COUNT(DISTINCT product_area_id)  -- returns 1 to 5, regardless of transaction volume
```

---

### Mistake 3: Using `=` when you want `>=`

```sql
-- Only customers with exactly 5 areas
HAVING COUNT(DISTINCT product_area_id) = 5

-- Customers with 3 or more areas (broader segment)
HAVING COUNT(DISTINCT product_area_id) >= 3
```

The `=` version is correct for this task (all 5 areas), but knowing you can use `>=`, `>`, `<` in `HAVING` makes this pattern flexible for many other business questions.

---

## Extended Business Use Cases

The **`COUNT(DISTINCT) + GROUP BY + HAVING`** pattern is one of the most used patterns in customer analytics. It answers any "how many unique X has each Y interacted with?" question:

| Industry | Business Question | Competitive / Profitability Angle |
|----------|--------------------|----------------------------------|
| **Grocery retail** | Which customers have bought from all 5 product areas? | Identify full-basket loyalists — lowest churn risk, highest LTV |
| **Streaming (Netflix/Spotify)** | Which users have watched content in 4+ genres this month? | Multi-genre users are 60% less likely to cancel — prioritise for retention spend |
| **Banking** | Which customers hold 3 or more product types (current account, savings, mortgage, credit card)? | Multi-product customers are the most profitable and hardest to poach |
| **E-commerce** | Which customers have bought from 5+ different product categories? | Broadest basket = lowest price sensitivity = full-price margin protection |
| **SaaS platform** | Which accounts use 4 out of 5 core features? | High feature adoption = high switching cost = best renewal candidates |
| **Retail pharmacy** | Which customers fill prescriptions AND buy OTC AND buy personal care products? | Multi-department engagement signals the pharmacy as their primary health destination |

In every case the competitive insight is the same: **customers who use more of your offering are your most defensible, most profitable customers.** Finding them, understanding them, and protecting them is one of the highest-return activities any data analyst can support.