# Weekly SQL Challenge 03

## Weekly SQL Challenge 03

Data: grocery_db schema data tables

Task: Write a query that provides the count of customers that meet the following criteria:

Are male
Live between 2 and 3 miles from the store (inclusive)
Have a credit score greater than 0.4
Expected Output: Your query should return one column called customer_count and just one row, which shows the number of customers that meet the criteria

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

Imagine you are a data analyst at a grocery retail chain. The marketing team wants to launch a **targeted direct-mail campaign** — physical flyers sent to homes nearby — for a new loyalty rewards programme.

The strategy is to:

- Focus on **male customers** (based on previous campaign data showing higher conversion rates for this demographic).
- Target customers who live **2–3 miles away** — close enough to visit regularly, but far enough that a small incentive (e.g., a discount voucher) might tip them into visiting more often. Customers under 2 miles likely shop there already; customers over 3 miles are unlikely to change behaviour.
- Prioritise customers with a **credit score above 0.4** — indicating they are financially stable and more likely to spend on premium or loyalty-linked products.

By counting how many customers fit this profile **before** running the campaign, the business can:

1. Estimate **print and postage costs** for the mailers.
2. Decide whether the segment is large enough to be worth targeting.
3. Set realistic **KPI benchmarks** (e.g., expected conversion rate × segment size = projected new loyal customers).
4. Compare this segment against others to **allocate marketing budget** where it will drive the most profitability.

This is a classic example of using SQL to support **data-driven decision making** — rather than guessing who to target, the business uses real customer data to identify the highest-value segment.

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

- `COUNT(*)` is an **aggregate function** that counts the total number of rows returned by the query after all filters are applied.
- The `*` means "count every row, regardless of whether any individual column is NULL" — it simply counts records that exist.
- `AS customer_count` **renames** the output column to `customer_count`. Without this alias, the column heading would display as `COUNT(*)`, which is less readable in a report or dashboard.
- **Business purpose:** This gives us one number — the size of the target audience for the campaign.

---

### Line 2 — `FROM grocery_db.customer_details`

```sql
FROM grocery_db.customer_details
```

- `FROM` tells SQL **which table** to query data from.
- `grocery_db` is the **schema** (or database) name — a logical container that groups related tables together.
- `customer_details` is the specific **table** within that schema, which holds one row per customer and columns such as `gender`, `distance_from_store`, and `credit_score`.
- **Business purpose:** We are sourcing our audience data from the company's central customer database.

---

### Line 3 — `WHERE gender = 'M'`

```sql
WHERE gender = 'M'
```

- `WHERE` begins the **filtering section** of the query — only rows that satisfy all the conditions listed will be counted.
- `gender = 'M'` filters the table to include only customers whose `gender` column contains the value `'M'` (male).
- The value `'M'` is wrapped in **single quotes** because it is a text (string) value, not a number.
- **Business purpose:** The marketing team's analysis showed male customers in this area responded better to the previous loyalty programme campaign, so we narrow the target list accordingly.

---

### Line 4 — `AND distance_from_store BETWEEN 2 AND 3`

```sql
AND distance_from_store BETWEEN 2 AND 3
```

- `AND` adds an **additional condition** — the row must satisfy both this condition AND the previous one.
- `distance_from_store BETWEEN 2 AND 3` is equivalent to writing `distance_from_store >= 2 AND distance_from_store <= 3`. The `BETWEEN` keyword is **inclusive on both ends**, meaning customers who live exactly 2 miles or exactly 3 miles away are included.
- **Business purpose:** The store's delivery radius and marketing budget don't extend beyond 3 miles, and customers under 2 miles are already frequent visitors who don't need additional incentivisation. The 2–3 mile "sweet spot" represents customers who are reachable but under-engaged.

---

### Line 5 — `AND credit_score > 0.4`

```sql
AND credit_score > 0.4;
```

- `AND` adds a **third condition** — the row must satisfy all three filters simultaneously.
- `credit_score > 0.4` keeps only customers whose credit score is **strictly greater than 0.4**. This is a strict inequality — a score of exactly 0.4 would be excluded (unlike `>=`).
- Credit scores here appear to be stored as **decimal values between 0 and 1** (e.g., 0.75 = strong credit, 0.2 = poor credit).
- The semicolon `;` at the end **terminates the SQL statement**, signalling to the database engine that the query is complete.
- **Business purpose:** Customers with stronger credit scores are more likely to sign up for loyalty credit products or spend more per visit. Excluding low-score customers reduces the risk of promoting financial products (like store credit cards) to customers who may be declined, which could harm the brand relationship.

---

## Summary Table

| Line | SQL Element                               | What It Does                                         | Business Reason                                             |
| ---- | ----------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| 1    | `COUNT(*) AS customer_count`              | Counts all qualifying rows; labels the result column | Tells us the segment size before committing budget          |
| 2    | `FROM grocery_db.customer_details`        | Specifies the source table                           | Pulls from the company's central customer database          |
| 3    | `WHERE gender = 'M'`                      | Filters to male customers only                       | Targets the demographic with higher campaign response rates |
| 4    | `AND distance_from_store BETWEEN 2 AND 3` | Filters to customers 2–3 miles away (inclusive)      | Focuses on the reachable but under-engaged distance band    |
| 5    | `AND credit_score > 0.4`                  | Filters to customers with credit score above 0.4     | Prioritises financially stable, higher-spend customers      |

---

## Key SQL Concepts Used

| Concept           | Description                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| `COUNT(*)`        | Aggregate function — counts rows matching the query conditions           |
| `AS`              | Alias — renames a column in the output for readability                   |
| `FROM`            | Identifies the table (and schema) to query                               |
| `WHERE`           | Begins the filter block; only matching rows are processed                |
| `AND`             | Combines multiple conditions — all must be true for a row to be included |
| `BETWEEN x AND y` | Range filter — inclusive on both ends; equivalent to `>= x AND <= y`     |
| `>`               | Strict greater-than comparison; excludes the boundary value itself       |
| `;`               | Statement terminator — marks the end of the SQL query                    |

---

## Extended Business Use Cases

This type of **count + filter** query is one of the most fundamental and powerful patterns in business SQL. Other similar scenarios include:

- **Retail:** Count customers who have not purchased in 90 days and have high lifetime spend — candidates for a win-back campaign.
- **Banking:** Count accounts with balances above £10,000 and no investment product — cross-sell opportunity.
- **Healthcare:** Count patients aged 40–60 with no recent check-up — flag for outreach programme.
- **E-commerce:** Count users who browsed a product category but never purchased — target for a discount email.

In every case, the business goal is the same: **find the right people, at the right time, with the right message** — and SQL `COUNT` with `WHERE` filters is the starting point for answering that question.
