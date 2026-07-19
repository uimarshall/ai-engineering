# Weekly SQL Challenge 07

## Overview

**Data:** `grocery_db` schema data tables  
**Tables used:** `grocery_db.customer_details`, `grocery_db.campaign_data`

---

## The Task

Write a query that returns, **for each gender and mailer type**, the number of customers, number of signups, and the **signup percentage** — all scoped to the `delivery_club` campaign only.

**Requirements:**

- Only include records where `gender` is populated (not NULL)
- Only include records where `campaign_name = 'delivery_club'`
- Alias output columns as `customer_count`, `signups`, and `signup_percentage`
- Round `signup_percentage` to **two decimal places**
- Sort results by `signup_percentage` **descending** (highest first)

**Expected Output:**

| gender | mailer_type | customer_count | signups | signup_percentage |
| ------ | ----------- | -------------- | ------- | ----------------- |
| F      | Premium     | 85             | 42      | 49.41             |
| M      | Premium     | 91             | 44      | 48.35             |
| F      | Standard    | 110            | 38      | 34.55             |
| ...    | ...         | ...            | ...     | ...               |

---

## Business Context & Why This Matters

You are a data analyst supporting the **Marketing & Campaigns** team at a grocery retail chain. The `delivery_club` is a subscription-style delivery service the business has launched to compete with online grocery rivals.

The campaign was run by sending mailers (physical or digital materials) to customers, and the `signup_flag` records whether each contacted customer actually signed up.

The key strategic questions being answered are:

- **Which mailer type converts better?** If a Premium mailer drives a 49% signup rate versus a Standard mailer's 34%, the incremental profit from higher conversions may outweigh the higher print cost of the Premium format — or vice versa.
- **Does gender affect conversion?** If female customers convert at a materially higher rate than male customers for a given mailer type, the business can optimise targeting to reduce wasted sends.
- **Where is budget best spent?** By ranking combinations of gender × mailer type by signup percentage (descending), the business can immediately see the highest-performing segments at the top of the result — and prioritise those in the next campaign run.
- **Competitive urgency:** Delivery club subscriptions are a battleground. Amazon, Ocado, and local competitors are all running similar programmes. Every percentage point of improvement in signup rate translates directly into subscriber growth, recurring revenue, and competitive moat — customers locked into a delivery subscription are far less likely to defect to a rival.

This query gives the marketing team an **evidence-based brief** for the next campaign: which format to use, which gender to prioritise, and what signup rate to benchmark against.

---

## The SQL Query (Fully Annotated)

```sql
SELECT
    a.gender,                                               -- Line 1
    b.mailer_type,                                          -- Line 2
    COUNT(*) AS customer_count,                             -- Line 3
    SUM(b.signup_flag) AS signups,                          -- Line 4
    ROUND(
        (SUM(b.signup_flag) * 1.0) / COUNT(*) * 100, 2
    ) AS signup_percentage                                  -- Line 5

FROM
    grocery_db.customer_details a                           -- Line 6
    INNER JOIN grocery_db.campaign_data b                   -- Line 7
        ON a.customer_id = b.customer_id                    -- Line 8

WHERE
    a.gender IS NOT NULL                                    -- Line 9
    AND b.campaign_name = 'delivery_club'                   -- Line 10

GROUP BY
    a.gender,                                               -- Line 11
    b.mailer_type                                           -- Line 11

ORDER BY
    signup_percentage DESC;                                 -- Line 12
```

---

## Line-by-Line Explanation

---

### Line 1 — `a.gender`

```sql
a.gender,
```

- Selects the `gender` column from `customer_details` (aliased `a`).
- This is one of the two **grouping dimensions** — the query will produce a separate row for each unique combination of gender and mailer type.
- Values are expected to be `'M'` (male) or `'F'` (female). The `WHERE` clause (Line 9) already excludes any NULL gender rows, so only populated values appear here.
- **Beginner tip:** When you see a non-aggregated column in `SELECT`, check that it also appears in `GROUP BY`. `a.gender` is on Line 11 in `GROUP BY` — it satisfies this rule.
- **Business purpose:** Enables the marketing team to compare conversion rates between male and female customers — essential for tailoring message and creative design in future campaigns.

