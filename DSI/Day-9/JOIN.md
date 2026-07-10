# SQL JOINS — Day 9

## Overview: Why Joins Matter for Competitive Business Intelligence

In a data-driven company, raw data rarely lives in a single table. Customer profiles, transaction histories,
loyalty metrics, product catalogs, and credit data are stored separately for performance and maintainability.
**Joins are the mechanism that brings these data islands together**, enabling analysts and data scientists to
answer cross-functional questions like:

- "Which high-credit customers have low loyalty scores — and are therefore at churn risk?"
- "Which product categories drive the most revenue from our top-tier loyalty members?"
- "Are there customers in our CRM who have never made a purchase?"

Answering these questions quickly gives your company a competitive edge by enabling faster, more precise
decisions across marketing, retention, pricing, and product strategy.

---

## Inspecting Source Tables

```sql
-- Always inspect your source tables before joining to understand
-- the shape of the data, key columns, and potential NULLs.
select * from grocery_db.customer_details;
select * from grocery_db.loyalty_scores;
```

**What to look for:**

- Are there duplicate `customer_id` values? Duplicates can cause row explosion in joins.
- Are there NULLs in the join key? NULL never equals NULL in SQL — those rows will be silently excluded from INNER JOINs.
- How many rows are in each table? A huge mismatch can indicate data quality issues.

---

## INNER JOIN

An INNER JOIN returns **only rows where a match exists in both tables**. Rows with no corresponding
record in the other table are completely excluded from the result.

```sql
-- Business scenario: The marketing team wants to launch a personalised
-- email campaign targeting customers whose loyalty score can be used to
-- tailor offers. We only want customers who ARE enrolled in the loyalty
-- programme (i.e., they appear in loyalty_scores).
-- Customers not yet enrolled should NOT appear — they will get a
-- separate "sign up" campaign instead.

select
    a.*,
    b.customer_loyalty_score
from
    grocery_db.customer_details a
    inner join grocery_db.loyalty_scores b on a.customer_id = b.customer_id;
```

**When to use INNER JOIN:**

- You need a clean, matched dataset with no NULLs from the joined table.
- Downstream ML models or BI dashboards require every row to have a loyalty score.
- You want to count only active/engaged customers for KPI reporting.

**Competitive use case:** A retailer can use this query to identify their _confirmed_ loyalty members and
immediately segment them by spend tier, enabling hyper-targeted promotions that competitors without clean
data pipelines cannot replicate at speed.

---

## LEFT JOIN

A LEFT JOIN returns **all rows from the left (primary) table**, plus matching rows from the right table.
Where no match exists, the right-table columns come back as NULL.

```sql
-- Business scenario: The retention team needs a full customer audit.
-- They want EVERY customer in the system — even those who have never
-- signed up for the loyalty programme — so they can identify gaps
-- and run re-engagement campaigns.

select
    a.*,
    b.customer_loyalty_score
from
    grocery_db.customer_details a
    left join grocery_db.loyalty_scores b on a.customer_id = b.customer_id;
```

**Why LEFT JOIN beats INNER JOIN here:** An INNER JOIN would silently drop customers with no loyalty record.
A LEFT JOIN preserves them with a NULL score, making it easy to filter with `WHERE customer_loyalty_score IS NULL`
to find exactly those customers for the re-engagement push.

**Generic template (reusable across datasets):**

```sql
-- Use this pattern whenever you need all records from a primary table
-- enriched with optional data from a secondary table.
select
    a.id         as id_t1,
    a.t1_col1,
    a.t1_col2,
    b.id         as id_t2,    -- will be NULL if no match
    b.t2_col1,                -- will be NULL if no match
    b.t2_col2                 -- will be NULL if no match
from
    table1 a
    left join table2 b on a.id = b.id;
```

---

## LEFT JOIN with Filtering Logic

Adding a `WHERE` clause after a LEFT JOIN lets you **slice the enriched dataset** to focus on
a specific sub-population.

```sql
-- Business scenario: The loyalty analytics team wants to understand
-- spending patterns among customers who are *already highly loyal*
-- (score > 0.5). These are your brand advocates — understanding what
-- drives them helps you replicate that success with mid-tier customers
-- and stay ahead of competitors who only look at average behaviour.

select
    a.*,
    b.customer_loyalty_score
from
    grocery_db.customer_details a
    left join grocery_db.loyalty_scores b on a.customer_id = b.customer_id
where customer_loyalty_score > 0.5;
```

