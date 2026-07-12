# Temp Tables & CTEs for Multiple Queries

## Why Multi-Step Queries Matter in a Competitive Business

In a data-driven company aiming to stay ahead of the competition, raw data rarely answers business questions directly. Most strategic decisions — from loyalty programmes to pricing strategy — require **aggregating data across multiple steps**. SQL provides two key tools for this: **Temporary Tables** and **Common Table Expressions (CTEs)**. Knowing when and how to use each is essential for any analyst supporting fast-moving business decisions.

---

## Exploring the Data

```sql
-- Preview all transactions for a single customer.
-- Use case: A customer success manager wants to quickly audit one customer's
-- purchase history before a retention call. Catching high-value customers
-- before they churn is a direct competitive advantage.

SELECT *                            -- retrieve every column (all transaction details)
FROM grocery_db.transactions        -- source table: raw transaction rows (one row per product bought)
WHERE customer_id = 1;             -- filter: only return rows belonging to customer 1
```

---

## Temporary Tables

A **temporary table** stores an intermediate result set in the database session. It behaves like a real table — you can query it multiple times, join it to other tables, or build on it further. The table is automatically dropped when the session ends.

**When to use:** When you need to reuse the same intermediate result across several separate queries, or when your query tool does not support CTEs.

### Step 1 — Build the Temporary Table

```sql
-- Business context: Our merchandising team needs to understand spending at the
-- transaction level (one receipt = one transaction_id) before comparing customers.
-- Because the raw transactions table stores one row per product within a transaction,
-- we must SUM sales_cost to roll each transaction up to a single total.
--
-- Competitive use case: Identifying which customers generate the highest revenue
-- per visit lets the marketing team target them with exclusive offers BEFORE
-- a rival grocery chain does.

CREATE TEMP TABLE cust_transactions AS (  -- creates a temporary table named cust_transactions;
                                           -- it exists only for the current session and is
                                           -- automatically dropped when the session closes
    SELECT
        customer_id,                       -- keep the customer identifier so we know who shopped
        transaction_id,                    -- keep the transaction identifier (one receipt = one trip)
        SUM(sales_cost) AS total_sales     -- add up the cost of every product in this transaction
                                           -- to produce a single basket total; alias it total_sales
    FROM grocery_db.transactions           -- read from the raw transactions table
    GROUP BY customer_id, transaction_id   -- collapse all product rows that share the same
                                           -- customer_id AND transaction_id into one summary row
);
```

### Step 2 — Inspect the Intermediate Result

```sql
-- Verify the temp table looks correct before building on top of it.
-- A quick sanity-check here prevents costly mistakes in downstream reports
-- that executives rely on for competitive pricing decisions.

SELECT *                  -- retrieve all columns (customer_id, transaction_id, total_sales)
FROM cust_transactions;   -- read from the temporary table we just created above
```

### Step 3 — Aggregate Again to Find Average Spend per Customer

```sql
-- Business context: The loyalty team wants to tier customers by average basket
-- size. Customers with a high average transaction value are prime candidates for
-- a "Premium" tier with exclusive perks — keeping them loyal and away from
-- competitor promotions.
--
-- Because we already aggregated to transaction level in the temp table, we can
-- now simply average those totals per customer without re-scanning the full
-- transactions table, which is faster and easier to read.

SELECT
    customer_id,                              -- identify which customer this row belongs to
    AVG(total_sales) AS avg_transaction_sales -- calculate the mean basket value across all of
                                              -- that customer's transactions; alias the result
FROM cust_transactions                        -- read from the temp table (already at transaction level)
GROUP BY customer_id;                         -- produce one summary row per unique customer
```

---

## Common Table Expressions (CTEs)

A **CTE** (introduced with the `WITH` keyword) defines a named subquery that exists only for the duration of the single statement that follows it. You can chain multiple CTEs together, each building on the previous one.

**When to use:** When all your logic can be expressed in one self-contained statement. CTEs are easier to read, version-control, and share with colleagues than temp tables.

```sql
-- Business context: The strategy team needs to know who the single highest-value
-- customer is by average transaction spend. This metric feeds directly into the
-- quarterly "Customer Lifetime Value" report used to benchmark against competitors.
--
-- CTE 1 (cust_transactions_cte): Rolls each transaction up to a total spend figure,
--   exactly the same first step as the temp table approach above.
--
-- CTE 2 (cust_sales_cte): Reads from CTE 1 and calculates each customer's
--   average transaction spend — a second level of aggregation on top of the first.
--
-- Final SELECT: Pulls the single maximum average from CTE 2, identifying the
--   top-spending customer segment for targeted competitive retention programmes.

WITH cust_transactions_cte AS (       -- WITH declares the start of a CTE block;
                                       -- cust_transactions_cte is the name of this first CTE

    SELECT
        customer_id,                   -- retain the customer identifier
        transaction_id,                -- retain the transaction identifier (one shopping trip)
        SUM(sales_cost) AS total_sales -- sum every product's cost within the same transaction
    FROM grocery_db.transactions       -- source: raw table with one row per product purchased
    GROUP BY customer_id, transaction_id -- group so each unique trip becomes one summary row

),                                     -- comma separates this CTE from the next one

cust_sales_cte AS (                    -- second CTE builds on the first

    SELECT
        customer_id,                          -- pass the customer identifier through
        AVG(total_sales) AS avg_transaction_sales -- average all transaction totals for this customer
    FROM cust_transactions_cte                -- read from the first CTE (already at transaction level)
    GROUP BY customer_id                      -- one row per customer

)

-- Final query: reads from the second CTE to find the single highest average
SELECT MAX(avg_transaction_sales) AS max_avg_sales  -- return only the top average spend value
FROM cust_sales_cte;                                -- sourced from the customer-level averages CTE
```

