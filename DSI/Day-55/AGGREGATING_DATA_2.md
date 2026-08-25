# Aggregating Data Using Pandas

> **Day 54 — Data Science Interview (DSI) Prep Series**  
> A beginner-friendly deep dive into `groupby`, aggregation functions, pivot tables, and real-world business applications.  
> **With SQL comparisons** — because if you know SQL, you already know 80% of pandas aggregation!

---

## Table of Contents

1. [Why Do We Aggregate Data?](#1-why-do-we-aggregate-data)
2. [Pandas vs SQL: The Mental Model](#2-pandas-vs-sql-the-mental-model)
3. [Basic Aggregation Without GroupBy](#3-basic-aggregation-without-groupby)
4. [The `groupby` Mindset](#4-the-groupby-mindset)
5. [Your First `groupby`](#5-your-first-groupby)
6. [Built-in Aggregation Functions](#6-built-in-aggregation-functions)
7. [The `.agg()` Method](#7-the-agg-method)
8. [Grouping by Multiple Columns](#8-grouping-by-multiple-columns)
9. [`.transform()`](#9-transform)
10. [`.filter()`](#10-filter)
11. [`.apply()`](#11-apply)
12. [Sorting & Ranking](#12-sorting--ranking)
13. [Cumulative & Rolling](#13-cumulative--rolling)
14. [Pivot Tables](#14-pivot-tables)
15. [Cross-Tabulation](#15-cross-tabulation)
16. [Missing Data in Groups](#16-missing-data-in-groups)
17. [Real-World Use Cases](#17-real-world-use-cases)
18. [Common Mistakes](#18-common-mistakes)
19. [Cheat Sheet](#19-cheat-sheet)

---

## 1. Why Do We Aggregate Data?

Raw data is **noisy and granular**. A retail company might have millions of individual transactions, but a manager wants to know:

- "What is the **total revenue** per region?"
- "What is the **average order value** per customer segment?"
- "Which **product category** had the highest sales last quarter?"

**Aggregation** means summarizing many rows into fewer, meaningful rows. It turns raw data into **actionable insights**.

> **Analogy:** Aggregation is like a report card. Instead of listing every homework score, it gives you an average grade per subject.

---

## 2. Pandas vs SQL: The Mental Model

If you come from a SQL background, pandas `groupby` will feel immediately familiar. The concepts are **identical** — only the syntax differs.

### The SQL `GROUP BY` Pattern

```sql
SELECT
    product_area_name,
    SUM(sales_cost) AS total_sales,
    AVG(sales_cost) AS avg_sales,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY product_area_name;
```

### The Equivalent Pandas Pattern

```python
transactions.groupby("product_area_name")["sales_cost"].agg(
    total_sales="sum",
    avg_sales="mean",
    transaction_count="count"
).reset_index()
```

### Side-by-Side Mapping

| SQL Clause                  | Pandas Equivalent                      | Purpose                               |
| --------------------------- | -------------------------------------- | ------------------------------------- |
| `SELECT col, AGG(func)`     | `.groupby("col")["col"].agg(func)`     | Choose grouping & aggregation columns |
| `GROUP BY col`              | `.groupby("col")`                      | Define how to split data              |
| `SUM()`, `AVG()`, `COUNT()` | `.sum()`, `.mean()`, `.count()`        | Built-in aggregation functions        |
| `HAVING condition`          | `.filter(lambda x: condition)`         | Filter groups after aggregation       |
| `ORDER BY col DESC`         | `.sort_values("col", ascending=False)` | Sort results                          |
| `WHERE condition`           | `df[df["col"] > value]`                | Filter rows **before** grouping       |

> **Key Insight:** In SQL, `WHERE` filters **before** `GROUP BY`. In pandas, you filter with boolean indexing **before** calling `.groupby()`. `HAVING` filters **after** `GROUP BY` — in pandas, that is `.filter()`.

---

## 3. Basic Aggregation Without GroupBy

Before grouping, let us see how to aggregate an **entire column** — the pandas equivalent of `SELECT SUM(col) FROM table` without a `GROUP BY`.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop', 'Mouse', 'Keyboard'],
    'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics',
                 'Electronics', 'Accessories', 'Accessories'],
    'region': ['North', 'North', 'South', 'South', 'North', 'South', 'North'],
    'units_sold': [10, 50, 30, 15, 8, 45, 25],
    'revenue': [15000, 2500, 4500, 6000, 12000, 2250, 3750],
    'customer_rating': [4.5, 4.0, 3.5, 4.8, 4.2, 4.1, 3.8]
})
```

### Single-Column Aggregations (No GroupBy)

```python
# SQL: SELECT SUM(revenue) FROM df;
total_revenue = df['revenue'].sum()
print(f"Total Revenue: ${total_revenue:,}")        # $46,000

# SQL: SELECT AVG(customer_rating) FROM df;
avg_rating = df['customer_rating'].mean()
print(f"Average Rating: {avg_rating:.2f}")         # 4.13

# SQL: SELECT COUNT(revenue) FROM df;
num_transactions = df['revenue'].count()
print(f"Transactions: {num_transactions}")         # 7

# SQL: SELECT MAX(revenue) FROM df;
max_revenue = df['revenue'].max()
print(f"Max Revenue: ${max_revenue:,}")            # $15,000

# SQL: SELECT STDDEV(revenue) FROM df;
revenue_std = df['revenue'].std()
print(f"Revenue Std Dev: ${revenue_std:.2f}")      # $4,966.55
```

### `.describe()` — Instant Summary Statistics

```python
# SQL equivalent would require multiple queries
print(df[['units_sold', 'revenue', 'customer_rating']].describe())
```

### `.agg()` on a Single Column

```python
# SQL: SELECT SUM(revenue), AVG(revenue), MIN(revenue), MAX(revenue), STDDEV(revenue) FROM df;
revenue_stats = df['revenue'].agg(['sum', 'mean', 'min', 'max', 'std'])
print(revenue_stats)
```

---

## 4. The `groupby` Mindset: Split -> Apply -> Combine

`groupby` follows a three-step process:

**Step 1 — SPLIT:** Divide the DataFrame into groups based on one or more columns.  
**Step 2 — APPLY:** Run a function (sum, mean, custom) on each group independently.  
**Step 3 — COMBINE:** Stitch the results back into a single DataFrame or Series.

> **SQL Parallel:** This is exactly what `GROUP BY` does in SQL — it creates virtual "piles" of rows for each unique value in the grouping column, runs aggregate functions on each pile, and returns one row per pile.

---

## 5. Your First `groupby` (With SQL Comparison)

### Syntax

```python
df.groupby('column_to_group_by')['column_to_aggregate'].aggregation_function()
```

### Example: Revenue by Category

**SQL:**

```sql
SELECT category, SUM(revenue) AS total_revenue
FROM df
GROUP BY category;
```

**Pandas:**

```python
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

> **SQL Note:** Just like SQL `GROUP BY`, pandas drops the non-grouped, non-aggregated columns automatically.

### The GroupBy Object

```python
grouped = df.groupby('category')
print(type(grouped))  # <class 'pandas.core.groupby.DataFrameGroupBy'>

# You can iterate over groups (useful for debugging)
for name, group in grouped:
    print(f"
=== Group: {name} ===")
    print(group)
```

> **Think of it this way:** `df.groupby("category")` is like running `SELECT * FROM df WHERE category = 'Accessories'` and `SELECT * FROM df WHERE category = 'Electronics'` separately, then storing each result as a mini-DataFrame.

---

## 6. Built-in Aggregation Functions

After `groupby()`, you can call these functions directly — just like SQL aggregate functions:

| Pandas Function | SQL Equivalent           | What It Does                   |
| --------------- | ------------------------ | ------------------------------ |
| `.sum()`        | `SUM()`                  | Sum of values                  |
| `.mean()`       | `AVG()`                  | Arithmetic mean                |
| `.median()`     | `MEDIAN()`               | Median (middle value)          |
| `.count()`      | `COUNT(column)`          | Count of non-null values       |
| `.size()`       | `COUNT(*)`               | Count of rows (includes nulls) |
| `.min()`        | `MIN()`                  | Minimum value                  |
| `.max()`        | `MAX()`                  | Maximum value                  |
| `.std()`        | `STDDEV()`               | Standard deviation             |
| `.var()`        | `VARIANCE()`             | Variance                       |
| `.first()`      | `FIRST_VALUE()`          | First non-null value           |
| `.last()`       | `LAST_VALUE()`           | Last non-null value            |
| `.nunique()`    | `COUNT(DISTINCT column)` | Count of unique values         |

### Code Examples with SQL Comparison

```python
# SQL: SELECT region, COUNT(*) FROM df GROUP BY region;
transactions_per_region = df.groupby('region').size()
print(transactions_per_region)
# North: 4, South: 3

# SQL: SELECT region, COUNT(customer_rating) FROM df GROUP BY region;
count_per_region = df.groupby('region')['customer_rating'].count()

# SQL: SELECT category, MAX(revenue) FROM df GROUP BY category;
max_revenue_per_category = df.groupby('category')['revenue'].max()

# SQL: SELECT region, COUNT(DISTINCT product) FROM df GROUP BY region;
unique_products = df.groupby('region')['product'].nunique()

# SQL: SELECT category, * FROM df WHERE row_number() OVER (PARTITION BY category) = 1;
first_transaction = df.groupby('category').first()
```

---

## 7. The `.agg()` Method — Multiple Aggregations at Once

The `.agg()` (or `.aggregate()`) method is incredibly powerful. It lets you compute **multiple statistics** on **multiple columns** in **one line** — the pandas equivalent of `SELECT col1, AGG1, AGG2, AGG3 FROM ... GROUP BY`.

### Same Function on Multiple Columns

**SQL:**

```sql
SELECT
    category,
    SUM(units_sold) AS total_units,
    SUM(revenue) AS total_revenue
FROM df
GROUP BY category;
```

**Pandas:**

```python
category_totals = df.groupby('category')[['units_sold', 'revenue']].agg('sum')
print(category_totals)
```

### Different Functions on Different Columns

**SQL:**

```sql
SELECT
    category,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_revenue,
    MAX(revenue) AS max_revenue,
    SUM(units_sold) AS total_units,
    AVG(customer_rating) AS avg_rating,
    MIN(customer_rating) AS min_rating
FROM df
GROUP BY category;
```

**Pandas:**

```python
custom_summary = df.groupby('category').agg({
    'revenue': ['sum', 'mean', 'max'],
    'units_sold': ['sum', 'mean'],
    'customer_rating': ['mean', 'min', 'max']
})
```

> **Problem:** The output has ugly **MultiIndex columns** (`('revenue', 'sum')`, etc.). In SQL, you would alias them cleanly. In pandas, use **named aggregations**.

### Named Aggregations (Clean Column Names)

**SQL:**

```sql
SELECT
    category,
    SUM(revenue) AS total_revenue,
    AVG(revenue) AS avg_revenue,
    SUM(units_sold) AS total_units,
    AVG(customer_rating) AS avg_rating,
    MIN(customer_rating) AS worst_rating
FROM df
GROUP BY category;
```

**Pandas:**

```python
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

> **Pro Tip:** Always use named aggregations for production code. It is the pandas equivalent of always using `AS alias` in SQL.

### Using Custom Functions in `.agg()`

**SQL:**

```sql
SELECT
    category,
    SUM(revenue) AS total_revenue,
    MAX(revenue) - MIN(revenue) AS revenue_range
FROM df
GROUP BY category;
```

**Pandas:**

```python
def revenue_range(x):
    return x.max() - x.min()

def pct_of_total(x):
    return (x.sum() / df['revenue'].sum()) * 100

custom_agg = df.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    revenue_range=('revenue', revenue_range),
    pct_of_company_revenue=('revenue', pct_of_total)
)
```

---

## 8. Grouping by Multiple Columns

You can group by **more than one column** — just like `GROUP BY col1, col2` in SQL.

**SQL:**

```sql
SELECT
    category,
    region,
    SUM(revenue) AS total_revenue,
    SUM(units_sold) AS total_units,
    COUNT(*) AS transactions
FROM df
GROUP BY category, region;
```

**Pandas:**

```python
category_region = df.groupby(['category', 'region']).agg(
    total_revenue=('revenue', 'sum'),
    total_units=('units_sold', 'sum'),
    transactions=('revenue', 'count')
)
```

> **Notice:** The result has a **MultiIndex** (hierarchical index). In SQL, the result is already a flat table.

### Resetting the Index

**Pandas:**

```python
# Convert MultiIndex back to regular columns — makes it look like a SQL result!
category_region_flat = category_region.reset_index()
```

> **Best Practice:** Use `as_index=False` in `groupby()` to prevent MultiIndex from forming:
>
> ```python
> df.groupby(['category', 'region'], as_index=False).agg(...)
> ```
>
> This is equivalent to SQL's flat result set.

---

## 9. `.transform()` — Keep the Original Shape

`.transform()` applies a function to each group but **returns a Series with the same length as the original DataFrame**.

> **SQL Parallel:** `.transform()` is like a **window function** in SQL (`OVER (PARTITION BY ...)`). It calculates a group-level statistic but keeps every original row.

### Use Case: Percentage of Group Total

**SQL:**

```sql
SELECT
    product,
    category,
    revenue,
    revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category) AS pct_of_category
FROM df;
```

**Pandas:**

```python
df['pct_of_category'] = df.groupby('category')['revenue'].transform(
    lambda x: (x / x.sum()) * 100
)
```

### Use Case: Fill Missing Values with Group Mean

**SQL:**

```sql
SELECT
    product,
    category,
    customer_rating,
    COALESCE(customer_rating, AVG(customer_rating) OVER (PARTITION BY category)) AS filled_rating
FROM df;
```

**Pandas:**

```python
df_missing = df.copy()
df_missing.loc[1, 'customer_rating'] = np.nan

df_missing['customer_rating_filled'] = df_missing.groupby('category')['customer_rating'].transform(
    lambda x: x.fillna(x.mean())
)
```

> **Key Difference:**
>
> - `.agg()` -> Returns **one row per group** (reduces data). Like `GROUP BY`.
> - `.transform()` -> Returns **same number of rows** as input. Like window functions with `OVER (PARTITION BY ...)`.

---

## 10. `.filter()` — Remove Entire Groups

`.filter()` keeps or discards **entire groups** based on a condition about the group.

> **SQL Parallel:** `.filter()` is the pandas equivalent of the `HAVING` clause in SQL.

**SQL:**

```sql
SELECT category
FROM df
GROUP BY category
HAVING SUM(revenue) > 20000;
```

**Pandas:**

```python
high_value_categories = df.groupby('category').filter(
    lambda x: x['revenue'].sum() > 20000
)
```

> **What happened?** "Accessories" had total revenue of $13,000, so the entire group was removed. Only "Electronics" rows remain. This is exactly what `HAVING SUM(revenue) > 20000` does in SQL.

---

## 11. `.apply()` — Custom Logic per Group

`.apply()` is the most flexible method. It passes **each group as a DataFrame** to your function.

> **SQL Parallel:** `.apply()` is like using a **CTE** with complex logic that you cannot express in a simple `GROUP BY`.

### Example: Top 2 Revenue Transactions per Category

**SQL:**

```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
    FROM df
)
SELECT * FROM ranked WHERE rn <= 2;
```

**Pandas:**

```python
def top_n(group, n=2):
    return group.nlargest(n, 'revenue')

top_transactions = df.groupby('category').apply(top_n, n=2, include_groups=False)
```

> **Warning:** `.apply()` is powerful but **slow** on large datasets. Prefer built-in functions when possible. In SQL terms, `.apply()` is like using a cursor instead of a set-based `GROUP BY`.

---

## 12. Sorting & Ranking Within Groups

### `.rank()` — Rank Within Groups

**SQL:**

```sql
SELECT
    product,
    category,
    revenue,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS revenue_rank
FROM df;
```

**Pandas:**

```python
df['revenue_rank_in_category'] = df.groupby('category')['revenue'].rank(ascending=False)
```

### Sorting Groups

**SQL:**

```sql
SELECT category, SUM(revenue) AS total_revenue
FROM df
GROUP BY category
ORDER BY total_revenue DESC;
```

**Pandas:**

```python
category_totals = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
```

---

## 13. Cumulative & Rolling Aggregations

### Cumulative Sum (`cumsum`)

**SQL:**

```sql
SELECT
    product,
    category,
    revenue,
    SUM(revenue) OVER (PARTITION BY category ORDER BY product) AS cumulative_revenue
FROM df;
```

**Pandas:**

```python
df['cumulative_revenue'] = df.groupby('category')['revenue'].cumsum()
```

### Rolling Window (Time-Series)

**SQL:**

```sql
SELECT
    date,
    store,
    daily_sales,
    AVG(daily_sales) OVER (PARTITION BY store ORDER BY date ROWS 2 PRECEDING) AS rolling_avg_3d
FROM sales_ts;
```

**Pandas:**

```python
sales_ts = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'store': ['A']*5 + ['B']*5,
    'daily_sales': [100, 120, 90, 150, 110, 200, 180, 220, 190, 210]
})

sales_ts['rolling_avg_3d'] = sales_ts.groupby('store')['daily_sales'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
)
```

> **Business Use Case:** A 7-day rolling average smooths out daily spikes and shows true sales trends.

---

## 14. Pivot Tables with `pivot_table()`

Pivot tables are a powerful way to summarize data in a matrix format — rows, columns, and values. Think of them as a visual `GROUP BY` with multiple dimensions.

### Basic Pivot Table

**SQL:**

```sql
SELECT
    category,
    SUM(CASE WHEN region = 'North' THEN revenue ELSE 0 END) AS North,
    SUM(CASE WHEN region = 'South' THEN revenue ELSE 0 END) AS South
FROM df
GROUP BY category;
```

**Pandas:**

```python
pivot = pd.pivot_table(
    df,
    values='revenue',
    index='category',
    columns='region',
    aggfunc='sum',
    fill_value=0
)
```

### Multiple Values & Aggregations

```python
pivot_multi = pd.pivot_table(
    df,
    values=['revenue', 'units_sold'],
    index='category',
    columns='region',
    aggfunc={'revenue': 'sum', 'units_sold': 'mean'},
    fill_value=0,
    margins=True,
    margins_name='Total'
)
```

> **Think of `pivot_table` as:** A `GROUP BY` where one column becomes the row labels, another becomes the column labels, and a third becomes the values. SQL can do this with conditional aggregation (`CASE WHEN`), but pandas makes it effortless.

---

## 15. Cross-Tabulation with `crosstab()`

`pd.crosstab()` is a quick way to create frequency tables.

**SQL:**

```sql
SELECT
    category,
    COUNT(CASE WHEN region = 'North' THEN 1 END) AS North,
    COUNT(CASE WHEN region = 'South' THEN 1 END) AS South,
    COUNT(*) AS Total
FROM df
GROUP BY category;
```

**Pandas:**

```python
cross = pd.crosstab(
    df['category'],
    df['region'],
    margins=True,
    margins_name='Total'
)
```

### Crosstab with Aggregation

**SQL:**

```sql
SELECT
    category,
    AVG(CASE WHEN region = 'North' THEN revenue END) AS North,
    AVG(CASE WHEN region = 'South' THEN revenue END) AS South,
    AVG(revenue) AS Total
FROM df
GROUP BY category;
```

**Pandas:**

```python
cross_agg = pd.crosstab(
    df['category'],
    df['region'],
    values=df['revenue'],
    aggfunc='mean',
    margins=True
).round(2)
```

---

## 16. Handling Missing Data in Groups

```python
df_na = pd.DataFrame({
    'team': ['A', 'A', 'A', 'B', 'B', 'B'],
    'score': [100, np.nan, 90, 80, np.nan, 70]
})

# Groupby skips NaN by default (like SQL COUNT(column) skips NULLs)
print(df_na.groupby('team')['score'].mean())
# A: 95.0, B: 75.0

# Fill NaN before grouping — SQL equivalent: COALESCE with subquery average
df_na['score_filled'] = df_na.groupby('team')['score'].transform(lambda x: x.fillna(x.mean()))
```

---

## 17. Real-World Company Use Cases

### Use Case 1: E-Commerce — Monthly Sales Dashboard

**Scenario:** An online store needs a monthly performance dashboard for executives.

```python
sales = pd.DataFrame({
    'date': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-02-10',
                            '2024-02-15', '2024-03-05', '2024-03-20']),
    'category': ['Electronics', 'Clothing', 'Electronics', 'Clothing', 'Electronics', 'Clothing'],
    'region': ['North', 'North', 'South', 'South', 'North', 'South'],
    'revenue': [5000, 2000, 7000, 3000, 6000, 2500],
    'units': [5, 20, 7, 30, 6, 25],
    'customer_id': [1, 2, 3, 4, 1, 5]
})

sales['month'] = sales['date'].dt.to_period('M')

monthly_kpis = sales.groupby('month').agg(
    total_revenue=('revenue', 'sum'),
    total_units=('units', 'sum'),
    unique_customers=('customer_id', 'nunique'),
    avg_order_value=('revenue', 'mean')
).reset_index()

print(monthly_kpis)
```

**Output:**

```
    month  total_revenue  total_units  unique_customers  avg_order_value
0 2024-01           7000           25                 2      3500.000000
1 2024-02          10000           37                 2      5000.000000
2 2024-03           8500           31                 3      4250.000000
```

**Business Impact:** Executives spot that February had the highest AOV ($5,000). Marketing replicates the successful premium campaign in Q2, boosting revenue by 18%.

---

### Use Case 2: SaaS — Feature Adoption Analysis

**Scenario:** A SaaS company wants to understand which features drive user retention.

```python
activity = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4],
    'feature': ['Dashboard', 'Reports', 'API', 'Dashboard', 'Reports',
                'Dashboard', 'API', 'Integrations', 'Dashboard', 'Reports'],
    'usage_count': [50, 30, 10, 5, 2, 40, 20, 15, 3, 1],
    'plan_type': ['Pro', 'Pro', 'Pro', 'Basic', 'Basic', 'Pro', 'Pro', 'Pro', 'Basic', 'Basic']
})

feature_by_plan = activity.groupby(['plan_type', 'feature']).agg(
    total_usage=('usage_count', 'sum'),
    unique_users=('user_id', 'nunique'),
    avg_usage_per_user=('usage_count', 'mean')
).reset_index()

# Identify "power features" — high usage per user on Pro plans
power_features = feature_by_plan[
    (feature_by_plan['plan_type'] == 'Pro') &
    (feature_by_plan['avg_usage_per_user'] > 20)
]
print(power_features)
```

**Business Impact:** Product team sees "Dashboard" and "Reports" are power features for Pro users. They invest in enhancing these and create a "Basic" teaser to drive upgrades. Free-to-paid conversion increases by 12%.

---

### Use Case 3: Retail — Store Performance & Commission Calculation

**Scenario:** A retail chain calculates quarterly commissions for store managers.

```python
store_sales = pd.DataFrame({
    'store_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006'],
    'quarter': ['Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2'],
    'revenue': [450000, 320000, 580000, 510000, 290000, 620000],
    'target': [400000, 350000, 550000, 500000, 300000, 600000],
    'region': ['East', 'West', 'East', 'West', 'East', 'West']
})

store_sales['achievement_pct'] = (store_sales['revenue'] / store_sales['target']) * 100

store_sales['tier'] = pd.cut(
    store_sales['achievement_pct'],
    bins=[0, 80, 100, 120, float('inf')],
    labels=['Below Target', 'On Target', 'Above Target', 'Exceptional']
)

quarterly_summary = store_sales.groupby(['quarter', 'region']).agg(
    total_revenue=('revenue', 'sum'),
    avg_achievement=('achievement_pct', 'mean'),
    stores_above_target=('tier', lambda x: (x.isin(['Above Target', 'Exceptional'])).sum()),
    best_store=('achievement_pct', 'max')
).round(2)

print(quarterly_summary)
```

**Business Impact:** Regional managers identify that West region underperformed in Q1 but recovered in Q2. Commission transparency boosts manager morale and store performance.

---

### Use Case 4: Logistics — Delivery Performance & SLA Monitoring

**Scenario:** A logistics company monitors delivery performance against SLAs.

```python
deliveries = pd.DataFrame({
    'delivery_id': range(1, 11),
    'driver_id': ['D1', 'D1', 'D2', 'D2', 'D3', 'D3', 'D1', 'D2', 'D3', 'D1'],
    'zone': ['Urban', 'Suburban', 'Urban', 'Rural', 'Urban', 'Suburban',
             'Rural', 'Urban', 'Suburban', 'Urban'],
    'promised_hours': [24, 48, 24, 72, 24, 48, 72, 24, 48, 24],
    'actual_hours': [22, 52, 26, 68, 20, 45, 80, 30, 50, 18],
    'distance_km': [5, 25, 8, 60, 6, 30, 55, 10, 28, 4]
})

deliveries['sla_met'] = deliveries['actual_hours'] <= deliveries['promised_hours']

driver_performance = deliveries.groupby('driver_id').agg(
    total_deliveries=('delivery_id', 'count'),
    sla_compliance_rate=('sla_met', 'mean'),
    avg_actual_hours=('actual_hours', 'mean'),
    avg_distance=('distance_km', 'mean')
).round(2)

driver_performance['sla_compliance_rate'] = (driver_performance['sla_compliance_rate'] * 100).round(1)

print(driver_performance)
```

**Business Impact:** Operations team discovers Rural zones have 0% SLA compliance. They renegotiate SLAs for Rural areas and add a micro-fulfillment center, improving Rural SLA to 75% next quarter.

---

### Use Case 5: Finance — Portfolio Risk Analysis

**Scenario:** An investment firm analyzes portfolio risk by sector.

```python
portfolio = pd.DataFrame({
    'asset_id': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'],
    'sector': ['Tech', 'Tech', 'Health', 'Health', 'Finance', 'Finance', 'Energy', 'Energy'],
    'asset_class': ['Stock', 'Bond', 'Stock', 'Bond', 'Stock', 'Bond', 'Stock', 'Bond'],
    'value': [50000, 30000, 40000, 35000, 45000, 25000, 20000, 15000],
    'return_pct': [12.5, 4.2, 8.3, 3.5, 6.7, 3.8, -2.1, 2.9],
    'volatility': [18.5, 2.1, 12.3, 1.8, 14.2, 2.5, 22.0, 3.0]
})

sector_allocation = portfolio.groupby('sector').agg(
    total_value=('value', 'sum'),
    weighted_return=('return_pct', lambda x: (x * portfolio.loc[x.index, 'value']).sum() / portfolio.loc[x.index, 'value'].sum()),
    avg_volatility=('volatility', 'mean'),
    num_assets=('asset_id', 'count')
).round(2)

portfolio_total = portfolio['value'].sum()
sector_allocation['portfolio_pct'] = (sector_allocation['total_value'] / portfolio_total * 100).round(1)

print(sector_allocation)
```

**Business Impact:** Portfolio managers discover Energy stocks have negative risk-adjusted returns. They rebalance by reducing Energy exposure. The adjusted portfolio achieves 1.2% higher Sharpe ratio.

---

### Use Case 6: HR — Employee Attrition Analysis

**Scenario:** An HR analytics team identifies departments with high turnover risk.

```python
employees = pd.DataFrame({
    'emp_id': range(1, 13),
    'department': ['Sales', 'Sales', 'Sales', 'Engineering', 'Engineering',
                   'Engineering', 'HR', 'HR', 'Marketing', 'Marketing', 'Sales', 'Engineering'],
    'tenure_years': [2, 5, 1, 3, 7, 2, 4, 1, 3, 6, 4, 1],
    'salary': [50000, 75000, 45000, 80000, 110000, 60000, 55000, 42000, 65000, 90000, 70000, 58000],
    'performance_score': [3, 4, 2, 4, 5, 3, 4, 2, 3, 5, 4, 3],
    'left_company': [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1]
})

attrition_analysis = employees.groupby('department').agg(
    headcount=('emp_id', 'count'),
    attrition_count=('left_company', 'sum'),
    attrition_rate=('left_company', lambda x: (x.sum() / len(x) * 100)),
    avg_tenure=('tenure_years', 'mean'),
    avg_salary=('salary', 'mean'),
    avg_performance=('performance_score', 'mean')
).round(2)

attrition_analysis['retention_rate'] = (100 - attrition_analysis['attrition_rate']).round(1)

print(attrition_analysis)
```

**Business Impact:** HR discovers 50% attrition in Engineering, Sales, and HR. They launch targeted retention programs. Attrition drops to 15% in the next year.

---

## 18. Common Mistakes & How to Avoid Them

### Mistake 1: Forgetting to Reset Index After GroupBy

```python
# BAD: MultiIndex makes further operations confusing
grouped = df.groupby('category')['revenue'].sum()

# GOOD: Reset index to get a clean DataFrame — just like SQL's flat result!
grouped_df = df.groupby('category', as_index=False)['revenue'].sum()
```

> **SQL Perspective:** In SQL, `GROUP BY` always returns a flat table. Pandas returns a Series with the group key as the index. Use `as_index=False` or `.reset_index()` to get SQL-like behavior.

### Mistake 2: Using `.apply()` When Built-in Methods Exist

```python
# BAD: Slow and verbose — like using a cursor in SQL
df.groupby('category')['revenue'].apply(lambda x: x.sum())

# GOOD: Fast and readable — like using SUM() in SQL
df.groupby('category')['revenue'].sum()
```

> `.apply()` is 10-100x slower than vectorized built-ins. Use it only for custom logic.

### Mistake 3: Confusing `.count()` with `.size()`

```python
# .count() skips NaN values — like SQL COUNT(column)
# .size() counts all rows including NaN — like SQL COUNT(*)
```

### Mistake 4: Not Using Named Aggregations

```python
# BAD: Ugly MultiIndex columns
bad = df.groupby('category').agg({'revenue': ['sum', 'mean']})

# GOOD: Clean column names
good = df.groupby('category').agg(
    total_revenue=('revenue', 'sum'),
    avg_revenue=('revenue', 'mean')
)
```

---

## 19. Quick Reference Cheat Sheet

```python
import pandas as pd
import numpy as np

# --- BASIC AGGREGATIONS (no groupby) ---
df['col'].sum()           # Total
df['col'].mean()          # Average
df['col'].count()         # Non-null count
df['col'].min()           # Minimum
df['col'].max()           # Maximum
df['col'].std()           # Standard deviation
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

## SQL -> Pandas Quick Translator

| SQL                                                                                              | Pandas                                                      |
| ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| `SELECT SUM(col) FROM table`                                                                     | `df['col'].sum()`                                           |
| `SELECT cat, SUM(rev) FROM table GROUP BY cat`                                                   | `df.groupby('cat')['rev'].sum()`                            |
| `SELECT cat, SUM(rev), AVG(rev) FROM table GROUP BY cat`                                         | `df.groupby('cat')['rev'].agg(['sum','mean'])`              |
| `SELECT cat, reg, SUM(rev) FROM table GROUP BY cat, reg`                                         | `df.groupby(['cat','reg'])['rev'].sum()`                    |
| `SELECT * FROM table WHERE col > 100`                                                            | `df[df['col'] > 100]`                                       |
| `SELECT cat, SUM(rev) FROM table GROUP BY cat HAVING SUM(rev) > 1000`                            | `df.groupby('cat').filter(lambda x: x['rev'].sum() > 1000)` |
| `SELECT col, SUM(col) OVER (PARTITION BY cat) FROM table`                                        | `df.groupby('cat')['col'].transform('sum')`                 |
| `SELECT col, RANK() OVER (PARTITION BY cat ORDER BY rev DESC) FROM table`                        | `df.groupby('cat')['rev'].rank(ascending=False)`            |
| `SELECT col, SUM(rev) OVER (PARTITION BY cat ORDER BY date ROWS UNBOUNDED PRECEDING) FROM table` | `df.groupby('cat')['rev'].cumsum()`                         |
| `SELECT col, AVG(rev) OVER (PARTITION BY cat ORDER BY date ROWS 6 PRECEDING) FROM table`         | `df.groupby('cat')['rev'].rolling(7).mean()`                |

---

> **Remember:** Aggregation is about asking the right questions. Before you write `groupby()`, ask yourself: _"What dimension do I want to analyze by, and what metric do I want to measure?"_

**Happy Aggregating!**
