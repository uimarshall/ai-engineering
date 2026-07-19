# Weekly SQL Challenge 08

## Overview

**Data:** `grocery_db` schema data tables  
**Tables used:** `grocery_db.customer_details`, `grocery_db.loyalty_scores`

---

## The Task

Calculate the **average loyalty score for customers, broken down by gender**.

**Special rule:** For customers who do **not** have a loyalty score in the `loyalty_scores` table, assign a **default score of 0.5** before calculating the average.

**Expected Output:** One row per gender with two columns:

| gender | average_loyalty_score |
| ------ | --------------------- |
| F      | 0.63                  |
| M      | 0.58                  |
| NULL   | 0.51                  |

---

## Business Context & Why This Matters

You are a data analyst at a grocery retail chain. The **Customer Experience & Loyalty** team wants to understand whether loyalty levels differ meaningfully between male and female customers — and whether the loyalty programme is being used as a true retention tool or just as a passive points collector.

Why does this matter competitively?

- **Loyalty scores are a predictive signal.** A customer with a high loyalty score visits more frequently, spends more per visit, and is significantly less likely to switch to a competitor. Knowing which gender segment has a lower average loyalty score reveals where the business has the most room to improve.
- **Gender-targeted loyalty strategy:** If female customers score consistently higher than male customers, the business can investigate _why_ — perhaps the current rewards are more relevant to one demographic — and redesign the programme to boost engagement in the lower-scoring group.
- **The default score of 0.5 matters strategically.** Customers with no loyalty score at all are likely newer or less engaged customers who have not yet triggered a score calculation. Assigning them 0.5 (the midpoint of 0–1) rather than excluding them prevents the average from being artificially inflated by only counting "active" scorers. It gives a more honest, **complete picture** of loyalty across the entire customer base.
- **Competitive benchmarking:** If the overall average loyalty score drops quarter-on-quarter, it may indicate that a competitor has launched an attractive counter-offer. Acting early — before churn data confirms the problem — is a critical advantage.

This query is the entry point to a loyalty health dashboard, feeding decisions on:

1. Which gender to prioritise in the next loyalty programme refresh.
2. Whether to invest in converting "no-score" customers into active loyalty participants.
3. How to allocate personalised reward budgets by segment to maximise retention ROI.

---

## The SQL Query (Fully Annotated)

```sql
SELECT
    a.gender,                                                    -- Line 1
    AVG(COALESCE(b.customer_loyalty_score, 0.5))                 -- Line 2
        AS average_loyalty_score

FROM
    grocery_db.customer_details a                                -- Line 3
    LEFT JOIN grocery_db.loyalty_scores b                        -- Line 4
        ON a.customer_id = b.customer_id                         -- Line 5

GROUP BY
    a.gender;                                                    -- Line 6
```

---

## Line-by-Line Explanation

---

### Line 1 — `a.gender`

```sql
a.gender,
```

- Selects the `gender` column from `customer_details` (aliased `a`).
- This is the **grouping dimension** — the query produces one output row for each unique value of `gender`.
- Possible values typically include `'M'`, `'F'`, and `NULL` (for customers whose gender was not recorded). Unlike Challenge 07, there is **no `IS NOT NULL` filter** here — the task asks for an average for each gender value including NULL, so all customers are included.
- **Beginner tip:** A `NULL` gender will form its own group in `GROUP BY`. In the output, that group represents customers with no recorded gender — still useful for completeness, though the business may choose to exclude them in downstream reporting.
- **Business purpose:** The split by gender is the strategic lens — it reveals whether loyalty programme engagement differs between demographic groups, driving targeted programme design decisions.

---

### Line 2 — `AVG(COALESCE(b.customer_loyalty_score, 0.5)) AS average_loyalty_score`

```sql
AVG(COALESCE(b.customer_loyalty_score, 0.5)) AS average_loyalty_score
```

This is the most technically significant line in the query. It nests two functions together. Work from the inside out:

---

#### Inner function: `COALESCE(b.customer_loyalty_score, 0.5)`

```sql
COALESCE(b.customer_loyalty_score, 0.5)
```