---

### Line 2 — `b.mailer_type`

```sql
b.mailer_type,
```

- Selects the `mailer_type` column from `campaign_data` (aliased `b`).
- This records the **format or tier of the marketing material** sent to each customer — for example: `'Standard'`, `'Premium'`, or `'Email'`.
- Like `gender`, this is a grouping dimension. Every unique combination of `gender` × `mailer_type` gets its own row in the output.
- **Beginner tip:** Both `a.gender` and `b.mailer_type` are in `GROUP BY` (Line 11). This is called a **multi-column GROUP BY** — it creates groups based on all listed column combinations together, not each column independently.
- **Business purpose:** The mailer type is directly tied to campaign cost. Knowing which format has the highest conversion rate lets the business choose the format that maximises **return on marketing spend (ROMS)**.

---

### Line 3 — `COUNT(*) AS customer_count`

```sql
COUNT(*) AS customer_count,
```

- `COUNT(*)` counts the total number of rows in each `gender` × `mailer_type` group after the `WHERE` filters are applied.
- Each row in the joined dataset represents one customer who was contacted by this campaign in this mailer type.
- `AS customer_count` gives the column a clean, readable name.
- **Beginner tip:** `COUNT(*)` counts every row including those where `signup_flag = 0` (did not sign up). This is correct here — we want the **total audience** (denominator) for the percentage calculation on Line 5.
- **Business purpose:** The total number of customers contacted per segment is the **base audience size** — required to calculate conversion rate and to assess whether the segment is large enough to be statistically meaningful.

---

### Line 4 — `SUM(b.signup_flag) AS signups`

```sql
SUM(b.signup_flag) AS signups,
```

This line uses a clever technique: **summing a binary flag to count positive outcomes**.

- `signup_flag` is a **binary column** — it contains only `1` (customer signed up) or `0` (customer did not sign up).
- `SUM(signup_flag)` adds up all the `1`s and `0`s within a group. Since `0` contributes nothing to the total, the result equals the **count of customers who signed up** within that gender × mailer type group.
- This is mathematically equivalent to `COUNT(*) WHERE signup_flag = 1`, but done in a single pass without a subquery or extra filter.
- `AS signups` names the column clearly.
- **Beginner tip:** Summing a 0/1 binary flag to count "yes" values is one of the most common and elegant patterns in SQL analytics. Whenever you see a flag column (is_active, has_purchased, signup_flag, churn_flag), you can `SUM()` it to count the `TRUE` / `1` cases.
- **Business purpose:** The raw number of signups per segment — the **numerator** in the conversion rate formula and a key performance metric for the campaign.

---

### Line 5 — `ROUND((SUM(b.signup_flag) * 1.0) / COUNT(*) * 100, 2) AS signup_percentage`

```sql
ROUND(
    (SUM(b.signup_flag) * 1.0) / COUNT(*) * 100,
    2
) AS signup_percentage
```

This is the most complex expression in the query. Break it into four parts:

#### Part 1: `SUM(b.signup_flag)` — the numerator

- The number of signups in this group (from Line 4 — reused here inside the formula).

#### Part 2: `* 1.0` — force decimal (floating-point) division

```sql
SUM(b.signup_flag) * 1.0
```

- In many SQL databases, dividing one integer by another integer performs **integer division** — it truncates the decimal part. For example, `3 / 10` would return `0` instead of `0.3`.
- Multiplying by `1.0` (a decimal number) forces the result to be treated as a **floating-point (decimal) number**, so the division preserves the decimal portion.
- **Beginner tip:** This is a type-casting trick. You could also write `CAST(SUM(b.signup_flag) AS FLOAT)` or `SUM(b.signup_flag) * 1.0` — both achieve the same result. Always check for integer division when computing percentages or ratios in SQL.

#### Part 3: `/ COUNT(*) * 100` — the conversion rate formula

```sql
/ COUNT(*) * 100
```

