# CONDITIONAL RULES USING `CASE WHEN`

## What is `CASE WHEN`?

`CASE WHEN` is SQL's way of writing **if/else logic** — the same idea as "if this is true, do this; otherwise, do that."

Think of it like a supermarket checkout operator who says:

- _"If the item is on sale, charge the sale price — otherwise charge the normal price."_

`CASE WHEN` lets you create a **new column** whose value depends on conditions you define. You can use it anywhere a column or expression is allowed.

---

## Keyword Glossary (Beginner Reference)

| Keyword       | What it means                                                          |
| ------------- | ---------------------------------------------------------------------- |
| `SELECT`      | Choose which columns to return in your results                         |
| `FROM`        | Specify which table to read data from                                  |
| `CASE`        | Start a conditional block (like an `if` statement)                     |
| `WHEN`        | Define a condition to test (like `if condition`)                       |
| `THEN`        | What value to return **when** the condition is true                    |
| `ELSE`        | The fallback value if **none** of the `WHEN` conditions are true       |
| `END`         | Closes the `CASE` block — every `CASE` must have an `END`              |
| `AS`          | Give the new column a name (alias)                                     |
| `SUM()`       | Add up all values in a column or expression                            |
| `GROUP BY`    | Group rows together so aggregate functions like `SUM()` work per group |
| `WHERE`       | Filter rows — only rows matching the condition are included            |
| `IS NOT NULL` | A condition that is true when a value is **not** missing/empty         |

---

## Example 1 — Basic `CASE WHEN` (numeric output)

```sql
select
  customer_id,
  customer_loyalty_score,
  case when customer_loyalty_score > 0.5 then 1 else 0 end as high_loyal_flag
from
  grocery_db.loyalty_scores;
```

### How to read this line by line

| Line                                     | Explanation                                                            |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| `select`                                 | We are asking the database to return specific columns                  |
| `customer_id`                            | Return the customer's unique ID number                                 |
| `customer_loyalty_score`                 | Return the customer's loyalty score (a decimal between 0 and 1)        |
| `case when customer_loyalty_score > 0.5` | Start a condition: "Is the score greater than 0.5?"                    |
| `then 1`                                 | If yes → put the number `1` in this column                             |
| `else 0`                                 | If no → put the number `0` in this column                              |
| `end`                                    | Close the `CASE` block                                                 |
| `as high_loyal_flag`                     | Name the new column `high_loyal_flag`                                  |
| `from grocery_db.loyalty_scores`         | Read data from the `loyalty_scores` table in the `grocery_db` database |

### What the output looks like

| customer_id | customer_loyalty_score | high_loyal_flag |
| ----------- | ---------------------- | --------------- |
| 1001        | 0.82                   | 1               |
| 1002        | 0.31                   | 0               |
| 1003        | 0.67                   | 1               |

> **Company Use Case:** An e-commerce retailer tags each customer as `1` (loyal) or `0` (not loyal) so the marketing team can quickly filter and target loyal customers with exclusive early-access promotions.

---

## Example 2 — `CASE WHEN` with text labels

```sql
select
  customer_id,
  customer_loyalty_score,
  case when customer_loyalty_score > 0.5 then 'High Loyalty' else 'Low Loyalty' end as high_loyal_flag
from
  grocery_db.loyalty_scores;
```

### What changed from Example 1?

Instead of returning `1` or `0` (numbers), we now return the text strings `'High Loyalty'` or `'Low Loyalty'`. Text values in SQL must be wrapped in **single quotes** (`'`).

### What the output looks like

| customer_id | customer_loyalty_score | high_loyal_flag |
| ----------- | ---------------------- | --------------- |
| 1001        | 0.82                   | High Loyalty    |
| 1002        | 0.31                   | Low Loyalty     |

> **Company Use Case:** A subscription box company generates a customer segment label to display inside a CRM (Customer Relationship Management) dashboard. Non-technical staff can read "High Loyalty" instantly without knowing what 0.5 means.

---

## Example 3 — Multiple Conditions (like `if / else if / else`)

```sql
select
  customer_id,
  customer_loyalty_score,
  case
    when customer_loyalty_score > 0.66 then 'High loyal'
    when customer_loyalty_score > 0.33 then 'Medium loyal'
    else 'Low loyal' end as loyalty_category
from
  grocery_db.loyalty_scores;
```

### How SQL evaluates multiple `WHEN` conditions

SQL checks each `WHEN` condition **from top to bottom** and stops at the **first one that is true**. This is important!

- A score of `0.80` → matches `> 0.66` first → result: `'High loyal'`
- A score of `0.50` → does NOT match `> 0.66`, but matches `> 0.33` → result: `'Medium loyal'`
- A score of `0.10` → matches neither → falls to `else` → result: `'Low loyal'`

### Full breakdown

| Condition                       | Score range | Label returned |
| ------------------------------- | ----------- | -------------- |
| `customer_loyalty_score > 0.66` | 0.67 – 1.00 | High loyal     |
| `customer_loyalty_score > 0.33` | 0.34 – 0.66 | Medium loyal   |
| `else`                          | 0.00 – 0.33 | Low loyal      |

> **Company Use Case — Airline:** A frequent flyer program uses three tiers to determine reward eligibility:
>
> - **High loyal** → eligible for business-class upgrade vouchers
> - **Medium loyal** → eligible for lounge day passes
> - **Low loyal** → standard member, no extras
>
> The marketing team runs monthly campaigns against each tier automatically.

---

## Example 4 — `CASE WHEN` + `SUM()` + `GROUP BY` (Pivot-style Aggregation)

This is one of the most powerful patterns in SQL. It lets you **reshape rows into columns** — sometimes called a "pivot."

