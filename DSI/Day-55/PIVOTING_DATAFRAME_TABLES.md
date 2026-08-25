# Pivoting DataFrames & Pivot Tables in Pandas

> **Day 54 — Data Science Interview (DSI) Prep Series**  
> A beginner-friendly guide to reshaping data with `pivot()`, `pivot_table()`, `melt()`, `stack()`, `unstack()`, and `crosstab()`.

---

## Table of Contents

1. [What is Pivoting and Why Do We Need It?](#1-what-is-pivoting-and-why-do-we-need-it)
2. [Long Format vs Wide Format](#2-long-format-vs-wide-format)
3. [`.pivot()` — Reshape Without Aggregation](#3-pivot--reshape-without-aggregation)
4. [`.pivot_table()` — Reshape With Aggregation](#4-pivot_table--reshape-with-aggregation)
5. [`.melt()` — The Reverse of Pivot](#5-melt--the-reverse-of-pivot)
6. [`.stack()` & `.unstack()` — Multi-Level Pivoting](#6-stack--unstack--multi-level-pivoting)
7. [`.crosstab()` — Frequency Tables](#7-crosstab--frequency-tables)
8. [Advanced Pivot Table Features](#8-advanced-pivot-table-features)
9. [Handling Missing Values in Pivots](#9-handling-missing-values-in-pivots)
10. [SQL Comparison](#10-sql-comparison)
11. [Real-World Company Use Cases](#11-real-world-company-use-cases)
12. [Common Mistakes & How to Avoid Them](#12-common-mistakes--how-to-avoid-them)
13. [Quick Reference Cheat Sheet](#13-quick-reference-cheat-sheet)

---

## 1. What is Pivoting and Why Do We Need It?

**Pivoting** means rotating your data — turning rows into columns or columns into rows. It is one of the most important data reshaping skills in data analysis.

> **Analogy:** Imagine a spreadsheet where each sale is a row. Pivoting is like creating a summary table where products are rows, months are columns, and sales values fill the cells. That is exactly what Excel's "Pivot Table" does — and pandas does it programmatically.

**Why pivot?**

- **Reporting:** Executives want to see metrics by time period and category in a grid.
- **Visualization:** Charts often need wide-format data.
- **Analysis:** Comparing categories side-by-side is easier in a matrix.
- **Data Cleaning:** Converting between long and wide formats for different tools.

---

## 2. Long Format vs Wide Format

Understanding these two shapes is essential before pivoting.

### Long Format (Tidy Data)

Each observation is a row. One column holds the variable name, another holds the value.

```
   date       product   sales
0  Jan-2024   Laptop    5000
1  Jan-2024   Mouse     1200
2  Feb-2024   Laptop    6000
3  Feb-2024   Mouse     1500
```

**Pros:** Easy to filter, group, and store.  
**Cons:** Hard to compare side-by-side.

### Wide Format (Matrix)

Each product gets its own column. Values are spread across columns.

```
   date       Laptop  Mouse
0  Jan-2024   5000    1200
1  Feb-2024   6000    1500
```

**Pros:** Easy to compare, perfect for dashboards.  
**Cons:** Harder to aggregate, not database-friendly.

> **The Golden Rule:** Store data in **long format**, but **pivot to wide format** for reporting and visualization.

---

## 3. `.pivot()` — Reshape Without Aggregation

`.pivot()` is the simplest form of pivoting. It reshapes data **without** any calculation — just rearranges values.

### When to Use `.pivot()`

Use `.pivot()` when your data has **no duplicate combinations** of index + columns. If there are duplicates, you will get an error.

### Syntax

```python
df.pivot(
    index='row_label_column',      # What becomes the rows
    columns='column_label_column', # What becomes the columns
    values='value_column'          # What fills the cells
)
```

### Basic Example

```python
import pandas as pd

# Long-format sales data
sales_long = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Feb', 'Feb', 'Mar', 'Mar'],
    'product': ['Laptop', 'Mouse', 'Laptop', 'Mouse', 'Laptop', 'Mouse'],
    'revenue': [5000, 1200, 6000, 1500, 5500, 1300]
})

print("=== LONG FORMAT ===")
print(sales_long)
```

**Output:**

```
  month product  revenue
0   Jan  Laptop     5000
1   Jan   Mouse     1200
2   Feb  Laptop     6000
3   Feb   Mouse     1500
4   Mar  Laptop     5500
5   Mar   Mouse     1300
```

```python
# Pivot to wide format
sales_wide = sales_long.pivot(
    index='month',
    columns='product',
    values='revenue'
)

print("
=== WIDE FORMAT (pivot) ===")
print(sales_wide)
```

**Output:**

```
product  Laptop  Mouse
month
Jan        5000   1200
Feb        6000   1500
Mar        5500   1300
```

**What happened?**

- `month` became the **index** (rows).
- `product` became the **columns**.
- `revenue` filled the **values**.
- Each cell now shows revenue for that month-product combination.

### Multiple Values

```python
# Data with multiple metrics
sales_multi = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Feb', 'Feb'],
    'product': ['Laptop', 'Mouse', 'Laptop', 'Mouse'],
    'revenue': [5000, 1200, 6000, 1500],
    'units': [10, 50, 12, 60]
})

# Pivot with multiple value columns
pivot_multi = sales_multi.pivot(
    index='month',
    columns='product',
    values=['revenue', 'units']
)

print(pivot_multi)
```

**Output:**

```
       revenue       units
product Laptop Mouse Laptop Mouse
month
Jan        5000  1200     10    50
Feb        6000  1500     12    60
```

> **Note:** This creates a **MultiIndex** on the columns. You can flatten it with `pivot_multi.columns = ['_'.join(col).strip() for col in pivot_multi.columns.values]`.

### The Duplicate Error

```python
# This will FAIL because (Jan, Laptop) appears twice
duplicate_data = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Jan'],
    'product': ['Laptop', 'Laptop', 'Mouse'],
    'revenue': [5000, 5200, 1200]
})

# This raises ValueError: Index contains duplicate entries, cannot reshape
try:
    duplicate_data.pivot(index='month', columns='product', values='revenue')
except ValueError as e:
    print(f"Error: {e}")
```

> **When you see this error, use `.pivot_table()` instead.** It handles duplicates by aggregating them.

---

## 4. `.pivot_table()` — Reshape With Aggregation

`.pivot_table()` is the **powerhouse** of pivoting. It can handle duplicates, apply aggregation functions, and create margins (totals).

### When to Use `.pivot_table()`

- When you have **duplicate combinations** of index + columns.
- When you need to **aggregate** values (sum, mean, count, etc.).
- When you want **totals/margins**.
- When you need **multiple aggregations**.

### Syntax

```python
pd.pivot_table(
    data=df,
    values='column_to_aggregate',     # The values to fill cells
    index='row_column',               # Column(s) for rows
    columns='column_column',          # Column(s) for columns
    aggfunc='sum',                    # How to aggregate: 'sum', 'mean', 'count', etc.
    fill_value=0,                     # What to put where there is no data
    margins=True,                     # Add row and column totals
    margins_name='Total',             # Name for the total row/column
    dropna=True,                      # Drop columns with all NaN
    observed=False                    # For categorical data
)
```

### Basic Example with Aggregation

```python
# Sales data with duplicates (multiple transactions per month-product)
sales_dup = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb'],
    'product': ['Laptop', 'Laptop', 'Mouse', 'Laptop', 'Mouse', 'Mouse'],
    'region': ['North', 'South', 'North', 'North', 'South', 'North'],
    'revenue': [3000, 2000, 1200, 3500, 800, 700]
})

print("=== DATA WITH DUPLICATES ===")
print(sales_dup)
```

**Output:**

```
  month product region  revenue
0   Jan  Laptop  North     3000
1   Jan  Laptop  South     2000
2   Jan   Mouse  North     1200
3   Feb  Laptop  North     3500
4   Feb   Mouse  South      800
5   Feb   Mouse  North      700
```

```python
# Pivot table: sum revenue by month (rows) and product (columns)
pivot_sum = pd.pivot_table(
    sales_dup,
    values='revenue',
    index='month',
    columns='product',
    aggfunc='sum',
    fill_value=0
)

print("
=== PIVOT TABLE (sum) ===")
print(pivot_sum)
```

**Output:**

```
product  Laptop  Mouse
month
Feb        3500   1500
Jan        5000   1200
```

**What happened?**

- Two "Jan + Laptop" rows (North: 3000, South: 2000) were **summed** to 5000.
- Two "Feb + Mouse" rows (South: 800, North: 700) were **summed** to 1500.
- `.pivot()` would have thrown an error. `.pivot_table()` handled it gracefully.

### Multiple Aggregation Functions

```python
# Multiple stats in one pivot
pivot_stats = pd.pivot_table(
    sales_dup,
    values='revenue',
    index='month',
    columns='product',
    aggfunc=['sum', 'mean', 'count'],
    fill_value=0
)

print(pivot_stats)
```

**Output:**

```
           sum         mean         count
product Laptop Mouse Laptop Mouse Laptop Mouse
month
Feb        3500  1500   3500   750      1     2
Jan        5000  1200   2500  1200      2     1
```

### Multiple Index and Column Levels

```python
# Multi-level pivot: month + region as rows, product as columns
pivot_multi_level = pd.pivot_table(
    sales_dup,
    values='revenue',
    index=['month', 'region'],
    columns='product',
    aggfunc='sum',
    fill_value=0
)

print(pivot_multi_level)
```

**Output:**

```
product            Laptop  Mouse
month region
Feb   North          3500    700
      South             0    800
Jan   North          3000   1200
      South          2000      0
```

### Margins (Totals)

```python
# Add row and column totals
pivot_with_totals = pd.pivot_table(
    sales_dup,
    values='revenue',
    index='month',
    columns='product',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Grand Total'
)

print(pivot_with_totals)
```

**Output:**

```
product    Laptop  Mouse  Grand Total
month
Feb          3500   1500         5000
Jan          5000   1200         6200
Grand Total  8500   2700        11200
```

### Different Aggregations for Different Values

```python
# Different metrics with different aggregations
sales_metrics = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Feb', 'Feb'],
    'product': ['Laptop', 'Mouse', 'Laptop', 'Mouse'],
    'revenue': [5000, 1200, 6000, 1500],
    'units': [10, 50, 12, 60],
    'returns': [1, 5, 0, 3]
})

pivot_mixed = pd.pivot_table(
    sales_metrics,
    values=['revenue', 'units', 'returns'],
    index='month',
    columns='product',
    aggfunc={
        'revenue': 'sum',
        'units': 'sum',
        'returns': 'mean'  # Average returns per transaction
    },
    fill_value=0
)

print(pivot_mixed)
```

---

## 5. `.melt()` — The Reverse of Pivot

`.melt()` converts **wide format** back to **long format**. It is the opposite of `.pivot()`.

### When to Use `.melt()`

- When data arrives in a "human-readable" wide format but you need it tidy for analysis.
- When preparing data for databases or machine learning pipelines.
- When you need to plot with seaborn (which prefers long format).

### Syntax

```python
df.melt(
    id_vars=['columns_to_keep'],      # Columns that stay as identifiers
    value_vars=['columns_to_melt'],   # Columns to unpivot (optional)
    var_name='new_name_for_variable', # Name for the new "variable" column
    value_name='new_name_for_value'   # Name for the new "value" column
)
```

### Basic Example

```python
# Wide format data (like an Excel export)
wide_df = pd.DataFrame({
    'employee': ['Alice', 'Bob', 'Charlie'],
    'Q1_Sales': [10000, 12000, 9000],
    'Q2_Sales': [11000, 11500, 10500],
    'Q3_Sales': [12000, 13000, 11000]
})

print("=== WIDE FORMAT ===")
print(wide_df)
```

**Output:**

```
  employee  Q1_Sales  Q2_Sales  Q3_Sales
0    Alice     10000     11000     12000
1      Bob     12000     11500     13000
2  Charlie      9000     10500     11000
```

```python
# Melt to long format
long_df = wide_df.melt(
    id_vars=['employee'],
    var_name='quarter',
    value_name='sales'
)

print("
=== LONG FORMAT (melt) ===")
print(long_df)
```

**Output:**

```
   employee  quarter  sales
0   Alice  Q1_Sales  10000
1     Bob  Q1_Sales  12000
2 Charlie  Q1_Sales   9000
3   Alice  Q2_Sales  11000
4     Bob  Q2_Sales  11500
5 Charlie  Q2_Sales  10500
6   Alice  Q3_Sales  12000
7     Bob  Q3_Sales  13000
8 Charlie  Q3_Sales  11000
```

### Selective Melting

```python
# Only melt specific columns
partial_melt = wide_df.melt(
    id_vars=['employee'],
    value_vars=['Q1_Sales', 'Q2_Sales'],  # Only melt Q1 and Q2
    var_name='quarter',
    value_name='sales'
)

print(partial_melt)
```

### Cleaning Melted Column Names

```python
# Often you want to clean up the variable names
long_df['quarter'] = long_df['quarter'].str.replace('_Sales', '')
print(long_df)
```

**Output:**

```
   employee quarter  sales
0   Alice      Q1  10000
1     Bob      Q1  12000
2 Charlie      Q1   9000
...
```

---

## 6. `.stack()` & `.unstack()` — Multi-Level Pivoting

`.stack()` and `.unstack()` work with **MultiIndex** DataFrames. They are lower-level pivoting tools.

### `.unstack()` — Pivot a Level of the Index to Columns

```python
# Create a MultiIndex DataFrame
multi = pd.DataFrame({
    'sales': [100, 150, 200, 250, 300, 350]
}, index=pd.MultiIndex.from_tuples([
    ('Jan', 'Online'), ('Jan', 'Store'),
    ('Feb', 'Online'), ('Feb', 'Store'),
    ('Mar', 'Online'), ('Mar', 'Store')
], names=['month', 'channel']))

print("=== MULTIINDEX (stacked) ===")
print(multi)
```

**Output:**

```
                 sales
month channel
Jan   Online       100
      Store        150
Feb   Online       200
      Store        250
Mar   Online       300
      Store        350
```

```python
# Unstack: move the inner index level to columns
unstacked = multi.unstack(level='channel')

print("
=== UNSTACKED (wide) ===")
print(unstacked)
```

**Output:**

```
        sales
channel Online Store
month
Jan         100   150
Feb         200   250
Mar         300   350
```

### `.stack()` — The Reverse

```python
# Stack: move columns back to the index
restacked = unstacked.stack()

print(restacked)
```

### Practical Use Case: Unstack After GroupBy

```python
# A common pattern: groupby -> unstack for a quick pivot
df = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Feb', 'Feb', 'Mar', 'Mar'],
    'channel': ['Online', 'Store', 'Online', 'Store', 'Online', 'Store'],
    'sales': [100, 150, 200, 250, 300, 350]
})

# Group and unstack — quick pivot without pivot_table!
quick_pivot = df.groupby(['month', 'channel'])['sales'].sum().unstack(level='channel')

print(quick_pivot)
```

**Output:**

```
channel  Online  Store
month
Jan         100    150
Feb         200    250
Mar         300    350
```

> **This pattern (`groupby` + `unstack`) is extremely common and often faster than `pivot_table` for simple cases.**

---

## 7. `.crosstab()` — Frequency Tables

`pd.crosstab()` is a specialized pivot for **counting frequencies**. It is essentially a shortcut for a pivot table with `aggfunc='count'`.

### Basic Crosstab

```python
# Customer survey data
survey = pd.DataFrame({
    'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'age_group': ['18-25', '26-35', '18-25', '26-35', '36-50', '18-25', '26-35', '36-50'],
    'satisfied': ['Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'No']
})

# Count of respondents by gender and age group
cross = pd.crosstab(
    survey['gender'],
    survey['age_group']
)

print(cross)
```

**Output:**

```
age_group  18-25  26-35  36-50
gender
F                2      1      1
M                1      2      1
```

### Crosstab with Normalization (Percentages)

```python
# Percentage of total
cross_pct = pd.crosstab(
    survey['gender'],
    survey['age_group'],
    normalize='all'  # 'all', 'index', or 'columns'
) * 100

print(cross_pct.round(1))
```

**Output:**

```
age_group  18-25  26-35  36-50
gender
F               25.0   12.5   12.5
M               12.5   25.0   12.5
```

### Crosstab with Aggregation

```python
# Average satisfaction score by gender and age
survey['satisfaction_score'] = survey['satisfied'].map({'Yes': 1, 'No': 0})

cross_agg = pd.crosstab(
    survey['gender'],
    survey['age_group'],
    values=survey['satisfaction_score'],
    aggfunc='mean'
).round(2)

print(cross_agg)
```

### Crosstab with Margins

```python
cross_total = pd.crosstab(
    survey['gender'],
    survey['age_group'],
    margins=True,
    margins_name='Total'
)

print(cross_total)
```

**Output:**

```
age_group  18-25  26-35  36-50  Total
gender
F                2      1      1      4
M                1      2      1      4
Total            3      3      2      8
```

---

## 8. Advanced Pivot Table Features

### Multiple Columns in `values`

```python
# Pivot multiple metrics at once
advanced = pd.pivot_table(
    sales_dup,
    values=['revenue', 'units'],
    index='month',
    columns='product',
    aggfunc={'revenue': 'sum', 'units': 'mean'},
    fill_value=0
)

print(advanced)
```

### Pivot with a Custom Aggregation Function

```python
# Custom function: percentage contribution
def pct_of_total(x):
    return (x.sum() / x.sum().sum()) * 100

pivot_custom = pd.pivot_table(
    sales_dup,
    values='revenue',
    index='month',
    columns='product',
    aggfunc=pct_of_total,
    fill_value=0
).round(2)

print(pivot_custom)
```

### Pivot with `observed=True` (Categorical Data)

```python
# When using categorical columns, observed=True only shows categories that exist
sales_dup['product'] = sales_dup['product'].astype('category')

pivot_observed = pd.pivot_table(
    sales_dup,
    values='revenue',
    index='month',
    columns='product',
    aggfunc='sum',
    fill_value=0,
    observed=True  # Only show categories with data
)
```

---

## 9. Handling Missing Values in Pivots

### `fill_value` Parameter

```python
# Data with missing combinations
sparse_data = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Feb'],
    'product': ['Laptop', 'Mouse', 'Laptop'],
    'revenue': [5000, 1200, 6000]
})

pivot_sparse = pd.pivot_table(
    sparse_data,
    values='revenue',
    index='month',
    columns='product',
    aggfunc='sum',
    fill_value=0  # Replace NaN with 0
)

print(pivot_sparse)
```

**Output:**

```
product  Laptop  Mouse
month
Jan        5000   1200
Feb        6000      0  # <- Mouse in Feb was missing, filled with 0
```

### After Pivot: Fill NaN with Group Statistics

```python
pivot_filled = pivot_sparse.copy()

# Fill missing values with the row mean (monthly average)
pivot_filled = pivot_filled.apply(lambda row: row.fillna(row.mean()), axis=1)

print(pivot_filled)
```

---

## 10. SQL Comparison

| SQL Pattern                                                 | Pandas Equivalent                                                         | Description             |
| ----------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------- |
| `SELECT * FROM table PIVOT (SUM(val) FOR col IN ('A','B'))` | `df.pivot_table(values='val', index='idx', columns='col', aggfunc='sum')` | Pivot with aggregation  |
| `SELECT idx, col, val FROM unpivoted`                       | `df.melt(id_vars='idx')`                                                  | Unpivot wide to long    |
| `SELECT a, b, COUNT(*) FROM table GROUP BY a, b`            | `pd.crosstab(df['a'], df['b'])`                                           | Frequency table         |
| `CASE WHEN col='A' THEN val END` in aggregation             | `pivot_table` with `columns='col'`                                        | Conditional aggregation |
| `GROUP BY ... WITH ROLLUP`                                  | `pivot_table(..., margins=True)`                                          | Add totals              |

### SQL PIVOT vs pandas pivot_table

**SQL (Oracle/SQL Server):**

```sql
SELECT *
FROM sales
PIVOT (
    SUM(revenue)
    FOR product IN ('Laptop' AS Laptop, 'Mouse' AS Mouse)
);
```

**Pandas:**

```python
pd.pivot_table(
    sales,
    values='revenue',
    index='month',
    columns='product',
    aggfunc='sum',
    fill_value=0
)
```

### SQL UNPIVOT vs pandas melt

**SQL:**

```sql
SELECT employee, quarter, sales
FROM sales_wide
UNPIVOT (
    sales FOR quarter IN (Q1_Sales, Q2_Sales, Q3_Sales)
);
```

**Pandas:**

```python
sales_wide.melt(
    id_vars=['employee'],
    var_name='quarter',
    value_name='sales'
)
```

---

## 11. Real-World Company Use Cases

### Use Case 1: E-Commerce — Monthly Product Performance Matrix

**Scenario:** An e-commerce director needs a monthly grid showing revenue per product category to identify seasonal trends.

```python
# Raw transaction data
ecom = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Mar', 'Mar', 'Mar'],
    'category': ['Electronics', 'Clothing', 'Electronics', 'Clothing',
                 'Electronics', 'Clothing', 'Electronics', 'Clothing', 'Home'],
    'revenue': [50000, 30000, 55000, 25000, 60000, 35000, 45000, 40000, 20000]
})

# Create the executive dashboard matrix
monthly_matrix = pd.pivot_table(
    ecom,
    values='revenue',
    index='month',
    columns='category',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)

print("=== MONTHLY REVENUE MATRIX ($) ===")
print(monthly_matrix)

# Calculate month-over-month growth
monthly_only = monthly_matrix.drop('Total', axis=0).drop('Total', axis=1)
growth = monthly_only.pct_change() * 100

print("
=== MONTH-OVER-MONTH GROWTH (%) ===")
print(growth.round(1))
```

**Output:**

```
=== MONTHLY REVENUE MATRIX ($) ===
category  Clothing  Electronics   Home    Total
month
Feb          25000      60000        0    85000
Jan          30000      50000        0    80000
Mar          40000      45000    20000   105000
Total        95000     155000    20000   270000

=== MONTH-OVER-MONTH GROWTH (%) ===
category  Clothing  Electronics   Home
month
Feb           -16.7       20.0    NaN
Jan             NaN        NaN    NaN
Mar            60.0      -25.0    inf
```

**Business Impact:** The director spots that Electronics revenue dropped 25% from Feb to Mar while Clothing grew 60%. They investigate and find a competitor launched a new gadget in March. The team responds with a targeted promotion, recovering 15% of lost Electronics revenue in April.

---

### Use Case 2: SaaS — Churn Analysis by Cohort

**Scenario:** A SaaS company tracks user retention by signup month (cohort) and active month to understand when users churn.

```python
# Cohort data: each row is a user-month combination
cohorts = pd.DataFrame({
    'signup_month': ['Jan', 'Jan', 'Jan', 'Jan', 'Feb', 'Feb', 'Feb', 'Mar', 'Mar'],
    'active_month': ['Jan', 'Feb', 'Mar', 'Apr', 'Feb', 'Mar', 'Apr', 'Mar', 'Apr'],
    'users_active': [100, 80, 65, 50, 120, 95, 75, 110, 90]
})

# Create cohort retention matrix
cohort_matrix = cohorts.pivot(
    index='signup_month',
    columns='active_month',
    values='users_active'
)

print("=== COHORT RETENTION (Active Users) ===")
print(cohort_matrix)

# Calculate retention percentages
cohort_sizes = cohorts.groupby('signup_month')['users_active'].first()
retention_matrix = cohort_matrix.divide(cohort_sizes, axis=0) * 100

print("
=== COHORT RETENTION (%) ===")
print(retention_matrix.round(1))
```

**Output:**

```
=== COHORT RETENTION (Active Users) ===
active_month   Apr   Feb   Jan   Mar
signup_month
Feb              75    95   NaN   120
Jan              50    80   100    65
Mar              90   NaN   NaN   110

=== COHORT RETENTION (%) ===
active_month   Apr   Feb   Jan   Mar
signup_month
Feb            62.5  79.2   NaN   100.0
Jan            50.0  80.0  100.0   65.0
Mar            81.8   NaN   NaN   100.0
```

**Business Impact:** The product team sees that Jan cohorts drop to 50% by month 4, while Mar cohorts retain 81.8%. They interview Mar cohort users and discover a new onboarding flow launched in March. The team rolls back the old onboarding for all users, improving overall 4-month retention from 50% to 72%.

---

### Use Case 3: Retail — Store Heatmap by Hour and Day

**Scenario:** A retail chain wants to optimize staffing by visualizing foot traffic by day of week and hour of day.

```python
# Foot traffic data
traffic = pd.DataFrame({
    'day': ['Mon', 'Mon', 'Mon', 'Tue', 'Tue', 'Wed', 'Wed', 'Thu', 'Thu', 'Fri', 'Fri'],
    'hour': [9, 12, 18, 9, 12, 9, 18, 9, 12, 9, 18],
    'visitors': [50, 120, 200, 45, 110, 55, 180, 60, 130, 70, 220]
})

# Create traffic heatmap matrix
traffic_heatmap = pd.pivot_table(
    traffic,
    values='visitors',
    index='hour',
    columns='day',
    aggfunc='mean',
    fill_value=0
)

# Reorder columns for the week
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
traffic_heatmap = traffic_heatmap.reindex(columns=day_order, fill_value=0)

print("=== STORE TRAFFIC HEATMAP (Visitors) ===")
print(traffic_heatmap)

# Identify peak hours
peak_hours = traffic_heatmap.max(axis=1)
print("
=== PEAK HOURS ===")
print(peak_hours)
```

**Output:**

```
=== STORE TRAFFIC HEATMAP (Visitors) ===
day   Mon   Tue   Wed   Thu   Fri  Sat  Sun
hour
9      50    45    55    60    70    0    0
12    120   110     0   130     0    0    0
18    200     0   180     0   220    0    0

=== PEAK HOURS ===
hour
9      70
12    130
18    220
```

**Business Impact:** Operations sees that 6 PM on Friday is the absolute peak (220 visitors). They shift one staff member from the Tuesday morning shift to Friday evening. Customer wait times drop by 35%, and Friday evening sales increase by 12%.

---

### Use Case 4: Finance — Currency Exposure Matrix

**Scenario:** A multinational company needs to track revenue exposure across regions and currencies to manage forex risk.

```python
# Revenue by region and currency
forex = pd.DataFrame({
    'region': ['EMEA', 'EMEA', 'APAC', 'APAC', 'Americas', 'Americas', 'EMEA', 'APAC'],
    'currency': ['EUR', 'GBP', 'JPY', 'CNY', 'USD', 'CAD', 'EUR', 'JPY'],
    'quarter': ['Q1', 'Q1', 'Q1', 'Q1', 'Q1', 'Q1', 'Q2', 'Q2'],
    'revenue_millions': [45, 20, 80, 35, 120, 15, 50, 85]
})

# Quarterly exposure matrix
exposure = pd.pivot_table(
    forex,
    values='revenue_millions',
    index='region',
    columns='currency',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total Exposure'
)

print("=== CURRENCY EXPOSURE MATRIX ($M) ===")
print(exposure)

# Calculate % of total per region
exposure_pct = exposure.div(exposure['Total Exposure'], axis=0) * 100
exposure_pct = exposure_pct.drop('Total Exposure', axis=1).drop('Total Exposure', axis=0)

print("
=== CURRENCY MIX BY REGION (%) ===")
print(exposure_pct.round(1))
```

**Output:**

```
=== CURRENCY EXPOSURE MATRIX ($M) ===
currency       CAD   CNY   EUR   GBP   JPY   USD  Total Exposure
region
Americas       15     0     0     0     0   120             135
APAC            0    35     0     0   165     0             200
EMEA            0     0    95    20     0     0             115
Total Exposure 15    35    95    20   165   120             450

=== CURRENCY MIX BY REGION (%) ===
currency       CAD   CNY   EUR   GBP   JPY   USD
region
Americas      11.1   0.0   0.0   0.0   0.0  88.9
APAC           0.0  17.5   0.0   0.0  82.5   0.0
EMEA           0.0   0.0  82.6  17.4   0.0   0.0
```

**Business Impact:** The CFO sees that APAC is 82.5% exposed to JPY, and JPY has been volatile. The treasury team hedges 50% of JPY exposure using forward contracts, protecting $68M in revenue from a 5% JPY depreciation.

---

### Use Case 5: Marketing — Campaign Performance by Channel and Audience

**Scenario:** A marketing team compares click-through rates (CTR) across channels and audience segments.

```python
# Campaign performance data
campaigns = pd.DataFrame({
    'channel': ['Email', 'Email', 'Email', 'Social', 'Social', 'Social',
                'PPC', 'PPC', 'PPC', 'Email', 'Social', 'PPC'],
    'audience': ['Young', 'Mid', 'Senior', 'Young', 'Mid', 'Senior',
                 'Young', 'Mid', 'Senior', 'Young', 'Mid', 'Senior'],
    'campaign': ['C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C1', 'C2', 'C2', 'C2'],
    'impressions': [10000, 8000, 5000, 15000, 12000, 6000, 20000, 10000, 4000, 12000, 18000, 22000],
    'clicks': [200, 160, 50, 450, 300, 60, 600, 250, 40, 300, 540, 550]
})

# Calculate CTR
campaigns['ctr'] = (campaigns['clicks'] / campaigns['impressions']) * 100

# Pivot: CTR by channel (rows) and audience (columns)
ctr_matrix = pd.pivot_table(
    campaigns,
    values='ctr',
    index='channel',
    columns='audience',
    aggfunc='mean',
    fill_value=0
).round(2)

# Reorder for logical flow
ctr_matrix = ctr_matrix[['Young', 'Mid', 'Senior']]

print("=== AVERAGE CTR BY CHANNEL & AUDIENCE (%) ===")
print(ctr_matrix)

# Find the best channel for each audience
best_channel = ctr_matrix.idxmax()
best_ctr = ctr_matrix.max()

print("
=== BEST CHANNEL PER AUDIENCE ===")
for audience in best_channel.index:
    print(f"{audience}: {best_channel[audience]} ({best_ctr[audience]:.2f}%)")
```

**Output:**

```
=== AVERAGE CTR BY CHANNEL & AUDIENCE (%) ===
audience  Young   Mid  Senior
channel
Email      2.08  2.00    1.00
PPC        3.00  2.50    1.00
Social     3.00  2.50    1.00

=== BEST CHANNEL PER AUDIENCE ===
Young: PPC (3.00%)
Mid: Social (2.50%)
Senior: Email (1.00%)
```

**Business Impact:** The marketing team reallocates budget: Young audiences get more PPC, Mid audiences get more Social, and Senior audiences get more Email. Overall campaign CTR improves from 2.1% to 2.8%, reducing cost-per-acquisition by 22%.

---

### Use Case 6: Manufacturing — Quality Control by Line and Shift

**Scenario:** A factory tracks defect rates by production line and shift to identify problem areas.

```python
# Quality control data
qc = pd.DataFrame({
    'line': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C'],
    'shift': ['Morning', 'Afternoon', 'Night', 'Morning', 'Afternoon', 'Night',
              'Morning', 'Afternoon', 'Night', 'Morning', 'Afternoon', 'Night'],
    'units_produced': [500, 450, 400, 520, 480, 420, 510, 470, 410, 530, 490, 430],
    'defects': [10, 18, 25, 8, 12, 30, 9, 15, 28, 7, 10, 22]
})

# Calculate defect rate
qc['defect_rate'] = (qc['defects'] / qc['units_produced']) * 100

# Pivot: defect rate by line (rows) and shift (columns)
defect_matrix = pd.pivot_table(
    qc,
    values='defect_rate',
    index='line',
    columns='shift',
    aggfunc='mean',
    fill_value=0
).round(2)

# Reorder columns
shift_order = ['Morning', 'Afternoon', 'Night']
defect_matrix = defect_matrix[shift_order]

print("=== DEFECT RATE BY LINE & SHIFT (%) ===")
print(defect_matrix)

# Highlight worst combinations
worst = defect_matrix.stack().idxmax()
worst_rate = defect_matrix.stack().max()

print(f"
Worst combination: Line {worst[0]}, {worst[1]} shift ({worst_rate:.2f}% defect rate)")

# Calculate overall line averages
line_avg = defect_matrix.mean(axis=1).round(2)
print("
=== AVERAGE DEFECT RATE BY LINE ===")
print(line_avg)
```

**Output:**

```
=== DEFECT RATE BY LINE & SHIFT (%) ===
shift   Morning  Afternoon  Night
line
A            1.54       4.00   6.25
B            1.76       3.13   7.14
C            1.32       2.04   5.12

Worst combination: Line B, Night shift (7.14% defect rate)

=== AVERAGE DEFECT RATE BY LINE ===
line
A    3.93
B    4.01
C    2.83
```

**Business Impact:** Quality engineers discover that Night shift consistently has 3-4x higher defect rates across all lines. Investigation reveals insufficient lighting and fatigue. The factory installs better lighting and adds a 15-minute break rotation. Night shift defect rates drop to 3.5%, saving $180,000 annually in rework costs.

---

## 12. Common Mistakes & How to Avoid Them

### Mistake 1: Using `.pivot()` When There Are Duplicates

```python
# BAD: Will raise ValueError
df.pivot(index='month', columns='product', values='revenue')
# ValueError: Index contains duplicate entries, cannot reshape

# GOOD: Use pivot_table with an aggregation function
pd.pivot_table(df, index='month', columns='product', values='revenue', aggfunc='sum')
```

> **Rule of thumb:** If you are not 100% sure there are no duplicates, use `.pivot_table()`.

### Mistake 2: Forgetting `fill_value` and Getting NaN Surprises

```python
# BAD: Missing combinations show as NaN, breaking calculations
pivot = df.pivot_table(index='month', columns='product', values='revenue', aggfunc='sum')
# Some cells will be NaN!

# GOOD: Always specify fill_value for clean output
pivot = df.pivot_table(index='month', columns='product', values='revenue',
                       aggfunc='sum', fill_value=0)
```

### Mistake 3: Not Handling MultiIndex After Pivot

```python
# After pivot with multiple values, columns become MultiIndex
pivot = df.pivot_table(values=['revenue', 'units'], index='month', columns='product', aggfunc='sum')

# BAD: Hard to work with MultiIndex columns

# GOOD: Flatten the columns
pivot.columns = ['_'.join(col).strip() for col in pivot.columns.values]
```

### Mistake 4: Melting Without Specifying `id_vars`

```python
# BAD: Melts EVERYTHING including the ID column
long = df.melt()  # Wrong!

# GOOD: Keep identifier columns separate
long = df.melt(id_vars=['employee_id', 'name'], var_name='quarter', value_name='sales')
```

### Mistake 5: Confusing `.pivot()` and `.pivot_table()`

| Function         | Use When                                   | Aggregation? |
| ---------------- | ------------------------------------------ | ------------ |
| `.pivot()`       | No duplicates in index+column combinations | No           |
| `.pivot_table()` | Duplicates exist, or you need aggregation  | Yes          |

### Mistake 6: Not Resetting Index After Unstack

```python
# After unstack, you often want a flat DataFrame for export/plotting
pivot = df.groupby(['month', 'product'])['revenue'].sum().unstack()

# GOOD: Reset index if you need month as a regular column
pivot_flat = pivot.reset_index()
```

---

## 13. Quick Reference Cheat Sheet

```python
import pandas as pd

# ============================================
# CHEAT SHEET: Pivoting DataFrames in Pandas
# ============================================

# --- .pivot() — Reshape without aggregation ---
# Use when: NO duplicates in index+column combinations
df.pivot(index='row_col', columns='col_col', values='val_col')

# Multiple values
df.pivot(index='row_col', columns='col_col', values=['val1', 'val2'])

# --- .pivot_table() — Reshape WITH aggregation ---
# Use when: Duplicates exist, or you need to aggregate
pd.pivot_table(
    df,
    values='val_col',
    index='row_col',
    columns='col_col',
    aggfunc='sum',        # 'sum', 'mean', 'count', 'max', custom_func
    fill_value=0,         # Replace NaN with this value
    margins=True,         # Add row/column totals
    margins_name='Total'
)

# Multiple aggregations
pd.pivot_table(df, values='val', index='row', columns='col', aggfunc=['sum', 'mean'])

# Different agg for different values
pd.pivot_table(df, values=['rev', 'units'], index='row', columns='col',
               aggfunc={'rev': 'sum', 'units': 'mean'})

# Multi-level index/columns
pd.pivot_table(df, values='val', index=['row1', 'row2'], columns=['col1', 'col2'])

# --- .melt() — Wide to Long ---
# Use when: Converting wide format back to tidy/long format
df.melt(
    id_vars=['keep_col1', 'keep_col2'],
    value_vars=['melt_col1', 'melt_col2'],  # Optional: which to melt
    var_name='variable_name',
    value_name='value_name'
)

# --- .stack() / .unstack() ---
# Use when: Working with MultiIndex DataFrames

# GroupBy + Unstack = Quick pivot
df.groupby(['row_col', 'col_col'])['val'].sum().unstack(level='col_col')

# Unstack a specific level
multi_index_df.unstack(level='column_level')

# Stack: move columns back to index
wide_df.stack()

# --- .crosstab() — Frequency tables ---
# Use when: Counting occurrences
pd.crosstab(df['row'], df['col'])
pd.crosstab(df['row'], df['col'], normalize='all')  # Percentages
pd.crosstab(df['row'], df['col'], margins=True)      # With totals

# Crosstab with aggregation
pd.crosstab(df['row'], df['col'], values=df['val'], aggfunc='mean')

# --- Flatten MultiIndex columns ---
df.columns = ['_'.join(col).strip() for col in df.columns.values]

# --- Reset index after pivot ---
df.pivot_table(...).reset_index()
```

---

## Summary: Which Function Should I Use?

| Goal                        | Function                        | Key Parameter                       |
| --------------------------- | ------------------------------- | ----------------------------------- |
| Reshape without calculation | `.pivot()`                      | `index`, `columns`, `values`        |
| Reshape with aggregation    | `.pivot_table()`                | `aggfunc`, `fill_value`, `margins`  |
| Wide -> Long format         | `.melt()`                       | `id_vars`, `var_name`, `value_name` |
| MultiIndex -> Wide          | `.unstack()`                    | `level`                             |
| Wide -> MultiIndex          | `.stack()`                      | —                                   |
| Count frequencies           | `.crosstab()`                   | `normalize`, `margins`              |
| Quick pivot from groupby    | `.unstack()` after `.groupby()` | `level`                             |

---

> **Remember:** Pivoting is about perspective. The same data tells a different story depending on whether you look at it as a list, a matrix, or a frequency table. Choose the shape that answers your question.

**Happy Pivoting!**
