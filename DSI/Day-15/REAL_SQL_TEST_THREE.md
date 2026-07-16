# SQL Test 3 — Grocery Retail Analytics

## Database Schema Reference

```
grocery_db.loyalty_scores      (customer_id, customer_loyalty_score)
grocery_db.customer_details    (customer_id, gender, distance_from_store, ...)
grocery_db.transactions        (transaction_id, customer_id, product_area_id, sales_cost, ...)
grocery_db.product_areas       (product_area_id, product_area_name)
```

> **Context:** A grocery retail chain wants to use data to stay ahead of competitors,
> improve customer retention, drive targeted marketing, and make smarter stock and
> store decisions. Every query below is a tool for achieving one or more of those goals.

---

## Query 01 — Filter High-Value Loyalty Customers by Exact Score

### Business Scenario

The marketing team wants to hand-pick customers sitting at specific loyalty score
thresholds (0.77, 0.88, 0.99) to send them a personalised upgrade offer — e.g.,
inviting them into a premium "Gold Card" tier. Instead of emailing the entire
customer base (costly, low ROI), the company targets only those who are already
close to elite status. This is a classic **precision-targeting** strategy used to
improve conversion rates and reduce marketing spend.

### SQL

```sql
SELECT *
FROM grocery_db.loyalty_scores
WHERE customer_loyalty_score IN (0.77, 0.88, 0.99);
```

### Line-by-Line Explanation

| Line | Code                                                 | What it does                                                                                                                                                                       |
| ---- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `SELECT *`                                           | Retrieve **all columns** from the table. The `*` means "everything" — customer_id, loyalty_score, and any other columns that exist.                                                |
| 2    | `FROM grocery_db.loyalty_scores`                     | Tells SQL to read from the `loyalty_scores` table inside the `grocery_db` database. The dot notation `database.table` is used when your SQL server hosts multiple databases.       |
| 3    | `WHERE customer_loyalty_score IN (0.77, 0.88, 0.99)` | Filters to only keep rows where the score exactly matches one of those three values. `IN (...)` is shorthand for `= 0.77 OR = 0.88 OR = 0.99` — it is cleaner and faster to write. |

### Sample Data & Result

**loyalty_scores table (before filter):**

```
+-------------+------------------------+
| customer_id | customer_loyalty_score |
+-------------+------------------------+
| 1001        | 0.55                   |
| 1002        | 0.77                   |  ← included
| 1003        | 0.88                   |  ← included
| 1004        | 0.62                   |
| 1005        | 0.99                   |  ← included
+-------------+------------------------+
```

**Result after WHERE IN filter:**

```
+-------------+------------------------+
| customer_id | customer_loyalty_score |
+-------------+------------------------+
| 1002        | 0.77                   |
| 1003        | 0.88                   |
| 1005        | 0.99                   |
+-------------+------------------------+
```

---

### Bonus Query — Count Unique Transactions

```sql
SELECT COUNT(DISTINCT transaction_id) AS trans_count
FROM grocery_db.transactions;
```

**What each part does:**

| Part                      | Explanation                                                                                                                                                                                    |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `COUNT(...)`              | Counts the number of rows that match the expression inside.                                                                                                                                    |
| `DISTINCT transaction_id` | Before counting, remove any duplicate `transaction_id` values. This ensures each transaction is counted only once, even if it appears in multiple rows (e.g., multiple items per transaction). |
| `AS trans_count`          | Renames the output column to `trans_count` instead of the default ugly heading `COUNT(DISTINCT transaction_id)`.                                                                               |

**Business use:** A quick sanity check on the size of your transactions dataset, or a
KPI dashboard figure showing total unique purchases in a period.

---

## Query 02 — Average Loyalty Score Split by Gender

### Business Scenario

The loyalty team suspects that loyalty programme engagement differs between male and
female customers. By comparing average scores, the company can:

- **Identify the under-engaged group** and build a targeted re-engagement campaign.
- **Justify budget allocation** — spend more on re-engaging the lower-scoring gender.
- **Benchmark over time** — run this query monthly to see if campaigns are working.

This is a fundamental **segmentation** query. Competitors who do not segment waste
budget on blanket campaigns; this company can be surgical.

### SQL

```sql
SELECT
    b.gender,                              -- the grouping column
    AVG(a.customer_loyalty_score) AS avg_loyalty_score  -- the metric per group

FROM
    grocery_db.loyalty_scores a            -- main table, aliased as 'a'
    INNER JOIN grocery_db.customer_details b  -- joined table, aliased as 'b'
        ON a.customer_id = b.customer_id   -- the link between the two tables

GROUP BY
    b.gender;                              -- collapse rows into gender groups
```