- `COALESCE()` is a **NULL-handling function**. It accepts two or more arguments and returns the **first non-NULL value** it encounters, reading left to right.
- Here:
  - If `b.customer_loyalty_score` exists (is not NULL) → return that score (e.g., `0.74`).
  - If `b.customer_loyalty_score` is NULL (because the customer has no record in `loyalty_scores`, which happens for unmatched rows in a `LEFT JOIN`) → return `0.5` as the default.
- The result is a column that **never contains NULL** — every customer has either their real score or the fallback of `0.5`.

**Why is `COALESCE` necessary here?**

Without it, `AVG()` would **silently ignore NULL values** — SQL's `AVG` function skips NULLs by design. That means customers without a loyalty score would be excluded from the average entirely. The result would only reflect engaged, scored customers — not the full customer base. The task explicitly requires unscored customers to be counted as `0.5`, so `COALESCE` enforces this inclusion.

**`COALESCE` with more than two arguments:**

```sql
COALESCE(score_column, backup_column, 0.5)
-- Returns: score_column if not NULL, else backup_column if not NULL, else 0.5
```

You can chain as many fallbacks as needed.

- **Beginner tip:** `COALESCE` is one of the most frequently used functions in production SQL. Whenever you see a `LEFT JOIN` that might produce NULLs in the right-hand table, ask yourself: _"Do I need to replace those NULLs with a default value?"_ If yes, wrap the column in `COALESCE`.

---

#### Outer function: `AVG(...)`

```sql
AVG(COALESCE(b.customer_loyalty_score, 0.5))
```

- `AVG()` is an **aggregate function** that calculates the arithmetic mean of all values within a group.
- Because `COALESCE` has already replaced all NULLs with `0.5`, `AVG()` now receives a complete set of values — real scores for scored customers, and `0.5` for unscored customers.
- The result is the **true average** across the entire gender group, not just the subset with existing scores.
- `AS average_loyalty_score` gives the computed column a clean, descriptive name.

**The mathematical impact of including the default:**

Imagine a gender group of 100 customers:

- 70 have a real loyalty score averaging `0.75`
- 30 have no score → default `0.5`

| Approach                            | Calculation                            | Result                                   |
| ----------------------------------- | -------------------------------------- | ---------------------------------------- |
| Without `COALESCE` (NULLs excluded) | AVG of 70 scores = `0.75`              | **Overstated** — misses 30% of customers |
| With `COALESCE` (all 100 included)  | (70 × 0.75 + 30 × 0.5) / 100 = `0.675` | **Accurate** — reflects the full base    |

The difference can significantly skew business decisions if not handled correctly.

---

### Line 3 — `FROM grocery_db.customer_details a`

```sql
FROM grocery_db.customer_details a
```

- Sets `customer_details` as the **primary (left) table**, aliased `a`.
- This table is the **authoritative customer list** — every customer the business knows about, regardless of whether they have a loyalty score.
- Critically, this table is the LEFT side of the `LEFT JOIN` — which means **every row here is preserved** in the output, even if no match is found in `loyalty_scores`.
- **Business purpose:** Ensures the analysis covers the complete customer base, not just those already enrolled in the loyalty programme. Complete coverage gives a more honest average and prevents a survivorship bias in the metric.

---

### Lines 4–5 — `LEFT JOIN grocery_db.loyalty_scores b ON a.customer_id = b.customer_id`

```sql
LEFT JOIN grocery_db.loyalty_scores b
    ON a.customer_id = b.customer_id
```

This is the most strategically important structural decision in the query. Understanding why `LEFT JOIN` is used instead of `INNER JOIN` is essential.

---

#### `LEFT JOIN` vs `INNER JOIN` — the critical distinction

| Join Type    | Keeps rows from left table with no match? | Result for unmatched rows                                           |
| ------------ | ----------------------------------------- | ------------------------------------------------------------------- |
| `INNER JOIN` | No — drops them                           | Only customers WITH a loyalty score appear                          |
| `LEFT JOIN`  | **Yes — keeps all**                       | Customers WITHOUT a score appear with NULL in loyalty score columns |

**If you used `INNER JOIN` here:**

- Only customers who _have_ a record in `loyalty_scores` would appear.
- Customers with no loyalty score would be silently dropped.
- The average would only reflect scored customers — a biased, incomplete metric.
- The `COALESCE` default of `0.5` would never be triggered because there would be no NULL rows to replace.

