# Weekly SQL Challenge 09

## Overview

**Data:** `grocery_db` schema data tables  
**Table used:** `grocery_db.transactions`

---

## The Task

Write a query that returns the **customer with the third highest total spend** across all customers.

**Expected Output:** One row, two columns:

| customer_id | total_spend |
| ----------- | ----------- |
| 1042        | 847.35      |

---

## Business Context & Why This Matters

You are a data analyst at a grocery retail chain. The **VIP Account Management** team wants to identify the store's **top spenders by rank** — not just the single highest spender, but the ability to retrieve any specific position in the spend ranking (3rd, 5th, 10th, etc.).

Why does this matter competitively?

- **Top-spend customers are disproportionately valuable.** In most retail businesses, the top 5–10% of customers by spend account for 30–50% of total revenue. Losing one of these customers to a competitor has an outsized revenue impact.
- **Rank-based targeting is more precise than threshold-based targeting.** Rather than saying "customers who spend over £500", rank-based identification finds _exactly_ the top N customers regardless of spend level — it adapts automatically as the customer base and spend patterns change over time.
- **The third-highest spender is a strategic focus.** In VIP programme design, the top 1 and 2 are often already receiving premium service. The third position is where the _next tier of effort_ should be directed — identifying these customers early and ensuring they receive exceptional service before a competitor wins them over.
- **Churn prevention:** If the third-highest spender's visits suddenly drop (visible in a weekly re-run of this query showing their rank changing), the account team can intervene proactively with a personalised offer.
- **Board-level reporting:** Executives often ask "who are our top customers?" not just by total spend but at specific ranks — this query structure supports that reporting cleanly and repeatably.

This query is the **foundation of a high-value customer (HVC) programme** — identifying, monitoring, and protecting the customers who contribute most to the business's revenue and profitability.

---

## The SQL Query (Fully Annotated)

```sql
-- STEP 1: CTE — calculate total spend per customer and rank them
WITH ranked_customers AS (
    SELECT
        customer_id,                                          -- Line A1
        SUM(sales_cost) AS total_spend,                       -- Line A2
        RANK() OVER (                                         -- Line A3
            ORDER BY SUM(sales_cost) DESC
        ) AS spending_rank

    FROM
        grocery_db.transactions                               -- Line A4

    GROUP BY
        customer_id                                           -- Line A5
)

-- STEP 2: Final SELECT — retrieve the third-ranked customer
SELECT
    customer_id,                                              -- Line B1
    total_spend                                               -- Line B2

FROM
    ranked_customers                                          -- Line B3

WHERE
    spending_rank = 3;                                        -- Line B4
```

---

## Section-by-Section Breakdown

---

### `WITH ranked_customers AS (...)` — The CTE

```sql
WITH ranked_customers AS (...)
```

- `WITH` introduces a **CTE (Common Table Expression)** — a named, temporary result set that exists only for the duration of this query.
- `ranked_customers` is the name given to this temporary table. It is referenced by name in the final `SELECT` block below.
- **Why use a CTE here?** The alternative is a nested subquery:
  ```sql
  -- Without CTE (harder to read)
  SELECT customer_id, total_spend
  FROM (
      SELECT customer_id, SUM(sales_cost) AS total_spend,
             RANK() OVER (ORDER BY SUM(sales_cost) DESC) AS spending_rank
      FROM grocery_db.transactions
      GROUP BY customer_id
  ) subquery
  WHERE spending_rank = 3;
  ```
  The CTE version separates the "build the ranking" step from the "filter by rank" step into clearly labelled blocks — easier to read, test, and modify.
- **Beginner tip:** CTEs do not change what the query does; they only change how it is organised. Think of a CTE as naming an intermediate step so you can refer to it clearly later.
- **Business purpose:** Breaks the problem into two logical steps: (1) rank all customers by spend, (2) retrieve the one at position 3.

---

### Line A1 — `customer_id`

```sql
customer_id,
```

- Selects the `customer_id` from `grocery_db.transactions`.
- This is the unique customer identifier — the key that the business uses to look up the customer in CRM, contact them, or apply rewards.
- It is also the `GROUP BY` column (Line A5), so each row in the CTE result represents one unique customer.
- **Business purpose:** Identifies _who_ the customer is so the account management team can act on the ranking result.

---

### Line A2 — `SUM(sales_cost) AS total_spend`

```sql
SUM(sales_cost) AS total_spend,
```