### Line-by-Line Explanation

| Line | Code                                                 | What it does                                                                                                                                                                                                                   |
| ---- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | `SELECT b.gender`                                    | Pick the `gender` column from the `customer_details` table (aliased `b`). The prefix `b.` specifies which table the column comes from — needed because two joined tables might have columns with the same name.                |
| 2    | `AVG(a.customer_loyalty_score) AS avg_loyalty_score` | Calculate the mathematical average of all loyalty scores within each gender group. `AS avg_loyalty_score` gives the result column a readable name.                                                                             |
| 3    | `FROM grocery_db.loyalty_scores a`                   | Read from `loyalty_scores`, giving it the short alias `a` to avoid typing the full name repeatedly.                                                                                                                            |
| 4    | `INNER JOIN grocery_db.customer_details b`           | Bring in the `customer_details` table (aliased `b`). `INNER JOIN` means: only keep rows where a match exists in **both** tables — customers with no loyalty record, or loyalty records with no customer profile, are excluded. |
| 5    | `ON a.customer_id = b.customer_id`                   | The join condition — the glue. SQL matches rows where the `customer_id` value is the same in both tables.                                                                                                                      |
| 6    | `GROUP BY b.gender`                                  | After the join, collapse all rows for the same gender into one summary row. This is what makes `AVG()` compute per-gender rather than for the whole table.                                                                     |

### Sample Data & Result

**After JOIN (combined data):**

```
+-------------+--------+------------------------+
| customer_id | gender | customer_loyalty_score |
+-------------+--------+------------------------+
| 1001        | Female | 0.55                   |
| 1002        | Male   | 0.77                   |
| 1003        | Female | 0.88                   |
| 1004        | Male   | 0.62                   |
| 1005        | Female | 0.99                   |
+-------------+--------+------------------------+
```

**After GROUP BY gender + AVG:**

```
+--------+-------------------+
| gender | avg_loyalty_score |
+--------+-------------------+
| Female | 0.807             |  (0.55 + 0.88 + 0.99) / 3
| Male   | 0.695             |  (0.77 + 0.62) / 2
+--------+-------------------+
```

**Business insight:** Female customers are on average ~11% more loyal. The company
should investigate why male loyalty is lower and design a campaign to close the gap.

---

## Query 03 — Tag Customers by Distance from Store (CASE WHEN)

### Business Scenario

The operations team wants to understand the store's catchment area. Knowing whether
customers walk or drive helps the business:

- **Decide where to open new stores** — if most customers drive 5+ miles, a new
  local branch could steal share from a competitor.
- **Tailor promotions** — walkers might respond to "drop in today" flash deals;
  drivers might need bigger planned-purchase incentives.
- **Plan delivery zones** — customers who are far away are prime candidates for a
  home delivery upsell.

### SQL

```sql
SELECT
    customer_id,
    distance_from_store,
    CASE
        WHEN distance_from_store IS NULL THEN 'Unknown'
        WHEN distance_from_store < 1     THEN 'Walking Distance'
        WHEN distance_from_store >= 1    THEN 'Driving Distance'
        ELSE 'Other'
    END AS distance_category

FROM grocery_db.customer_details;
```

### Line-by-Line Explanation

| Line | Code                                                    | What it does                                                                                                                                                                                         |
| ---- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `SELECT customer_id`                                    | Return the unique customer identifier so we know which customer each row belongs to.                                                                                                                 |
| 2    | `distance_from_store`                                   | Return the raw distance value as well, so analysts can see the exact number alongside the category.                                                                                                  |
| 3    | `CASE`                                                  | Opens a conditional block — SQL's equivalent of `if / else if / else`. SQL evaluates each `WHEN` condition from top to bottom and stops at the first one that is true.                               |
| 4    | `WHEN distance_from_store IS NULL THEN 'Unknown'`       | **Must be checked first.** `IS NULL` tests for missing data. If we checked `< 1` first, a NULL value would not match and would fall through to `ELSE` — we explicitly handle it upfront for clarity. |
| 5    | `WHEN distance_from_store < 1 THEN 'Walking Distance'`  | If the distance is less than 1 mile, tag the customer as a walker.                                                                                                                                   |
| 6    | `WHEN distance_from_store >= 1 THEN 'Driving Distance'` | If the distance is 1 mile or more, tag as a driver.                                                                                                                                                  |
| 7    | `ELSE 'Other'`                                          | A safety net for any value that didn't match the above conditions. Good practice to always include `ELSE`.                                                                                           |
| 8    | `END AS distance_category`                              | Closes the `CASE` block and names the resulting column `distance_category`.                                                                                                                          |
| 9    | `FROM grocery_db.customer_details`                      | Source table containing customer location data.                                                                                                                                                      |