**With `LEFT JOIN`:**

- Every customer in `customer_details` appears in the result.
- Customers with no matching row in `loyalty_scores` appear with `NULL` in the `b.customer_loyalty_score` column.
- `COALESCE` then replaces those NULLs with `0.5` before `AVG` computes the mean.
- The result is a complete, unbiased average across all customers.

**`LEFT JOIN` visualised:**

```
customer_details (LEFT)    loyalty_scores (RIGHT)
─────────────────────────  ──────────────────────
customer_id = 1001    ───► loyalty_score = 0.82   ✓ matched
customer_id = 1002    ───► loyalty_score = 0.65   ✓ matched
customer_id = 1003    ───► (no record)             → NULL in output
customer_id = 1004    ───► loyalty_score = 0.91   ✓ matched
```

Customer 1003 stays in the result with `NULL` for the score — then `COALESCE` converts that NULL to `0.5`.

- `ON a.customer_id = b.customer_id` — the join condition, linking the two tables via the shared `customer_id` key.
- **Beginner tip:** The rule of thumb for choosing join type: _"Do I want to keep all rows from the left table, even when there is no match on the right?"_ If yes → `LEFT JOIN`. If you only want matched rows → `INNER JOIN`.
- **Business purpose:** Ensures every customer is represented in the loyalty average, including those who have never engaged with the loyalty programme — the most important group to understand and potentially convert.

---

### Line 6 — `GROUP BY a.gender;`

```sql
GROUP BY a.gender;
```

- `GROUP BY` **bundles all rows with the same gender value together**, applying `AVG(COALESCE(...))` within each bundle.
- The number of output rows equals the number of distinct `gender` values in `customer_details`, including `NULL` if any customers have no gender recorded.
- The semicolon `;` terminates the SQL statement.
- **Beginner tip:** Without `GROUP BY`, `AVG(COALESCE(...))` would compute a single average across all customers of all genders — one number instead of one per gender. `GROUP BY` is what creates the per-gender breakdown.
- **Business purpose:** Produces a gender-level summary of loyalty health — the essential starting point for demographic segmentation of the loyalty programme.

---

## Full Query Logic Flow (Visual Summary)

```
customer_details (ALL customers — left table)
        │
        ▼
LEFT JOIN loyalty_scores
        │
        ├── Matched customers → real loyalty score (e.g., 0.74)
        └── Unmatched customers → NULL in loyalty score column
                │
                ▼
        COALESCE(score, 0.5)
        │
        ├── Real score → kept as-is
        └── NULL → replaced with 0.5
                │
                ▼
        GROUP BY gender
        AVG() computed within each gender group
                │
                ▼
        Final result:
        gender | average_loyalty_score
        F      | 0.63
        M      | 0.58
        NULL   | 0.51
```

---

## Summary Table

| Line | SQL Element                                            | What It Does                                                         | Business Reason                                                         |
| ---- | ------------------------------------------------------ | -------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 1    | `a.gender`                                             | Grouping dimension; one output row per gender value                  | Segments loyalty health by demographic                                  |
| 2    | `AVG(COALESCE(b.customer_loyalty_score, 0.5))`         | Replaces NULL scores with 0.5, then averages all values per group    | Produces an honest, complete average including unscored customers       |
| 3    | `FROM grocery_db.customer_details a`                   | Source of the complete customer list                                 | Guarantees all customers are included, not just loyalty-programme users |
| 4–5  | `LEFT JOIN grocery_db.loyalty_scores b ON customer_id` | Brings in loyalty scores, keeping all customers even without a score | Prevents silently dropping unscored customers from the average          |
| 6    | `GROUP BY a.gender;`                                   | Creates one output row per gender                                    | Enables per-demographic loyalty comparison                              |

---

## Key SQL Concepts Used