**Note:** Filtering on a LEFT JOIN column (`customer_loyalty_score > 0.5`) effectively converts it into
an INNER JOIN for that condition, because NULLs fail the comparison. If you want to keep NULLs as well,
use: `WHERE customer_loyalty_score > 0.5 OR customer_loyalty_score IS NULL`.

---

## JOINING MULTIPLE TABLES

Real-world business questions often require combining three or more tables. Each join adds a new dimension
of context to your analysis.

```sql
-- Business scenario: The category management team wants to know which
-- product areas are generating the most transactions among high-loyalty
-- customers. This insight drives shelf-space decisions, promotional
-- budgets, and supplier negotiations — all of which directly impact
-- competitive positioning.
--
-- We need three tables:
--   transactions     → the fact table (every purchase event)
--   loyalty_scores   → enriches each transaction with the buyer's loyalty tier
--   product_areas    → decodes the product_area_id into a human-readable name

select
    a.*,
    b.customer_loyalty_score,
    c.product_area_name
from
    grocery_db.transactions a
    left join  grocery_db.loyalty_scores b on a.customer_id      = b.customer_id
    inner join grocery_db.product_areas  c on a.product_area_id  = c.product_area_id;
```

**Join type reasoning here:**

- `LEFT JOIN loyalty_scores` — some transactions may be from guest/non-loyalty customers; we keep those rows
  and note the NULL score rather than discarding the transaction data.
- `INNER JOIN product_areas` — every transaction MUST belong to a product area; if it doesn't, the data is
  corrupt and we want those rows excluded, not hidden behind NULLs.

**Competitive use case:** By layering loyalty tiers on top of product-area sales, your merchandising team
can identify which categories over-index with loyal customers vs. casual shoppers. Stocking and pricing
decisions built on this insight are far more precise than competitors relying on aggregate sales alone.

---

## Setting Up Test Tables for Advanced Join Types

```sql
-- Create two small temp tables to illustrate FULL OUTER JOIN and CROSS JOIN.
-- table1 has IDs 'A' and 'B'; table2 has IDs 'A' and 'C'.
-- Only 'A' is common — useful for demonstrating what each join type returns.

create temp table table1 (id char(1), t1_col1 int, t1_col2 int);
insert into table1 values ('A', 1, 1), ('B', 1, 1);
select * from table1;

create temp table table2 (id char(1), t2_col1 int, t2_col2 int);
insert into table2 values ('A', 2, 2), ('C', 2, 2);
select * from table2;
```

---

## INNER JOIN vs FULL OUTER JOIN — Side-by-Side Comparison

### INNER JOIN (intersection only)

```sql
-- Returns ONLY the row where id = 'A' (the only match).
-- Rows 'B' (table1 only) and 'C' (table2 only) are dropped.
--
-- Business scenario: Useful when you need a strictly matched dataset,
-- e.g., customers who appear in BOTH your CRM and your email platform —
-- the overlap you can actually contact with personalised messaging.

select
    a.id as id_t1,
    a.t1_col1,
    a.t1_col2,
    b.id as id_t2,
    b.t2_col1,
    b.t2_col2
from
    table1 a
    inner join table2 b on a.id = b.id;
```

### FULL OUTER JOIN (union of both tables)

```sql
-- Returns ALL rows from both tables.
-- 'A' is matched; 'B' appears with NULLs for table2 cols;
-- 'C' appears with NULLs for table1 cols.
--
-- Business scenario: Data reconciliation and gap analysis.
-- A retail chain merging two regional databases (e.g., after an
-- acquisition) can use FULL OUTER JOIN to identify:
--   - Products in both systems (matched rows)          → de-duplicate
--   - Products only in the old system (NULLs on right) → migrate
--   - Products only in the new system (NULLs on left)  → back-fill history
-- This is critical for staying competitive post-merger by having
-- a single source of truth faster than rivals.

select
    a.id as id_t1,
    a.t1_col1,
    a.t1_col2,
    b.id as id_t2,
    b.t2_col1,
    b.t2_col2
from
    table1 a
    full outer join table2 b on a.id = b.id;
```