- `SUM(sales_cost)` adds up every `sales_cost` value across all transaction rows that belong to the same `customer_id` group.
- The `transactions` table has one row per line item per visit — a customer who shopped 20 times and bought 10 items per visit has 200 rows. `SUM` collapses all 200 rows into a single total spend figure.
- `AS total_spend` names the column clearly and makes it available by that name in the final `SELECT` block (Line B2).
- **Beginner tip:** The `SUM` runs _within each group_ defined by `GROUP BY customer_id` — it does not sum across all customers, just across all rows belonging to the same customer.
- **Business purpose:** Total lifetime spend is the primary metric for identifying high-value customers. It is more reliable than frequency alone (a customer who buys cheap items often may contribute less revenue than one who shops rarely but spends large).

---

### Line A3 — `RANK() OVER (ORDER BY SUM(sales_cost) DESC) AS spending_rank`

```sql
RANK() OVER (
    ORDER BY SUM(sales_cost) DESC
) AS spending_rank
```

This is the core of the query — a **window function** that assigns a competitive rank to each customer based on their total spend. Break it down:

---

#### `RANK()` — the ranking function

- `RANK()` assigns a **sequential integer rank** to each row based on the ordering defined in `OVER(...)`.
- The customer with the highest spend gets rank `1`, the second highest gets rank `2`, the third gets rank `3`, and so on.
- **How `RANK()` handles ties (equal spend):** If two customers have the _same_ total spend, they receive the _same rank_, and the next rank is skipped:
  ```
  Customer A: spend=900 → rank 1
  Customer B: spend=850 → rank 2
  Customer C: spend=850 → rank 2  (tie with B)
  Customer D: spend=800 → rank 4  (rank 3 is skipped)
  ```
  This means if two customers tie for 2nd place, nobody has rank 3 — `WHERE spending_rank = 3` would return no rows in that scenario.

---

#### `OVER (ORDER BY SUM(sales_cost) DESC)` — the window definition

- `OVER(...)` is what makes `RANK()` a **window function** rather than a regular aggregate.
- Window functions compute values across a set of rows defined by the `OVER` clause **without collapsing rows** — every row in the CTE gets its own `spending_rank` value while still keeping all its other columns intact.
- `ORDER BY SUM(sales_cost) DESC` tells `RANK()` to assign rank `1` to the row with the **highest** `SUM(sales_cost)`. `DESC` = descending = largest value first.
- **Notice:** `SUM(sales_cost)` appears inside `OVER(ORDER BY ...)` even though `SUM` is already an aggregate function applied in `GROUP BY`. This is valid — after `GROUP BY` collapses the rows, the `SUM` value already exists per customer row, and `RANK()` then ranks those per-customer totals.
- `AS spending_rank` names the computed column.

---

#### `RANK()` vs `ROW_NUMBER()` vs `DENSE_RANK()` — choosing the right ranking function

This is one of the most important distinctions in SQL. All three are window functions but handle ties differently:

| Function       | Tie behaviour                                          | Example (scores: 900, 850, 850, 800) |
| -------------- | ------------------------------------------------------ | ------------------------------------ |
| `ROW_NUMBER()` | No ties — every row gets a unique number arbitrarily   | 1, 2, 3, 4                           |
| `RANK()`       | Ties share the same rank; **next rank is skipped**     | 1, 2, 2, **4**                       |
| `DENSE_RANK()` | Ties share the same rank; **next rank is NOT skipped** | 1, 2, 2, **3**                       |

**Which to use for this task?**

- `RANK()` is used here. If two customers tie for 3rd place, both appear when you filter `spending_rank = 3` — the business sees both equally-ranked customers, which is the correct behaviour (fair treatment of ties).
- `ROW_NUMBER()` would arbitrarily pick one of two tied customers and call one 3rd and one 4th — potentially missing a valid result.
- `DENSE_RANK()` would also work cleanly for this task and is often preferred when the absolute rank number matters (no gaps in the sequence).

- **Beginner tip:** Default to `RANK()` when you want ties to share a position and gaps are acceptable. Use `DENSE_RANK()` when you want ties to share a position but gaps are undesirable (e.g., leaderboards). Use `ROW_NUMBER()` when you need every row to be unique regardless of ties (e.g., pagination).

- **Business purpose:** `RANK()` ensures the business sees all customers genuinely at position 3 — it does not arbitrarily exclude a tied customer from the result.

---

### Line A4 — `FROM grocery_db.transactions`

