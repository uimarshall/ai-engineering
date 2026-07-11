# SQL UNION & UNION ALL

## Overview

`UNION` and `UNION ALL` are SQL set operators that **stack result sets from two or more SELECT queries on top of each other** (vertical combination). Both queries must return the same number of columns with compatible data types.

| Operator    | Removes duplicates? | Performance              |
| ----------- | ------------------- | ------------------------ |
| `UNION`     | Yes                 | Slower (sort/dedup step) |
| `UNION ALL` | No                  | Faster                   |

---

## UNION — Combining Distinct Results from Different Product Areas

**What it does:** Returns a single deduplicated list of product area names drawn from two separate filters.

**Business scenario:** A grocery retail chain is conducting a **competitive market analysis**. The strategy team wants to identify which product categories the company currently leads in versus where rivals are gaining ground. They start by pulling together a master list of all product areas under review — combining the "Bakery & Dairy" cluster (IDs 1–2) with the "Health & Organic" cluster (IDs 4–5) — making sure each area name appears only once to avoid skewing reporting dashboards.

```sql
-- Retrieve a deduplicated list of product areas from two separate business clusters.
-- UNION automatically removes duplicate names, ensuring clean data for reporting.
SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (1, 2)  -- Cluster 1: e.g., Bakery, Dairy

UNION

SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (4, 5); -- Cluster 2: e.g., Health Foods, Organic
```

**Why this matters competitively:** Having a clean, deduplicated list of product areas is the foundation for reliable KPI dashboards, assortment gap analysis, and pricing benchmarking against competitors. Duplicates in this list would inflate counts and distort category-level performance metrics.

---

## UNION — Deduplication Behaviour When Sources Overlap

**What it does:** Demonstrates that `UNION` removes duplicates even when both SELECT statements query the **same set of rows**.

**Business scenario:** A data engineering team is building an automated **product catalogue consolidation pipeline**. Two upstream systems (a legacy ERP and a new POS system) both report product areas with IDs 1 and 2. When merging feeds, the team uses `UNION` to guarantee the output contains each product area exactly once, regardless of how many source systems report it. This prevents over-counting in inventory and shelf-space allocation tools.

```sql
-- Both queries return the same rows (product_area_id IN (1,2)).
-- UNION deduplicates the combined result, returning each product area name only once.
-- Use this pattern when consolidating data from multiple systems that may report the same records.
SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (1, 2)

UNION

SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (1, 2);
```

**Why this matters competitively:** Data pipelines that fail to deduplicate lead to inflated stock counts and misleading demand signals. Competitors with cleaner data pipelines make faster, more accurate replenishment decisions — using `UNION` correctly keeps your data trustworthy at the source.

---

## UNION ALL — Preserving All Rows Including Duplicates

**What it does:** Returns every row from all SELECT statements combined, **including duplicates**. This is faster than `UNION` because the database skips the sort-and-deduplicate step.

**Business scenario:** A grocery chain's **sales analytics team** is building a **trend volume report** to measure promotional impact. They need to count how many times each product area appeared across three separate weekly promotion batches — even if the same area was promoted multiple times. Using `UNION ALL` preserves every occurrence, enabling accurate frequency and reach calculations. If `UNION` were used instead, repeat promotions would be silently dropped, understating campaign reach.

```sql
-- Combine three promotion batch snapshots into one dataset, keeping all duplicate rows.
-- UNION ALL is preferred here because:
--   1. Duplicates are intentional — we want to count every promotional occurrence.
--   2. It is faster than UNION since no deduplication step is performed.
--   3. The downstream aggregation (COUNT, SUM) relies on all rows being present.
SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (1, 2)  -- Promotion Batch 1

UNION ALL

SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (1, 2)  -- Promotion Batch 2 (same areas re-promoted)

UNION ALL

SELECT product_area_name
FROM grocery_db.product_areas
WHERE product_area_id IN (1, 2); -- Promotion Batch 3 (same areas re-promoted again)
```

**Why this matters competitively:** Promotional frequency analysis is a core weapon in retail competition. Knowing that "Dairy" was promoted three times in Q2 while a competitor only promoted it once gives the merchandising team a concrete advantage when negotiating supplier terms and planning next quarter's price-match strategy. `UNION ALL` ensures none of those data points are lost.

---

## Key Decision Guide: UNION vs UNION ALL

```
Do you need each row to appear only once in the final result?
├── YES → Use UNION   (deduplicates, slightly slower)
└── NO  → Use UNION ALL (keeps all rows, faster — preferred for aggregations and audit trails)
```

**Competitive edge tip:** Always default to `UNION ALL` in high-volume ETL pipelines and wrap deduplication in an outer query (`SELECT DISTINCT` or `ROW_NUMBER()`) only when needed. This gives you full control over performance and data fidelity — critical when processing millions of daily transactions to stay ahead of competitors in real-time analytics.
