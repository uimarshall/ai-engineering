# Weekly SQL Challenge 10

## Problem Summary

You are working with `grocery_db.transactions` and need to calculate the **average spend per customer** for customers who shopped **less than 5 times**.

### Required Output Columns

- `customer_id`
- `average_transaction_spend`
- `transaction_count`

## Why This Matters in a Business

This type of analysis helps companies identify **low-frequency customers** and decide how to increase retention and profitability.

### Example Use Cases

- A grocery company can find customers who only buy 1-4 times, then send targeted coupons to increase visit frequency.
- A retail company can compare average spend among low-frequency customers to decide whether to focus on:
  - Increasing basket size (upsell/cross-sell)
  - Increasing visit frequency (loyalty campaigns)
- Leadership can use this as an early signal for churn risk and plan actions before customers stop buying.

## Important Data Modeling Note

The table is at:

- `customer_id + transaction_id + product_area_id`

That means a **single transaction** may appear in multiple rows (one row per product area).
So transaction count must be based on unique `transaction_id` (or a grouped transaction-level table), not raw row count.

## SQL Solution

```sql
with transaction_totals as (
 select
  customer_id,
  transaction_id,
  sum(sales_cost) as total_transaction_spend
 from
  grocery_db.transactions
 group by
  customer_id,
  transaction_id
),
customer_avg_spend as (
 select
  customer_id,
  avg(total_transaction_spend) as average_transaction_spend,
  count(transaction_id) as transaction_count
 from
  transaction_totals
 group by
  customer_id
)
select
 customer_id,
 average_transaction_spend,
 transaction_count
from
 customer_avg_spend
where
 transaction_count < 5;
```

## Beginner Explanation (Step by Step)

### Step 1: `transaction_totals` CTE

Goal: Convert product-area-level rows into **one row per transaction**.

- `sum(sales_cost)` adds all product area costs in the same transaction.
- Grouping by `customer_id, transaction_id` ensures one total per customer transaction.

Business impact:

- Gives true basket value per visit.
- Prevents over-counting purchases, which would lead to incorrect KPIs and poor business decisions.

### Step 2: `customer_avg_spend` CTE

Goal: Roll up transaction-level data to **customer-level behavior**.

- `avg(total_transaction_spend)` calculates average basket size per customer.
- `count(transaction_id)` gives number of transactions per customer.

Business impact:

- Helps segment customers by value and engagement.
- Supports strategy decisions like loyalty tiers, personalized offers, and budget allocation.

### Step 3: Final Filter

Goal: Keep only customers with `transaction_count < 5`.

Business impact:

- Focuses on less active customers who may be easier to grow than acquiring brand-new customers.
- Useful for retention campaigns that improve profitability over time.

## Line-by-Line SQL Breakdown

1. `with transaction_totals as (`
   - Starts a CTE named `transaction_totals`.

2. `select`
   - Begins selecting columns for this CTE.

3. `customer_id,`
   - Keeps the customer identifier.

4. `transaction_id,`
   - Keeps the transaction identifier.

5. `sum(sales_cost) as total_transaction_spend`
   - Adds all sales amounts in the same transaction and names it `total_transaction_spend`.

6. `from`
   - Starts the source table reference.

7. `grocery_db.transactions`
   - Reads data from the transactions table.

8. `group by`
   - Starts aggregation grouping.

9. `customer_id,`
   - Group key part 1.

10. `transaction_id`
    - Group key part 2. Together, this gives one row per transaction per customer.

11. `),`
    - Ends first CTE.

12. `customer_avg_spend as (`
    - Starts second CTE to calculate customer-level metrics.

13. `select`
    - Begins selecting columns for second CTE.

14. `customer_id,`
    - Keeps the customer identifier.

15. `avg(total_transaction_spend) as average_transaction_spend,`
    - Calculates each customer's average spend across their transactions.

16. `count(transaction_id) as transaction_count`
    - Counts how many transactions each customer has.

17. `from`
    - Starts source reference for this CTE.

18. `transaction_totals`
    - Uses output from first CTE (already one row per transaction).

19. `group by`
    - Groups results by customer.

20. `customer_id`
    - One row per customer.

21. `)`
    - Ends second CTE.

22. `select`
    - Starts final result selection.

23. `customer_id,`
    - Returns customer ID.

24. `average_transaction_spend,`
    - Returns average spend metric.

25. `transaction_count`
    - Returns number of transactions.

26. `from`
    - Starts source reference for final output.

27. `customer_avg_spend`
    - Reads from second CTE.

28. `where`
    - Starts filtering condition.

29. `transaction_count < 5;`
    - Keeps only customers with fewer than 5 transactions.

## Practical Company Actions After This Query

- Build a campaign list of low-frequency customers and send personalized reactivation offers.
- Prioritize customers with high average spend but low visit count (high upside segment).
- Track conversion of this segment month-over-month to measure retention and profit lift.