```sql
select
  customer_id,
  sum(case when product_area_id = 1 then sales_cost else 0 end) as non_food_sales,
  sum(case when product_area_id = 2 then sales_cost else 0 end) as veg_sales,
  sum(case when product_area_id = 3 then sales_cost else 0 end) as fruit_sales,
  sum(case when product_area_id = 4 then sales_cost else 0 end) as dairy_sales,
  sum(case when product_area_id = 5 then sales_cost else 0 end) as meat_sales
from
  grocery_db.transactions
group by
  customer_id;
```

### Understanding the pattern

Take this one line as an example:

```sql
sum(case when product_area_id = 1 then sales_cost else 0 end) as non_food_sales
```

| Part                            | Explanation                                                    |
| ------------------------------- | -------------------------------------------------------------- |
| `case when product_area_id = 1` | Check: is this transaction from product area 1 (non-food)?     |
| `then sales_cost`               | If yes → use the actual `sales_cost` value from this row       |
| `else 0`                        | If no → use `0` (so it doesn't affect the total for this area) |
| `sum(...)`                      | Add up all those values per customer after grouping            |
| `as non_food_sales`             | Name this new total column `non_food_sales`                    |

### Why `else 0` is important

Without `else 0`, the `else` would return `NULL`. Adding `NULL` to a number in SQL returns `NULL`, which would break your totals. Using `else 0` ensures you're always adding a safe value.

### What the output looks like

| customer_id | non_food_sales | veg_sales | fruit_sales | dairy_sales | meat_sales |
| ----------- | -------------- | --------- | ----------- | ----------- | ---------- |
| 1001        | 12.50          | 8.00      | 5.25        | 14.00       | 22.75      |
| 1002        | 0.00           | 18.50     | 3.00        | 9.50        | 0.00       |

> **Company Use Case — Supermarket Chain:** The commercial analytics team wants to understand each customer's spending split across departments. This "spend per category" view is fed into a recommendation engine that suggests relevant promotions — a customer spending heavily on meat gets a butcher counter deal, while a high veg spender gets organic range offers.

---

## Practical Exercise — Distance Category

### Task description

You've been tasked with creating a categorised version of a customer's distance from the store.

Your new column (`distance_from_store_category`) will follow these rules:

- If a customer lives **less than 1 mile** from the store → `"distance: close"`
- If a customer lives **less than 2.5 miles** (but more than 1 mile) → `"distance: medium"`
- Otherwise, if a customer lives **further than 2.5 miles** → `"distance: far"`

Your query will return three columns: `customer_id`, `distance_from_store`, `distance_from_store_category`.

**Bonus:** Exclude any rows where `distance_from_store` is missing (NULL).

---

### Solution

```sql
select
  customer_id,
  distance_from_store,
  case when distance_from_store < 1   then 'distance: close'
       when distance_from_store < 2.5 then 'distance: medium'
       else 'distance: far' end as distance_from_store_category
from
  grocery_db.customer_details
where
  distance_from_store is not null;
```

### Keyword breakdown for this query

| Keyword / Expression                    | Role in this query                                                        |
| --------------------------------------- | ------------------------------------------------------------------------- |
| `select`                                | Choose the three columns to return                                        |
| `customer_id`                           | The unique identifier for each customer                                   |
| `distance_from_store`                   | The raw distance value stored in the table                                |
| `case when distance_from_store < 1`     | Start condition: is the distance under 1 mile?                            |
| `then 'distance: close'`                | If yes → label it close                                                   |
| `when distance_from_store < 2.5`        | Next condition: is it under 2.5 miles? (already know it's ≥ 1 from above) |
| `then 'distance: medium'`               | If yes → label it medium                                                  |
| `else 'distance: far'`                  | Everything else (≥ 2.5 miles) → label it far                              |
| `end`                                   | Close the `CASE` block                                                    |
| `as distance_from_store_category`       | Name the new column                                                       |
| `from grocery_db.customer_details`      | The table containing customer data                                        |
| `where distance_from_store is not null` | **Bonus filter** — exclude rows with no distance value recorded           |

### Why `IS NOT NULL` matters

If a customer has no recorded distance, `CASE WHEN` cannot evaluate it correctly and would fall into `else 'distance: far'` — which would be wrong. By filtering those rows out with `WHERE distance_from_store IS NOT NULL`, you keep your data clean and accurate.

### What the output looks like

| customer_id | distance_from_store | distance_from_store_category |
| ----------- | ------------------- | ---------------------------- |
| 2001        | 0.4                 | distance: close              |
| 2002        | 1.8                 | distance: medium             |
| 2003        | 4.1                 | distance: far                |
| 2004        | 0.9                 | distance: close              |

> **Company Use Case — Retail Chain:** The operations team uses distance categories to decide delivery logistics:
>
> - **Close** customers → targeted for walk-in promotions and same-day click & collect
> - **Medium** customers → offered next-day home delivery
> - **Far** customers → offered scheduled weekly delivery slots or partner courier options
>
> The delivery cost model is also applied per category, allowing the finance team to estimate logistics budgets without calculating distances manually each time.

---

## Summary — When to Use `CASE WHEN`

| Scenario                            | Pattern to use                                      |
| ----------------------------------- | --------------------------------------------------- |
| Flag a condition as 1 or 0          | `CASE WHEN condition THEN 1 ELSE 0 END`             |
| Label rows with readable text       | `CASE WHEN condition THEN 'Label' ELSE 'Other' END` |
| Create multiple tiers / buckets     | Chain multiple `WHEN ... THEN` blocks before `ELSE` |
| Pivot rows into columns with totals | Wrap `CASE WHEN` inside `SUM()` with `GROUP BY`     |