| Concept                        | Description                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------- |
| **`LEFT JOIN`**                | Keeps all rows from the left table; unmatched right-table rows appear as NULL   |
| **`INNER JOIN` (contrast)**    | Would silently drop customers with no loyalty score — wrong for this task       |
| **`COALESCE(value, default)`** | Returns the first non-NULL argument; replaces NULLs with a default              |
| **NULL handling**              | SQL `AVG` ignores NULLs by default; `COALESCE` forces inclusion with a default  |
| **`AVG()`**                    | Aggregate function — arithmetic mean of all values in a group                   |
| **`GROUP BY`**                 | Collapses rows into one per group; required when mixing columns with aggregates |
| **Nesting functions**          | `AVG(COALESCE(...))` — inner function runs first, output feeds outer function   |

---

## Common Beginner Mistakes to Avoid

### Mistake 1: Using `INNER JOIN` instead of `LEFT JOIN`

```sql
-- WRONG — drops customers with no loyalty score
INNER JOIN grocery_db.loyalty_scores b ON a.customer_id = b.customer_id

-- CORRECT — keeps all customers; unmatched rows get NULL
LEFT JOIN grocery_db.loyalty_scores b ON a.customer_id = b.customer_id
```

Using `INNER JOIN` here would silently exclude a portion of the customer base — the average would be inflated and misleading.

---

### Mistake 2: Forgetting `COALESCE` — relying on AVG to handle NULLs

```sql
-- WRONG — AVG silently ignores NULLs, excluding unscored customers
AVG(b.customer_loyalty_score)

-- CORRECT — COALESCE replaces NULLs with 0.5 before AVG runs
AVG(COALESCE(b.customer_loyalty_score, 0.5))
```

Without `COALESCE`, the `LEFT JOIN` brings unscored customers into the data but `AVG` immediately discards them — you get the same biased result as an `INNER JOIN`, just with more query overhead.

---

### Mistake 3: Using `ISNULL` or `NVL` instead of `COALESCE`

Different SQL databases have different NULL-replacement functions:

| Function                 | Database                              | Example                |
| ------------------------ | ------------------------------------- | ---------------------- |
| `COALESCE(col, default)` | **All SQL databases** (ANSI standard) | `COALESCE(score, 0.5)` |
| `ISNULL(col, default)`   | SQL Server, MySQL                     | `ISNULL(score, 0.5)`   |
| `NVL(col, default)`      | Oracle                                | `NVL(score, 0.5)`      |
| `IFNULL(col, default)`   | MySQL, SQLite                         | `IFNULL(score, 0.5)`   |

`COALESCE` is the safest choice — it is the ANSI SQL standard and works across all major databases. Prefer it over vendor-specific alternatives for portability.

---

## Extended Business Use Cases

The **`LEFT JOIN` + `COALESCE` + `AVG`** pattern solves any problem where you need to include all members of a group in an average, even those missing a value in a secondary table:

| Industry           | Business Question                                                                                                                 | Why LEFT JOIN + COALESCE                                                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Grocery retail** | What is the average loyalty score per gender, including unscored customers?                                                       | Unscored customers must not be silently excluded — they are often the least engaged and most at-risk segment            |
| **Banking**        | What is the average credit utilisation by age band, defaulting to 0 for customers with no credit product?                         | Customers without a credit product should show 0% utilisation, not be excluded from the average                         |
| **E-commerce**     | What is the average review rating per product category, defaulting to 3.0 (neutral) for unreviewed products?                      | Unreviewed products should not be excluded from category health metrics                                                 |
| **HR / Workforce** | What is the average performance score per department, defaulting to the company midpoint for new employees with no review yet?    | New employees without scores must be represented to give an accurate department average                                 |
| **Healthcare**     | What is the average patient satisfaction score per ward, defaulting to 5 (neutral on a 1–10 scale) for patients not yet surveyed? | Incomplete survey coverage should not skew ward comparisons — default anchors the missing values at neutral             |
| **SaaS**           | What is the average NPS (Net Promoter Score) per customer tier, defaulting to 0 for customers who have not responded?             | Non-responders are often disengaged customers — defaulting to 0 includes their likely low sentiment in the tier average |

The business principle behind all these cases: **excluding missing data silently creates survivorship bias** — you end up measuring only your most engaged customers and drawing overly optimistic conclusions. `LEFT JOIN` + `COALESCE` is the technical solution to that analytical trap, and using it correctly is a hallmark of rigorous, trustworthy data analysis.
