## WINDOW FUNCTIONS

---

### What is a Window Function?

A **window function** performs a calculation across a set of rows that are related to the current row — without collapsing those rows into a single output like `GROUP BY` does. The "window" is the defined set of rows the function operates on.

**Why this matters for staying competitive:**
Every data-driven company — from retail giants to startups — needs to analyse performance _within_ categories (e.g., per product, per region, per customer) while still seeing the full row-level detail. Window functions make this possible in a single query, eliminating the need for slow, complex subqueries or multiple passes over the data.

**Key syntax pattern:**

```sql
<function>() OVER (
    PARTITION BY <column>   -- defines the "window" or group
    ORDER BY <column>       -- defines ordering within the window
)
```

---

### 1. SUM OVER — Transaction Totals & Contribution Percentages

**What it does:**

- `sum(sales_cost) over (partition by transaction_id)` calculates the total sales cost for each transaction while keeping every individual product row intact.
- Dividing `sales_cost` by that window total gives each product's **percentage contribution** to the transaction.

**Business scenario — Retail chain competing on basket analysis:**
A national grocery chain wants to identify which product categories drive the most revenue per transaction. By seeing each item's `transaction_sales_percent`, the merchandising team can spot that, for example, alcohol consistently makes up 40% of high-value baskets — informing promotional bundling strategies to increase average basket size and outcompete rivals.

```sql
SELECT
    *,
    -- Total value of the entire transaction (all items within the same transaction_id)
    SUM(sales_cost) OVER (PARTITION BY transaction_id) AS transaction_total_sales,

    -- Each item's share of the transaction total, expressed as a proportion (0 to 1)
    -- Multiply by 100 to get a percentage
    sales_cost / SUM(sales_cost) OVER (PARTITION BY transaction_id) AS transaction_sales_percent

FROM
    grocery_db.transactions;
```

> **Tip:** The result still returns one row per item. Unlike `GROUP BY`, no rows are collapsed — you get item detail AND the aggregate in the same row. This is a key competitive advantage when building real-time dashboards.

---

### 2. ROW_NUMBER — Sequencing Customer Transactions

**What it does:**
`ROW_NUMBER()` assigns a unique sequential integer to each row within a partition. No two rows in the same partition share the same number, even if they have identical values.

**Business scenario — Personalisation engine at scale:**
An e-commerce company wants to build a personalised email campaign targeting customers based on their _first_ purchase (row 1) versus their most recent purchase (highest row number). Knowing transaction order per customer allows the data team to calculate time-between-purchases, identify churn risk early, and trigger automated win-back campaigns before competitors do.

```sql
SELECT
    *,
    -- Assigns a sequential number to each transaction per customer
    -- ordered by date first, then by transaction_id to break ties on the same date
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY transaction_date, transaction_id
    ) AS transaction_number

FROM
    grocery_db.transactions;
```

> **Note:** `transaction_number = 1` identifies each customer's very first transaction — a powerful signal for new-customer onboarding analysis. Filtering `WHERE transaction_number = 1` gives a clean "first purchase" dataset.

---

### 3. RANK vs ROW_NUMBER — Understanding the Difference

| Function       | Tied rows                        | Gap after ties?               |
| -------------- | -------------------------------- | ----------------------------- |
| `ROW_NUMBER()` | Unique number regardless of ties | No                            |
| `RANK()`       | Same rank for ties               | Yes — skips numbers (1,1,1,4) |
| `DENSE_RANK()` | Same rank for ties               | No — consecutive (1,1,1,2)    |

---

### 4. NTILE — Segmenting Customers into Loyalty Tiers

**What it does:**
`NTILE(n)` divides the ordered result set into `n` roughly equal buckets and assigns each row a bucket number. This is ideal for creating **percentile** or **decile** rankings.

