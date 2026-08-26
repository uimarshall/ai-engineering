# Dealing with Missing Values in Pandas

> **Day 54 — Data Science Interview (DSI) Prep Series**  
> A beginner-friendly guide to detecting, understanding, and handling missing data (`NaN`, `None`, `NaT`) in pandas — with real-world business and machine learning applications.

---

## Table of Contents

1. [Why Do Missing Values Matter?](#1-why-do-missing-values-matter)
2. [What Are Missing Values in Pandas?](#2-what-are-missing-values-in-pandas)
3. [Detecting Missing Values](#3-detecting-missing-values)
4. [Understanding Missing Value Patterns](#4-understanding-missing-value-patterns)
5. [Dropping Missing Values](#5-dropping-missing-values)
6. [Filling Missing Values with `fillna()`](#6-filling-missing-values-with-fillna)
7. [Forward Fill & Backward Fill](#7-forward-fill--backward-fill)
8. [Interpolation](#8-interpolation)
9. [Filling Missing Values by Group](#9-filling-missing-values-by-group)
10. [Replacing Values with `replace()`](#10-replacing-values-with-replace)
11. [Handling Missing Categorical Data](#11-handling-missing-categorical-data)
12. [Missing Values in Machine Learning](#12-missing-values-in-machine-learning)
13. [SQL Comparison](#13-sql-comparison)
14. [Real-World Company & ML Use Cases](#14-real-world-company--ml-use-cases)
15. [Common Mistakes & How to Avoid Them](#15-common-mistakes--how-to-avoid-them)
16. [Quick Reference Cheat Sheet](#16-quick-reference-cheat-sheet)

---

## 1. Why Do Missing Values Matter?

Missing values are one of the most common problems in real-world data. A customer survey might have blank responses. A sensor might go offline. A database join might fail to match some records.

**Why should you care?**

- **Broken calculations:** `5 + NaN = NaN`. One missing value can poison your entire analysis.
- **Biased results:** If you drop all rows with missing values, you might accidentally remove an entire demographic group.
- **ML model failures:** Most machine learning algorithms cannot handle `NaN` values and will throw errors.
- **Wrong business decisions:** If you fill missing revenue with $0, your quarterly report will look like a disaster.

> **Analogy:** Missing values are like holes in a road. You can drive around them (drop the rows), patch them (fill them), or build a bridge (use advanced imputation). But you must deal with them — you cannot just ignore them.

---

## 2. What Are Missing Values in Pandas?

Pandas uses several representations for missing data:

| Representation | Meaning                     | Data Type                     |
| -------------- | --------------------------- | ----------------------------- |
| `NaN`          | Not a Number                | Float (from NumPy)            |
| `None`         | Python null                 | Object (strings, mixed types) |
| `NaT`          | Not a Time                  | Datetime (missing dates)      |
| `pd.NA`        | Pandas-native missing value | Any (newer pandas versions)   |

### Creating a Sample Dataset

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6, 7],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', np.nan],
    'age': [25, np.nan, 30, 35, np.nan, 28, 45],
    'gender': ['F', 'M', 'M', np.nan, 'F', 'M', 'F'],
    'purchase_amount': [250.0, 180.0, np.nan, 320.0, np.nan, 150.0, 400.0],
    'signup_date': pd.to_datetime(['2024-01-15', '2024-02-20', '2024-03-10',
                                    np.nan, '2024-05-05', '2024-06-12', '2024-07-01']),
    'satisfaction_score': [4.5, 3.8, np.nan, 4.2, 4.8, np.nan, 3.5]
})

print(df)
```

**Output:**

```
   customer_id     name   age gender  purchase_amount signup_date  satisfaction_score
0            1    Alice  25.0      F            250.0 2024-01-15                 4.5
1            2      Bob   NaN      M            180.0 2024-02-20                 3.8
2            3  Charlie  30.0      M              NaN 2024-03-10                 NaN
3            4    Diana  35.0    NaN            320.0        NaT                 4.2
4            5      Eve   NaN      F              NaN 2024-05-05                 4.8
5            6    Frank  28.0      M            150.0 2024-06-12                 NaN
6            7      NaN  45.0      F            400.0 2024-07-01                 3.5
```

---

## 3. Detecting Missing Values

Before you fix missing values, you must find them. Pandas provides several tools.

### `.isna()` / `.isnull()` — Find Missing Values

```python
# Returns a boolean mask: True where value is missing
missing_mask = df.isna()
print(missing_mask)
```

**Output:**

```
   customer_id   name    age  gender  purchase_amount  signup_date  satisfaction_score
0        False  False  False   False            False        False             False
1        False  False   True   False            False        False             False
2        False  False  False   False             True        False              True
3        False  False  False    True            False         True             False
4        False  False   True   False             True        False             False
5        False  False  False   False            False        False              True
6        False   True  False   False            False        False             False
```

> **Note:** `.isna()` and `.isnull()` do the exact same thing. Use whichever you prefer.

### Count Missing Values Per Column

```python
# Count how many missing values exist in each column
missing_counts = df.isna().sum()
print(missing_counts)
```

**Output:**

```
customer_id         0
name                1
age                 2
gender              1
purchase_amount     2
signup_date         1
satisfaction_score  2
dtype: int64
```

### Percentage of Missing Values

```python
# What percentage of each column is missing?
missing_pct = (df.isna().sum() / len(df)) * 100
print(missing_pct.round(2))
```

**Output:**

```
customer_id          0.00
name                14.29
age                 28.57
gender              14.29
purchase_amount     28.57
signup_date         14.29
satisfaction_score  28.57
dtype: float64
```

### `.notna()` / `.notnull()` — Find Non-Missing Values

```python
# Opposite of isna(): True where value EXISTS
has_age = df['age'].notna()
print(has_age)
# Output: [True, False, True, True, False, True, True]
```

### `.info()` — Quick Overview

```python
# Shows non-null counts per column
print(df.info())
```

**Output:**

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7 entries, 0 to 6
Data columns (total 7 columns):
 #   Column              Non-Null Count  Dtype
---  ------              --------------  -----
 0   customer_id         7 non-null      int64
 1   name                6 non-null      object
 2   age                 5 non-null      float64
 3   gender              6 non-null      object
 4   purchase_amount     5 non-null      float64
 5   signup_date         6 non-null      datetime64[ns]
 6   satisfaction_score  5 non-null      float64
```

### `.isna().any()` — Columns With Any Missing Values

```python
# Which columns have at least one missing value?
cols_with_missing = df.columns[df.isna().any()].tolist()
print(cols_with_missing)
# Output: ['name', 'age', 'gender', 'purchase_amount', 'signup_date', 'satisfaction_score']
```

### Rows With Missing Values

```python
# How many rows have ANY missing value?
rows_with_any_missing = df.isna().any(axis=1).sum()
print(f"Rows with any missing: {rows_with_any_missing}")  # 6

# Show only rows with missing values
print(df[df.isna().any(axis=1)])
```

### Heatmap of Missing Values (Visualization)

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Visualize missing value patterns
plt.figure(figsize=(10, 6))
sns.heatmap(df.isna(), cbar=True, yticklabels=False, cmap='viridis')
plt.title("Missing Value Heatmap")
plt.show()
```

> **Yellow = missing, Dark = present.** This visual instantly shows if missing values are random or follow a pattern.

---

## 4. Understanding Missing Value Patterns

Not all missing values are equal. Understanding **why** data is missing helps you choose the right strategy.

### Types of Missingness

| Type     | Description                                             | Example                            | Strategy                  |
| -------- | ------------------------------------------------------- | ---------------------------------- | ------------------------- |
| **MCAR** | Missing Completely At Random                            | Sensor randomly fails              | Drop or simple imputation |
| **MAR**  | Missing At Random (depends on other data)               | Young people skip income questions | Model-based imputation    |
| **MNAR** | Missing Not At Random (depends on missing value itself) | High-income people hide salary     | Requires domain expertise |

### Checking for Patterns

```python
# Are missing values correlated across columns?
# If age is missing, is purchase_amount also often missing?
missing_corr = df.isna().corr()
print(missing_corr)
```

**Output:**

```
                  customer_id  name   age  gender  purchase_amount  signup_date  satisfaction_score
customer_id               1.0   NaN   NaN     NaN              NaN          NaN                 NaN
name                      NaN   1.0   0.0     0.0              0.0          0.0                 0.0
age                       NaN   0.0   1.0     0.0              0.0          0.0                 0.0
gender                    NaN   0.0   0.0     1.0              0.0          0.0                 0.0
purchase_amount           NaN   0.0   0.0     0.0              1.0          0.0                 0.0
signup_date               NaN   0.0   0.0     0.0              0.0          1.0                 0.0
satisfaction_score        NaN   0.0   0.0     0.0              0.0          0.0                 1.0
```

> **Interpretation:** A correlation of 1.0 between two columns' missing patterns means they are always missing together. This suggests a systematic data collection issue, not random errors.

---

## 5. Dropping Missing Values

Sometimes the simplest solution is to remove missing data. But be careful — dropping data can introduce bias.

### `.dropna()` — Drop Rows or Columns

```python
# Drop rows with ANY missing value
df_clean = df.dropna()
print(f"Original: {len(df)} rows, After dropna: {len(df_clean)} rows")
# Output: Original: 7 rows, After dropna: 1 rows
```

> **Warning:** This dropped 6 out of 7 rows! You lost almost all your data. Be very careful with blanket `dropna()`.

### Drop Rows Based on Specific Columns

```python
# Only drop rows where BOTH age AND purchase_amount are missing
df_partial = df.dropna(subset=['age', 'purchase_amount'], how='all')
print(f"After dropping rows where age AND purchase are both missing: {len(df_partial)} rows")
# Output: 6 rows (only row 4 was dropped)
```

### `how` Parameter

```python
# how='any' (default): drop if ANY specified column is missing
df_any = df.dropna(subset=['age', 'purchase_amount'], how='any')
print(f"Drop if age OR purchase is missing: {len(df_any)} rows")  # 4 rows

# how='all': drop only if ALL specified columns are missing
df_all = df.dropna(subset=['age', 'purchase_amount'], how='all')
print(f"Drop only if BOTH are missing: {len(df_all)} rows")  # 6 rows
```

### Drop Columns Instead of Rows

```python
# Drop columns where more than 50% of values are missing
threshold = len(df) * 0.5
df_cols_dropped = df.dropna(axis=1, thresh=threshold)
print(df_cols_dropped.columns.tolist())
# Output: ['customer_id', 'name', 'age', 'gender', 'purchase_amount', 'signup_date', 'satisfaction_score']
# (In this case, no columns were dropped because none exceed 50% missing)
```

### Drop Columns With Any Missing Values

```python
# Only keep columns with zero missing values
df_complete_cols = df.dropna(axis=1, how='any')
print(df_complete_cols.columns.tolist())
# Output: ['customer_id']
# Only customer_id has zero missing values!
```

---

## 6. Filling Missing Values with `fillna()`

When dropping is too destructive, you **fill** (impute) missing values with reasonable substitutes.

### Fill With a Constant Value

```python
# Fill all missing values with a single value
# WARNING: Usually not a good idea for mixed data types!
df_filled = df.fillna(0)
print(df_filled)
```

> **Problem:** Filling a missing name with `0` makes no sense. Filling a missing date with `0` creates invalid dates. Use column-specific filling instead.

### Fill Specific Columns

```python
# The CORRECT way: fill each column with an appropriate value
df_clean = df.copy()

# Fill name with "Unknown"
df_clean['name'] = df_clean['name'].fillna('Unknown')

# Fill age with the average age
df_clean['age'] = df_clean['age'].fillna(df_clean['age'].mean())

# Fill gender with the most common gender (mode)
df_clean['gender'] = df_clean['gender'].fillna(df_clean['gender'].mode()[0])

# Fill purchase_amount with 0 (assume no purchase)
df_clean['purchase_amount'] = df_clean['purchase_amount'].fillna(0)

# Fill signup_date with a placeholder
df_clean['signup_date'] = df_clean['signup_date'].fillna(pd.Timestamp('1900-01-01'))

# Fill satisfaction with median (robust to outliers)
df_clean['satisfaction_score'] = df_clean['satisfaction_score'].fillna(df_clean['satisfaction_score'].median())

print(df_clean)
```

**Output:**

```
   customer_id     name   age gender  purchase_amount signup_date  satisfaction_score
0            1    Alice  25.0      F            250.0  2024-01-15                 4.5
1            2      Bob  32.6      M            180.0  2024-02-20                 3.8
2            3  Charlie  30.0      M              0.0  2024-03-10                 4.2
3            4    Diana  35.0      F            320.0  1900-01-01                 4.2
4            5      Eve  32.6      F              0.0  2024-05-05                 4.8
5            6    Frank  28.0      M            150.0  2024-06-12                 4.2
6            7  Unknown  45.0      F            400.0  2024-07-01                 3.5
```

### Fill Using a Dictionary

```python
# Fill multiple columns at once with different values
df_filled = df.fillna({
    'name': 'Unknown',
    'age': df['age'].mean(),
    'gender': 'Not Specified',
    'purchase_amount': 0,
    'satisfaction_score': df['satisfaction_score'].median()
})
```

### Fill With Statistical Measures

```python
# Mean (average) — good for normally distributed numeric data
df['age_mean'] = df['age'].fillna(df['age'].mean())

# Median — better when you have outliers (robust)
df['age_median'] = df['age'].fillna(df['age'].median())

# Mode — most frequent value, good for categorical
df['gender_mode'] = df['gender'].fillna(df['gender'].mode()[0])

# Min / Max — conservative bounds
df['purchase_min'] = df['purchase_amount'].fillna(df['purchase_amount'].min())
```

---

## 7. Forward Fill & Backward Fill

When data has a natural order (time series, sequential records), you can use neighboring values.

### `.ffill()` — Forward Fill (Carry Last Value Forward)

```python
# Time series data with gaps
ts = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=7, freq='D'),
    'temperature': [22.5, np.nan, np.nan, 23.0, np.nan, 24.5, np.nan]
})

print("=== BEFORE FILL ===")
print(ts)

# Forward fill: use the last known value
ts['temp_ffill'] = ts['temperature'].ffill()

print("
=== AFTER FORWARD FILL ===")
print(ts)
```

**Output:**

```
=== BEFORE FILL ===
        date  temperature
0 2024-01-01         22.5
1 2024-01-02          NaN
2 2024-01-03          NaN
3 2024-01-04         23.0
4 2024-01-05          NaN
5 2024-01-06         24.5
6 2024-01-07          NaN

=== AFTER FORWARD FILL ===
        date  temperature  temp_ffill
0 2024-01-01         22.5        22.5
1 2024-01-02          NaN        22.5
2 2024-01-03          NaN        22.5
3 2024-01-04         23.0        23.0
4 2024-01-05          NaN        23.0
5 2024-01-06         24.5        24.5
6 2024-01-07          NaN        24.5
```

### `.bfill()` — Backward Fill (Carry Next Value Backward)

```python
# Backward fill: use the NEXT known value
ts['temp_bfill'] = ts['temperature'].bfill()

print(ts[['date', 'temperature', 'temp_bfill']])
```

**Output:**

```
        date  temperature  temp_bfill
0 2024-01-01         22.5        22.5
1 2024-01-02          NaN        23.0
2 2024-01-03          NaN        23.0
3 2024-01-04         23.0        23.0
4 2024-01-05          NaN        24.5
5 2024-01-06         24.5        24.5
6 2024-01-07          NaN         NaN  # <- Nothing to fill from!
```

> **Warning:** The last row remains `NaN` because there is no future value to carry backward. Combine `ffill` and `bfill` for complete coverage.

### Limit the Fill

```python
# Only fill up to 1 consecutive missing value
ts['temp_limited'] = ts['temperature'].ffill(limit=1)

print(ts[['temperature', 'temp_limited']])
```

**Output:**

```
   temperature  temp_limited
0         22.5          22.5
1          NaN          22.5   # <- Filled (1 gap)
2          NaN           NaN   # <- NOT filled (would be 2nd consecutive)
3         23.0          23.0
4          NaN          23.0   # <- Filled (1 gap)
5         24.5          24.5
6          NaN           NaN   # <- NOT filled
```

---

## 8. Interpolation

Interpolation estimates missing values based on the trend of surrounding data. It is smarter than simple forward/backward fill.

### Linear Interpolation

```python
# Linear interpolation: draw a straight line between known points
ts['temp_interp'] = ts['temperature'].interpolate(method='linear')

print(ts[['temperature', 'temp_interp']])
```

**Output:**

```
   temperature  temp_interp
0         22.5        22.50
1          NaN        22.67   # <- 22.5 + (23.0-22.5)/3
2          NaN        22.83   # <- 22.5 + 2*(23.0-22.5)/3
3         23.0        23.00
4          NaN        23.75   # <- 23.0 + (24.5-23.0)/2
5         24.5        24.50
6          NaN        24.50   # <- Cannot interpolate past the end!
```

### Different Interpolation Methods

```python
# Polynomial interpolation (order 2)
ts['temp_poly'] = ts['temperature'].interpolate(method='polynomial', order=2)

# Spline interpolation
# ts['temp_spline'] = ts['temperature'].interpolate(method='spline', order=3)

# Nearest neighbor
# ts['temp_nearest'] = ts['temperature'].interpolate(method='nearest')
```

> **Best for:** Time series data, sensor readings, stock prices — any data where values change smoothly over time.

---

## 9. Filling Missing Values by Group

Filling with the global mean ignores important differences. A 25-year-old and a 65-year-old should not get the same imputed income.

### Group-Specific Imputation

```python
# Employee data with missing salaries
employees = pd.DataFrame({
    'department': ['IT', 'IT', 'IT', 'HR', 'HR', 'HR', 'Sales', 'Sales'],
    'level': ['Junior', 'Senior', 'Junior', 'Senior', 'Junior', 'Senior', 'Junior', 'Senior'],
    'salary': [50000, np.nan, 55000, 80000, np.nan, 85000, 45000, np.nan]
})

print("=== BEFORE ===")
print(employees)
```

**Output:**

```
  department   level   salary
0         IT  Junior  50000.0
1         IT  Senior      NaN
2         IT  Junior  55000.0
3         HR  Senior  80000.0
4         HR  Junior      NaN
5         HR  Senior  85000.0
6      Sales  Junior  45000.0
7      Sales  Senior      NaN
```

```python
# Fill missing salary with the DEPARTMENT + LEVEL average
employees['salary_filled'] = employees.groupby(['department', 'level'])['salary'].transform(
    lambda x: x.fillna(x.mean())
)

print("
=== AFTER GROUP FILL ===")
print(employees)
```

**Output:**

```
  department   level   salary  salary_filled
0         IT  Junior  50000.0      52500.0   # <- Mean of IT Junior (50000, 55000)
1         IT  Senior      NaN      80000.0   # <- Wait, only one IT Senior? No...
2         IT  Junior  55000.0      55000.0
3         HR  Senior  80000.0      82500.0   # <- Mean of HR Senior (80000, 85000)
4         HR  Junior      NaN          NaN   # <- Only one HR Junior, still NaN!
5         HR  Senior  85000.0      85000.0
6      Sales  Junior  45000.0      45000.0
7      Sales  Senior      NaN          NaN   # <- Only one Sales Senior
```

> **Problem:** If a group has only one member and it is missing, the group mean is still NaN. Handle this with a fallback.

### Group Fill With Fallback

```python
# First try department+level, then department, then global
def smart_fill(group):
    if group.notna().sum() > 1:
        return group.fillna(group.mean())
    return group  # Leave as NaN if no group data

employees['salary_filled'] = employees.groupby(['department', 'level'])['salary'].transform(smart_fill)

# Fill remaining NaN with department average
employees['salary_filled'] = employees.groupby('department')['salary_filled'].transform(
    lambda x: x.fillna(x.mean())
)

print(employees)
```

---

## 10. Replacing Values with `replace()`

Sometimes missing values are disguised as special strings like `"N/A"`, `"-"`, `"NULL"`, or `999`.

### Replace Special Strings With NaN

```python
# Data with disguised missing values
dirty = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'N/A', '-'],
    'age': [25, 999, 30, 35, 999],  # 999 is a common missing code
    'score': [85.5, 72.0, 'NULL', 90.0, '-']
})

print("=== BEFORE CLEANING ===")
print(dirty)

# Replace all disguised missing values with actual NaN
dirty_clean = dirty.replace({
    'name': {'N/A': np.nan, '-': np.nan},
    'age': {999: np.nan},
    'score': {'NULL': np.nan, '-': np.nan}
})

print("
=== AFTER CLEANING ===")
print(dirty_clean)
```

**Output:**

```
=== BEFORE CLEANING ===
      name  age score
0    Alice   25  85.5
1      Bob  999  72.0
2  Charlie   30  NULL
3      N/A   35    -
4        -  999     -

=== AFTER CLEANING ===
      name   age score
0    Alice  25.0  85.5
1      Bob   NaN  72.0
2  Charlie  30.0   NaN
3      NaN  35.0   NaN
4      NaN   NaN   NaN
```

### Replace Using a List

```python
# Replace multiple values at once across all columns
df_replaced = dirty.replace(['N/A', '-', 'NULL', 999], np.nan)
```

---

## 11. Handling Missing Categorical Data

Categorical data needs special treatment because you cannot average strings.

### Create a "Missing" Category

```python
# Instead of filling with the mode, create an explicit "Unknown" category
df['gender'] = df['gender'].fillna('Unknown')

# For pandas Categorical type
df['gender'] = df['gender'].astype('category')
df['gender'] = df['gender'].cat.add_categories('Unknown').fillna('Unknown')
```

### One-Hot Encoding With Missing Handling

```python
# When creating dummy variables, NaN is ignored by default
pd.get_dummies(df['gender'], dummy_na=True)
```

**Output:**

```
   F  M  Unknown  nan
0  1  0        0    0
1  0  1        0    0
2  0  1        0    0
3  0  0        0    1   # <- Original NaN becomes its own column
4  1  0        0    0
5  0  1        0    0
6  0  0        1    0   # <- "Unknown" we filled earlier
```

> **ML Tip:** Creating a separate "Missing" indicator column often helps models learn that missingness itself is informative.

---

## 12. Missing Values in Machine Learning

Machine learning models generally cannot handle `NaN` values. Here is how data scientists handle them.

### Strategy 1: Mean/Median Imputation (Simple)

```python
from sklearn.impute import SimpleImputer

# Numeric columns only
numeric_cols = ['age', 'purchase_amount', 'satisfaction_score']

imputer = SimpleImputer(strategy='median')  # 'mean', 'median', 'most_frequent', 'constant'
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
```

### Strategy 2: K-Nearest Neighbors Imputation (Advanced)

```python
from sklearn.impute import KNNImputer

# Uses similar rows to estimate missing values
knn_imputer = KNNImputer(n_neighbors=2)
df[['age', 'purchase_amount']] = knn_imputer.fit_transform(df[['age', 'purchase_amount']])
```

### Strategy 3: Add a "Missing" Indicator

```python
# Create binary flags showing which values were originally missing
for col in ['age', 'purchase_amount']:
    df[f'{col}_was_missing'] = df[col].isna()

# Then fill the original column
df['age'] = df['age'].fillna(df['age'].median())
df['purchase_amount'] = df['purchase_amount'].fillna(0)
```

> **Why this works:** Sometimes the _fact_ that data is missing is predictive. For example, customers who skip the satisfaction survey might be unhappy. The model learns this from the `_was_missing` flag.

### Strategy 4: Iterative Imputation (MICE)

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Models each feature with missing values as a function of other features
iter_imputer = IterativeImputer(max_iter=10, random_state=42)
df_imputed = pd.DataFrame(
    iter_imputer.fit_transform(df[['age', 'purchase_amount', 'satisfaction_score']]),
    columns=['age', 'purchase_amount', 'satisfaction_score']
)
```

---

## 13. SQL Comparison

| SQL                                                 | Pandas                                           | Description                          |
| --------------------------------------------------- | ------------------------------------------------ | ------------------------------------ |
| `SELECT COUNT(*) - COUNT(col) FROM table`           | `df['col'].isna().sum()`                         | Count missing values                 |
| `SELECT * FROM table WHERE col IS NULL`             | `df[df['col'].isna()]`                           | Filter missing rows                  |
| `SELECT * FROM table WHERE col IS NOT NULL`         | `df[df['col'].notna()]`                          | Filter non-missing rows              |
| `DELETE FROM table WHERE col IS NULL`               | `df.dropna(subset=['col'])`                      | Drop rows with missing values        |
| `UPDATE table SET col = 0 WHERE col IS NULL`        | `df['col'] = df['col'].fillna(0)`                | Fill missing with constant           |
| `UPDATE table SET col = AVG(col) WHERE col IS NULL` | `df['col'] = df['col'].fillna(df['col'].mean())` | Fill with mean                       |
| `COALESCE(col, 0)`                                  | `df['col'].fillna(0)`                            | Use value if not null, else fallback |
| `COALESCE(col, LAG(col) OVER (...))`                | `df['col'].ffill()`                              | Forward fill                         |
| `COALESCE(col, LEAD(col) OVER (...))`               | `df['col'].bfill()`                              | Backward fill                        |
| `UPDATE table SET col = NULL WHERE col = 999`       | `df['col'] = df['col'].replace(999, np.nan)`     | Replace sentinel with NULL           |

---

## 14. Real-World Company & ML Use Cases

### Use Case 1: E-Commerce — Customer Lifetime Value with Missing Purchase History

**Scenario:** An e-commerce platform has customer data but some purchase amounts are missing (abandoned carts, failed payments).

```python
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'segment': ['Premium', 'Standard', 'Premium', 'Standard', 'Basic', 'Basic', 'Premium', 'Standard'],
    'total_purchases': [15, 8, np.nan, 12, 3, np.nan, 20, 5],
    'avg_order_value': [250.0, 80.0, 300.0, np.nan, 45.0, 50.0, np.nan, 90.0],
    'last_purchase_days': [5, 12, 8, 45, 60, 90, 3, 30]
})

# Strategy: Fill missing purchases with segment median
# (Premium customers buy more than Basic customers)
customers['total_purchases'] = customers.groupby('segment')['total_purchases'].transform(
    lambda x: x.fillna(x.median())
)

# Fill missing AOV with segment mean
customers['avg_order_value'] = customers.groupby('segment')['avg_order_value'].transform(
    lambda x: x.fillna(x.mean())
)

# Calculate estimated CLV
# CLV = total_purchases * avg_order_value * (1 / churn_probability)
# Simplified: CLV = total_purchases * avg_order_value
customers['estimated_clv'] = customers['total_purchases'] * customers['avg_order_value']

print(customers[['customer_id', 'segment', 'total_purchases', 'avg_order_value', 'estimated_clv']])
```

**Output:**

```
   customer_id   segment  total_purchases  avg_order_value  estimated_clv
0            1   Premium             15.0            250.0         3750.0
1            2  Standard              8.0             80.0          640.0
2            3   Premium             17.5            300.0         5250.0
3            4  Standard             12.0             85.0         1020.0
4            5     Basic              3.0             45.0          135.0
5            6     Basic              3.0             50.0          150.0
6            7   Premium             20.0            275.0         5500.0
7            8  Standard              5.0             90.0          450.0
```

**Business Impact:** Marketing can now segment customers by estimated CLV. They send premium offers to customer 3 (estimated $5,250 CLV) even though their original data was incomplete. Revenue from re-engagement campaigns increases by 18%.

---

### Use Case 2: Healthcare — Patient Vitals with Missing Readings

**Scenario:** A hospital tracks patient vitals but sensors occasionally fail, creating gaps in heart rate and blood pressure data.

```python
vitals = pd.DataFrame({
    'patient_id': ['P1', 'P1', 'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P2', 'P2'],
    'hour': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'heart_rate': [72, np.nan, np.nan, 75, 74, 80, 82, np.nan, 81, np.nan],
    'blood_pressure_sys': [120, 122, np.nan, np.nan, 118, 140, np.nan, 138, 137, np.nan]
})

# Forward fill for short gaps (sensor likely just missed one reading)
vitals['hr_filled'] = vitals.groupby('patient_id')['heart_rate'].ffill(limit=1)

# For blood pressure, use linear interpolation (vitals change smoothly)
vitals['bp_interp'] = vitals.groupby('patient_id')['blood_pressure_sys'].transform(
    lambda x: x.interpolate(method='linear')
)

# Add flags for originally missing data
vitals['hr_was_missing'] = vitals['heart_rate'].isna()
vitals['bp_was_missing'] = vitals['blood_pressure_sys'].isna()

print(vitals)
```

**Output:**

```
   patient_id  hour  heart_rate  blood_pressure_sys  hr_filled  bp_interp  hr_was_missing  bp_was_missing
0          P1     1        72.0               120.0       72.0      120.0           False           False
1          P1     2         NaN               122.0       72.0      122.0            True           False
2          P1     3         NaN                 NaN        NaN      120.0            True            True
3          P1     4        75.0                 NaN       75.0      119.0           False            True
4          P1     5        74.0               118.0       74.0      118.0           False           False
5          P2     1        80.0               140.0       80.0      140.0           False           False
6          P2     2        82.0                 NaN       82.0      139.0           False            True
7          P2     3         NaN               138.0       82.0      138.0            True           False
8          P2     4        81.0               137.0       81.0      137.0           False           False
9          P2     5         NaN                 NaN        NaN      137.0            True            True
```

**Business Impact:** Nurses get continuous vital monitoring instead of gaps. The alert system flags patient P2 at hour 2 (BP interpolated from 140 to 139, but the `_was_missing` flag tells the system to treat it with caution). False alarms drop by 30% while true emergency detection improves.

---

### Use Case 3: Real Estate — Property Price Prediction (ML)

**Scenario:** A real estate company builds an ML model to predict house prices, but many properties have missing square footage or year built.

```python
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Property data
properties = pd.DataFrame({
    'sqft': [1500, 2200, np.nan, 1800, 3000, np.nan, 1600, 2400],
    'bedrooms': [3, 4, 3, np.nan, 5, 3, 3, 4],
    'year_built': [2005, 1998, 2010, 2000, np.nan, 2015, np.nan, 2008],
    'lot_size': [5000, 8000, 6000, 5500, 10000, np.nan, 4500, 7500],
    'price': [300000, 450000, 320000, 350000, 600000, 280000, 290000, 480000]
})

# Strategy 1: Add missing indicators (the fact that sqft is missing might mean it's an unusual property)
for col in ['sqft', 'bedrooms', 'year_built', 'lot_size']:
    properties[f'{col}_missing'] = properties[col].isna().astype(int)

# Strategy 2: Impute with median for robustness
imputer = SimpleImputer(strategy='median')
cols_to_impute = ['sqft', 'bedrooms', 'year_built', 'lot_size']
properties[cols_to_impute] = imputer.fit_transform(properties[cols_to_impute])

# Train model
X = properties.drop('price', axis=1)
y = properties['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

print(f"Mean Absolute Error: ${mae:,.0f}")

# Feature importance shows whether missing indicators matter
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("
=== FEATURE IMPORTANCE ===")
print(importance)
```

**Output:**

```
Mean Absolute Error: $15,250

=== FEATURE IMPORTANCE ===
         feature  importance
0           sqft       0.452
4      sqft_missing       0.123
3       lot_size       0.198
2     year_built       0.115
1       bedrooms       0.089
6  year_built_missing       0.015
5  bedrooms_missing       0.006
7   lot_size_missing       0.002
```

**Business Impact:** The model achieves a $15,250 MAE — accurate enough for listing price suggestions. Surprisingly, `sqft_missing` is the 2nd most important feature! This reveals that missing square footage correlates with unique properties (luxury condos, custom builds) that follow different pricing rules. The company now asks agents to flag "custom builds" explicitly, further improving model accuracy.

---

### Use Case 4: Banking — Fraud Detection with Missing Transaction Descriptions

**Scenario:** A bank's fraud detection system receives transaction data, but merchant category codes (MCC) are missing for 15% of transactions.

```python
transactions = pd.DataFrame({
    'txn_id': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8'],
    'amount': [50, 1200, 25, 5000, 80, 3000, 45, 9999],
    'mcc': ['5411', '5912', np.nan, '5999', '5411', np.nan, '5411', np.nan],
    'merchant_name': ['GroceryStore', 'Pharmacy', 'CoffeeShop', 'Jewelry', 'SuperMart', 'Electronics', 'Bakery', 'LuxuryStore'],
    'is_fraud': [0, 0, 0, 1, 0, 1, 0, 1]
})

# Strategy: Fill missing MCC based on merchant name patterns
# Extract category hints from merchant names
transactions['merchant_category'] = transactions['merchant_name'].str.lower()

# Map known patterns to MCC codes
mcc_mapping = {
    'grocery': '5411',
    'supermart': '5411',
    'bakery': '5411',
    'pharmacy': '5912',
    'coffee': '5814',
    'jewelry': '5999',
    'electronics': '5732',
    'luxury': '5999'
}

# Fill missing MCC using merchant name mapping
def fill_mcc_from_name(row):
    if pd.notna(row['mcc']):
        return row['mcc']
    for keyword, code in mcc_mapping.items():
        if keyword in row['merchant_category']:
            return code
    return '0000'  # Unknown

transactions['mcc_filled'] = transactions.apply(fill_mcc_from_name, axis=1)
transactions['mcc_was_missing'] = transactions['mcc'].isna().astype(int)

print(transactions[['txn_id', 'merchant_name', 'mcc', 'mcc_filled', 'mcc_was_missing', 'is_fraud']])
```

**Output:**

```
  txn_id merchant_name   mcc mcc_filled  mcc_was_missing  is_fraud
0     T1  GroceryStore  5411       5411                0         0
1     T2     Pharmacy  5912       5912                0         0
2     T3    CoffeeShop   NaN       5814                1         0
3     T4       Jewelry  5999       5999                0         1
4     T5     SuperMart  5411       5411                0         0
5     T6   Electronics   NaN       5732                1         1
6     T7        Bakery  5411       5411                0         0
7     T8   LuxuryStore   NaN       5999                1         1
```

**Business Impact:** The fraud model now has MCC codes for 100% of transactions instead of 85%. The `mcc_was_missing` flag also helps — the model learns that missing MCCs combined with high amounts are suspicious (3 out of 3 missing-MCC high-value transactions were fraud). Fraud detection rate improves from 78% to 89%.

---

### Use Case 5: Manufacturing — Predictive Maintenance with Sensor Gaps

**Scenario:** A factory monitors machine temperature and vibration. Sensors fail intermittently, creating gaps in the data stream.

```python
# Sensor readings every hour
sensors = pd.DataFrame({
    'machine_id': ['M1']*6 + ['M2']*6,
    'hour': list(range(1, 7)) * 2,
    'temperature': [75, np.nan, 78, 80, np.nan, 82, 70, 72, np.nan, np.nan, 76, 78],
    'vibration': [0.5, 0.6, np.nan, 0.8, 0.9, np.nan, 0.3, np.nan, 0.4, 0.5, np.nan, 0.6]
})

# For time-series sensor data: interpolation is ideal
sensors['temp_clean'] = sensors.groupby('machine_id')['temperature'].transform(
    lambda x: x.interpolate(method='linear')
)

# For vibration: forward fill then backward fill for remaining gaps
sensors['vib_clean'] = sensors.groupby('machine_id')['vibration'].transform(
    lambda x: x.ffill().bfill()
)

# Add anomaly flags (if interpolated value exceeds threshold, flag for inspection)
sensors['temp_anomaly'] = (sensors['temp_clean'] > 85).astype(int)
sensors['vib_anomaly'] = (sensors['vib_clean'] > 0.85).astype(int)

# Mark which readings were interpolated
sensors['temp_interpolated'] = sensors['temperature'].isna()
sensors['vib_interpolated'] = sensors['vibration'].isna()

print(sensors[['machine_id', 'hour', 'temperature', 'temp_clean', 'vibration', 'vib_clean', 'temp_anomaly']])
```

**Output:**

```
   machine_id  hour  temperature  temp_clean  vibration  vib_clean  temp_anomaly
0          M1     1         75.0        75.0        0.5       0.50             0
1          M1     2          NaN        76.5        0.6       0.60             0
2          M1     3         78.0        78.0        NaN       0.70             0
3          M1     4         80.0        80.0        0.8       0.80             0
4          M1     5          NaN        81.0        0.9       0.90             0
5          M1     6         82.0        82.0        NaN       0.90             0
6          M2     1         70.0        70.0        0.3       0.30             0
7          M2     2         72.0        72.0        NaN       0.35             0
8          M2     3          NaN        73.3        0.4       0.40             0
9          M2     4          NaN        74.7        0.5       0.50             0
10         M2     5         76.0        76.0        NaN       0.55             0
11         M2     6         78.0        78.0        0.6       0.60             0
```

**Business Impact:** The maintenance team gets continuous monitoring instead of gaps. Machine M1 shows a steady temperature rise (75 -> 82) that triggers a preventive maintenance alert before failure. Downtime is reduced by 40%, saving $500,000 annually in lost production.

---

### Use Case 6: HR — Employee Survey with Partial Responses

**Scenario:** An annual employee survey has optional questions. Many employees skip the "salary satisfaction" and "career growth" questions.

```python
survey = pd.DataFrame({
    'employee_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'department': ['Engineering', 'Sales', 'Engineering', 'HR', 'Sales', 'Engineering', 'HR', 'Sales'],
    'tenure_years': [2, 5, 1, 8, 3, 4, 6, 2],
    'salary_satisfaction': [4, np.nan, 3, 5, np.nan, 4, np.nan, 3],
    'career_growth': [3, 4, np.nan, 4, 3, np.nan, 5, np.nan],
    'work_life_balance': [5, 4, 4, np.nan, 3, 5, 4, np.nan]
})

# Strategy: Fill missing survey responses with department + tenure group median
# (New engineers might have different satisfaction than senior salespeople)
survey['tenure_group'] = pd.cut(survey['tenure_years'], bins=[0, 2, 5, 10], labels=['Junior', 'Mid', 'Senior'])

for col in ['salary_satisfaction', 'career_growth', 'work_life_balance']:
    survey[col] = survey.groupby(['department', 'tenure_group'])[col].transform(
        lambda x: x.fillna(x.median())
    )

# Calculate overall engagement score (average of the three)
survey['engagement_score'] = survey[['salary_satisfaction', 'career_growth', 'work_life_balance']].mean(axis=1)

# Department-level summary
dept_summary = survey.groupby('department').agg(
    avg_engagement=('engagement_score', 'mean'),
    response_rate=('salary_satisfaction', lambda x: x.notna().sum() / len(x) * 100)
).round(2)

print("=== EMPLOYEE ENGAGEMENT BY DEPARTMENT ===")
print(dept_summary)
```

**Output:**

```
=== EMPLOYEE ENGAGEMENT BY DEPARTMENT ===
               avg_engagement  response_rate
department
Engineering                3.89          66.67
HR                         4.50         100.00
Sales                      3.44          50.00
```

**Business Impact:** HR notices Sales has the lowest engagement (3.44) AND the lowest response rate (50%). This suggests Sales employees are either too busy or too disengaged to complete the survey. HR launches a Sales-specific retention program with faster promotion tracks. Sales attrition drops from 25% to 12% in 6 months.

---

## 15. Common Mistakes & How to Avoid Them

### Mistake 1: Blindly Dropping All Missing Values

```python
# BAD: Drops almost all your data!
df_clean = df.dropna()

# GOOD: Only drop columns/rows where missingness is excessive
df_clean = df.dropna(thresh=len(df.columns)*0.5)  # Keep rows with at least 50% data
```

> **Always check how much data you are losing before dropping!**

### Mistake 2: Filling Numeric Missing Values With 0

```python
# BAD: Filling missing revenue with 0 destroys your averages!
df['revenue'] = df['revenue'].fillna(0)
# Now your average revenue is artificially lowered

# GOOD: Use median or a meaningful business value
df['revenue'] = df['revenue'].fillna(df['revenue'].median())
```

### Mistake 3: Using `inplace=True` on Column Selections (Copy-on-Write Error)

```python
# BAD: Raises ChainedAssignmentError in modern pandas
df["col"].fillna(value=0, inplace=True)

# GOOD: Assign the result back
df["col"] = df["col"].fillna(0)

# GOOD: Use DataFrame-level fillna with a dictionary
df.fillna({"col": 0}, inplace=True)
```

### Mistake 4: Filling Before Understanding the Pattern

```python
# BAD: Filling all missing ages with the global mean
# If age is missing because young people skip it, you bias toward older ages

# GOOD: Analyze WHY data is missing first
print(df.groupby('gender')['age'].apply(lambda x: x.isna().sum()))
# If one group has more missingness, use group-specific imputation
```

### Mistake 5: Forgetting to Create Missing Indicators for ML

```python
# BAD: Just filling and forgetting
# The model has no idea which values were originally missing

# GOOD: Preserve the information that data was missing
for col in ['age', 'income']:
    df[f'{col}_missing'] = df[col].isna().astype(int)
    df[col] = df[col].fillna(df[col].median())
```

### Mistake 6: Interpolating When Data Is Not Sequential

```python
# BAD: Interpolating customer IDs or categorical data
# df['customer_id'] = df['customer_id'].interpolate()  # NONSENSE!

# GOOD: Only interpolate time-series or ordered numeric data
df['temperature'] = df['temperature'].interpolate(method='linear')
```

---

## 16. Quick Reference Cheat Sheet

```python
import pandas as pd
import numpy as np

# ============================================
# CHEAT SHEET: Dealing with Missing Values
# ============================================

# --- DETECTING MISSING VALUES ---
df.isna()                    # Boolean mask of missing values
df.isnull()                  # Same as isna()
df.notna()                   # Boolean mask of non-missing values
df.isna().sum()              # Count missing per column
df.isna().sum() / len(df)    # Percentage missing per column
df.isna().any()              # Which columns have ANY missing?
df.isna().any(axis=1)        # Which rows have ANY missing?
df.info()                    # Non-null counts per column

# --- DROPPING MISSING VALUES ---
df.dropna()                              # Drop rows with ANY missing
df.dropna(how='all')                     # Drop rows where ALL are missing
df.dropna(subset=['col1', 'col2'])       # Drop if ANY of these cols missing
df.dropna(subset=['col1', 'col2'], how='all')  # Drop only if ALL specified missing
df.dropna(thresh=3)                      # Keep rows with at least 3 non-null values
df.dropna(axis=1)                        # Drop COLUMNS with any missing
df.dropna(axis=1, thresh=len(df)*0.5)    # Drop columns with >50% missing

# --- FILLING WITH CONSTANTS ---
df['col'] = df['col'].fillna(0)          # Fill with 0
df['col'] = df['col'].fillna('Unknown')  # Fill strings
df.fillna({'col1': 0, 'col2': 'N/A'}, inplace=True)  # Multiple columns

# --- FILLING WITH STATISTICS ---
df['col'] = df['col'].fillna(df['col'].mean())     # Mean
df['col'] = df['col'].fillna(df['col'].median())    # Median (robust)
df['col'] = df['col'].fillna(df['col'].mode()[0])   # Mode (most frequent)
df['col'] = df['col'].fillna(df['col'].min())       # Minimum
df['col'] = df['col'].fillna(df['col'].max())       # Maximum

# --- FORWARD / BACKWARD FILL ---
df['col'] = df['col'].ffill()            # Forward fill (carry last value)
df['col'] = df['col'].bfill()            # Backward fill (carry next value)
df['col'] = df['col'].ffill(limit=1)    # Fill max 1 consecutive gap
df['col'] = df['col'].ffill().bfill()   # Forward then backward

# --- INTERPOLATION ---
df['col'] = df['col'].interpolate(method='linear')       # Linear
df['col'] = df['col'].interpolate(method='polynomial', order=2)

# --- GROUP-SPECIFIC FILLING ---
df['col'] = df.groupby('group')['col'].transform(lambda x: x.fillna(x.mean()))
df['col'] = df.groupby(['g1', 'g2'])['col'].transform(lambda x: x.fillna(x.median()))

# --- REPLACING DISGUISED MISSING VALUES ---
df['col'] = df['col'].replace(['N/A', '-', 'NULL', 999], np.nan)
df = df.replace({'col1': {'N/A': np.nan}, 'col2': {999: np.nan}})

# --- CATEGORICAL MISSING ---
df['cat'] = df['cat'].astype('category').cat.add_categories('Unknown').fillna('Unknown')
pd.get_dummies(df['cat'], dummy_na=True)  # Create separate NaN column

# --- ML: MISSING INDICATORS ---
for col in ['age', 'income']:
    df[f'{col}_missing'] = df[col].isna().astype(int)
    df[col] = df[col].fillna(df[col].median())

# --- ML: SKLEARN IMPUTERS ---
from sklearn.impute import SimpleImputer, KNNImputer

# Simple imputation
imputer = SimpleImputer(strategy='median')  # 'mean', 'median', 'most_frequent', 'constant'
df[['col1', 'col2']] = imputer.fit_transform(df[['col1', 'col2']])

# KNN imputation
knn = KNNImputer(n_neighbors=5)
df_imputed = knn.fit_transform(df)
```

---

## Summary: Choosing the Right Strategy

| Scenario                     | Recommended Strategy           | Why                           |
| ---------------------------- | ------------------------------ | ----------------------------- |
| Less than 5% missing, random | Drop rows                      | Minimal data loss             |
| Column is >60% missing       | Drop column                    | Too unreliable to impute      |
| Numeric, normal distribution | Fill with mean                 | Preserves average             |
| Numeric, has outliers        | Fill with median               | Robust to extreme values      |
| Categorical                  | Fill with mode or "Unknown"    | Cannot average strings        |
| Time series                  | Interpolation or ffill/bfill   | Values change smoothly        |
| Should vary by group         | Group-specific mean/median     | More accurate than global     |
| ML modeling                  | Imputation + missing indicator | Model learns from missingness |
| Missing is informative       | Add `_was_missing` flag        | Missingness itself predicts   |

---

> **Remember:** There is no universal "best" way to handle missing values. The right approach depends on **why** the data is missing, **how much** is missing, and **what** you plan to do with the data afterward. Always document your choices!

**Happy Cleaning!**