```sql
FROM grocery_db.transactions
```

- Specifies the **sole data source** for the CTE: the raw transaction line items table.
- This table has one row per item per transaction — many rows per customer. The `GROUP BY` and `SUM` on Lines A5 and A2 collapse these into one summary row per customer.
- **Business purpose:** Every sale the store has ever made flows through this table — the complete, authoritative record of customer spend behaviour.

---

### Line A5 — `GROUP BY customer_id`

```sql
GROUP BY customer_id
```

- **Collapses all transaction rows per customer into a single row**, allowing `SUM(sales_cost)` to produce one total spend per customer.
- Without this, `SUM(sales_cost)` would return a single total across all customers combined — and `RANK()` would have nothing meaningful to rank.
- The CTE result after `GROUP BY` has exactly one row per unique `customer_id`, with their `total_spend` and `spending_rank`.
- **Beginner tip:** `GROUP BY customer_id` is the instruction that turns "a table of millions of transaction rows" into "a table of one row per customer" — this transformation is the foundation of almost all customer-level analytics.

---

### Line B1–B2 — `SELECT customer_id, total_spend`

```sql
SELECT
    customer_id,
    total_spend
```

- Selects only the two columns required by the task from the `ranked_customers` CTE.
- `spending_rank` is intentionally **not** selected here — the task only asks for `customer_id` and `total_spend`. The rank column was an intermediate computation needed to filter; it does not need to appear in the final output.
- **Beginner tip:** CTEs often contain more columns than the final output requires. Selecting only the needed columns in the final `SELECT` keeps the output clean and prevents information leakage (e.g., internal ranking data appearing in external reports).

---

### Line B3 — `FROM ranked_customers`

```sql
FROM ranked_customers
```

- References the **CTE defined above** as if it were a real table.
- This is the key benefit of CTEs: once defined with `WITH`, the CTE can be queried just like a table anywhere in the remainder of the statement.
- **Beginner tip:** The CTE only exists for the duration of this single query execution. It is not stored in the database. Each time the query runs, the CTE is recomputed from the underlying tables.

---

### Line B4 — `WHERE spending_rank = 3;`

```sql
WHERE spending_rank = 3;
```

- Filters the CTE result to keep only the row(s) where `spending_rank` equals `3`.
- Because `spending_rank` is a column in the CTE (not an aggregate in the current SELECT block), **`WHERE` is the correct filter here** — not `HAVING`. The ranking already exists as a column value in `ranked_customers`; no aggregation is happening in the final SELECT.
- If `RANK()` produced a tie at position 3, this filter returns multiple rows — both customers with rank 3 appear.
- If no customer has exactly rank 3 (due to a tie at rank 2 causing rank 3 to be skipped), this filter returns zero rows.
- The semicolon `;` terminates the statement.
- **Beginner tip:** To retrieve the top N customers instead of just one rank, change `= 3` to `<= 3` — this returns all customers ranked 1st, 2nd, and 3rd. To get a range (ranks 3 through 5), use `BETWEEN 3 AND 5`.
- **Business purpose:** The precision filter that extracts exactly the answer to the business question: _"Who is our third-highest spending customer right now?"_

---

## Full Query Logic Flow (Visual Summary)

```
grocery_db.transactions
(millions of rows — one per item per visit)
        │
        ▼
  GROUP BY customer_id
  SUM(sales_cost) → total_spend per customer
        │
        ▼
  RANK() OVER (ORDER BY total_spend DESC)
  → Assigns competitive rank to each customer
  Customer 1001: total=£1,200  rank=1
  Customer 1042: total=£  950  rank=2
  Customer 1089: total=£  847  rank=3   ← target
  Customer 1017: total=£  820  rank=4
  ...
        │
  All of the above lives inside: CTE "ranked_customers"
        │
        ▼
  Final SELECT from ranked_customers
  WHERE spending_rank = 3
        │
        ▼
  Result:
  customer_id | total_spend
  1089        | 847.35
```

---

## Summary Table

