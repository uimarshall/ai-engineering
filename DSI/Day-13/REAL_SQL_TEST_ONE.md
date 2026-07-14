# SQL TEST — Grocery Business Analytics

> **Business Context:** A grocery retail company wants to leverage its transaction and customer data to stay ahead of the competition, make smarter inventory and marketing decisions, and drive profitability. The queries below demonstrate real analytical SQL that supports those goals.

---

## 01. How many rows are there in the transactions table?

**Business Scenario:** Before running any analysis, a data analyst or business intelligence team needs to audit the size of the dataset. Knowing the total transaction count establishes a baseline — if that number drops unexpectedly compared to the prior week, it could indicate a data pipeline failure, a system outage, or a sudden drop in customer activity that needs immediate attention.

```sql
SELECT COUNT(*) FROM grocery_db.transactions;
```

**Line-by-line breakdown:**

- `SELECT COUNT(*)` — Counts every row in the table, including rows with NULL values in any column. This returns a single integer representing the total number of transaction records.
- `FROM grocery_db.transactions` — Targets the `transactions` table inside the `grocery_db` database schema.

**Profitability Insight:** Monitoring this count over time can reveal sales volume trends — rising counts signal growth; declining counts may warrant a competitive pricing review or a marketing campaign.

---

## 02. Return the customer_id for the customer who lives farthest from the store

**Business Scenario:** A grocery chain wants to understand the reach of its brand and identify loyal customers who go out of their way to shop at their store despite the distance. These customers are prime candidates for a "Loyalty Champion" rewards tier, a home delivery upsell, or a targeted retention campaign — all of which directly protect revenue from competitors who may be geographically closer to that customer.

### Method 1 — Simple ORDER BY with LIMIT (single result)

```sql
SELECT
    customer_id,
    distance_from_store

FROM grocery_db.customer_details

WHERE
    distance_from_store IS NOT NULL

ORDER BY
    distance_from_store DESC

LIMIT 1;
```

**Line-by-line breakdown:**

- `SELECT customer_id, distance_from_store` — Retrieves only the two columns needed: the customer identifier and how far they live from the store.
- `FROM grocery_db.customer_details` — Pulls data from the `customer_details` table in the `grocery_db` schema.
- `WHERE distance_from_store IS NOT NULL` — Filters out any customers where distance data was not recorded, ensuring we don't accidentally surface a NULL as the maximum value.
- `ORDER BY distance_from_store DESC` — Sorts all remaining rows from the largest distance to the smallest (descending), putting the farthest customer at the top.
- `LIMIT 1` — Returns only the first row after sorting, which is the single customer with the greatest distance.

**Limitation:** If two customers are tied for the maximum distance, this method returns only one of them arbitrarily.

---

### Method 2 — Subquery JOIN (handles ties correctly)

```sql
SELECT
    a.customer_id

FROM
    grocery_db.customer_details a

INNER JOIN (
    SELECT
        MAX(distance_from_store) AS max_dist
    FROM grocery_db.customer_details
) b ON a.distance_from_store = b.max_dist;
```

**Line-by-line breakdown:**

- `SELECT a.customer_id` — Returns only the customer ID(s) from the outer query. The alias `a` refers to the main `customer_details` table.
- `FROM grocery_db.customer_details a` — The outer query reads from `customer_details`, aliased as `a` for readability when used alongside the subquery.
- `INNER JOIN (...)` — Joins the main table to the result of a subquery. An `INNER JOIN` only returns rows where a match exists in both sides.
- `SELECT MAX(distance_from_store) AS max_dist FROM grocery_db.customer_details` — The subquery calculates the single highest distance value across the entire table and labels it `max_dist`.
- `b ON a.distance_from_store = b.max_dist` — The join condition: only customers whose distance equals the maximum distance (computed in the subquery) are returned. If multiple customers share the same maximum, all of them are returned — no tie-breaking ambiguity.

**Profitability Insight:** Identifying distant loyal customers allows the business to offer targeted delivery or click-and-collect incentives before a competitor does, protecting high-value customer relationships.

---

## 03. Return the number of unique customers, split by gender

**Business Scenario:** Understanding the gender split of your customer base is foundational to targeted marketing. If 65% of customers are female, a grocery chain can prioritise promotional spend on products that over-index with that segment (e.g., beauty, organic foods). Matching marketing spend to actual customer demographics is a direct lever for improving return on ad spend (ROAS) and outpacing competitors who market generically.

```sql
SELECT
    gender,
    COUNT(DISTINCT customer_id) AS customer_count

FROM
    grocery_db.customer_details

GROUP BY gender;
```

**Line-by-line breakdown:**