---

## CROSS JOIN (Cartesian Product)

A CROSS JOIN returns **every combination** of rows from both tables. With 2 rows in table1 and 2 in table2,
you get 2 × 2 = 4 rows. With 1,000 × 1,000 rows you get 1,000,000 — use with care.

```sql
-- Returns all 4 combinations: (A,A), (A,C), (B,A), (B,C).
--
-- Business scenario: Competitive pricing matrix.
-- A company wants to model every combination of its product tiers
-- (Basic, Pro, Enterprise) against every customer segment (SMB, Mid-Market,
-- Enterprise) to build a full pricing grid for a go-to-market strategy.
-- CROSS JOIN generates all 3 × 3 = 9 tier-segment combinations in one shot,
-- which analysts then enrich with revenue projections — far faster than
-- building the matrix manually in a spreadsheet.

select
    a.id as id_t1,
    a.t1_col1,
    a.t1_col2,
    b.id as id_t2,
    b.t2_col1,
    b.t2_col2
from
    table1 a
    cross join table2 b;
```

**Other real-world CROSS JOIN uses:**

- Generate a full calendar × store grid for retail sales forecasting.
- Create all campaign × audience combinations for A/B test planning.
- Build a recommendation matrix pairing every customer with every product category.

---

## Practical Exercise: Credit Score vs. Loyalty Analysis

```sql
/*
  BUSINESS CONTEXT
  ─────────────────────────────────────────────────────────────────────────
  The Chief Data Officer has tasked the analytics team with investigating
  whether customers with higher credit scores also tend to be more loyal.

  If a positive correlation exists, the company can:
    1. Pre-approve high-credit prospects for premium loyalty tiers at sign-up,
       reducing the time-to-value for new members.
    2. Build predictive models that identify high-credit / low-loyalty customers
       as high-potential targets for a loyalty activation campaign.
    3. Share these insights with the finance team to create co-branded credit
       products — a revenue stream competitors without this data connection
       cannot easily replicate.

  REQUIREMENTS
  ─────────────────────────────────────────────────────────────────────────
  - Return only customers who HAVE a loyalty score (stakeholder wants a clean
    dataset for correlation analysis — no NULLs).
  - Return three columns: customer_id, credit_score, customer_loyalty_score.

  APPROACH
  ─────────────────────────────────────────────────────────────────────────
  We use an INNER JOIN so that only customers present in BOTH tables are
  returned. This guarantees every row has a non-NULL loyalty score, making
  the dataset immediately usable by the data science team without further
  cleaning.

  Table aliases ('a' for customer_details, 'b' for loyalty_scores) keep the
  query readable and prevent column-name ambiguity when both tables share
  common column names.
*/

select
    a.customer_id,
    a.credit_score,
    b.customer_loyalty_score
from
    grocery_db.customer_details a
    inner join grocery_db.loyalty_scores b on a.customer_id = b.customer_id;
```

**Extending this query for deeper competitive insight:**

```sql
-- Add a loyalty tier label and sort by credit score descending
-- to immediately surface the highest-value targets for the CDO's review.
select
    a.customer_id,
    a.credit_score,
    b.customer_loyalty_score,
    case
        when b.customer_loyalty_score >= 0.8 then 'Platinum'
        when b.customer_loyalty_score >= 0.6 then 'Gold'
        when b.customer_loyalty_score >= 0.4 then 'Silver'
        else 'Bronze'
    end as loyalty_tier
from
    grocery_db.customer_details a
    inner join grocery_db.loyalty_scores b on a.customer_id = b.customer_id
order by a.credit_score desc;
```

---

## Quick Reference: Choosing the Right Join

| Join Type       | Rows returned                                       | Best competitive use case                             |
| --------------- | --------------------------------------------------- | ----------------------------------------------------- |
| INNER JOIN      | Only matched rows                                   | Clean datasets for ML models, targeted campaigns      |
| LEFT JOIN       | All left rows + matched right rows (NULLs for gaps) | Full customer audits, churn detection, gap analysis   |
| FULL OUTER JOIN | All rows from both tables (NULLs where unmatched)   | Post-merger reconciliation, data quality checks       |
| CROSS JOIN      | Every combination of both tables                    | Pricing matrices, A/B test grids, recommendation prep |