**Business scenario — Loyalty programme optimisation:**
A grocery retailer wants to stay ahead of competitors by targeting its top customers with premium rewards. Using `NTILE(3)`, customers are split into three loyalty tiers (Gold, Silver, Bronze). The marketing team then allocates budget proportionally — spending more on retaining Gold-tier customers who generate the most lifetime value, and designing upgrade campaigns for Silver-tier customers to push them into Gold before a competitor poaches them.

The `NTILE(10)` decile split enables even finer segmentation for the data science team building propensity-to-churn models.

```sql
SELECT
    customer_id,
    customer_loyalty_score,

    -- Splits customers into 3 tiers based on loyalty score (descending)
    -- Tier 1 = highest scorers (Gold), Tier 3 = lowest scorers (Bronze)
    NTILE(3) OVER (ORDER BY customer_loyalty_score DESC) AS loyalty_category,

    -- Splits customers into 10 deciles for more granular ML-based targeting
    -- Decile 1 = top 10% of customers by loyalty score
    NTILE(10) OVER (ORDER BY customer_loyalty_score DESC) AS loyalty_decile

FROM
    grocery_db.loyalty_scores;
```

> **Competitive use case:** Combine this with `SUM(sales_cost)` per tier to quantify how much revenue each loyalty tier generates. If the top 10% (decile 1) accounts for 50%+ of revenue, that is your strategic retention priority.

---

### 5. RANK with PARTITION — Distance-Based Store Catchment Analysis

**Business scenario — Store expansion & competitor benchmarking:**
A grocery chain planning to open new stores needs to understand its current customer catchment area by gender to tailor store layouts and product ranges. Ranking customers by `distance_from_store` (ascending, so rank 1 = closest) and partitioning by gender reveals whether male or female customers travel further — insight used to make geo-targeted advertising decisions and site-selection choices before a competitor opens a nearby location.

**Key requirement:** `RANK()` is used (not `ROW_NUMBER()`) because tied distances should receive the same rank, reflecting real-world fairness in analysis. The gap after ties (1,1,1,4) clearly signals how many customers share that proximity level.

**Filters applied:**

- `distance_from_store IS NOT NULL` — excludes customers with missing location data to avoid skewing the rankings.
- `gender IN ('M', 'F')` — focuses on customers with a recorded gender value.

```sql
/*
  TASK: Rank customers by distance from the store, split by gender.

  Rules:
    - Ascending rank: rank 1 = closest customer to the store
    - Partition by gender so male and female customers are ranked independently
    - Use RANK() so tied distances share the same rank, with a gap after
      (e.g. two customers at rank 1 means the next rank is 3, not 2)
    - Exclude customers with missing distance or gender values
*/

SELECT
    customer_id,
    gender,
    distance_from_store,

    -- RANK() within each gender group, ordered by proximity (closest = rank 1)
    -- Tied distances get the same rank; the count skips forward (1,1,1,4)
    RANK() OVER (
        PARTITION BY gender
        ORDER BY distance_from_store ASC
    ) AS distance_from_store_rank

FROM
    grocery_db.customer_details

WHERE
    gender IN ('M', 'F')
    AND distance_from_store IS NOT NULL;
```

> **Strategic insight:** Filter `WHERE distance_from_store_rank <= 10` (using a CTE or subquery) to identify the ten closest customers per gender — prime targets for a hyper-local loyalty programme or same-day delivery pilot, a capability that directly counters competitor convenience offerings.

---

### Summary — When to Use Each Window Function

| Function         | Best used for                                                       |
| ---------------- | ------------------------------------------------------------------- |
| `SUM() OVER`     | Running totals, contribution percentages, cumulative revenue        |
| `ROW_NUMBER()`   | Deduplication, first/last record identification, sequence numbering |
| `RANK()`         | Leaderboards where ties should share a rank with gaps               |
| `DENSE_RANK()`   | Leaderboards where ties share a rank with no gaps                   |
| `NTILE(n)`       | Customer segmentation, decile/percentile splits, cohort analysis    |
| `LAG() / LEAD()` | Period-over-period comparisons (e.g. month-on-month revenue change) |
