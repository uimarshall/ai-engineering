# Weekly SQL Challenge 04

## Overview

**Data:** `grocery_db` schema data tables  
**Table used:** `grocery_db.customer_details`

---

## The Task

Write a query that provides the **count of customers** that meet ALL of the following criteria:

- Are **male**
- Live **between 2 and 3 miles** from the store (inclusive)
- Have a **credit score greater than 0.4**

**Expected Output:** One column called `customer_count` and one row showing the number of qualifying customers.

---

## Business Context & Why This Matters

You are a data analyst at a mid-sized grocery retail chain competing against larger supermarket brands. The leadership team wants to **stay ahead of the competition** by running smarter, more precise marketing campaigns rather than blanketing all customers with generic promotions — a tactic that burns budget without moving the needle.

The **Head of Commercial Strategy** has asked: *"Before we greenlight the next loyalty mailer, how many customers in our database actually fit the profile we want to target?"*

The business rationale behind each filter is:

- **Male customers only** — internal A/B test data shows this demographic has a **12% higher redemption rate** on loyalty vouchers in this region. Rather than treating all customers the same, the business uses data to focus spend where ROI is strongest.
- **2–3 miles from the store** — customers under 2 miles already shop frequently; they don't need a nudge. Customers beyond 3 miles rarely convert from a mailer alone. The 2–3 mile band is the **growth opportunity zone** — people aware of the store who could be nudged into becoming regulars.
- **Credit score above 0.4** — the loyalty programme includes an optional store credit card. Customers with a credit score of 0.4 or below are unlikely to qualify and including them wastes print costs. Higher-score customers also tend to have higher average basket sizes, improving the **revenue-per-campaign-contact** metric.

Getting this count right enables the business to:

1. **Right-size the campaign budget** — cost per mailer × qualifying count = total spend.
2. **Forecast revenue impact** — qualifying count × historical conversion rate × average basket value = projected incremental revenue.
3. **Benchmark against competitors** — if the segment is smaller than expected, the team can investigate whether a competitor has recently opened nearby and is pulling customers away.
4. **Protect margin** — by avoiding irrelevant contacts, the campaign cost-per-acquisition improves, directly supporting profitability targets.

---

## The SQL Query

```sql
SELECT
    COUNT(*) AS customer_count   -- Line 1

FROM
    grocery_db.customer_details  -- Line 2

WHERE
    gender = 'M'                             -- Line 3
    AND distance_from_store BETWEEN 2 AND 3  -- Line 4
    AND credit_score > 0.4;                  -- Line 5
```

---

## Line-by-Line Explanation

### Line 1 — `COUNT(*) AS customer_count`

```sql
COUNT(*) AS customer_count
```

- `SELECT` is the keyword that opens every query — it tells the database *what* to return. Here we are not returning individual rows of data; we are returning a single computed value.
- `COUNT(*)` is an **aggregate function**. It counts the total number of rows that survive all the `WHERE` filters. The `*` (asterisk) means "count every row regardless of NULL values in any column" — it counts the record's existence, not the content of a specific field.
- `AS customer_count` is a **column alias** — it renames the output column from the default `COUNT(*)` label to the human-friendly name `customer_count`. This matters when the result feeds into a dashboard, report, or downstream application that references the column by name.
- **Beginner tip:** If you used `COUNT(gender)` instead of `COUNT(*)`, any rows where the `gender` column is NULL would be silently skipped. `COUNT(*)` is safer when you want a true headcount of all matching rows.
- **Business purpose:** The result is the single number the marketing team needs to go to the budget meeting — the size of the targetable audience.

---

### Line 2 — `FROM grocery_db.customer_details`

```sql
FROM grocery_db.customer_details
```

- `FROM` specifies **the source of the data** — which table the database engine should look in.
- `grocery_db` is the **schema** (sometimes called a database or namespace depending on your SQL dialect). Schemas are organisational containers that group related tables — like folders on a computer.
- `customer_details` is the **table name** within that schema. This table holds one row per customer with columns storing attributes such as `gender`, `distance_from_store`, `credit_score`, and likely many others (name, email, signup date, etc.).
- The dot `.` between `grocery_db` and `customer_details` is the **schema separator** — it tells the database engine to look inside `grocery_db` for a table called `customer_details`.
- **Beginner tip:** Always qualify table names with their schema in professional environments. It avoids ambiguity when multiple schemas contain tables with the same name.
- **Business purpose:** This is the company's master customer registry. All customer segmentation, targeting, and analysis starts here.

---

### Line 3 — `WHERE gender = 'M'`

```sql
WHERE gender = 'M'
```

- `WHERE` begins the **filter clause** — a set of conditions that every row must pass before it is counted. Think of it as a security gate: only rows that meet all the criteria are allowed through.
- `gender = 'M'` is a simple **equality filter**. It keeps only rows where the `gender` column holds the exact string value `'M'`.
- The value `'M'` is wrapped in **single quotes** `' '` because it is a text (string/varchar) value. Numbers do not need quotes; text always does.
- The `=` sign is the **equality operator** — the value in the column must exactly match `'M'`. If the data stored `'Male'` or `'m'` (lowercase), this filter would miss those rows.
- **Beginner tip:** Always check how values are stored in your data before writing filters — use `SELECT DISTINCT gender FROM grocery_db.customer_details;` to see all unique values first.
- **Business purpose:** Narrows the audience to the demographic segment with the highest proven campaign ROI, making every pound of marketing spend work harder.

---

