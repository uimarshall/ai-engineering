# Sorting and Ranking Data with Pandas

> **Day 51 — Data Science Interview Prep**  
> This guide explains how to sort and rank data using pandas, with detailed explanations for beginners and real-world company use cases.

---

## Table of Contents

- [Sorting and Ranking Data with Pandas](#sorting-and-ranking-data-with-pandas)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Sorting Data](#sorting-data)
    - [Sorting a Series by Values](#sorting-a-series-by-values)
    - [Sorting a DataFrame by a Single Column](#sorting-a-dataframe-by-a-single-column)
    - [Sorting by Multiple Columns](#sorting-by-multiple-columns)
    - [Sorting in Descending Order](#sorting-in-descending-order)
    - [Sorting by Index](#sorting-by-index)
    - [Handling Missing Values (NaN) While Sorting](#handling-missing-values-nan-while-sorting)
    - [In-Place Sorting](#in-place-sorting)
    - [Resetting Index After Sorting](#resetting-index-after-sorting)
  - [Ranking Data](#ranking-data)
    - [Basic Ranking](#basic-ranking)
    - [Ranking Methods (Tie-Breaking)](#ranking-methods-tie-breaking)
    - [Ranking in Descending Order](#ranking-in-descending-order)
    - [Ranking with Percentages](#ranking-with-percentages)
    - [Handling NaN Values in Ranking](#handling-nan-values-in-ranking)
    - [Ranking Across Rows vs Columns](#ranking-across-rows-vs-columns)
  - [Practical Company Use Cases](#practical-company-use-cases)
    - [1. **E-Commerce: Product Ranking by Sales Performance**](#1-e-commerce-product-ranking-by-sales-performance)
    - [2. **HR Analytics: Employee Performance Ranking**](#2-hr-analytics-employee-performance-ranking)
    - [3. **Finance: Credit Score Ranking for Loan Approval**](#3-finance-credit-score-ranking-for-loan-approval)
    - [4. **Supply Chain: Vendor Ranking by Reliability**](#4-supply-chain-vendor-ranking-by-reliability)
    - [5. **Marketing: Customer Segmentation by Purchase Frequency**](#5-marketing-customer-segmentation-by-purchase-frequency)
  - [Summary Cheat Sheet](#summary-cheat-sheet)
  - [Key Takeaways for Beginners](#key-takeaways-for-beginners)

---

## Introduction

**Sorting** means arranging data in a specific order — typically ascending (smallest to largest, A to Z) or descending (largest to smallest, Z to A).  
**Ranking** means assigning a position (1st, 2nd, 3rd…) to each value based on its relative size compared to others.

Think of sorting like rearranging books on a shelf by height, and ranking like giving each book a sticker saying "1st tallest", "2nd tallest", etc.

In pandas, we use:

- `.sort_values()` — to sort data by values
- `.sort_index()` — to sort data by its index (row or column labels)
- `.rank()` — to assign ranks to values

---

## Sorting Data

### Sorting a Series by Values

A **Series** is a single column of data (like a list with labels).

```python
import pandas as pd
import numpy as np

# Create a Series with random numbers
obj = pd.Series([4, 7, -3, 2])

# Sort the Series in ascending order (default)
sorted_obj = obj.sort_values()
print(sorted_obj)
```

**Detailed Explanation for Beginners:**

- `pd.Series([4, 7, -3, 2])` creates a pandas Series. Think of it as a column in a spreadsheet with automatic row numbers (0, 1, 2, 3).
- `.sort_values()` rearranges the numbers from smallest to largest.
- The numbers on the left (0, 2, 3, 1) are the **original index positions** — pandas remembers where each value came from!
- `-3` is the smallest, so it appears first. `7` is the largest, so it appears last.

**Output:**

```
2   -3
3    2
0    4
1    7
dtype: int64
```

---

### Sorting a DataFrame by a Single Column

A **DataFrame** is a table with rows and columns (like an Excel sheet).

```python
# Create a sample DataFrame
frame = pd.DataFrame({
    "b": [4, 7, -3, 2],
    "a": [0, 1, 0, 1]
})

print("Original DataFrame:")
print(frame)

# Sort by column 'b'
sorted_frame = frame.sort_values("b")
print("
Sorted by column 'b':")
print(sorted_frame)
```

**Detailed Explanation for Beginners:**

- `pd.DataFrame({"b": [4, 7, -3, 2], "a": [0, 1, 0, 1]})` creates a table with 2 columns (`b` and `a`) and 4 rows.
- `.sort_values("b")` tells pandas: "Look at column `b` and rearrange ALL rows based on the values in that column."
- Notice that when row 2 (with `b = -3`) moves to the top, its corresponding `a` value (`0`) moves with it! The entire row stays together.
- By default, sorting is **ascending** (smallest to largest).

**Output:**

```
Original DataFrame:
   b  a
0  4  0
1  7  1
2 -3  0
3  2  1

Sorted by column 'b':
   b  a
2 -3  0
3  2  1
0  4  0
1  7  1
```

---

### Sorting by Multiple Columns

Sometimes you want to sort by one column first, and if there are ties (equal values), sort by another column.

```python
frame2 = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "department": ["Sales", "IT", "Sales", "IT", "Sales"],
    "salary": [50000, 70000, 55000, 72000, 48000]
})

# Sort by department first, then by salary within each department
sorted_frame2 = frame2.sort_values(["department", "salary"])
print(sorted_frame2)
```

**Detailed Explanation for Beginners:**

- We pass a **list** of column names: `["department", "salary"]`.
- Pandas first sorts by `department` alphabetically: all "IT" people come before all "Sales" people.
- Then, within the "IT" group, it sorts by `salary` from lowest to highest.
- Then, within the "Sales" group, it sorts by `salary` from lowest to highest.
- This is like sorting a class roster by grade level first, then by last name within each grade.

**Output:**

```
      name department  salary
3    David         IT   72000
1      Bob         IT   70000
4      Eve      Sales   48000
0    Alice      Sales   50000
2  Charlie      Sales   55000
```

---

### Sorting in Descending Order

Use `ascending=False` to sort from largest to smallest.

```python
# Sort by salary from highest to lowest
sorted_desc = frame2.sort_values("salary", ascending=False)
print(sorted_desc)
```

**Detailed Explanation for Beginners:**

- `ascending=False` flips the order. Now the highest salary appears first.
- Think of it like flipping a stack of pancakes — the biggest one is now on top!
- You can also use `ascending=False` with multiple columns by passing a list: `ascending=[True, False]`.

**Output:**

```
      name department  salary
3    David         IT   72000
1      Bob         IT   70000
2  Charlie      Sales   55000
0    Alice      Sales   50000
4      Eve      Sales   48000
```

---

### Sorting by Index

Sometimes you want to sort by the row numbers or column names, not by the data values.

```python
# Create a DataFrame with a shuffled index
frame3 = pd.DataFrame(
    {"A": [1, 2, 3], "B": [4, 5, 6]},
    index=[2, 0, 1]  # Custom index: 2, 0, 1 (not the usual 0, 1, 2)
)

print("Original:")
print(frame3)

# Sort by index (row labels) — puts index in order 0, 1, 2
sorted_by_index = frame3.sort_index()
print("
Sorted by index:")
print(sorted_by_index)

# Sort columns alphabetically (axis=1 means columns)
sorted_cols = frame3.sort_index(axis=1, ascending=False)
print("
Sorted columns descending:")
print(sorted_cols)
```

**Detailed Explanation for Beginners:**

- `.sort_index()` sorts the **row labels** (the numbers on the left) in order.
- `axis=1` tells pandas to sort the **column labels** instead of row labels.
- `axis=0` (default) = rows, `axis=1` = columns.
- This is useful when your data got shuffled and you want to restore order.

---

### Handling Missing Values (NaN) While Sorting

Missing values are called `NaN` (Not a Number) in pandas. By default, they go to the end.

```python
obj_with_nan = pd.Series([4, np.nan, 7, np.nan, -3, 2])

# Default: NaN goes to the end
print("NaN at end (default):")
print(obj_with_nan.sort_values())

# Move NaN to the beginning
print("
NaN at beginning:")
print(obj_with_nan.sort_values(na_position="first"))
```

**Detailed Explanation for Beginners:**

- `np.nan` represents missing or empty data.
- By default, pandas puts missing values at the **bottom** so they don't interfere with your sorted data.
- `na_position="first"` moves them to the top — useful if you want to spot missing data quickly.
- `na_position="last"` is the default behavior.

**Output:**

```
NaN at end (default):
4   -3.0
5    2.0
0    4.0
2    7.0
1    NaN
3    NaN

NaN at beginning:
1    NaN
3    NaN
4   -3.0
5    2.0
0    4.0
2    7.0
```

---

### In-Place Sorting

By default, `.sort_values()` returns a **new** DataFrame and leaves the original unchanged. Use `inplace=True` to modify the original.

```python
frame4 = pd.DataFrame({"C": [3, 1, 2], "D": [6, 4, 5]})

# Method 1: Create a new DataFrame (original stays the same)
new_frame = frame4.sort_values("C")
print("Original unchanged:", frame4["C"].tolist())
print("New sorted:", new_frame["C"].tolist())

# Method 2: Modify the original DataFrame directly
frame4.sort_values("C", inplace=True)
print("Original now modified:", frame4["C"].tolist())
```

**Detailed Explanation for Beginners:**

- `inplace=True` is like using a pen to edit the original paper instead of making a photocopy.
- **Warning:** Once you use `inplace=True`, you cannot undo it! The original data is permanently changed.
- For beginners, it's often safer to create a new variable (Method 1) so you can compare before and after.

---

### Resetting Index After Sorting

After sorting, the row index might be out of order (like 2, 3, 0, 1). You can reset it.

```python
frame5 = pd.DataFrame({"value": [30, 10, 20]})
sorted_frame5 = frame5.sort_values("value")

print("Sorted but index is shuffled:")
print(sorted_frame5)

# Reset index to 0, 1, 2...
sorted_reset = sorted_frame5.reset_index(drop=True)
print("
Index reset:")
print(sorted_reset)

# Or do it in one step with ignore_index
sorted_clean = frame5.sort_values("value", ignore_index=True)
print("
Using ignore_index=True:")
print(sorted_clean)
```

**Detailed Explanation for Beginners:**

- After sorting, the index labels stay attached to their original rows, so they might look like `1, 2, 0` instead of `0, 1, 2`.
- `.reset_index(drop=True)` creates a fresh index starting from 0 and removes the old index.
- `ignore_index=True` inside `.sort_values()` does the same thing in one step — cleaner and faster!

---

## Ranking Data

### Basic Ranking

Ranking assigns each value a position number based on its size.

```python
obj = pd.Series([7, -5, 7, 4, 2, 0, 4])

# Default ranking (ascending, average method for ties)
ranks = obj.rank()
print(ranks)
```

**Detailed Explanation for Beginners:**

- `.rank()` looks at all values and gives the smallest value rank `1.0`, the second smallest rank `2.0`, etc.
- The value `-5` is the smallest, so it gets rank `1.0`.
- The value `0` is the second smallest, so it gets rank `2.0`.
- The value `2` is third, so it gets rank `3.0`.
- There are **two 4s** and **two 7s** — these are called **ties**.
- By default (`method='average'`), tied values get the **average** of the ranks they would have received.
  - The two `4`s occupy positions 4 and 5, so they both get `(4+5)/2 = 4.5`.
  - The two `7`s occupy positions 6 and 7, so they both get `(6+7)/2 = 6.5`.

**Output:**

```
0    6.5
1    1.0
2    6.5
3    4.5
4    3.0
5    2.0
6    4.5
dtype: float64
```

---

### Ranking Methods (Tie-Breaking)

When values are equal, pandas offers different ways to break the tie:

```python
df_ties = pd.DataFrame({
    "score": [100, 85, 85, 85, 70, 60]
})

print("Original scores:")
print(df_ties)

# Average (default): all tied items get the average rank
df_ties["rank_average"] = df_ties["score"].rank(method="average")

# Min: all tied items get the BEST available rank
df_ties["rank_min"] = df_ties["score"].rank(method="min")

# Max: all tied items get the WORST available rank
df_ties["rank_max"] = df_ties["score"].rank(method="max")

# First: ties are broken by order of appearance in the data
df_ties["rank_first"] = df_ties["score"].rank(method="first")

# Dense: like min, but next rank is always +1 (no gaps)
df_ties["rank_dense"] = df_ties["score"].rank(method="dense")

print("
Different ranking methods:")
print(df_ties)
```

**Detailed Explanation for Beginners:**

| Method    | How It Works                                                        | Example with three 85s                             |
| --------- | ------------------------------------------------------------------- | -------------------------------------------------- |
| `average` | All tied values get the average of the ranks they would occupy      | Ranks 2, 3, 4 → all get **3.0**                    |
| `min`     | All tied values get the **best** (smallest) rank available          | All three get **2.0** (next rank jumps to 5)       |
| `max`     | All tied values get the **worst** (largest) rank available          | All three get **4.0**                              |
| `first`   | First appearance gets the better rank, second gets next, etc.       | 2.0, 3.0, 4.0 (based on row order)                 |
| `dense`   | Like `min`, but the next different value gets the very next integer | All three get **2.0**, next gets **3.0** (no gap!) |

**Real-world analogy:** Imagine a race where three people tie for 2nd place:

- **average**: They all share a "2nd-3rd-4th place" trophy (average = 3rd)
- **min**: They all get 2nd place medals, and the next person gets 5th (skipping 3rd and 4th)
- **max**: They all get 4th place (the worst of the tied positions)
- **first**: Whoever crossed the line first among the three gets 2nd, next gets 3rd, etc.
- **dense**: They all get 2nd, and the next person gets 3rd (no skipped numbers)

**Output:**

```
   score  rank_average  rank_min  rank_max  rank_first  rank_dense
0    100           6.0       6.0       6.0         6.0         4.0
1     85           3.0       2.0       4.0         2.0         2.0
2     85           3.0       2.0       4.0         3.0         2.0
3     85           3.0       2.0       4.0         4.0         2.0
4     70           5.0       5.0       5.0         5.0         3.0
5     60           1.0       1.0       1.0         1.0         1.0
```

---

### Ranking in Descending Order

By default, `.rank()` gives the smallest value rank 1. Use `ascending=False` to reverse this.

```python
scores = pd.Series([50, 90, 90, 75, 60])

# Default: smallest gets rank 1
print("Ascending ranks (worst = 1):")
print(scores.rank())

# Descending: largest gets rank 1
print("
Descending ranks (best = 1):")
print(scores.rank(ascending=False))
```

**Detailed Explanation for Beginners:**

- `ascending=False` is what you want for **competition scores** — the highest score should be rank 1 (the winner!).
- Without it, the lowest score would be rank 1, which is usually not what you want for rankings.
- This is essential for leaderboards, sports rankings, and sales performance tables.

---

### Ranking with Percentages

Sometimes you want to know what **percentage** of values are below a given value.

```python
exam_scores = pd.Series([55, 78, 82, 91, 65, 88, 72])

# Rank as percentage (0 to 1)
percentile_ranks = exam_scores.rank(pct=True)
print("Percentile ranks:")
print(percentile_ranks)
```

**Detailed Explanation for Beginners:**

- `pct=True` converts ranks to percentiles between 0 and 1.
- A percentile rank of `0.857` means this score is better than ~85.7% of all scores.
- This is how standardized tests like the SAT report scores!
- Multiply by 100 to get a traditional percentage: `0.857 * 100 = 85.7%`.

**Output:**

```
Percentile ranks:
0    0.143
1    0.429
2    0.571
3    1.000
4    0.286
5    0.857
6    0.714
```

---

### Handling NaN Values in Ranking

```python
scores_with_nan = pd.Series([80, np.nan, 95, np.nan, 70])

# Default: NaN gets NaN rank (excluded from ranking)
print("Default (keep NaN):")
print(scores_with_nan.rank())

# Put NaN at the bottom (worst rank)
print("
NaN at bottom:")
print(scores_with_nan.rank(na_option="bottom"))

# Put NaN at the top (best rank)
print("
NaN at top:")
print(scores_with_nan.rank(na_option="top"))
```

**Detailed Explanation for Beginners:**

- `na_option="keep"` (default): Missing values are not ranked at all — they stay as `NaN`.
- `na_option="bottom"`: Missing values get the worst possible rank (as if they were the smallest/largest depending on `ascending`).
- `na_option="top"`: Missing values get the best possible rank.
- Use `"bottom"` if missing data should be penalized (e.g., missing exam score = last place).

---

### Ranking Across Rows vs Columns

By default, `.rank()` ranks down each column. You can rank across rows instead.

```python
frame = pd.DataFrame({
    "math": [85, 90, 78],
    "science": [92, 88, 95],
    "english": [78, 85, 88]
}, index=["Alice", "Bob", "Charlie"])

print("Original:")
print(frame)

# Rank each student's subjects (row-wise)
# axis=1 means rank across columns for each row
row_ranks = frame.rank(axis=1, ascending=False)
print("
Row-wise ranks (1 = best subject for each student):")
print(row_ranks)

# Rank each subject across students (column-wise, default)
# axis=0 means rank down each column
col_ranks = frame.rank(axis=0, ascending=False)
print("
Column-wise ranks (1 = best student in each subject):")
print(col_ranks)
```

**Detailed Explanation for Beginners:**

- `axis=1` (row-wise): For each student (row), rank their subjects. Alice's best subject gets 1, second best gets 2, etc.
- `axis=0` (column-wise, default): For each subject (column), rank all students. The best math score gets 1, second best gets 2, etc.
- Think of `axis=1` as reading left-to-right across a row, and `axis=0` as reading top-to-bottom down a column.

**Output:**

```
Original:
         math  science  english
Alice      85       92       78
Bob        90       88       85
Charlie    78       95       88

Row-wise ranks (1 = best subject for each student):
         math  science  english
Alice     2.0      1.0      3.0
Bob       1.0      2.0      3.0
Charlie   3.0      1.0      2.0

Column-wise ranks (1 = best student in each subject):
         math  science  english
Alice     3.0      2.0      3.0
Bob       1.0      3.0      2.0
Charlie   2.0      1.0      1.0
```

---

## Practical Company Use Cases

### 1. **E-Commerce: Product Ranking by Sales Performance**

**Scenario:** An online retailer wants to identify their top-performing products.

```python
import pandas as pd

# Sales data
products = pd.DataFrame({
    "product_id": ["P001", "P002", "P003", "P004", "P005"],
    "product_name": ["Wireless Mouse", "USB-C Hub", "Mechanical Keyboard", "Webcam 4K", "Monitor Stand"],
    "units_sold": [1200, 850, 1500, 600, 950],
    "revenue": [36000, 25500, 112500, 18000, 14250],
    "customer_rating": [4.5, 4.2, 4.8, 3.9, 4.1]
})

# Rank products by revenue (descending = best seller is #1)
products["revenue_rank"] = products["revenue"].rank(ascending=False, method="min")

# Rank products by customer rating
products["rating_rank"] = products["customer_rating"].rank(ascending=False, method="dense")

# Sort by revenue rank to see top sellers first
top_products = products.sort_values("revenue_rank")
print(top_products[["product_name", "revenue", "revenue_rank", "rating_rank"]])
```

**Business Value:**

- Quickly identify which products drive the most revenue.
- Compare revenue rank vs. rating rank to find "hidden gems" (high rating but low sales — potential for marketing push).
- Inventory teams can prioritize stock for top-ranked items.

---

### 2. **HR Analytics: Employee Performance Ranking**

**Scenario:** A company's HR department needs to rank employees for annual bonuses.

```python
employees = pd.DataFrame({
    "employee_id": ["E101", "E102", "E103", "E104", "E105", "E106"],
    "name": ["John", "Sarah", "Mike", "Emma", "David", "Lisa"],
    "department": ["Sales", "Sales", "IT", "IT", "Sales", "IT"],
    "sales_made": [450000, 380000, 0, 0, 520000, 0],
    "projects_completed": [8, 6, 12, 10, 9, 11],
    "customer_satisfaction": [4.7, 4.5, 4.8, 4.2, 4.9, 4.6]
})

# Rank sales employees by sales made (within Sales department only)
sales_staff = employees[employees["department"] == "Sales"].copy()
sales_staff["sales_rank"] = sales_staff["sales_made"].rank(ascending=False, method="min")

# Rank IT employees by projects completed
it_staff = employees[employees["department"] == "IT"].copy()
it_staff["project_rank"] = it_staff["projects_completed"].rank(ascending=False, method="dense")

print("Sales Team Rankings:")
print(sales_staff[["name", "sales_made", "sales_rank"]].sort_values("sales_rank"))

print("
IT Team Rankings:")
print(it_staff[["name", "projects_completed", "project_rank"]].sort_values("project_rank"))
```

**Business Value:**

- Fairly distribute bonuses based on objective rankings.
- Department-specific rankings ensure fair comparison (don't compare salespeople to IT staff directly).
- Identify top performers for promotion consideration.

---

### 3. **Finance: Credit Score Ranking for Loan Approval**

**Scenario:** A bank wants to rank loan applicants by creditworthiness.

```python
applicants = pd.DataFrame({
    "applicant_id": ["A001", "A002", "A003", "A004", "A005"],
    "credit_score": [720, 680, 750, 620, 700],
    "annual_income": [75000, 52000, 95000, 45000, 60000],
    "debt_to_income_ratio": [0.25, 0.40, 0.15, 0.55, 0.30]
})

# Lower debt-to-income is better, so ascending=True (default)
applicants["dti_rank"] = applicants["debt_to_income_ratio"].rank(method="min")

# Higher credit score is better
applicants["credit_rank"] = applicants["credit_score"].rank(ascending=False, method="dense")

# Sort by credit rank to see most creditworthy first
best_applicants = applicants.sort_values("credit_rank")
print(best_applicants[["applicant_id", "credit_score", "credit_rank", "debt_to_income_ratio", "dti_rank"]])
```

**Business Value:**

- Automate loan approval decisions — only approve top-ranked applicants.
- Risk assessment teams can quickly identify high-risk (low-ranked) applicants.
- Set interest rates based on ranking tiers (top rank = lower interest rate).

---

### 4. **Supply Chain: Vendor Ranking by Reliability**

**Scenario:** A manufacturing company ranks vendors to decide who gets the biggest contracts.

```python
vendors = pd.DataFrame({
    "vendor_name": ["Vendor_A", "Vendor_B", "Vendor_C", "Vendor_D", "Vendor_E"],
    "on_time_delivery_pct": [95, 88, 92, 98, 85],
    "quality_score": [4.2, 4.5, 3.8, 4.7, 4.0],
    "cost_per_unit": [12.50, 11.00, 10.50, 13.00, 11.50]
})

# Rank by on-time delivery (higher is better)
vendors["delivery_rank"] = vendors["on_time_delivery_pct"].rank(ascending=False, method="min")

# Rank by quality (higher is better)
vendors["quality_rank"] = vendors["quality_score"].rank(ascending=False, method="min")

# Rank by cost (lower is better — use ascending=True)
vendors["cost_rank"] = vendors["cost_per_unit"].rank(ascending=True, method="dense")

# Composite score: average of all ranks (lower composite = better overall)
vendors["composite_rank"] = (vendors["delivery_rank"] + vendors["quality_rank"] + vendors["cost_rank"]) / 3

# Sort by composite rank
best_vendors = vendors.sort_values("composite_rank")
print(best_vendors[["vendor_name", "composite_rank", "delivery_rank", "quality_rank", "cost_rank"]])
```

**Business Value:**

- Make data-driven vendor selection decisions instead of relying on gut feeling.
- Identify which vendors excel in specific areas (e.g., best quality vs. best cost).
- Negotiate better terms with top-ranked vendors by offering larger contract volumes.

---

### 5. **Marketing: Customer Segmentation by Purchase Frequency**

**Scenario:** A marketing team wants to rank customers by engagement to target VIP campaigns.

```python
customers = pd.DataFrame({
    "customer_id": ["C001", "C002", "C003", "C004", "C005", "C006"],
    "total_purchases": [45, 12, 78, 23, 56, 8],
    "total_spent": [2300, 450, 5600, 890, 3200, 200],
    "last_purchase_days_ago": [5, 45, 3, 30, 10, 60]
})

# Rank by total purchases (descending)
customers["purchase_rank"] = customers["total_purchases"].rank(ascending=False, method="min")

# Rank by total spent (descending)
customers["spending_rank"] = customers["total_spent"].rank(ascending=False, method="min")

# Rank by recency — fewer days since last purchase is BETTER, so ascending=True
customers["recency_rank"] = customers["last_purchase_days_ago"].rank(ascending=True, method="dense")

# Identify VIP customers (top 3 in spending)
customers["is_vip"] = customers["spending_rank"] <= 3

print(customers[["customer_id", "total_spent", "spending_rank", "is_vip"]].sort_values("spending_rank"))
```

**Business Value:**

- Automatically identify VIP customers for exclusive offers and early access to sales.
- Create tiered loyalty programs (Gold, Silver, Bronze) based on spending ranks.
- Target at-risk customers (high recency rank = haven't purchased in a while) with win-back campaigns.

---

## Summary Cheat Sheet

| Task                   | Method                                 | Key Parameters                                              |
| ---------------------- | -------------------------------------- | ----------------------------------------------------------- |
| Sort by column values  | `df.sort_values("col")`                | `by`, `ascending`, `inplace`, `na_position`, `ignore_index` |
| Sort by index          | `df.sort_index()`                      | `axis`, `ascending`, `inplace`                              |
| Rank values            | `df["col"].rank()`                     | `method`, `ascending`, `na_option`, `pct`, `axis`           |
| Handle ties            | `.rank(method="...")`                  | `"average"`, `"min"`, `"max"`, `"first"`, `"dense"`         |
| Put NaN first/last     | `.sort_values(na_position="first")`    | `"first"` or `"last"`                                       |
| Rank as percentile     | `.rank(pct=True)`                      | Returns 0.0 to 1.0                                          |
| Sort descending        | `.sort_values(ascending=False)`        | Flip the order                                              |
| Reset index after sort | `.sort_values(..., ignore_index=True)` | Clean 0, 1, 2... index                                      |

---

## Key Takeaways for Beginners

1. **Sorting** rearranges rows; **Ranking** adds a new column with position numbers.
2. Always check whether you want `ascending=True` (default) or `ascending=False` — this is the most common mistake!
3. Ties happen when values are equal. Choose the right `method` based on your business logic:
   - Use `"min"` for competition rankings (3 people tied for 2nd all get 2nd place).
   - Use `"dense"` when you don't want gaps in ranking (2nd, 2nd, 2nd, 3rd).
   - Use `"first"` when order of appearance matters.
4. `inplace=True` modifies the original DataFrame. When in doubt, create a copy instead.
5. `ignore_index=True` or `.reset_index(drop=True)` cleans up messy index numbers after sorting.
6. Missing data (`NaN`) can be handled with `na_position` (for sorting) and `na_option` (for ranking).

---

_Happy Learning! Keep practicing with real datasets to master sorting and ranking in pandas._