- `SELECT gender` — Retrieves the gender field, which will become the label for each group in the result set.
- `COUNT(DISTINCT customer_id) AS customer_count` — Counts only unique customer IDs within each gender group. Using `DISTINCT` prevents double-counting a customer who may appear multiple times in the table (e.g., due to duplicate records). The result is aliased as `customer_count` for clarity.
- `FROM grocery_db.customer_details` — Reads from the customer details table.
- `GROUP BY gender` — Collapses all rows into one row per distinct gender value, so the `COUNT` aggregation is applied per group rather than across the entire table.

**Profitability Insight:** Gender-segmented counts feed directly into demographic dashboards used by category managers and CMOs to allocate shelf space, plan seasonal promotions, and set competitive pricing strategies.

---

## 04. Total sales by product area for July 2020, ordered highest to lowest

**Business Scenario:** A Head of Trading wants to know which product areas (e.g., Bakery, Produce, Meat, Dairy) generated the most revenue in a specific month. This drives decisions about where to expand shelf space, which suppliers to negotiate harder with, and which departments are underperforming relative to competitors. Month-on-month comparisons of this query can surface emerging trends before competitors act on them.

```sql
SELECT
    b.product_area_name,
    SUM(a.sales_cost) AS total_sales

FROM
    grocery_db.transactions a

INNER JOIN grocery_db.product_areas b
    ON a.product_area_id = b.product_area_id

WHERE
    a.transaction_date BETWEEN '2020-07-01' AND '2020-07-31'

GROUP BY
    b.product_area_name

ORDER BY
    total_sales DESC;
```

**Line-by-line breakdown:**

- `SELECT b.product_area_name` — Retrieves the human-readable product area name (e.g., "Bakery") from the `product_areas` table (aliased `b`), rather than just the numeric ID.
- `SUM(a.sales_cost) AS total_sales` — Adds up all individual transaction sale amounts for each product area, aliased as `total_sales`.
- `FROM grocery_db.transactions a` — The primary table containing one row per transaction. Aliased as `a`.
- `INNER JOIN grocery_db.product_areas b ON a.product_area_id = b.product_area_id` — Joins the transactions table to the product areas lookup table. The `ON` clause links the numeric foreign key (`product_area_id`) in transactions to the matching primary key in `product_areas`. Only transactions that have a matching product area are included (INNER JOIN behaviour).
- `WHERE a.transaction_date BETWEEN '2020-07-01' AND '2020-07-31'` — Filters the data to only include transactions that occurred within July 2020. `BETWEEN` is inclusive of both boundary dates.
- `GROUP BY b.product_area_name` — Collapses all rows sharing the same product area name into a single row so the `SUM` aggregation operates per product area.
- `ORDER BY total_sales DESC` — Sorts the final result from the highest-grossing product area to the lowest, making it immediately readable for business stakeholders.

**Profitability Insight:** If "Bakery" consistently ranks near the bottom, the business might consider a premium in-store bakery refit to compete with rival chains. If "Produce" is top, investing in fresh supply chain improvements protects that revenue stream.

---

## 05. Customers who do NOT have a loyalty score

**Business Scenario:** A loyalty programme is one of the strongest competitive moats in grocery retail. Customers enrolled in a loyalty scheme are less price-sensitive and churn less to competitors. This query identifies customers who exist in the system but have never been assigned a loyalty score — these are "unengaged" customers who have not yet been brought into the loyalty ecosystem. They are high-priority targets for onboarding campaigns (e.g., "Sign up for points today!") to deepen their relationship with the brand before a competitor captures them.

```sql
SELECT
    DISTINCT a.customer_id

FROM
    grocery_db.customer_details a

LEFT JOIN grocery_db.loyalty_scores b
    ON a.customer_id = b.customer_id

WHERE
    b.customer_id IS NULL;
```

**Line-by-line breakdown:**

- `SELECT DISTINCT a.customer_id` — Returns unique customer IDs from the `customer_details` table. `DISTINCT` ensures no customer appears more than once in the output even if they have multiple detail records.
- `FROM grocery_db.customer_details a` — The base table containing all known customers, aliased as `a`. This is the "left" side of the join, meaning all rows from here are preserved.
- `LEFT JOIN grocery_db.loyalty_scores b ON a.customer_id = b.customer_id` — A `LEFT JOIN` returns every row from `customer_details` and any matching rows from `loyalty_scores`. If a customer has no loyalty score, the columns from `loyalty_scores` are filled with `NULL` for that row.
- `WHERE b.customer_id IS NULL` — After the LEFT JOIN, this filter keeps only the rows where there was **no match** in `loyalty_scores` — i.e., the customer exists in `customer_details` but is absent from `loyalty_scores`. This is the classic "anti-join" pattern for finding gaps between two tables.

**Profitability Insight:** Enrolling even 10% of unscored customers into the loyalty programme can measurably increase basket size and visit frequency. This query is the starting point for building that targeted outreach list — a direct, data-driven driver of revenue growth and competitive differentiation.