- Divides the decimal-safe signup count by the total customer count to get a proportion (e.g., `0.4941`).
- Multiplying by `100` converts the proportion to a **percentage** (e.g., `49.41`).
- The formula is: `(signups ÷ total_customers) × 100 = signup rate %`

#### Part 4: `ROUND(..., 2)` — limit decimal places

```sql
ROUND( ... , 2)
```

- `ROUND(value, decimal_places)` rounds the result to the specified number of decimal places.
- Here, `2` means the percentage is rounded to two decimal places (e.g., `49.41` rather than `49.412857...`).
- **Beginner tip:** `ROUND(value, 0)` rounds to the nearest whole number. `ROUND(value, -2)` rounds to the nearest hundred. Negative values round left of the decimal point.

- `AS signup_percentage` names the column.
- **Business purpose:** The conversion rate is the **primary KPI** of this analysis. Displayed as a percentage rounded to 2 decimal places, it is immediately readable in a slide or dashboard without further formatting. Higher signup percentage = more effective use of campaign budget = stronger competitive position in the delivery subscription market.

---

### Line 6 — `FROM grocery_db.customer_details a`

```sql
FROM grocery_db.customer_details a
```

- Specifies `customer_details` as the **primary (left) table**, aliased `a`.
- This table holds demographic information about each customer, including `gender`, `customer_id`, `distance_from_store`, `credit_score`, etc.
- `a` is the table alias used throughout the query to prefix columns from this table.
- **Business purpose:** Provides the demographic dimension (`gender`) needed to segment the campaign results by customer profile.

---

### Lines 7–8 — `INNER JOIN grocery_db.campaign_data b ON a.customer_id = b.customer_id`

```sql
INNER JOIN grocery_db.campaign_data b
    ON a.customer_id = b.customer_id
```

- `INNER JOIN` merges `customer_details` with `campaign_data`, keeping only rows where a `customer_id` exists in **both** tables.
- `grocery_db.campaign_data` (aliased `b`) holds the campaign-specific records: which campaign each customer was sent, which mailer type they received, and whether they signed up (`signup_flag`).
- `ON a.customer_id = b.customer_id` is the **join condition** — the shared key linking the two tables.
- Customers who appear in `customer_details` but were never part of a campaign will not appear in the output (no match in `campaign_data`). Campaigns records with no matching customer profile are also excluded.
- **Beginner tip:** This JOIN effectively asks: _"Give me only customers who have BOTH a profile AND a campaign record."_ Any customer missing from either table is dropped from the result.
- **Business purpose:** Combines "who the customer is" (demographics from `customer_details`) with "how they responded to the campaign" (behaviour from `campaign_data`) — the two perspectives needed to measure campaign performance by audience segment.

---

### Lines 9–10 — `WHERE a.gender IS NOT NULL AND b.campaign_name = 'delivery_club'`

```sql
WHERE
    a.gender IS NOT NULL
    AND b.campaign_name = 'delivery_club'
```

Two filters applied before any grouping or aggregation:

#### `a.gender IS NOT NULL` (Line 9)

- `IS NOT NULL` is the correct SQL syntax for checking that a value exists (is not missing).
- **Important:** You cannot write `a.gender != NULL` or `a.gender <> NULL` in SQL — comparisons with NULL using `=` or `!=` always return UNKNOWN, not TRUE or FALSE. `IS NOT NULL` is the only reliable way to check for the presence of a value.
- This filter excludes customers whose gender was not recorded — keeping the analysis clean and avoiding a meaningless NULL group in the results.
- **Beginner tip:** In SQL, `NULL` means "unknown" — it is not a value but the absence of one. Any comparison using `=` against NULL returns UNKNOWN (not TRUE), which behaves like FALSE in a `WHERE` clause. Always use `IS NULL` or `IS NOT NULL`.

#### `b.campaign_name = 'delivery_club'` (Line 10)

- Restricts the analysis to **only records from the delivery_club campaign**.
- Without this filter, the query would aggregate data from all campaigns combined — mixing delivery club signups with signups from unrelated promotions, making the conversion rate meaningless for this specific campaign.
- `'delivery_club'` is a string value, so it requires **single quotes**.
- **Business purpose:** Scopes the entire analysis to one specific campaign — standard practice when evaluating a single campaign's performance independently of others.