### Line 4 — `AND distance_from_store BETWEEN 2 AND 3`

```sql
AND distance_from_store BETWEEN 2 AND 3
```

- `AND` is a **logical operator** that chains conditions together. For a row to pass, it must satisfy the `gender` condition *AND* this condition *AND* every other condition in the `WHERE` block.
- `distance_from_store BETWEEN 2 AND 3` is a **range filter**. It is exactly equivalent to writing `distance_from_store >= 2 AND distance_from_store <= 3`.
- Critically, `BETWEEN` is **inclusive on both boundaries** — customers living exactly 2.0 miles or exactly 3.0 miles away are included in the count.
- The column `distance_from_store` stores a numeric value representing how far (in miles) a customer lives from the nearest store.
- **Beginner tip:** Be careful with `BETWEEN` on date columns — the upper boundary includes the entire day only if the time component is `00:00:00`. For date ranges, it is often safer to use `>= start_date AND < end_date`.
- **Business purpose:** The 2–3 mile band is the strategic "growth zone." Customers here have latent demand — they know the store exists but haven't formed a habit. A targeted incentive can convert them into regular shoppers, increasing basket frequency and long-term customer lifetime value (CLV), a key profitability driver.

---

### Line 5 — `AND credit_score > 0.4;`

```sql
AND credit_score > 0.4;
```

- `AND` adds the **third and final condition** — all three filters must be true simultaneously for a row to be counted.
- `credit_score > 0.4` is a **strict greater-than comparison**. Only customers with a score *strictly above* 0.4 qualify. A customer with a score of exactly 0.4 would be **excluded** (use `>=` if you want to include the boundary value).
- `credit_score` appears to be stored as a **decimal between 0 and 1**, where values closer to 1 indicate stronger creditworthiness (e.g., 0.85 = excellent credit, 0.35 = poor credit).
- The **semicolon** `;` at the very end terminates the SQL statement. It tells the database engine that the query is complete and ready to execute. In some tools you can omit it, but it is good practice to always include it, especially when running multiple statements in sequence.
- **Beginner tip:** `>` means "greater than, excluding the value itself." `>=` means "greater than or equal to, including the value." Choosing the wrong one can silently over- or under-count your results.
- **Business purpose:** Filtering to credit score > 0.4 pre-qualifies the audience for the store credit card component of the loyalty offer. It also correlates with higher average spend. Targeting this group improves the **revenue yield per contact**, keeping campaign ROI above the business's minimum acceptable threshold.

---

## Summary Table

| Line | SQL Element | What It Does | Business Reason |
|------|-------------|--------------|-----------------|
| 1 | `COUNT(*) AS customer_count` | Counts all rows surviving the filters; names the output column | Delivers the audience size needed for budget and ROI forecasting |
| 2 | `FROM grocery_db.customer_details` | Specifies the source table and schema | Queries the company's authoritative customer database |
| 3 | `WHERE gender = 'M'` | Keeps only male customers | Targets the demographic with the highest voucher redemption rate |
| 4 | `AND distance_from_store BETWEEN 2 AND 3` | Keeps customers 2–3 miles away (inclusive on both ends) | Focuses on the reachable growth-opportunity distance band |
| 5 | `AND credit_score > 0.4;` | Keeps customers with credit score strictly above 0.4; ends statement | Pre-qualifies for credit card offer and correlates with higher basket spend |

---

## Key SQL Concepts Used

| Concept | Syntax | Description |
|---------|--------|-------------|
| Aggregate function | `COUNT(*)` | Collapses many rows into a single computed value |
| Column alias | `AS customer_count` | Renames the output column for readability |
| Schema-qualified table | `grocery_db.customer_details` | Avoids ambiguity when multiple schemas exist |
| Filter clause | `WHERE` | Gates which rows are included in the result |
| Equality filter | `= 'M'` | Exact string match; text values require single quotes |
| Logical AND | `AND` | All conditions must be true simultaneously |
| Inclusive range filter | `BETWEEN x AND y` | Equivalent to `>= x AND <= y` |
| Strict comparison | `> 0.4` | Greater than, excluding the boundary value itself |
| Statement terminator | `;` | Signals the end of the SQL statement |

---

## Extended Business Use Cases

The `COUNT` + `WHERE` pattern is a foundational building block for competitive intelligence and profit-focused decision-making across every industry:

| Industry | Example Query Goal | Business Decision Driven |
|----------|--------------------|--------------------------|
| **Grocery retail** | Count high-credit male customers 2–3 miles away | Size a loyalty mailer campaign; protect CAC budget |
| **Telecom** | Count contract customers whose plan expires in 30 days with no service complaint | Proactive retention call list; reduce churn before a competitor poaches them |
| **Banking** | Count current-account holders aged 25–40 with no savings product and balance > £2,000 | Cross-sell savings or investment accounts; grow fee revenue |
| **E-commerce** | Count users who added items to cart but did not purchase in the last 7 days | Trigger an abandoned-cart email with a time-limited discount |
| **Healthcare** | Count patients over 50 with no check-up in 18 months | Proactive outreach to improve preventive care metrics and reduce costly late-stage treatments |
| **SaaS / Tech** | Count free-tier users who logged in 5+ times last month but haven't upgraded | Identify users at peak engagement — the ideal moment for an upgrade nudge |

In every scenario the logic is identical: **define the right audience precisely, count them first, then act.** Using SQL to do this replaces guesswork with evidence, turning customer data into a direct competitive and financial advantage.