# Weekly SQL Challenge 12

## Problem Summary

You are working with `grocery_db.customer_details`.

Goal: return the **average customer credit score**, split by gender, for customers who live **less than 2 miles** from the store.

## Expected Output

Your result should contain one row per gender and these columns:

- `gender`
- `avg_credit_score`

## Why This Matters for Business

This query helps businesses understand the financial profile of nearby customers. Nearby customers are easier and cheaper to target, so this can guide profitable local marketing and credit-related strategies.

### Company Use Cases (Competition + Profitability)

- Build localized campaigns for nearby customer groups with stronger purchasing power.
- Adjust promotions and payment options by customer segment to improve conversion.
- Support risk-aware decisions for programs like buy-now-pay-later or store financing.
- Improve marketing ROI by focusing on high-potential customers close to store locations.
- Stay competitive by tailoring offers using local customer behavior instead of one-size-fits-all campaigns.

## SQL Solution

```sql
select
  gender,
  avg(credit_score) as avg_credit_score
from
  grocery_db.customer_details
where
  distance_from_store < 2
group by
  gender;
```

## Beginner Explanation (Step by Step)

### Step 1: Choose what to show

We want gender and an average score.

- `gender` tells us the segment.
- `avg(credit_score)` calculates the average credit score for each segment.

### Step 2: Pick the source table

Use `grocery_db.customer_details`, which contains customer attributes like gender, credit score, and distance from the store.

### Step 3: Filter to nearby customers

`distance_from_store < 2` keeps only customers who live less than 2 miles away.

### Step 4: Group by gender

`group by gender` creates one group per gender so the average is calculated separately for each group.

## Line-by-Line SQL Breakdown

1. `select`
   - Starts the query and defines the output columns.

2. `gender,`
   - Returns the gender value for each group.

3. `avg(credit_score) as avg_credit_score`
   - Calculates the average credit score for rows in each group.
   - Names this calculated result `avg_credit_score`.

4. `from`
   - Starts the table reference.

5. `grocery_db.customer_details`
   - Reads data from the customer details table.

6. `where`
   - Starts row filtering before grouping.

7. `distance_from_store < 2`
   - Keeps only customers located within 2 miles of the store.

8. `group by`
   - Tells SQL to aggregate rows by the listed column.

9. `gender;`
   - Groups rows by gender so each output row is one gender segment.

## Decision-Making Insights for Leaders

- If one nearby segment has a higher average credit score, the company can test premium offers in that segment.
- If a segment has lower average credit score, the company can design lower-risk, high-volume promotions.
- Combining this with purchase history helps decide where to invest in store expansion or hyper-local advertising.

## Practical Caution

Credit score usage should follow legal, compliance, and fairness policies. Use aggregated insights for strategy, and avoid unfair treatment of protected groups.