---

### Line 11 — `GROUP BY a.gender, b.mailer_type`

```sql
GROUP BY
    a.gender,
    b.mailer_type
```

- `GROUP BY` with **two columns** creates one output row per unique combination of `gender` × `mailer_type`.
- For example, if there are 2 genders (`M`, `F`) and 2 mailer types (`Standard`, `Premium`), the result has up to 4 rows:
  - `F` + `Standard`
  - `F` + `Premium`
  - `M` + `Standard`
  - `M` + `Premium`
- The aggregate functions `COUNT(*)` and `SUM(signup_flag)` are then computed **independently within each of these groups**.
- **Beginner tip:** Multi-column `GROUP BY` is not "group by gender, then separately group by mailer_type." It is "group by every unique _combination_ of gender AND mailer_type together." The order of columns in `GROUP BY` does not affect the result — only which combinations exist in the data.
- **Business purpose:** Produces a **cross-tabulation** of campaign performance, letting the team compare every gender × format combination side by side in a single query.

---

### Line 12 — `ORDER BY signup_percentage DESC;`

```sql
ORDER BY signup_percentage DESC;
```

- `ORDER BY` sorts the final result set before returning it.
- `signup_percentage` is the **column alias** defined on Line 5 — SQL allows you to reference aliases in `ORDER BY` (but not in `WHERE` or `HAVING`).
- `DESC` means **descending order** — the highest signup percentage appears first. This places the best-performing gender × mailer combination at the top of the results.
- The semicolon `;` terminates the statement.
- **Beginner tip:** Default sort order is `ASC` (ascending, lowest first). Always explicitly write `DESC` when you want largest-first. Forgetting `DESC` on a percentage-rank query is a common mistake that reverses the intended sort.
- **Business purpose:** Presenting results highest-conversion-first means the most actionable insight is immediately visible without having to scan or sort the output. In a business review, the first row of the result directly answers: _"Which segment should we focus the next campaign on?"_

---

## Full Query Logic Flow (Visual Summary)

```
customer_details (demographics)    campaign_data (campaign behaviour)
        │                                    │
        └──────── INNER JOIN ────────────────┘
                ON customer_id
                      │
                      ▼
            Apply WHERE filters:
            - gender IS NOT NULL
            - campaign_name = 'delivery_club'
                      │
                      ▼
            GROUP BY gender + mailer_type
            ┌──────────────────────────────────┐
            │  COUNT(*) → customer_count       │
            │  SUM(signup_flag) → signups      │
            │  (signups * 1.0 / count) * 100   │
            │  → signup_percentage (rounded)   │
            └──────────────────────────────────┘
                      │
                      ▼
            ORDER BY signup_percentage DESC
                      │
                      ▼
            Final result:
            gender | mailer_type | customer_count | signups | signup_percentage
            F      | Premium     | 85             | 42      | 49.41
            M      | Premium     | 91             | 44      | 48.35
            F      | Standard    | 110            | 38      | 34.55
            ...
```

---

## Summary Table

| Line | SQL Element                                                | What It Does                                    | Business Reason                                      |
| ---- | ---------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------- |
| 1    | `a.gender`                                                 | First grouping dimension — male or female       | Segment conversion by demographic                    |
| 2    | `b.mailer_type`                                            | Second grouping dimension — mailer format       | Compare campaign material formats by effectiveness   |
| 3    | `COUNT(*) AS customer_count`                               | Counts total customers contacted per group      | Base audience size — denominator for conversion rate |
| 4    | `SUM(b.signup_flag) AS signups`                            | Sums binary 0/1 flag to count signups           | Count of positive outcomes per segment               |
| 5    | `ROUND((SUM * 1.0) / COUNT * 100, 2) AS signup_percentage` | Calculates rounded conversion rate as a %       | Primary KPI — which segment responds best            |
| 6    | `FROM grocery_db.customer_details a`                       | Source of customer demographics                 | Provides gender and customer identity                |
| 7–8  | `INNER JOIN grocery_db.campaign_data b ON customer_id`     | Merges demographics with campaign response data | Links who customers are with how they responded      |
| 9    | `WHERE a.gender IS NOT NULL`                               | Excludes customers with missing gender          | Keeps analysis clean; avoids NULL group in results   |
| 10   | `AND b.campaign_name = 'delivery_club'`                    | Scopes analysis to one campaign only            | Prevents mixing results from different campaigns     |
| 11   | `GROUP BY a.gender, b.mailer_type`                         | Creates one row per gender × mailer combination | Enables cross-segment comparison                     |
| 12   | `ORDER BY signup_percentage DESC;`                         | Sorts by conversion rate, highest first         | Best-performing segment immediately visible at top   |