### Sample Data & Result

**customer_details (input):**

```
+-------------+---------------------+
| customer_id | distance_from_store |
+-------------+---------------------+
| 1001        | 0.3                 |
| 1002        | 2.7                 |
| 1003        | NULL                |
| 1004        | 0.9                 |
| 1005        | 5.1                 |
+-------------+---------------------+
```

**Result:**

```
+-------------+---------------------+-------------------+
| customer_id | distance_from_store | distance_category |
+-------------+---------------------+-------------------+
| 1001        | 0.3                 | Walking Distance  |
| 1002        | 2.7                 | Driving Distance  |
| 1003        | NULL                | Unknown           |
| 1004        | 0.9                 | Walking Distance  |
| 1005        | 5.1                 | Driving Distance  |
+-------------+---------------------+-------------------+
```

**Business insight:** 40% of customers are within walking distance. A "no-car needed"
campaign or a loyalty points bonus for frequent small visits could capture daily
footfall that competitors are missing.

---

## Query 04 — Divide Customers into Loyalty Deciles (CTE + NTILE Window Function)

### Business Scenario

Rather than treating all 400 loyalty customers as one group, the company divides them
into 10 equal bands (deciles) ranked from most to least loyal. For each decile, it
then calculates the average distance from the store. This reveals a critical insight:

> _"Do our most loyal customers live closest to us? Or are highly loyal customers
> spread far away — suggesting our brand has strong pull even over distance?"_

This drives decisions like:

- **Decile 1 (most loyal):** Are they close? Reward them with in-store perks. Are
  they far? Consider delivery incentives to keep them loyal despite competitors nearby.
- **Decile 10 (least loyal):** Are they far away? They may be defecting to a
  closer competitor — a targeted win-back campaign could recover them.
- **Competitor benchmarking:** If a rival opens a new branch 0.5 miles from your
  Decile 8–10 customers, you can model churn risk immediately.

### SQL

```sql
-- Step 1: CTE — build a named temporary dataset
WITH loyalty_info AS (

    SELECT
        a.customer_id,
        a.customer_loyalty_score,
        NTILE(10) OVER (ORDER BY a.customer_loyalty_score DESC) AS loyalty_decile,
        b.distance_from_store

    FROM
        grocery_db.loyalty_scores a
        INNER JOIN grocery_db.customer_details b
            ON a.customer_id = b.customer_id
)

-- Step 2: Main query — aggregate the temporary dataset
SELECT
    loyalty_decile,
    AVG(distance_from_store) AS avg_distance

FROM
    loyalty_info

GROUP BY
    loyalty_decile;
```

### Line-by-Line Explanation

#### CTE Block (`WITH loyalty_info AS (...)`)

| Line | Code                                                                        | What it does                                                                                                                                                                                                                                                                                                                                                       |
| ---- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | `WITH loyalty_info AS (`                                                    | Opens a **Common Table Expression (CTE)** — a named temporary result set. Think of it as creating a temporary table just for this query. It makes complex queries readable by splitting them into logical steps.                                                                                                                                                   |
| 2    | `SELECT a.customer_id`                                                      | Retrieve each customer's unique ID from the loyalty table.                                                                                                                                                                                                                                                                                                         |
| 3    | `a.customer_loyalty_score`                                                  | Retrieve the raw loyalty score so we can see what score each decile boundary falls on.                                                                                                                                                                                                                                                                             |
| 4    | `NTILE(10) OVER (ORDER BY a.customer_loyalty_score DESC) AS loyalty_decile` | **The heart of this query.** `NTILE(10)` is a **window function** that splits all rows into 10 equal-sized groups (buckets). `ORDER BY ... DESC` ranks customers from highest to lowest score first, so Decile 1 = most loyal, Decile 10 = least loyal. `OVER (...)` defines the "window" — here, the entire result set. `AS loyalty_decile` names the new column. |
| 5    | `b.distance_from_store`                                                     | Pull in the distance from the `customer_details` table (joined below).                                                                                                                                                                                                                                                                                             |
| 6    | `FROM grocery_db.loyalty_scores a`                                          | Start with the loyalty table, alias `a`.                                                                                                                                                                                                                                                                                                                           |
| 7    | `INNER JOIN grocery_db.customer_details b ON a.customer_id = b.customer_id` | Join in the customer details. Only customers present in **both** tables are included (inner join).                                                                                                                                                                                                                                                                 |
| 8    | `)`                                                                         | Closes the CTE definition. The result of everything inside is now accessible as a virtual table named `loyalty_info`.                                                                                                                                                                                                                                              |

