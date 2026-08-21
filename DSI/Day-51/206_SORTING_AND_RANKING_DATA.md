# Day 51 — Sorting and Ranking Data with Pandas

> **File:** `206_Sorting_And_Ranking.py`  
> **Dataset:** `grocery_database.xlsx` (sheets: `customer_details`, `product_areas`)  
> **Goal:** Learn how to sort DataFrames and assign ranks to values using pandas.

---

## Table of Contents

1. [Setup & Data Loading](#setup--data-loading)
2. [Sorting DataFrames](#sorting-dataframes)
   - [Ascending Sort (Default)](#ascending-sort-default)
   - [Descending Sort](#descending-sort)
   - [Sorting by Multiple Columns](#sorting-by-multiple-columns)
   - [Handling Missing Values (NaN) in Sorting](#handling-missing-values-nan-in-sorting)
3. [Ranking Values](#ranking-values)
   - [Basic Ranking](#basic-ranking)
   - [Ranking Methods: `average`, `min`, `max`, `first`, `dense`](#ranking-methods)
   - [Handling NaN Values in Ranking](#handling-nan-values-in-ranking)
4. [Practical Company Use Cases](#practical-company-use-cases)
5. [Common Mistakes & Tips](#common-mistakes--tips)

---

## Setup & Data Loading

```python
# -*- coding: utf-8 -*-
```

**Explanation:** Declares the file encoding. Good practice for files that might contain special characters, though Python 3 handles UTF-8 by default.

```python
import pandas as pd
import numpy as np
```

**Explanation:**

- `pandas` (as `pd`) — the main library for data tables.
- `numpy` (as `np`) — a library for numerical computing. We need it here for `np.nan` (missing values) used in the ranking examples.

```python
customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")
```

**Explanation:**

- Loads two sheets from the grocery database Excel file:
  - `customer_details` — likely has columns like `customer_id`, `gender`, `distance_from_store`, `credit_score`, etc.
  - `product_areas` — likely has columns like `product_area_id`, `product_area_name`, `profit_margin`, etc.

---

## Sorting DataFrames

### What is Sorting?

Sorting means rearranging the rows of a DataFrame so that the values in one or more columns appear in a specific order — either from smallest to largest (**ascending**) or largest to smallest (**descending**).

Think of it like arranging books on a shelf by price: cheapest first (ascending) or most expensive first (descending).

---

### Ascending Sort (Default)

```python
customer_details.sort_values(by = "distance_from_store", inplace = True)
```

**Line-by-Line Explanation:**

1. `customer_details` — the DataFrame we want to sort.
2. `.sort_values()` — the pandas method for sorting rows by column values.
3. `by = "distance_from_store"` — tells pandas which column to use as the sorting key. In the grocery database, this column likely shows how far (in miles or km) each customer lives from the store.
4. `inplace = True` — **modifies the original DataFrame directly** instead of creating a copy. After this line, `customer_details` is permanently reordered.

**What happens?**

| Before (random order) | After (sorted by distance) |
| --------------------- | -------------------------- |
| Alice — 5.2 miles     | Bob — 1.1 miles            |
| Bob — 1.1 miles       | Carol — 2.5 miles          |
| Carol — 2.5 miles     | Alice — 5.2 miles          |

> **Beginner Tip:** `inplace=True` is like using a pen to edit the original paper. If you want to keep the original order too, use `inplace=False` (or omit it, since False is the default) and save the result to a new variable:
>
> ```python
> sorted_customers = customer_details.sort_values(by="distance_from_store")
> ```

---

### Descending Sort

```python
customer_details.sort_values(by = "distance_from_store", inplace = True, ascending = False)
```

**Line-by-Line Explanation:**

1. `by = "distance_from_store"` — same as before, sort by the distance column.
2. `ascending = False` — **reverses the order**. Now the largest values come first.
3. `inplace = True` — modifies the original DataFrame.

**What happens?**

| After (descending order) |
| ------------------------ |
| Alice — 5.2 miles        |
| Carol — 2.5 miles        |
| Bob — 1.1 miles          |

> **Beginner Tip:** `ascending=False` is what you use for "top 10" lists — top spenders, highest credit scores, most distant customers, etc.

**Business Context:** A grocery store might want to see the most distant customers first to plan delivery routes or identify areas where a new store location would help.

---

### Sorting by Multiple Columns

```python
customer_details.sort_values(by = ["distance_from_store", "credit_score"], inplace = True)
```

**Line-by-Line Explanation:**

1. `by = ["distance_from_store", "credit_score"]` — passes a **list** of two column names.
2. Pandas first sorts by the **first column** (`distance_from_store`).
3. If two customers have the **same distance**, pandas then sorts those tied rows by the **second column** (`credit_score`).

**Visual Example:**

| customer | distance | credit_score | Sort Order                        |
| -------- | -------- | ------------ | --------------------------------- |
| Bob      | 1.1      | 720          | 1st (closest)                     |
| Dave     | 1.1      | 680          | 2nd (same distance, lower credit) |
| Carol    | 2.5      | 750          | 3rd                               |
| Alice    | 5.2      | 700          | 4th (farthest)                    |

**Why two customers with distance 1.1?** Bob and Dave live equally close, but Bob has a better credit score (720 vs 680), so Bob appears first.

> **Beginner Tip:** You can add as many columns as you want to the list: `by=["col1", "col2", "col3"]`. Each additional column acts as a "tie-breaker."

**Business Context:** The store might want to prioritize marketing to close customers with good credit (they're nearby AND likely to pay for premium services).

---

### Handling Missing Values (NaN) in Sorting

```python
customer_details.sort_values(by = "distance_from_store", inplace = True, na_position = "first")
```

**Line-by-Line Explanation:**

1. `na_position = "first"` — tells pandas where to put rows that have **missing values** (`NaN`) in the sorting column.
2. `"first"` means missing values go to the **top** of the DataFrame.
3. The default is `"last"` (missing values go to the bottom).

**What happens?**

| customer | distance | Position         |
| -------- | -------- | ---------------- |
| Eve      | NaN      | 1st (NaN at top) |
| Bob      | 1.1      | 2nd              |
| Carol    | 2.5      | 3rd              |
| Alice    | 5.2      | 4th              |

> **Beginner Tip:** Use `na_position="first"` when you want to quickly spot missing data. It's like putting all the blank forms at the top of the pile so you notice them immediately.

**Business Context:** If a customer's distance is missing, the store might need to update their address in the system. Putting NaN first makes these records easy to find and fix.

---

## Ranking Values

### What is Ranking?

While **sorting** rearranges rows, **ranking** adds a new column that shows each value's position (1st, 2nd, 3rd...) relative to others.

Think of sorting like rearranging race finishers by time, and ranking like giving each runner a medal saying "1st place", "2nd place", etc.

---

### Basic Ranking

```python
x = pd.DataFrame({"column1" : [1,1,1,2,3,4,5,np.nan,6,8]})
```

**Line-by-Line Explanation:**

1. We create a small DataFrame `x` with one column called `"column1"`.
2. The values are: `1, 1, 1, 2, 3, 4, 5, NaN, 6, 8`.
3. Notice:
   - The value `1` appears **three times** — this is called a **tie**.
   - There is one `np.nan` (missing value).

```python
x["column1"].rank()
```

**Line-by-Line Explanation:**

1. `x["column1"]` — selects the column (a Series).
2. `.rank()` — assigns a rank to each value.
3. By default:
   - Smallest value gets rank `1.0`.
   - Ties get the **average** of the ranks they would have occupied.
   - `NaN` gets `NaN` rank (excluded from ranking).

**How the ranking works step by step:**

| Value | Position if no ties | Rank (average method) | Explanation              |
| ----- | ------------------- | --------------------- | ------------------------ |
| 1     | 1st, 2nd, 3rd       | 2.0                   | Average of 1, 2, 3 = 2.0 |
| 1     | 1st, 2nd, 3rd       | 2.0                   | Same tie                 |
| 1     | 1st, 2nd, 3rd       | 2.0                   | Same tie                 |
| 2     | 4th                 | 4.0                   | Next available rank      |
| 3     | 5th                 | 5.0                   | —                        |
| 4     | 6th                 | 6.0                   | —                        |
| 5     | 7th                 | 7.0                   | —                        |
| NaN   | —                   | NaN                   | Excluded                 |
| 6     | 8th                 | 8.0                   | —                        |
| 8     | 9th                 | 9.0                   | Largest value            |

> **Beginner Tip:** The three `1`s occupy ranks 1, 2, and 3. Since they're tied, they all get the average: `(1+2+3)/3 = 2.0`.

---

### Code: Creating Rank Columns

```python
x["column1_rank"] = x["column1"].rank()
```

**Explanation:** Creates a new column with the **default ranking** (same as above — `average` method, ascending, NaN excluded).

```python
x["average_rank"] = x["column1"].rank(method = "average")
```

**Explanation:** Explicitly uses the `"average"` method (same as default). Tied values get the average of their would-be ranks.

```python
x["min_rank"] = x["column1"].rank(method = "min")
```

**Explanation:** Uses the `"min"` method. All tied values get the **best** (smallest) rank available.

**For our three 1s:** They would occupy ranks 1, 2, 3. With `method="min"`, they ALL get rank `1.0`. The next value (`2`) gets rank `4.0` (skipping 2 and 3).

> **Real-world analogy:** Three people tie for 1st place in a race. They all get 1st place medals. The next person gets 4th place (not 2nd) because 2nd and 3rd were "used up" by the tie.

```python
x["max_rank"] = x["column1"].rank(method = "max")
```

**Explanation:** Uses the `"max"` method. All tied values get the **worst** (largest) rank available.

**For our three 1s:** They would occupy ranks 1, 2, 3. With `method="max"`, they ALL get rank `3.0`.

> **Real-world analogy:** Three people tie, but they all get the worst rank of the group — they all get 3rd place. The next person gets 4th place.

```python
x["first_rank"] = x["column1"].rank(method = "first")
```

**Explanation:** Uses the `"first"` method. Ties are broken by the **order they appear** in the data.

**For our three 1s:**

- The first `1` (row 0) gets rank `1.0`.
- The second `1` (row 1) gets rank `2.0`.
- The third `1` (row 2) gets rank `3.0`.

> **Real-world analogy:** Even though they finished at the same time, the person who crossed the line first (based on photo finish) gets 1st, the next gets 2nd, etc.

```python
x["dense_rank"] = x["column1"].rank(method = "dense")
```

**Explanation:** Uses the `"dense"` method. Similar to `"min"`, but the next rank is always exactly `+1` — no gaps!

**For our three 1s:** They ALL get rank `1.0`. The next value (`2`) gets rank `2.0` (not `4.0` like with `"min"`).

> **Real-world analogy:** Three people tie for 1st. They all get 1st place. The next person gets 2nd place (not 4th). There are no "missing" ranks.

**Complete Results Table:**

| column1 | average_rank | min_rank | max_rank | first_rank | dense_rank |
| ------- | ------------ | -------- | -------- | ---------- | ---------- |
| 1       | 2.0          | 1.0      | 3.0      | 1.0        | 1.0        |
| 1       | 2.0          | 1.0      | 3.0      | 2.0        | 1.0        |
| 1       | 2.0          | 1.0      | 3.0      | 3.0        | 1.0        |
| 2       | 4.0          | 4.0      | 4.0      | 4.0        | 2.0        |
| 3       | 5.0          | 5.0      | 5.0      | 5.0        | 3.0        |
| 4       | 6.0          | 6.0      | 6.0      | 6.0        | 4.0        |
| 5       | 7.0          | 7.0      | 7.0      | 7.0        | 5.0        |
| NaN     | NaN          | NaN      | NaN      | NaN        | NaN        |
| 6       | 8.0          | 8.0      | 8.0      | 8.0        | 6.0        |
| 8       | 9.0          | 9.0      | 9.0      | 9.0        | 7.0        |

---

### Handling NaN Values in Ranking

```python
x["dense_rank_na_top"] = x["column1"].rank(method = "dense", na_option = "top")
```

**Line-by-Line Explanation:**

1. `method = "dense"` — uses the dense ranking method.
2. `na_option = "top"` — assigns `NaN` values the **best** (smallest) rank, as if they were the smallest values.
3. The `NaN` gets rank `1.0`, and all other values are pushed down.

```python
x["dense_rank_na_bottom"] = x["column1"].rank(method = "dense", na_option = "bottom")
```

**Line-by-Line Explanation:**

1. `method = "dense"` — uses the dense ranking method.
2. `na_option = "bottom"` — assigns `NaN` values the **worst** (largest) rank, as if they were the largest values.
3. The `NaN` gets the last rank, and all other values keep their normal relative order.

**Comparison:**

| column1 | dense_rank (default) | dense_rank_na_top | dense_rank_na_bottom |
| ------- | -------------------- | ----------------- | -------------------- |
| 1       | 1.0                  | 2.0               | 1.0                  |
| 1       | 1.0                  | 2.0               | 1.0                  |
| 1       | 1.0                  | 2.0               | 1.0                  |
| 2       | 2.0                  | 3.0               | 2.0                  |
| ...     | ...                  | ...               | ...                  |
| NaN     | NaN                  | 1.0               | 8.0                  |

> **Beginner Tip:** Use `na_option="bottom"` when missing data should be penalized (e.g., missing exam score = last place). Use `na_option="top"` when missing data should be prioritized (rare, but useful in some ranking systems).

---

## Practical Company Use Cases

### Use Case 1: Grocery Store — Sorting Customers by Distance for Delivery Route Optimization

**Scenario:** The grocery store offers home delivery and wants to plan efficient routes.

```python
# Sort customers by distance — closest first for same-day delivery
customer_details.sort_values(by="distance_from_store", inplace=True)
```

**Business Value:**

- Delivery drivers visit the closest customers first, reducing fuel costs and delivery time.
- Customers who live nearby get faster service, improving satisfaction.
- Operations managers can estimate total delivery time by looking at the sorted list.

**Extended Example:**

```python
# Find the 10 closest customers for a quick delivery run
closest_10 = customer_details.sort_values(by="distance_from_store").head(10)
print(closest_10[["customer_id", "distance_from_store"]])
```

---

### Use Case 2: Grocery Store — Sorting by Multiple Criteria for VIP Identification

**Scenario:** The store wants to identify their most valuable customers using multiple factors.

```python
# Sort by distance (close customers are more likely to visit frequently)
# Then by credit score (higher score = more trustworthy for credit programs)
customer_details.sort_values(
    by=["distance_from_store", "credit_score"],
    ascending=[True, False],  # Close first, then high credit first
    inplace=True
)
```

**Business Value:**

- Marketing teams can create a "VIP" list of close, high-credit customers.
- These customers are ideal targets for premium membership programs.
- Store planners can use this data to decide where to open new locations (areas with many close, high-credit customers).

---

### Use Case 3: Grocery Store — Ranking Product Areas by Profit Margin

**Scenario:** The store wants to rank product areas to decide which categories deserve more shelf space.

```python
product_areas["profit_rank"] = product_areas["profit_margin"].rank(ascending=False, method="min")
product_areas.sort_values("profit_rank", inplace=True)
print(product_areas[["product_area_name", "profit_margin", "profit_rank"]])
```

**Business Value:**

- Category managers can instantly see which areas are most profitable.
- `"min"` method ensures that if two areas have the same profit margin, they both get the best available rank (e.g., both get 1st place if tied).
- `ascending=False` makes the highest profit margin rank #1 (the winner!).
- Underperforming areas (low rank) can be reviewed for pricing or product mix changes.

---

### Use Case 4: Grocery Store — Handling Missing Distance Data

**Scenario:** Some customers have missing address data, so their `distance_from_store` is NaN. The data entry team needs to find and fix these records.

```python
# Put all customers with missing distance at the TOP of the list
customer_details.sort_values(
    by="distance_from_store",
    na_position="first",
    inplace=True
)

# Extract just the ones with missing data
missing_distance = customer_details[customer_details["distance_from_store"].isna()]
print(f"Found {len(missing_distance)} customers with missing distance data.")
```

**Business Value:**

- Data quality team can quickly export the missing records for follow-up.
- Prevents delivery failures caused by incomplete addresses.
- Ensures analytics and reports are based on complete data.

---

### Use Case 5: Grocery Store — Dense Ranking for Employee Sales Performance

**Scenario:** The store ranks sales staff by monthly sales. They want a clean ranking system without gaps.

```python
sales_staff = pd.DataFrame({
    "employee": ["John", "Sarah", "Mike", "Emma", "David"],
    "monthly_sales": [45000, 52000, 52000, 38000, 41000]
})

# Three methods compared
sales_staff["average_rank"] = sales_staff["monthly_sales"].rank(ascending=False, method="average")
sales_staff["min_rank"] = sales_staff["monthly_sales"].rank(ascending=False, method="min")
sales_staff["dense_rank"] = sales_staff["monthly_sales"].rank(ascending=False, method="dense")

print(sales_staff.sort_values("monthly_sales", ascending=False))
```

**Results:**

| employee | monthly_sales | average_rank | min_rank | dense_rank |
| -------- | ------------- | ------------ | -------- | ---------- |
| Sarah    | 52000         | 1.5          | 1.0      | 1.0        |
| Mike     | 52000         | 1.5          | 1.0      | 1.0        |
| John     | 45000         | 3.0          | 3.0      | 2.0        |
| David    | 41000         | 4.0          | 4.0      | 3.0        |
| Emma     | 38000         | 5.0          | 5.0      | 4.0        |

**Business Value:**

- **HR uses `dense_rank`** for clean tier-based bonuses: Rank 1 = 20% bonus, Rank 2 = 15% bonus, Rank 3 = 10% bonus, etc. No skipped tiers.
- **Competition uses `min_rank`** for leaderboards: Two people tied for 1st both get 1st place. The next person is 3rd (no 2nd place).
- **Analytics uses `average_rank`** for statistical analysis: Tied employees get the average position, which is fair for calculating mean rankings.

---

## Common Mistakes & Tips

### Mistake 1: Forgetting `inplace=True` and Thinking the DataFrame Changed

```python
# This does NOT modify customer_details!
customer_details.sort_values(by="distance_from_store")
print(customer_details)  # Still in original order!

# CORRECT: Either use inplace=True...
customer_details.sort_values(by="distance_from_store", inplace=True)

# ...or save the result to a new variable
sorted_customers = customer_details.sort_values(by="distance_from_store")
```

### Mistake 2: Sorting Descending Without `ascending=False`

```python
# WRONG: This sorts ascending (smallest first) — NOT what you want for "top customers"
customer_details.sort_values(by="credit_score", inplace=True)

# CORRECT: Use ascending=False for "best first"
customer_details.sort_values(by="credit_score", ascending=False, inplace=True)
```

### Mistake 3: Using the Wrong Ranking Method for Your Business Case

```python
# WRONG for a competition leaderboard:
# "average" gives tied people fractional ranks (1.5, 2.5) — confusing for medals!

# CORRECT for competitions:
product_areas["rank"] = product_areas["profit_margin"].rank(method="min")

# CORRECT for tiered rewards (no gaps):
product_areas["tier"] = product_areas["profit_margin"].rank(method="dense")
```

### Tip: Always Check Your Data After Sorting

```python
# Verify the sort worked correctly
print(customer_details["distance_from_store"].head())
print(customer_details["distance_from_store"].tail())
```

### Tip: Combine Sorting with `.reset_index()` for Clean Output

```python
# After sorting, the index might be shuffled (e.g., 5, 2, 8, 1...)
# Reset it for a clean 0, 1, 2, 3... index
customer_details.sort_values(by="distance_from_store", inplace=True)
customer_details.reset_index(drop=True, inplace=True)
```

### Tip: Rank with `ascending=False` for "Higher is Better" Metrics

```python
# For sales, profit, credit score — higher is better, so rank 1 should be the HIGHEST
product_areas["profit_rank"] = product_areas["profit_margin"].rank(ascending=False)

# For cost, distance, complaints — lower is better, so rank 1 should be the LOWEST
customer_details["distance_rank"] = customer_details["distance_from_store"].rank(ascending=True)
```

---

## Summary Cheat Sheet

| Task                                | Code                                                      | Key Parameters                                |
| ----------------------------------- | --------------------------------------------------------- | --------------------------------------------- |
| Sort ascending (default)            | `df.sort_values(by="col", inplace=True)`                  | `by`, `inplace`                               |
| Sort descending                     | `df.sort_values(by="col", ascending=False, inplace=True)` | `ascending=False`                             |
| Sort by multiple columns            | `df.sort_values(by=["col1", "col2"], inplace=True)`       | List of column names                          |
| Put NaN first                       | `df.sort_values(by="col", na_position="first")`           | `na_position`                                 |
| Basic ranking                       | `series.rank()`                                           | Default: `method="average"`, `ascending=True` |
| Competition ranking (no fractional) | `series.rank(method="min")`                               | Tied values get best rank                     |
| Dense ranking (no gaps)             | `series.rank(method="dense")`                             | Next rank is always +1                        |
| Break ties by appearance order      | `series.rank(method="first")`                             | First seen gets better rank                   |
| Penalize missing values             | `series.rank(na_option="bottom")`                         | NaN gets worst rank                           |
| Prioritize missing values           | `series.rank(na_option="top")`                            | NaN gets best rank                            |
| Rank descending (best = 1)          | `series.rank(ascending=False)`                            | For "higher is better" metrics                |

---

_Master sorting and ranking, and you'll be able to organize any dataset and identify top performers with confidence!_