---

## Business Challenge: Incentivising Big-Basket Shoppers

**Stakeholder brief:** The commercial director wants to launch a "Mega Basket" reward for customers who spend the most in a single visit. To design the reward thresholds, they need each customer's **largest single transaction** in dollar terms.

**Why this matters competitively:** Knowing which customers already make large one-off purchases lets the business craft a targeted voucher or cashback offer _before_ a competitor does. Retaining these high-value shoppers can meaningfully shift basket-size benchmarks across the chain.

**The data challenge:** The `transactions` table stores one row _per product_, so a single shopping trip (one `transaction_id`) spans many rows. We must:

1. **First aggregation** — SUM `sales_cost` by `customer_id` + `transaction_id` to get the value of each complete transaction.
2. **Second aggregation** — MAX those transaction totals by `customer_id` to find each customer's biggest single spend.

**Output required:** One row per customer, with columns `customer_id` and `max_transaction_sales`, sorted ascending by `customer_id` so the stakeholder can cross-reference a customer list easily.

---

### Solution A — Using a CTE

```sql
-- CTE approach: both aggregation steps live inside one readable statement.
-- Ideal for sharing in a BI tool or embedding in a scheduled report because
-- there is no session-state dependency — anyone can run it cold and get the
-- same result.

WITH cust_transactions_cte AS (  -- begin the CTE; name it cust_transactions_cte

    -- Step 1: collapse product-level rows into one total per transaction.
    SELECT
        customer_id,               -- which customer made this purchase
        transaction_id,            -- which specific shopping trip (receipt)
        SUM(sales_cost) AS total_sales  -- total spend for all items in this one trip
    FROM grocery_db.transactions   -- raw source: one row per product line on a receipt
    GROUP BY
        customer_id,               -- ┐ group by both columns so we get one row
        transaction_id             -- ┘ per unique customer + trip combination

)                                  -- end of the CTE definition (no semicolon here)

-- Step 2: from those transaction totals, find the biggest single spend
-- per customer. ORDER BY customer_id makes the output easy to join
-- against a CRM export for the marketing campaign.
SELECT
    customer_id,                            -- identify the customer in the output
    MAX(total_sales) AS max_transaction_sales -- find the single largest basket value
                                             -- across all trips for this customer
FROM cust_transactions_cte                  -- read from the CTE defined above
GROUP BY
    customer_id                             -- one output row per customer
ORDER BY
    customer_id;                            -- sort ascending by customer_id so stakeholders
                                            -- can easily look up a specific customer
```

---

### Solution B — Using a Temporary Table

```sql
-- Temporary table approach: useful when an analyst needs to run several
-- follow-up queries against the intermediate result — e.g., also checking
-- average and median transaction sizes — without recomputing the first
-- aggregation each time. In a large grocery database with millions of rows,
-- this can save significant query time during an interactive analysis session.

-- Step 1: create the intermediate transaction-level summary.
CREATE TEMP TABLE cust_transactions AS (  -- create a session-scoped temporary table;
                                           -- it persists until the session ends or is dropped manually

    SELECT
        customer_id,                       -- the customer who made the purchase
        transaction_id,                    -- the unique identifier for one shopping trip
        SUM(sales_cost) AS total_sales     -- sum the cost of every product line within
                                           -- the same transaction to get one basket total
    FROM grocery_db.transactions           -- raw source table (one row per product per transaction)
    GROUP BY
        customer_id,                       -- ┐ group by both to produce one row per
        transaction_id                     -- ┘ unique customer + transaction combination

);                                         -- semicolon ends the CREATE TEMP TABLE statement

-- Step 2: query the temp table to surface each customer's peak spend.
-- The temp table can be reused for additional questions (e.g., average,
-- percentile breakdowns) without hitting the raw transactions table again.
SELECT
    customer_id,                            -- identify the customer in the result set
    MAX(total_sales) AS max_transaction_sales -- find the highest basket value recorded
                                             -- across all of this customer's transactions
FROM cust_transactions                      -- read from the temp table (already aggregated)
GROUP BY
    customer_id                             -- collapse to one row per customer
ORDER BY
    customer_id;                            -- sort by customer_id ascending so the output
                                            -- is easy to scan or merge with other reports
```

---

## Key Takeaways

|                 | Temporary Table                                                | CTE                                                                      |
| --------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Reusability** | Can be queried multiple times in the same session              | Single statement only                                                    |
| **Readability** | Logic split across multiple statements                         | All logic in one place                                                   |
| **Performance** | Result materialised on disk/memory; faster for repeated access | Re-evaluated each time (in most databases)                               |
| **Best for**    | Interactive exploration, iterative follow-up questions         | Scheduled reports, sharing queries, complex multi-step logic in one shot |

> **In both solutions, the pattern is identical:** first aggregate product rows up to the transaction level, then aggregate those transaction totals up to the customer level. Mastering this two-step aggregation pattern is one of the most valuable skills for an analyst supporting competitive business intelligence.