#### Main Query Block

| Line | Code                                       | What it does                                                                                                                       |
| ---- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| 9    | `SELECT loyalty_decile`                    | Pick the decile number (1–10) as the grouping column.                                                                              |
| 10   | `AVG(distance_from_store) AS avg_distance` | For each decile group, calculate the mean distance from the store across all customers in that group.                              |
| 11   | `FROM loyalty_info`                        | Read from the CTE we just defined — not from the raw tables. This is what makes CTEs powerful: you query the pre-processed result. |
| 12   | `GROUP BY loyalty_decile`                  | Collapse all customers in the same decile into one row so `AVG()` produces a single figure per decile.                             |

### Sample Result

```
+----------------+--------------+
| loyalty_decile | avg_distance |
+----------------+--------------+
| 1              | 0.8          |  Most loyal — live very close
| 2              | 1.1          |
| 3              | 1.4          |
| 4              | 1.9          |
| 5              | 2.3          |
| 6              | 2.8          |
| 7              | 3.2          |
| 8              | 3.7          |
| 9              | 4.1          |
| 10             | 5.0          |  Least loyal — live furthest away
+----------------+--------------+
```

**Business insight:** There is a clear pattern — loyalty **decreases as distance
increases**. This confirms that proximity is a key driver of loyalty, and that
customers in Deciles 8–10 are at high risk of switching to a closer competitor.
The business should investigate opening a new location or launching delivery in
those high-distance postcodes.

---

## Query 05 — Revenue Share by Product Area (CTE + Subquery Percentage)

### Business Scenario

The category management team needs to know which product areas (e.g., Produce, Bakery,
Meat, Dairy) generate the most revenue — and critically, **what percentage of the
total** each one represents. This drives:

- **Shelf space allocation:** Give more prime shelf space to the highest-earning
  categories to maximise revenue per square foot.
- **Supplier negotiation:** If Produce is 35% of revenue, the business has leverage
  to negotiate better terms with produce suppliers.
- **Competitive gap analysis:** If a rival chain is known for its Bakery, and your
  Bakery is only 5% of revenue, there is a strategic opportunity to invest there.
- **Promotional budget split:** Allocate marketing spend proportional to (or
  strategically counter to) each category's revenue share.

### SQL

```sql
-- Step 1: CTE — calculate total sales per product area
WITH sales AS (

    SELECT
        b.product_area_name,
        SUM(a.sales_cost) AS total_sales

    FROM
        grocery_db.transactions a
        INNER JOIN grocery_db.product_areas b
            ON a.product_area_id = b.product_area_id

    GROUP BY
        b.product_area_name
)

-- Step 2: Main query — add the percentage column
SELECT
    product_area_name,
    total_sales,
    total_sales / (SELECT SUM(total_sales) FROM sales) AS total_sales_pc

FROM
    sales;
```

### Line-by-Line Explanation

#### CTE Block (`WITH sales AS (...)`)

| Line | Code                                                                             | What it does                                                                                                                                                                 |
| ---- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `WITH sales AS (`                                                                | Opens a CTE named `sales`. This will hold one row per product area with its summed revenue.                                                                                  |
| 2    | `SELECT b.product_area_name`                                                     | Retrieve the human-readable product area name (e.g., "Produce", "Bakery") from the `product_areas` table.                                                                    |
| 3    | `SUM(a.sales_cost) AS total_sales`                                               | Add up all individual transaction costs (`sales_cost`) for each product area. Each row in `transactions` is one purchase; `SUM` collapses them into a single total per area. |
| 4    | `FROM grocery_db.transactions a`                                                 | Start from the transactions table (aliased `a`) — this is the fact table containing every sale.                                                                              |
| 5    | `INNER JOIN grocery_db.product_areas b ON a.product_area_id = b.product_area_id` | Join in the `product_areas` table to get the name of each area. Without this join, you would only have numeric IDs, not readable names.                                      |
| 6    | `GROUP BY b.product_area_name`                                                   | Collapse all transactions belonging to the same product area into one row so `SUM` produces a single total per area.                                                         |
| 7    | `)`                                                                              | Closes the CTE. The result is a small table with one row per product area and its total sales figure.                                                                        |

