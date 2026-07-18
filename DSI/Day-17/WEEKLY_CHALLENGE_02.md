# Weekly SQL Challenge 02

**Database:** `grocery_db` schema  
**Tables:** `transactions`, `product_areas`

---

## Business Context

You work as a data analyst for a mid-sized grocery chain competing against large retailers like Walmart and Costco. The operations and marketing teams need to understand which product areas are driving the most volume so they can:

- Allocate **shelf space more profitably** — placing the highest-selling categories in prime store positions to maximise basket size
- Focus **promotional campaigns** where customer demand is already strong, increasing conversion rates and protecting margins
- Strengthen **supplier negotiations** — knowing your top volume areas gives you leverage to secure better pricing and priority stock from key suppliers
- **Benchmark against competitors** — if a rival is outperforming you in a high-volume area like Beverages, that gap signals both a threat and an opportunity to win market share

---

## Task

Identify the **top 3 product areas** based on the **highest total number of items sold**.

### Why This Matters

Total items sold is a direct measure of customer demand by category. Combining this with financial data gives leadership a clear picture of where to invest next:

| Dimension            | What it tells us                                                   |
| -------------------- | ------------------------------------------------------------------ |
| Total items sold     | Raw customer demand and footfall by category                       |
| Product area ranking | Which categories anchor the store visit and drive repeat purchases |

The top 3 areas are where the business is winning. Protecting and growing them is essential for **sustainable profitability** — any dip in volume in a top area is an early warning sign worth acting on immediately.

---

## Expected Output

Three rows ordered by `total_items` in **descending order** (highest first).

| Column              | Description                                                     |
| ------------------- | --------------------------------------------------------------- |
| `product_area_name` | Human-readable category name (e.g. Dairy, Bakery, Beverages)    |
| `total_items`       | Total number of items sold across all transactions in that area |

---

## Step 1 — Inspect the Raw Tables

> **Always do this before writing your main query.**  
> Confirms column names, data types, and gives you a feel for the data. Prevents typos and wrong assumptions in the final query.

```sql
-- Returns every column and row from the transactions table.
-- Look for: transaction_id, customer_id, product_area_id, num_items, transaction_date.
SELECT * FROM grocery_db.transactions;

-- Returns every column and row from the product_areas lookup table.
-- Look for: product_area_id (the numeric key) and product_area_name (the label).
SELECT * FROM grocery_db.product_areas;
```

---

## Step 2 — The Main Analytical Query

```sql
SELECT
    b.product_area_name,
    SUM(a.num_items) AS total_items
FROM
    grocery_db.transactions a
    INNER JOIN grocery_db.product_areas b ON a.product_area_id = b.product_area_id
GROUP BY
    b.product_area_name
ORDER BY
    total_items DESC
LIMIT 3;
```

---

## Line-by-Line Explanation

### SELECT — Choosing the Output Columns

```sql
SELECT
    b.product_area_name,
    SUM(a.num_items) AS total_items
```

| Line                              | What it does                                                                                                                                                                                                                                                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `b.product_area_name`             | Retrieves the human-readable category label (e.g. "Dairy") from the `product_areas` table. The `b.` prefix uses the table alias defined in `FROM`. Without the join this would only be a numeric ID — meaningless to business users.                                          |
| `SUM(a.num_items) AS total_items` | `SUM()` is an **aggregate function** — it adds up every `num_items` value for all transactions belonging to the same product area (after `GROUP BY` is applied). `AS total_items` gives the result a clear, readable column name instead of displaying the raw function call. |

---

### FROM and INNER JOIN — Combining the Two Tables

```sql
FROM
    grocery_db.transactions a
    INNER JOIN grocery_db.product_areas b ON a.product_area_id = b.product_area_id
```

| Concept                                    | Explanation                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grocery_db.transactions a`                | The primary (driving) table. Each row represents one product line in a customer's basket. `a` is a **table alias** — a short nickname so we don't repeat the full table name on every column reference.                                                                                                                                              |
| `INNER JOIN`                               | Returns only rows that have a matching record in **both** tables (the overlap in a Venn diagram). Transactions with an unrecognised `product_area_id` and product areas with no transactions are both excluded, keeping results clean.                                                                                                               |
| `ON a.product_area_id = b.product_area_id` | The **join condition** — the bridge between the two tables. `a.product_area_id` is the numeric foreign key on each transaction; `b.product_area_id` is the primary key in the lookup table. Without this condition, the database would pair every transaction with every product area, producing millions of meaningless rows (a cartesian product). |

---

### GROUP BY — Collapsing Rows into Summaries

```sql
GROUP BY
    b.product_area_name