| Line  | SQL Element                                   | What It Does                                            | Business Reason                                                 |
| ----- | --------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| CTE   | `WITH ranked_customers AS (...)`              | Names the intermediate ranking step as a reusable block | Separates "build ranking" logic from "filter by rank" logic     |
| A1    | `customer_id`                                 | Customer identifier; grouping key                       | Needed to identify the customer and to group their transactions |
| A2    | `SUM(sales_cost) AS total_spend`              | Totals all spend per customer                           | The primary metric for ranking customer value                   |
| A3    | `RANK() OVER (ORDER BY SUM(sales_cost) DESC)` | Assigns a spend rank per customer; handles ties fairly  | Positions each customer in the spend leaderboard                |
| A4    | `FROM grocery_db.transactions`                | Source of all raw transaction data                      | The authoritative record of every sale ever made                |
| A5    | `GROUP BY customer_id`                        | Collapses rows into one per customer                    | Required to aggregate spend at the customer level               |
| B1–B2 | `SELECT customer_id, total_spend`             | Returns only the required output columns                | Keeps output clean; excludes internal ranking column            |
| B3    | `FROM ranked_customers`                       | Queries the CTE as a virtual table                      | References the pre-computed ranking                             |
| B4    | `WHERE spending_rank = 3;`                    | Retrieves only the third-ranked customer(s)             | Answers the exact business question                             |

---

## Key SQL Concepts Used

| Concept                        | Description                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------ |
| **CTE (`WITH ... AS`)**        | Named temporary result set; organises complex logic into readable steps        |
| **`SUM()`**                    | Aggregate — totals numeric values within a group                               |
| **`GROUP BY`**                 | Collapses rows into one per group; required with aggregate functions           |
| **`RANK()`**                   | Window function — assigns a rank; tied rows share a rank; next rank is skipped |
| **`ROW_NUMBER()`**             | Window function — always assigns unique numbers; no ties                       |
| **`DENSE_RANK()`**             | Window function — tied rows share a rank; no gaps in sequence                  |
| **`OVER (ORDER BY ... DESC)`** | Defines the window and sort order for the ranking function                     |
| **`WHERE` on CTE column**      | Filters rows from a CTE just like a real table; use `WHERE` not `HAVING` here  |
| **`;`**                        | Statement terminator                                                           |

---

## Common Beginner Mistakes to Avoid

### Mistake 1: Using `ROW_NUMBER()` instead of `RANK()` — silently missing tied results

```sql
-- With ROW_NUMBER() — arbitrarily assigns 3 to one of two tied customers
ROW_NUMBER() OVER (ORDER BY SUM(sales_cost) DESC) AS spending_rank

-- With RANK() — both tied customers get rank 3 and both appear in results
RANK() OVER (ORDER BY SUM(sales_cost) DESC) AS spending_rank
```

---

### Mistake 2: Trying to filter on a window function result using `HAVING`

```sql
-- WRONG — HAVING filters aggregate results, not named CTE columns
SELECT customer_id, total_spend
FROM ranked_customers
HAVING spending_rank = 3

-- CORRECT — spending_rank is a plain column in the CTE; use WHERE
WHERE spending_rank = 3
```

---

### Mistake 3: Forgetting `DESC` in the `OVER(ORDER BY ...)` clause

```sql
-- WRONG — ASC is the default; this ranks lowest spend as rank 1
RANK() OVER (ORDER BY SUM(sales_cost))

-- CORRECT — DESC puts highest spend at rank 1
RANK() OVER (ORDER BY SUM(sales_cost) DESC)
```

Forgetting `DESC` means rank 1 is the _lowest_ spender — the entire ranking is inverted and the business receives completely misleading results.

---

## Extended Business Use Cases

The **CTE + `SUM` + `RANK()`** pattern solves any "find the Nth item in a ranked list" problem — one of the most common requests in business analytics:

| Industry           | Business Question                                           | Rank Applied To           |
| ------------------ | ----------------------------------------------------------- | ------------------------- |
| **Grocery retail** | Who is the 3rd highest spending customer?                   | Customer total spend      |
| **E-commerce**     | What is the 5th best-selling product this month?            | Product total revenue     |
| **Banking**        | Which branch has the 2nd highest loan origination volume?   | Branch loan totals        |
| **Streaming**      | Which show has the 10th most watch hours this week?         | Show total watch time     |
| **Sales team**     | Which sales rep is ranked 4th by deals closed this quarter? | Rep deal count or value   |
| **Supply chain**   | Which supplier is 3rd by total order volume this year?      | Supplier order totals     |
| **HR**             | Which department has the 2nd highest average salary?        | Department average salary |

In every case the competitive advantage is the ability to **monitor rank positions over time**. Running the same query weekly and comparing results reveals movement in the rankings — a customer dropping from rank 3 to rank 8 is an early signal worth investigating; a product rising from rank 10 to rank 2 is a trend worth capitalising on immediately.