---

## Key SQL Concepts Used

| Concept                         | Description                                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------- |
| **Multi-column `GROUP BY`**     | Groups by every unique _combination_ of two or more columns                            |
| **Binary flag summing**         | `SUM(flag)` on a 0/1 column counts the number of `1` (true) values                     |
| **Integer division prevention** | `* 1.0` casts an integer to decimal so division preserves the fractional part          |
| **`ROUND(value, n)`**           | Rounds a number to `n` decimal places                                                  |
| **`IS NOT NULL`**               | Tests for presence of a value; `= NULL` does NOT work in SQL                           |
| **`INNER JOIN`**                | Returns only rows with matching keys in both tables                                    |
| **Column alias in `ORDER BY`**  | SQL allows referencing `SELECT` aliases in `ORDER BY` (but not in `WHERE` or `HAVING`) |
| **`ORDER BY ... DESC`**         | Sorts largest values first; default without `DESC` is ascending                        |

---

## Common Beginner Mistakes to Avoid

### Mistake 1: Using `= NULL` instead of `IS NOT NULL`

```sql
-- WRONG — always returns no rows because NULL = anything is UNKNOWN
WHERE a.gender != NULL

-- CORRECT
WHERE a.gender IS NOT NULL
```

---

### Mistake 2: Integer division producing zero

```sql
-- WRONG — if SUM() and COUNT() are both integers, result is truncated
(SUM(b.signup_flag) / COUNT(*)) * 100  -- could return 0 or wrong value

-- CORRECT — multiply by 1.0 first to force decimal arithmetic
(SUM(b.signup_flag) * 1.0) / COUNT(*) * 100
```

---

### Mistake 3: Referencing an alias in `WHERE`

```sql
-- WRONG — aliases cannot be used in WHERE (evaluated too early)
WHERE signup_percentage > 40

-- CORRECT — use HAVING for post-aggregation filters
HAVING ROUND((SUM(b.signup_flag) * 1.0) / COUNT(*) * 100, 2) > 40
```

---

## Extended Business Use Cases

The **multi-dimension campaign conversion analysis** pattern is used across every industry that runs outreach programmes:

| Industry               | Business Question                                                           | Dimensions Analysed        | Primary KPI         |
| ---------------------- | --------------------------------------------------------------------------- | -------------------------- | ------------------- |
| **Grocery retail**     | Which gender × mailer type has the highest delivery club signup rate?       | gender, mailer_type        | `signup_percentage` |
| **Financial services** | Which age band × product tier has the highest credit card application rate? | age_band, product_tier     | `application_rate`  |
| **Telecom**            | Which region × contract type has the highest upgrade conversion?            | region, contract_type      | `upgrade_rate`      |
| **E-commerce**         | Which device type × discount level produces the best cart-to-purchase rate? | device_type, discount_band | `conversion_rate`   |
| **Charity / NGO**      | Which donor segment × ask amount has the highest donation rate?             | donor_segment, ask_amount  | `response_rate`     |
| **Healthcare**         | Which age group × outreach channel has the highest flu vaccination uptake?  | age_group, channel         | `uptake_percentage` |

In every case the competitive or strategic value is identical: **spend campaign budget where the data shows the highest return.** Rather than applying the same creative and format to every customer, the business uses evidence to personalise at scale — a practice that consistently delivers 20–40% improvements in campaign ROI over one-size-fits-all approaches.