```

Before `GROUP BY`, the result has one row per transaction — potentially millions of rows. `GROUP BY` merges all rows that share the same `product_area_name` into a **single summary row**, which is what makes `SUM()` meaningful.

> **Analogy:** Think of sorting every receipt in the store into labelled folders — one folder per product area — then counting the total items across all receipts in each folder.

> **Rule:** every column in `SELECT` that is **not** inside an aggregate function (`SUM`, `COUNT`, `AVG`, etc.) **must** appear in `GROUP BY`. Here `product_area_name` is the only plain column, so it is the only one listed.

---

### ORDER BY — Sorting the Results

```sql
ORDER BY
    total_items DESC
```

| Part                   | What it does                                                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ORDER BY total_items` | Sorts the grouped results by the `total_items` alias defined in `SELECT`. SQL allows referencing aliases in `ORDER BY`.                                 |
| `DESC`                 | **Descending** order — the product area with the **most** items sold appears first (rank #1 at the top). Ascending (`ASC`) would show the lowest first. |

**Business value:** decision-makers expect a ranked list — "show me the best performers first." Descending order makes the top opportunities immediately visible without manual scanning.

---

### LIMIT — Capping the Number of Rows Returned

```sql
LIMIT 3;
```

Returns only the first 3 rows **after sorting** — i.e. the top 3 product areas by items sold.

> **Why 3?** The business question asks specifically for the top 3 so leadership can focus resources on a manageable shortlist. In a real-world dashboard this number is often a parameter users can adjust (e.g. top 5 or top 10).

> **Important:** `LIMIT` is applied **after** `ORDER BY`, so the 3 rows kept are guaranteed to be the highest-ranked ones.

---

## Query Execution Order

Understanding the order in which the database processes each clause helps you write correct filters and debug unexpected results.

| Step | Clause     | What happens                                                        |
| ---- | ---------- | ------------------------------------------------------------------- |
| 1    | `FROM`     | Load the `transactions` table                                       |
| 2    | `JOIN`     | Combine with `product_areas` on matching `product_area_id`          |
| 3    | `WHERE`    | _(not used here, but would filter individual rows at this stage)_   |
| 4    | `GROUP BY` | Collapse all transaction rows into one row per `product_area_name`  |
| 5    | `HAVING`   | _(not used here, but would filter aggregated groups at this stage)_ |
| 6    | `SELECT`   | Pick the output columns and calculate the `SUM` alias               |
| 7    | `ORDER BY` | Sort the groups by `total_items` descending                         |
| 8    | `LIMIT`    | Keep only the top 3 rows                                            |

> **Common beginner mistake:** trying to filter on `total_items` inside a `WHERE` clause. This fails because `WHERE` runs at step 3 — before `SUM()` is calculated at step 6. Use `HAVING` to filter on aggregated values.

---

## Business Decisions This Query Enables

The result is a ranked shortlist of the three categories driving the most customer volume — a direct input to strategy.

### Operations & Merchandising Team

- Assign **premium shelf positions and aisle frontage** to the top 3 areas to maximise visibility and impulse purchases
- Schedule more frequent **stock replenishment** in high-volume areas to eliminate costly out-of-stock events
- Use the ranking to brief buyers on which **supplier relationships** to prioritise in the next contract cycle

### Marketing Team

- Design **cross-category promotions** around the top areas (e.g. a Dairy + Bakery bundle deal) to increase average basket size
- Build **lookalike customer audiences** who buy heavily in these areas and target them for acquisition campaigns
- Monitor month-on-month shifts in the ranking — a category dropping out of the top 3 is an early warning sign requiring immediate investigation

### Finance & Strategy Team

- Allocate **capital expenditure** (refrigeration, shelving, staffing) proportionally to where volume is highest
- Set **revenue forecasts** anchored to top-area volume trends rather than guessing from overall store data
- If a competitor is outperforming in one of the top 3 areas, quantify the revenue gap and model whether a targeted investment would be profitable — directly linking SQL analysis to competitive strategy and profitability decisions