#### Main Query Block

| Line | Code                                                                   | What it does                                                                                                                                                                                                                                                                                                               |
| ---- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 8    | `SELECT product_area_name`                                             | Display the product area name in the final output.                                                                                                                                                                                                                                                                         |
| 9    | `total_sales`                                                          | Display the raw total sales figure for that area.                                                                                                                                                                                                                                                                          |
| 10   | `total_sales / (SELECT SUM(total_sales) FROM sales) AS total_sales_pc` | **The percentage calculation.** The inner `(SELECT SUM(total_sales) FROM sales)` is a **scalar subquery** — it runs as a single calculation and returns one number: the grand total across all product areas. Dividing each area's `total_sales` by this grand total gives a decimal between 0 and 1 (e.g., `0.35` = 35%). |
| 11   | `FROM sales`                                                           | Read from the CTE `sales` defined above — not the raw tables.                                                                                                                                                                                                                                                              |

> **Tip:** To display as a percentage, wrap in `ROUND(... * 100, 2)`:
>
> ```sql
> ROUND(total_sales / (SELECT SUM(total_sales) FROM sales) * 100, 2) AS total_sales_pct
> ```

### Sample Data & Result

**transactions (raw — millions of rows):**

```
+----------------+-------------+--------------+
| transaction_id | product_area_id | sales_cost |
+----------------+-------------+--------------+
| T001           | 1           | 12.50        |
| T002           | 2           | 5.00         |
| T003           | 1           | 8.00         |
| T004           | 3           | 22.00        |
+----------------+-------------+--------------+

product_areas:
+----------------+-------------------+
| product_area_id| product_area_name |
+----------------+-------------------+
| 1              | Produce           |
| 2              | Bakery            |
| 3              | Meat              |
+----------------+-------------------+
```

**CTE `sales` result:**

```
+-------------------+-------------+
| product_area_name | total_sales |
+-------------------+-------------+
| Produce           | 20.50       |
| Bakery            |  5.00       |
| Meat              | 22.00       |
+-------------------+-------------+
Grand total = 47.50
```

**Final result:**

```
+-------------------+-------------+----------------+
| product_area_name | total_sales | total_sales_pc |
+-------------------+-------------+----------------+
| Meat              | 22.00       | 0.463  (46.3%) |
| Produce           | 20.50       | 0.432  (43.2%) |
| Bakery            |  5.00       | 0.105  (10.5%) |
+-------------------+-------------+----------------+
```

**Business insight:** Bakery contributes only 10.5% of revenue despite likely having
significant shelf space. This is an actionable signal — either cut shelf allocation
and redirect space to Meat/Produce, or launch a Bakery promotional campaign to grow
its share and compete with rival chains that are known for their fresh bread.

---

## Key Concepts Summary

| Concept                           | What it does                                  | When to use it                                                  |
| --------------------------------- | --------------------------------------------- | --------------------------------------------------------------- |
| `SELECT *`                        | Retrieve all columns                          | Exploratory queries; avoid in production (slow on large tables) |
| `IN (...)`                        | Match any value in a list                     | Cleaner alternative to multiple `OR` conditions                 |
| `COUNT(DISTINCT ...)`             | Count unique values only                      | Avoid double-counting (e.g., customers with multiple orders)    |
| `INNER JOIN`                      | Combine tables, keep only matched rows        | When you only want records that exist in both tables            |
| `GROUP BY`                        | Collapse rows into groups for aggregation     | Any time you use SUM, COUNT, AVG on a subset                    |
| `AVG()`                           | Calculate the mean of a set of values         | KPI dashboards, benchmarking, segmentation                      |
| `CASE WHEN`                       | Conditional logic — if/else inside SQL        | Creating labels, segments, or bucketed categories               |
| `WITH ... AS` (CTE)               | Define a named temporary result set           | Breaking complex queries into readable steps                    |
| `NTILE(n) OVER (...)`             | Divide rows into n equal-sized ranked buckets | Decile/quartile analysis for segmentation                       |
| `SUM() OVER ()` / scalar subquery | Compute a grand total to use in a percentage  | Revenue share, market share calculations                        |
| `IS NULL`                         | Test for missing/unknown data                 | Always handle NULLs explicitly in CASE WHEN                     |
