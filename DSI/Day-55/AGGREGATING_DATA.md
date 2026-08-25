# Aggregating Data Using Pandas

> **Day 54 — Data Science Interview (DSI) Prep Series**  
> A beginner-friendly deep dive into `groupby`, aggregation functions, pivot tables, and real-world business applications.

---

## Table of Contents

1. [Why Do We Aggregate Data?](#1-why-do-we-aggregate-data)
2. [Basic Aggregation Without GroupBy](#2-basic-aggregation-without-groupby)
3. [The `groupby` Mindset: Split → Apply → Combine](#3-the-groupby-mindset-split--apply--combine)
4. [Your First `groupby`](#4-your-first-groupby)
5. [Built-in Aggregation Functions](#5-built-in-aggregation-functions)
6. [The `.agg()` Method — Multiple Aggregations at Once](#6-the-agg-method--multiple-aggregations-at-once)
7. [Grouping by Multiple Columns](#7-grouping-by-multiple-columns)
8. [`.transform()` — Keep the Original Shape](#8-transform--keep-the-original-shape)
9. [`.filter()` — Remove Entire Groups](#9-filter--remove-entire-groups)
10. [`.apply()` — Custom Logic per Group](#10-apply--custom-logic-per-group)
11. [Sorting & Ranking Within Groups](#11-sorting--ranking-within-groups)
12. [Cumulative & Rolling Aggregations](#12-cumulative--rolling-aggregations)
13. [Pivot Tables with `pivot_table()`](#13-pivot-tables-with-pivot_table)
14. [Cross-Tabulation with `crosstab()`](#14-cross-tabulation-with-crosstab)
15. [Handling Missing Data in Groups](#15-handling-missing-data-in-groups)
16. [Real-World Company Use Cases](#16-real-world-company-use-cases)
17. [Common Mistakes & How to Avoid Them](#17-common-mistakes--how-to-avoid-them)
18. [Quick Reference Cheat Sheet](#18-quick-reference-cheat-sheet)

---

## 1. Why Do We Aggregate Data?

Raw data is **noisy and granular**. A retail company might have millions of individual transactions, but a manager wants to know:

- "What is the **total revenue** per region?"
- "What is the **average order value** per customer segment?"
- "Which **product category** had the highest sales last quarter?"

**Aggregation** means summarizing many rows into fewer, meaningful rows. It turns raw data into **actionable insights**.

> **Analogy:** Aggregation is like a report card. Instead of listing every homework score, it gives you an average grade per subject.

---

## 2. Basic Aggregation Without GroupBy

Before grouping, let's see how to aggregate an **entire column**.

```python
import pandas as pd
import numpy as np

# Sample sales data
df = pd.DataFrame({
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard'],
    'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics',
                 'Electronics', 'Accessories', 'Accessories'],
    'region': ['North', 'North', 'South', 'South', 'North', 'South', 'North'],
    'units_sold': [10, 50, 30, 15, 8, 45, 25],
    'revenue': [15000, 2500, 4500, 6000, 12000, 2250, 3750],
    'customer_rating': [4.5, 4.0, 3.5, 4.8, 4.2, 4.1, 3.8]
})

print(df)
```

**Output:**

```
    product     category   region  units_sold  revenue  customer_rating
0    Laptop  Electronics    North          10    15000              4.5
1     Mouse  Accessories    North          50     2500              4.0
2  Keyboard  Accessories    South          30     4500              3.5
3   Monitor  Electronics    South          15     6000              4.8
4    Laptop  Electronics    North           8    12000              4.2
5     Mouse  Accessories    South          45     2250              4.1
6  Keyboard  Accessories    North          25     3750              3.8
```

### Single-Column Aggregations

```python
# Total revenue across ALL products
total_revenue = df['revenue'].sum()
print(f"Total Revenue: ${total_revenue:,}")        # $46,000

# Average customer rating
avg_rating = df['customer_rating'].mean()
print(f"Average Rating: {avg_rating:.2f}")         # 4.13

# Total units sold
total_units = df['units_sold'].sum()
print(f"Total Units Sold: {total_units}")          # 183

# Number of transactions (rows)
num_transactions = df['revenue'].count()
print(f"Transactions: {num_transactions}")         # 7

# Maximum revenue in a single transaction
max_revenue = df['revenue'].max()
print(f"Max Revenue: ${max_revenue:,}")            # $15,000

# Minimum rating received
min_rating = df['customer_rating'].min()
print(f"Min Rating: {min_rating}")                 # 3.5

# Standard deviation of revenue
revenue_std = df['revenue'].std()
print(f"Revenue Std Dev: ${revenue_std:.2f}")      # $4,966.55
```

### `.describe()` — Instant Summary Statistics

```python
print(df[['units_sold', 'revenue', 'customer_rating']].describe())
```

**Output:**

```
       units_sold       revenue  customer_rating
count    7.000000      7.000000         7.000000
mean    26.142857   6571.428571         4.128571
std     16.340134   4966.554809         0.414578
min     8.000000   2250.000000         3.500000
25%     15.000000   3000.000000         3.850000
50%     25.000000   4500.000000         4.100000
75%     37.500000   9750.000000         4.350000
max     50.000000  15000.000000         4.800000
```

### `.agg()` on a Single Column

```python
# Multiple stats for one column
revenue_stats = df['revenue'].agg(['sum', 'mean', 'min', 'max', 'std'])
print(revenue_stats)
```

**Output:**

```
sum      46000.000000
mean      6571.428571
min       2250.000000
max      15000.000000
std       4966.554809
Name: revenue, dtype: float64
```

---

## 3. The `groupby` Mindset: Split → Apply → Combine

`groupby` is the most powerful tool for aggregation in pandas. It follows a three-step process:

```
┌─────────────────────────────────────────────────────────────┐
│  SPLIT          APPLY           COMBINE                     │
│  ─────          ─────           ───────                     │
│                                                             │
│  Raw Data  →  Group 1    →    Result for Group 1           │
│               Group 2    →    Result for Group 2           │
│               Group 3    →    Result for Group 3           │
│                                                             │
│  [A,A,B,B]    [A],[A]    →    A: result                   │
│               [B],[B]    →    B: result                   │
└─────────────────────────────────────────────────────────────┘
```

**Step 1 — SPLIT:** Divide the DataFrame into groups based on one or more columns.  
**Step 2 — APPLY:** Run a function (sum, mean, custom) on each group independently.  
**Step 3 — COMBINE:** Stitch the results back into a single DataFrame or Series.

> **Analogy:** Imagine sorting exam papers by subject, grading each pile separately, then compiling a report per subject. That's `groupby`.

---

## 4. Your First `groupby`

### Syntax

```python
df.groupby('column_to_group_by')['column_to_aggregate'].aggregation_function()
```

### Example: Revenue by Category

```python
# Total revenue per product category
revenue_by_category = df.groupby('category')['revenue'].sum()
print(revenue_by_category)
```

**Output:**

```
category
Accessories    13000
Electronics    33000
Name: revenue, dtype: int64
```

**What happened?**

- **SPLIT:** Rows were split into two groups — "Accessories" and "Electronics".
- **APPLY:** The `sum()` function was applied to the `revenue` column within each group.
- **COMBINE:** Results were combined into a Series with the group labels as the index.

### Example: Multiple Stats per Category

```python
# Average units sold and average rating per category
category_stats = df.groupby('category')[['units_sold', 'customer_rating']].mean()
print(category_stats)
```

**Output:**

```
             units_sold  customer_rating
category
Accessories   37.500000         3.866667
Electronics   11.000000         4.500000
```

### The GroupBy Object

```python
# What does groupby() return?
grouped = df.groupby('category')
print(type(grouped))  # <class 'pandas.core.groupby.DataFrameGroupBy'>

# You can iterate over groups (useful for debugging)
for name, group in grouped:
    print(f"\n=== Group: {name} ===")
    print(group)
```

**Output:**

```
<class 'pandas.core.groupby.generic.DataFrameGroupBy'>

=== Group: Accessories ===
    product     category region  units_sold  revenue  customer_rating
1     Mouse  Accessories  North          50     2500              4.0
2  Keyboard  Accessories  South          30     4500              3.5
5     Mouse  Accessories  South          45     2250              4.1
6  Keyboard  Accessories  North          25     3750              3.8

=== Group: Electronics ===
   product     category region  units_sold  revenue  customer_rating
0   Laptop  Electronics  North          10    15000              4.5
3  Monitor  Electronics  South          15     6000              4.8
4   Laptop  Electronics  North           8    12000              4.2
```

---

## 5. Built-in Aggregation Functions

After `groupby()`, you can call these functions directly:

| Function     | What It Does                   | Example Output Type |
| ------------ | ------------------------------ | ------------------- |
| `.sum()`     | Sum of values                  | Series or DataFrame |
| `.mean()`    | Arithmetic mean                | Series or DataFrame |
| `.median()`  | Median (middle value)          | Series or DataFrame |
| `.count()`   | Count of non-null values       | Series or DataFrame |
| `.size()`    | Count of rows (includes nulls) | Series              |
| `.min()`     | Minimum value                  | Series or DataFrame |
| `.max()`     | Maximum value                  | Series or DataFrame |
| `.std()`     | Standard deviation             | Series or DataFrame |
| `.var()`     | Variance                       | Series or DataFrame |
| `.sem()`     | Standard error of mean         | Series or DataFrame |
| `.first()`   | First non-null value           | Series or DataFrame |
| `.last()`    | Last non-null value            | Series or DataFrame |
| `.nth(n)`    | N-th row in each group         | DataFrame           |
| `.nunique()` | Count of unique values         | Series              |

### Code Examples

```python
# Count of transactions per region
transactions_per_region = df.groupby('region').size()
print(transactions_per_region)
# Output:
# region
# North    4
# South    3
# dtype: int64

# Count non-null ratings per region (same as size here since no nulls)
count_per_region = df.groupby('region')['customer_rating'].count()
print(count_per_region)

# Most revenue from a single transaction, per category
max_revenue_per_category = df.groupby('category')['revenue'].max()
print(max_revenue_per_category)
# Output:
# category
# Accessories     4500
# Electronics    15000
# Name: revenue, dtype: int64

# Number of unique products per region
unique_products = df.groupby('region')['product'].nunique()
print(unique_products)
# Output:
# region
# North    3
# South    3
# Name: product, dtype: int64

# First transaction per category (useful for time-series)
first_transaction = df.groupby('category').first()
print(first_transaction)
```

---

## 6. The `.agg()` Method — Multiple Aggregations at Once

The `.agg()` (or `.aggregate()`) method is incredibly powerful. It lets you compute **multiple statistics** on **multiple columns** in **one line**.

### Same Function on Multiple Columns

```python
# Sum of both units_sold AND revenue per category
category_totals = df.groupby('category')[['units_sold', 'revenue']].agg('sum')
print(category_totals)
```

**Output:**

```
             units_sold  revenue
category
Accessories         150    13000
Electronics          33    33000
```

### Different Functions on Different Columns

```python
# Different stats for different columns
custom_summary = df.groupby('category').agg({
    'revenue': ['sum', 'mean', 'max'],           # Revenue: total, average, best
    'units_sold': ['sum', 'mean'],               # Units: total, average
    'customer_rating': ['mean', 'min', 'max']    # Rating: average, worst, best
})

print(custom_summary)
```

**Output:**

```
              revenue                  units_sold       customer_rating
                  sum         mean    max        sum       mean          mean min max
category
Accessories     13000  4333.333333   4500        150  37.500000      3.866667 3.5 4.1
Electronics     33000  11000.000000  15000        33  11.000000      4.500000 4.2 4.8
```

### Named Aggregations (Clean Column Names)

The output above has ugly MultiIndex columns. Use **named aggregation** for clean names:

```python
# Clean, readable column names
clean_summary = df.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    avg_revenue=('revenue', 'mean'),
    total_units=('units_sold', 'sum'),
    avg_rating=('customer_rating', 'mean'),
    worst_rating=('customer_rating', 'min')
)

print(clean_summary)
```

**Output:**

```
             total_revenue  avg_revenue  total_units  avg_rating  worst_rating
category
Accessories          13000  4333.333333          150    3.866667           3.5
Electronics          33000  11000.000000          33    4.500000           4.2
```

> **Pro Tip:** Always use named aggregations for production code. Your future self (and your teammates) will thank you.

### Using Custom Functions in `.agg()`

```python
# Define custom aggregation functions
def revenue_range(x):
    return x.max() - x.min()

def pct_of_total(x):
    return (x.sum() / df['revenue'].sum()) * 100

custom_agg = df.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    revenue_range=('revenue', revenue_range),
    pct_of_company_revenue=('revenue', pct_of_total)
)

print(custom_agg)
```

**Output:**

```
             total_revenue  revenue_range  pct_of_company_revenue
category
Accessories          13000           2250               28.26087
Electronics          33000           9000               71.73913
```

---

## 7. Grouping by Multiple Columns

You can group by **more than one column** to get more granular insights.

```python
# Revenue by category AND region
category_region = df.groupby(['category', 'region']).agg(
    total_revenue=('revenue', 'sum'),
    total_units=('units_sold', 'sum'),
    transactions=('revenue', 'count')
)

print(category_region)
```

**Output:**

```
                        total_revenue  total_units  transactions
category    region
Accessories North              6250           75             2
            South              6750           75             2
Electronics North             27000           18             2
            South              6000           15             1
```

> **Notice:** The result has a **MultiIndex** (hierarchical index). You can access groups like `category_region.loc['Electronics']` or `category_region.loc[('Electronics', 'North')]`.

### Resetting the Index

```python
# Convert MultiIndex back to regular columns
category_region_flat = category_region.reset_index()
print(category_region_flat)
```

**Output:**

```
      category region  total_revenue  total_units  transactions
0  Accessories  North           6250           75             2
1  Accessories  South           6750           75             2
2  Electronics  North          27000           18             2
3  Electronics  South           6000           15             1
```

---

## 8. `.transform()` — Keep the Original Shape

`.transform()` applies a function to each group but **returns a Series with the same length as the original DataFrame**. This is perfect for adding calculated columns.

### Use Case: Percentage of Group Total

```python
# What percentage of each category's revenue does each transaction represent?
df['pct_of_category'] = df.groupby('category')['revenue'].transform(
    lambda x: (x / x.sum()) * 100
)

print(df[['product', 'category', 'revenue', 'pct_of_category']])
```

**Output:**

```
    product     category  revenue  pct_of_category
0    Laptop  Electronics    15000        45.454545
1     Mouse  Accessories     2500        19.230769
2  Keyboard  Accessories     4500        34.615385
3   Monitor  Electronics     6000        18.181818
4    Laptop  Electronics    12000        36.363636
5     Mouse  Accessories     2250        17.307692
6  Keyboard  Accessories     3750        28.846154
```

### Use Case: Z-Score Within Each Group

```python
# Standardize revenue within each category (z-score)
df['revenue_zscore'] = df.groupby('category')['revenue'].transform(
    lambda x: (x - x.mean()) / x.std()
)

print(df[['product', 'category', 'revenue', 'revenue_zscore']])
```

### Use Case: Fill Missing Values with Group Mean

```python
# Create data with missing values
df_missing = df.copy()
df_missing.loc[1, 'customer_rating'] = np.nan
df_missing.loc[4, 'customer_rating'] = np.nan

# Fill missing ratings with the average rating of that category
df_missing['customer_rating_filled'] = df_missing.groupby('category')['customer_rating'].transform(
    lambda x: x.fillna(x.mean())
)

print(df_missing[['product', 'category', 'customer_rating', 'customer_rating_filled']])
```

**Output:**

```
    product     category  customer_rating  customer_rating_filled
0    Laptop  Electronics              4.5                   4.5
1     Mouse  Accessories              NaN                   3.8
2  Keyboard  Accessories              3.5                   3.5
3   Monitor  Electronics              4.8                   4.8
4    Laptop  Electronics              NaN                   4.5
5     Mouse  Accessories              4.1                   4.1
6  Keyboard  Accessories              3.8                   3.8
```

> **Key Difference:**
>
> - `.agg()` → Returns **one row per group** (reduces data).
> - `.transform()` → Returns **same number of rows** as input (broadcasts result).

---

## 9. `.filter()` — Remove Entire Groups

`.filter()` keeps or discards **entire groups** based on a condition about the group.

```python
# Only keep categories with total revenue > $20,000
high_value_categories = df.groupby('category').filter(
    lambda x: x['revenue'].sum() > 20000
)

print(high_value_categories)
```

**Output:**

```
   product     category region  units_sold  revenue  customer_rating
0   Laptop  Electronics  North          10    15000              4.5
3  Monitor  Electronics  South          15     6000              4.8
4   Laptop  Electronics  North           8    12000              4.2
```

> **What happened?** "Accessories" had total revenue of $13,000, so the entire group was removed. Only "Electronics" rows remain.

### More Filter Examples

```python
# Keep only products that appear in more than 1 transaction
popular_products = df.groupby('product').filter(lambda x: len(x) > 1)
print(popular_products[['product', 'region', 'revenue']])

# Keep groups where the average rating is above 4.0
well_rated = df.groupby('category').filter(lambda x: x['customer_rating'].mean() > 4.0)
print(well_rated)
```

---

## 10. `.apply()` — Custom Logic per Group

`.apply()` is the most flexible method. It passes **each group as a DataFrame** to your function.

### Example: Top 2 Revenue Transactions per Category

```python
def top_n(group, n=2):
    return group.nlargest(n, 'revenue')

top_transactions = df.groupby('category').apply(top_n, n=2, include_groups=False)
print(top_transactions)
```

**Output:**

```
                    product region  units_sold  revenue  customer_rating
category
Accessories 2      Keyboard  South          30     4500              3.5
            6      Keyboard  North          25     3750              3.8
Electronics 0        Laptop  North          10    15000              4.5
            4        Laptop  North           8    12000              4.2
```

### Example: Custom Group-Wide Calculation

```python
def calculate_profit_margin(group):
    # Assume cost is 60% of revenue for Electronics, 70% for Accessories
    if group.name == 'Electronics':
        cost_ratio = 0.60
    else:
        cost_ratio = 0.70

    group['cost'] = group['revenue'] * cost_ratio
    group['profit'] = group['revenue'] - group['cost']
    group['profit_margin'] = (group['profit'] / group['revenue']) * 100
    return group

df_with_profit = df.groupby('category').apply(calculate_profit_margin, include_groups=False)
print(df_with_profit[['product', 'category', 'revenue', 'profit', 'profit_margin']])
```

> **Warning:** `.apply()` is powerful but **slow** on large datasets. Prefer built-in functions (`.agg()`, `.transform()`) when possible.

---

## 11. Sorting & Ranking Within Groups

### `.rank()` — Rank Within Groups

```python
# Rank products by revenue within each category
df['revenue_rank_in_category'] = df.groupby('category')['revenue'].rank(ascending=False)

print(df[['product', 'category', 'revenue', 'revenue_rank_in_category']])
```

**Output:**

```
    product     category  revenue  revenue_rank_in_category
0    Laptop  Electronics    15000                       1.0
1     Mouse  Accessories     2500                       3.0
2  Keyboard  Accessories     4500                       1.0
3   Monitor  Electronics     6000                       3.0
4    Laptop  Electronics    12000                       2.0
5     Mouse  Accessories     2250                       4.0
6  Keyboard  Accessories     3750                       2.0
```

### Sorting Groups

```python
# Sort categories by total revenue (descending)
category_totals = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
print(category_totals)

# Sort within groups: top revenue per region
sorted_by_region = df.sort_values(['region', 'revenue'], ascending=[True, False])
print(sorted_by_region[['region', 'product', 'revenue']])
```

---

## 12. Cumulative & Rolling Aggregations

### Cumulative Sum (`cumsum`)

```python
# Running total of revenue per category
df['cumulative_revenue'] = df.groupby('category')['revenue'].cumsum()
print(df[['product', 'category', 'revenue', 'cumulative_revenue']])
```

**Output:**

```
    product     category  revenue  cumulative_revenue
0    Laptop  Electronics    15000               15000
1     Mouse  Accessories     2500                2500
2  Keyboard  Accessories     4500                7000
3   Monitor  Electronics     6000               21000
4    Laptop  Electronics    12000               33000
5     Mouse  Accessories     2250                9250
6  Keyboard  Accessories     3750               13000
```

### Expanding Mean

```python
# Running average rating per category
df['expanding_avg_rating'] = df.groupby('category')['customer_rating'].expanding().mean().reset_index(level=0, drop=True)
print(df[['product', 'category', 'customer_rating', 'expanding_avg_rating']])
```

### Rolling Window (Time-Series)

```python
# Create time-series data
sales_ts = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'store': ['A']*5 + ['B']*5,
    'daily_sales': [100, 120, 90, 150, 110, 200, 180, 220, 190, 210]
})

# 3-day rolling average per store
sales_ts['rolling_avg_3d'] = sales_ts.groupby('store')['daily_sales'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
)

print(sales_ts)
```

**Output:**

```
        date store  daily_sales  rolling_avg_3d
0 2024-01-01     A          100      100.000000
1 2024-01-02     A          120      110.000000
2 2024-01-03     A           90      103.333333
3 2024-01-04     A          150      120.000000
4 2024-01-05     A          110      116.666667
5 2024-01-06     B          200      200.000000
6 2024-01-07     B          180      190.000000
7 2024-01-08     B          220      200.000000
8 2024-01-09     B          190      196.666667
9 2024-01-10     B          210      206.666667
```

> **Business Use Case:** A 7-day rolling average smooths out daily spikes and shows true sales trends.

---

## 13. Pivot Tables with `pivot_table()`

Pivot tables are a powerful way to summarize data in a matrix format — rows, columns, and values.

### Basic Pivot Table

```python
# Revenue by category (rows) and region (columns)
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='category',
    columns='region',
    aggfunc='sum',
    fill_value=0
)

print(pivot)
```

**Output:**

```
region         North  South
category
Accessories     6250   6750
Electronics    27000   6000
```

### Multiple Values & Aggregations

```python
# Multiple metrics in one pivot
pivot_multi = pd.pivot_table(
    df,
    values=['revenue', 'units_sold'],
    index='category',
    columns='region',
    aggfunc={'revenue': 'sum', 'units_sold': 'mean'},
    fill_value=0,
    margins=True,        # Add row/column totals
    margins_name='Total'
)

print(pivot_multi)
```

### Multiple Index Levels

```python
# More granular pivot
pivot_granular = pd.pivot_table(
    df,
    values='revenue',
    index=['category', 'product'],
    columns='region',
    aggfunc='sum',
    fill_value=0
)

print(pivot_granular)
```

**Output:**

```
region                    North  South
category    product
Accessories Keyboard       3750   4500
            Mouse          2500   2250
Electronics Laptop        27000      0
            Monitor           0   6000
```

---

## 14. Cross-Tabulation with `crosstab()`

`pd.crosstab()` is a quick way to create frequency tables (like pivot tables but simpler).

```python
# Count of transactions by category and region
cross = pd.crosstab(
    df['category'],
    df['region'],
    margins=True,
    margins_name='Total'
)
print(cross)
```

**Output:**

```
region       North  South  Total
category
Accessories      2      2      4
Electronics      2      1      3
Total            4      3      7
```

### Crosstab with Aggregation

```python
# Average revenue per category-region combination
cross_agg = pd.crosstab(
    df['category'],
    df['region'],
    values=df['revenue'],
    aggfunc='mean',
    margins=True
).round(2)

print(cross_agg)
```

**Output:**

```
region         North   South    All
category
Accessories    3125.0  3375.0  3250.0
Electronics   13500.0  6000.0  11000.0
All            8312.5  4500.0  6571.43
```

---

## 15. Handling Missing Data in Groups

```python
# Data with missing values
df_na = pd.DataFrame({
    'team': ['A', 'A', 'A', 'B', 'B', 'B'],
    'score': [100, np.nan, 90, 80, np.nan, 70]
})

# Groupby skips NaN by default
print(df_na.groupby('team')['score'].mean())
# A: 95.0, B: 75.0

# Include NaN as a group (rarely needed)
print(df_na.groupby('team', dropna=False)['score'].mean())

# Fill NaN before grouping
df_na['score_filled'] = df_na.groupby('team')['score'].transform(lambda x: x.fillna(x.mean()))
print(df_na)
```

---

## 16. Real-World Company Use Cases

### Use Case 1: E-Commerce — Monthly Sales Dashboard

**Scenario:** An online store needs a monthly performance dashboard for executives.

```python
# sales.csv: order_id, date, category, region, revenue, units, customer_id
sales = pd.DataFrame({
    'date': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-02-10',
                            '2024-02-15', '2024-03-05', '2024-03-20']),
    'category': ['Electronics', 'Clothing', 'Electronics', 'Clothing', 'Electronics', 'Clothing'],
    'region': ['North', 'North', 'South', 'South', 'North', 'South'],
    'revenue': [5000, 2000, 7000, 3000, 6000, 2500],
    'units': [5, 20, 7, 30, 6, 25],
    'customer_id': [1, 2, 3, 4, 1, 5]
})

# Extract month
sales['month'] = sales['date'].dt.to_period('M')

# Monthly KPIs
monthly_kpis = sales.groupby('month').agg(
    total_revenue=('revenue', 'sum'),
    total_units=('units', 'sum'),
    unique_customers=('customer_id', 'nunique'),
    avg_order_value=('revenue', 'mean')
).reset_index()

print("=== MONTHLY EXECUTIVE DASHBOARD ===")
print(monthly_kpis)
```

**Output:**

```
=== MONTHLY EXECUTIVE DASHBOARD ===
    month  total_revenue  total_units  unique_customers  avg_order_value
0 2024-01           7000           25                 2      3500.000000
1 2024-02          10000           37                 2      5000.000000
2 2024-03           8500           31                 3      4250.000000
```

**Business Impact:** Executives spot that February had the highest AOV ($5,000). Marketing investigates and discovers a successful premium product campaign. They replicate it in Q2, boosting revenue by 18%.

---

### Use Case 2: SaaS — Feature Adoption Analysis

**Scenario:** A SaaS company wants to understand which features drive user retention.

```python
# user_activity.csv: user_id, feature, usage_count, plan_type, signup_date
activity = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
    'feature': ['Dashboard', 'Reports', 'API', 'Dashboard', 'Reports',
                'Dashboard', 'API', 'Integrations', 'Dashboard', 'Reports'],
    'usage_count': [50, 30, 10, 5, 2, 40, 20, 15, 3, 1],
    'plan_type': ['Pro', 'Pro', 'Pro', 'Basic', 'Basic', 'Pro', 'Pro', 'Pro', 'Basic', 'Basic']
})

# Feature popularity by plan type
feature_by_plan = activity.groupby(['plan_type', 'feature']).agg(
    total_usage=('usage_count', 'sum'),
    unique_users=('user_id', 'nunique'),
    avg_usage_per_user=('usage_count', 'mean')
).reset_index()

print("=== FEATURE ADOPTION BY PLAN ===")
print(feature_by_plan)

# Identify "power features" — high usage per user on Pro plans
power_features = feature_by_plan[
    (feature_by_plan['plan_type'] == 'Pro') &
    (feature_by_plan['avg_usage_per_user'] > 20)
]
print("\n=== POWER FEATURES (Pro Users) ===")
print(power_features)
```

**Output:**

```
=== FEATURE ADOPTION BY PLAN ===
   plan_type      feature  total_usage  unique_users  avg_usage_per_user
0      Basic    Dashboard            8             2            4.000000
1      Basic      Reports            3             2            1.500000
2        Pro          API           30             2           15.000000
3        Pro    Dashboard           90             2           45.000000
4        Pro  Integrations           15             1           15.000000
5        Pro      Reports           30             1           30.000000

=== POWER FEATURES (Pro Users) ===
  plan_type   feature  total_usage  unique_users  avg_usage_per_user
2       Pro Dashboard           90             2                45.0
4       Pro   Reports           30             1                30.0
```

**Business Impact:** Product team sees that "Dashboard" and "Reports" are power features for Pro users. They invest in enhancing these features and create a "Basic" teaser to drive upgrades. Free-to-paid conversion increases by 12%.

---

### Use Case 3: Retail — Store Performance & Commission Calculation

**Scenario:** A retail chain calculates quarterly commissions for store managers based on performance tiers.

```python
# store_sales.csv: store_id, quarter, revenue, target, region
store_sales = pd.DataFrame({
    'store_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006'],
    'quarter': ['Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2'],
    'revenue': [450000, 320000, 580000, 510000, 290000, 620000],
    'target': [400000, 350000, 550000, 500000, 300000, 600000],
    'region': ['East', 'West', 'East', 'West', 'East', 'West']
})

# Calculate achievement % per store
store_sales['achievement_pct'] = (store_sales['revenue'] / store_sales['target']) * 100

# Performance tier per store
store_sales['tier'] = pd.cut(
    store_sales['achievement_pct'],
    bins=[0, 80, 100, 120, float('inf')],
    labels=['Below Target', 'On Target', 'Above Target', 'Exceptional']
)

# Quarterly summary by region
quarterly_summary = store_sales.groupby(['quarter', 'region']).agg(
    total_revenue=('revenue', 'sum'),
    avg_achievement=('achievement_pct', 'mean'),
    stores_above_target=('tier', lambda x: (x.isin(['Above Target', 'Exceptional'])).sum()),
    best_store=('achievement_pct', 'max')
).round(2)

print("=== QUARTERLY REGIONAL PERFORMANCE ===")
print(quarterly_summary)

# Commission calculation: 2% of revenue if Above Target, 3% if Exceptional
commissions = store_sales.groupby('store_id').apply(
    lambda x: pd.Series({
        'revenue': x['revenue'].iloc[0],
        'tier': x['tier'].iloc[0],
        'commission_rate': 0.03 if x['tier'].iloc[0] == 'Exceptional' else
                          (0.02 if x['tier'].iloc[0] == 'Above Target' else 0),
        'commission': x['revenue'].iloc[0] * (0.03 if x['tier'].iloc[0] == 'Exceptional' else
                                             (0.02 if x['tier'].iloc[0] == 'Above Target' else 0))
    }),
    include_groups=False
)

print("\n=== STORE COMMISSIONS ===")
print(commissions)
```

**Output:**

```
=== QUARTERLY REGIONAL PERFORMANCE ===
                total_revenue  avg_achievement  stores_above_target  best_store
quarter region
Q1      East           1030000           109.09                    2      105.45
        West            320000            91.43                    0       91.43
Q2      East            800000            96.67                    0       96.67
        West           1130000           110.83                    2      103.33

=== STORE COMMISSIONS ===
        revenue          tier  commission_rate  commission
store_id
S001     450000    Above Target             0.02      9000.0
S002     320000    Below Target             0.00         0.0
S003     580000  Exceptional               0.03     17400.0
S004     510000    Above Target             0.02     10200.0
S005     290000    Below Target             0.00         0.0
S006     620000  Exceptional               0.03     18600.0
```

**Business Impact:** Regional managers identify that West region underperformed in Q1 but recovered in Q2. They analyze S002 and S005 to understand what changed. Commission transparency boosts manager morale and store performance.

---

### Use Case 4: Logistics — Delivery Performance & SLA Monitoring

**Scenario:** A logistics company monitors delivery performance against Service Level Agreements (SLAs).

```python
# deliveries.csv: delivery_id, driver_id, zone, promised_date, delivered_date, distance_km
deliveries = pd.DataFrame({
    'delivery_id': range(1, 11),
    'driver_id': ['D1', 'D1', 'D2', 'D2', 'D3', 'D3', 'D1', 'D2', 'D3', 'D1'],
    'zone': ['Urban', 'Suburban', 'Urban', 'Rural', 'Urban', 'Suburban',
             'Rural', 'Urban', 'Suburban', 'Urban'],
    'promised_hours': [24, 48, 24, 72, 24, 48, 72, 24, 48, 24],
    'actual_hours': [22, 52, 26, 68, 20, 45, 80, 30, 50, 18],
    'distance_km': [5, 25, 8, 60, 6, 30, 55, 10, 28, 4]
})

# SLA compliance
deliveries['sla_met'] = deliveries['actual_hours'] <= deliveries['promised_hours']

# Driver performance
driver_performance = deliveries.groupby('driver_id').agg(
    total_deliveries=('delivery_id', 'count'),
    sla_compliance_rate=('sla_met', 'mean'),
    avg_actual_hours=('actual_hours', 'mean'),
    avg_distance=('distance_km', 'mean'),
    worst_delay=('actual_hours', lambda x: (x - deliveries.loc[x.index, 'promised_hours']).max())
).round(2)

driver_performance['sla_compliance_rate'] = (driver_performance['sla_compliance_rate'] * 100).round(1)

print("=== DRIVER PERFORMANCE ===")
print(driver_performance)

# Zone-level analysis
zone_analysis = deliveries.groupby('zone').agg(
    deliveries=('delivery_id', 'count'),
    sla_met=('sla_met', 'sum'),
    sla_rate=('sla_met', lambda x: (x.sum() / len(x) * 100)),
    avg_distance=('distance_km', 'mean')
).round(2)

print("\n=== ZONE ANALYSIS ===")
print(zone_analysis)

# Identify problematic routes
problematic = deliveries.groupby(['driver_id', 'zone']).filter(
    lambda x: (x['sla_met'] == False).sum() >= 2
)
print("\n=== PROBLEMATIC ROUTES (2+ Late Deliveries) ===")
print(problematic[['driver_id', 'zone', 'promised_hours', 'actual_hours']])
```

**Output:**

```
=== DRIVER PERFORMANCE ===
           total_deliveries  sla_compliance_rate  avg_actual_hours  avg_distance  worst_delay
driver_id
D1                        4                 75.0             43.00         21.25           8.0
D2                        3                 33.3             41.33         26.00          -4.0
D3                        3                 66.7             36.67         31.33           8.0

=== ZONE ANALYSIS ===
           deliveries  sla_met  sla_rate  avg_distance
zone
Rural               2        0      0.00         57.50
Suburban            3        1      33.33         34.33
Urban               5        4      80.00          6.60

=== PROBLEMATIC ROUTES (2+ Late Deliveries) ===
   delivery_id driver_id     zone  promised_hours  actual_hours
2            3        D2    Urban              24            26
6            7        D1    Rural              72            80
7            8        D2    Urban              24            30
```

**Business Impact:** Operations team discovers Rural zones have 0% SLA compliance due to long distances. They renegotiate SLAs for Rural areas and add a micro-fulfillment center, improving Rural SLA to 75% next quarter.

---

### Use Case 5: Finance — Portfolio Risk Analysis

**Scenario:** An investment firm analyzes portfolio risk by sector and asset class.

```python
# portfolio.csv: asset_id, sector, asset_class, value, return_pct, volatility
portfolio = pd.DataFrame({
    'asset_id': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
    'sector': ['Tech', 'Tech', 'Health', 'Health', 'Finance', 'Finance', 'Energy', 'Energy'],
    'asset_class': ['Stock', 'Bond', 'Stock', 'Bond', 'Stock', 'Bond', 'Stock', 'Bond'],
    'value': [50000, 30000, 40000, 35000, 45000, 25000, 20000, 15000],
    'return_pct': [12.5, 4.2, 8.3, 3.5, 6.7, 3.8, -2.1, 2.9],
    'volatility': [18.5, 2.1, 12.3, 1.8, 14.2, 2.5, 22.0, 3.0]
})

# Portfolio allocation by sector
sector_allocation = portfolio.groupby('sector').agg(
    total_value=('value', 'sum'),
    weighted_return=('return_pct', lambda x: (x * portfolio.loc[x.index, 'value']).sum() / portfolio.loc[x.index, 'value'].sum()),
    avg_volatility=('volatility', 'mean'),
    num_assets=('asset_id', 'count')
).round(2)

# Calculate portfolio %
portfolio_total = portfolio['value'].sum()
sector_allocation['portfolio_pct'] = (sector_allocation['total_value'] / portfolio_total * 100).round(1)

print("=== SECTOR ALLOCATION & RISK ===")
print(sector_allocation)

# Risk-Return matrix by sector and asset class
risk_return_matrix = pd.pivot_table(
    portfolio,
    values=['return_pct', 'volatility'],
    index='sector',
    columns='asset_class',
    aggfunc='mean'
).round(2)

print("\n=== RISK-RETURN MATRIX ===")
print(risk_return_matrix)

# Identify high-risk, low-return assets
portfolio['risk_adjusted_return'] = portfolio['return_pct'] / portfolio['volatility']
underperformers = portfolio.groupby('sector').apply(
    lambda x: x.nsmallest(1, 'risk_adjusted_return'),
    include_groups=False
)[['asset_id', 'return_pct', 'volatility', 'risk_adjusted_return']]

print("\n=== WORST RISK-ADJUSTED RETURN PER SECTOR ===")
print(underperformers)
```

**Output:**

```
=== SECTOR ALLOCATION & RISK ===
         total_value  weighted_return  avg_volatility  num_assets  portfolio_pct
sector
Energy         35000            -0.09           12.50           2            8.8
Finance        70000             5.64            8.35           2           17.5
Health         75000             6.09            7.05           2           18.8
Tech           80000             9.39           10.30           2           20.0

=== RISK-RETURN MATRIX ===
         return_pct         volatility
asset_class     Bond  Stock         Bond Stock
sector
Energy           2.9   -2.1          3.0  22.0
Finance          3.8    6.7          2.5  14.2
Health           3.5    8.3          1.8  12.3
Tech             4.2   12.5          2.1  18.5

=== WORST RISK-ADJUSTED RETURN PER SECTOR ===
         asset_id  return_pct  volatility  risk_adjusted_return
sector
Energy         A8         2.9         3.0              0.966667
Finance        A6         3.8         2.5              1.520000
Health         A4         3.5         1.8              1.944444
Tech           A2         4.2         2.1              2.000000
```

**Business Impact:** Portfolio managers discover Energy stocks have negative risk-adjusted returns. They rebalance by reducing Energy exposure and increasing Health allocation. The adjusted portfolio achieves 1.2% higher Sharpe ratio.

---

### Use Case 6: HR — Employee Attrition Analysis

**Scenario:** An HR analytics team identifies departments with high turnover risk.

```python
# employees.csv: emp_id, department, tenure_years, salary, performance_score, left_company
employees = pd.DataFrame({
    'emp_id': range(1, 13),
    'department': ['Sales', 'Sales', 'Sales', 'Engineering', 'Engineering',
                   'Engineering', 'HR', 'HR', 'Marketing', 'Marketing', 'Sales', 'Engineering'],
    'tenure_years': [2, 5, 1, 3, 7, 2, 4, 1, 3, 6, 4, 1],
    'salary': [50000, 75000, 45000, 80000, 110000, 60000, 55000, 42000, 65000, 90000, 70000, 58000],
    'performance_score': [3, 4, 2, 4, 5, 3, 4, 2, 3, 5, 4, 3],
    'left_company': [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
})

# Department-level attrition analysis
attrition_analysis = employees.groupby('department').agg(
    headcount=('emp_id', 'count'),
    attrition_count=('left_company', 'sum'),
    attrition_rate=('left_company', lambda x: (x.sum() / len(x) * 100)),
    avg_tenure=('tenure_years', 'mean'),
    avg_salary=('salary', 'mean'),
    avg_performance=('performance_score', 'mean')
).round(2)

attrition_analysis['retention_rate'] = (100 - attrition_analysis['attrition_rate']).round(1)

print("=== DEPARTMENT ATTRITION ANALYSIS ===")
print(attrition_analysis)

# Identify at-risk profile: low tenure + low performance + below-dept-avg salary
employees['dept_avg_salary'] = employees.groupby('department')['salary'].transform('mean')
employees['at_risk'] = (
    (employees['tenure_years'] < 3) &
    (employees['performance_score'] < 3) &
    (employees['salary'] < employees['dept_avg_salary'])
)

risk_summary = employees.groupby('department')['at_risk'].sum().reset_index()
risk_summary.columns = ['department', 'at_risk_employees']

print("\n=== AT-RISK EMPLOYEES BY DEPARTMENT ===")
print(risk_summary)
```

**Output:**

```
=== DEPARTMENT ATTRITION ANALYSIS ===
               headcount  attrition_count  attrition_rate  avg_tenure  avg_salary  avg_performance  retention_rate
department
Engineering            4                2            50.00        3.25       77000.0             3.75            50.0
HR                     2                1            50.00        2.50       48500.0             3.00            50.0
Marketing              2                0             0.00        4.50       77500.0             4.00           100.0
Sales                  4                2            50.00        3.00       60000.0             3.25            50.0

=== AT-RISK EMPLOYEES BY DEPARTMENT ===
    department  at_risk_employees
0  Engineering                  0
1           HR                  1
2    Marketing                  0
3        Sales                  1
```

**Business Impact:** HR discovers 50% attrition in Engineering, Sales, and HR. They launch targeted retention programs: Engineering gets mentorship for junior staff, Sales gets revised commission structures. Attrition drops to 15% in the next year.

---

## 17. Common Mistakes & How to Avoid Them

### Mistake 1: Forgetting to Reset Index After GroupBy

```python
# BAD: MultiIndex makes further operations confusing
grouped = df.groupby('category')['revenue'].sum()
# grouped is a Series with 'category' as index

# GOOD: Reset index to get a clean DataFrame
grouped_df = df.groupby('category', as_index=False)['revenue'].sum()
# Now it's a DataFrame with 'category' as a regular column
```

### Mistake 2: Using `.apply()` When Built-in Methods Exist

```python
# BAD: Slow and verbose
df.groupby('category')['revenue'].apply(lambda x: x.sum())

# GOOD: Fast and readable
df.groupby('category')['revenue'].sum()
```

> `.apply()` is 10-100x slower than vectorized built-ins. Use it only for custom logic.

### Mistake 3: Not Handling Empty Groups

```python
# If a group has no rows, some operations fail or return unexpected results
# Always check group sizes:
group_sizes = df.groupby('category').size()
print(group_sizes[group_sizes == 0])  # Check for empty groups
```

### Mistake 4: Confusing `.count()` with `.size()`

```python
# .count() skips NaN values
# .size() counts all rows including NaN

df_with_na = df.copy()
df_with_na.loc[0, 'customer_rating'] = np.nan

print(df_with_na.groupby('category')['customer_rating'].count())  # Excludes NaN
print(df_with_na.groupby('category')['customer_rating'].size())   # Includes NaN
```

### Mistake 5: Modifying Data Inside GroupBy Without `.copy()`

```python
# BAD: Modifying the original DataFrame unexpectedly
def bad_func(group):
    group['new_col'] = group['revenue'] * 2  # Modifies original!
    return group

# GOOD: Use .copy()
def good_func(group):
    group = group.copy()
    group['new_col'] = group['revenue'] * 2
    return group
```

### Mistake 6: Not Using Named Aggregations

```python
# BAD: Ugly MultiIndex columns
bad = df.groupby('category').agg({'revenue': ['sum', 'mean']})
# Columns: ('revenue', 'sum'), ('revenue', 'mean')

# GOOD: Clean column names
good = df.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    avg_revenue=('revenue', 'mean')
)
```

---

## 18. Quick Reference Cheat Sheet

```python
import pandas as pd
import numpy as np

# ============================================
# CHEAT SHEET: Pandas Aggregation & GroupBy
# ============================================

# --- BASIC AGGREGATIONS (no groupby) ---
df['col'].sum()           # Total
df['col'].mean()          # Average
df['col'].median()        # Median
df['col'].count()         # Non-null count
df['col'].min()           # Minimum
df['col'].max()           # Maximum
df['col'].std()           # Standard deviation
df['col'].var()           # Variance
df['col'].nunique()       # Unique count
df[['col1', 'col2']].describe()  # Full summary stats

# --- GROUPBY BASICS ---
df.groupby('category')['revenue'].sum()
df.groupby('category')['revenue'].mean()
df.groupby('category')[['rev', 'units']].sum()

# --- MULTI-COLUMN GROUPBY ---
df.groupby(['cat', 'region'])['revenue'].sum()

# --- NAMED AGGREGATIONS (BEST PRACTICE) ---
df.groupby('category').agg(
    total=('revenue', 'sum'),
    average=('revenue', 'mean'),
    count=('revenue', 'count'),
    best=('revenue', 'max')
)

# --- MULTIPLE FUNCS PER COLUMN ---
df.groupby('category').agg({
    'revenue': ['sum', 'mean'],
    'units': ['sum', 'count']
})

# --- TRANSFORM (keep original shape) ---
df['pct_of_group'] = df.groupby('cat')['rev'].transform(lambda x: x / x.sum())
df['group_mean'] = df.groupby('cat')['rev'].transform('mean')
df['filled'] = df.groupby('cat')['val'].transform(lambda x: x.fillna(x.mean()))

# --- FILTER (remove groups) ---
df.groupby('cat').filter(lambda x: x['rev'].sum() > 1000)
df.groupby('cat').filter(lambda x: len(x) > 5)

# --- APPLY (custom logic) ---
df.groupby('cat').apply(lambda x: x.nlargest(2, 'revenue'), include_groups=False)

# --- RANK WITHIN GROUPS ---
df['rank'] = df.groupby('cat')['rev'].rank(ascending=False)

# --- CUMULATIVE WITHIN GROUPS ---
df.groupby('cat')['rev'].cumsum()       # Running total
df.groupby('cat')['rev'].cummean()      # Running mean
df.groupby('cat')['rev'].cumcount()     # Row number within group

# --- ROLLING WITHIN GROUPS ---
df.groupby('store')['sales'].transform(lambda x: x.rolling(7, min_periods=1).mean())

# --- PIVOT TABLE ---
pd.pivot_table(df, values='rev', index='cat', columns='region', aggfunc='sum', fill_value=0, margins=True)

# --- CROSSTAB ---
pd.crosstab(df['cat'], df['region'], values=df['rev'], aggfunc='mean', margins=True)

# --- RESET INDEX ---
df.groupby('cat', as_index=False)['rev'].sum()   # Prevent MultiIndex
df.groupby('cat')['rev'].sum().reset_index()     # Flatten after

# --- SORT GROUPS ---
df.groupby('cat')['rev'].sum().sort_values(ascending=False)

# --- ITERATE GROUPS (debugging) ---
for name, group in df.groupby('cat'):
    print(name, len(group))
```

---

## Summary: When to Use What?

| Task                                  | Method          | Returns                               |
| ------------------------------------- | --------------- | ------------------------------------- |
| Summarize groups into fewer rows      | `.agg()`        | One row per group                     |
| Add group stats to every original row | `.transform()`  | Same rows as input                    |
| Keep/remove entire groups             | `.filter()`     | Subset of original rows               |
| Custom logic per group                | `.apply()`      | Flexible (usually same or fewer rows) |
| Matrix view of aggregated data        | `pivot_table()` | Pivot table DataFrame                 |
| Frequency table                       | `crosstab()`    | Cross-tabulation DataFrame            |

---

> **Remember:** Aggregation is about asking the right questions. Before you write `groupby()`, ask yourself: _"What dimension do I want to analyze by, and what metric do I want to measure?"_

**Happy Aggregating! 🐼**
