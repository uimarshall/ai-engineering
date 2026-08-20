# Day 46: Introduction to Pandas (Python)

## 1. What is Pandas?

**Pandas** is a free, open-source Python library for **data manipulation and analysis**.

- Pandas work with tabular data similar to SQL and equally similar to the type of data used in excel spreadsheet.

- Note `Pandas` is built on top of `Numpy`.

The name comes from "**Pan**elt **Da**ta" (a play on "Python Data"). It was created by Wes McKinney (2008) and is now one of the most important libraries in the data science and machine learning ecosystem.

```python
import pandas as pd
```

At its core, Pandas gives you two main data structures:

| Structure     | Dimensions           | Analogy                          |
| ------------- | -------------------- | -------------------------------- |
| **Series**    | 1D (a single column) | A labeled list / row in a table  |
| **DataFrame** | 2D (rows + columns)  | An Excel spreadsheet / SQL table |

### Why use Pandas instead of plain Python lists or NumPy?

- Handles **mixed data types** (text + numbers + dates) in one structure
- Built-in **labels (index + column names)** — no need to track positions
- Handles **missing data (NaN)** gracefully
- Fast vectorized operations (written in C, far faster than Python loops)
- Easy **file I/O**: CSV, Excel, JSON, SQL, HTML, Parquet
- First-class **date/time** handling

---

## 2. What is Pandas Used For in Companies?

Pandas is everywhere in industry. Real corporate use cases:

| Industry / Team                   | Typical Use Case                                                                                                                  |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Finance / Banking**             | Transaction analysis, portfolio returns, fraud detection, risk reports, regulatory (Basel) reporting                              |
| **E-commerce (Amazon, Flipkart)** | Daily sales dashboards, inventory tracking, pricing analysis, customer segmentation, A/B test summaries                           |
| **Marketing / AdTech**            | Campaign ROI analysis, conversion funnels, customer Lifetime Value (LTV), cohort analysis                                         |
| **Healthcare / Pharma**           | Clinical trial data cleaning, patient records analysis, drug efficacy stats                                                       |
| **Retail / Supply Chain**         | Demand forecasting data prep, stock-outs analysis, supplier performance                                                           |
| **HR / Operations**               | Employee attrition analysis, payroll processing, KPI reporting                                                                    |
| **Data Engineering / ML**         | **ETL pipelines** — cleaning raw data before feeding it into machine learning models (Pandas is the "kitchen" before ML "dinner") |
| **Startups (Analytics teams)**    | Building KPI tables for dashboards (Tableau, Power BI), weekly business reviews                                                   |

A typical day for a data analyst at a company: pull raw sales data (CSV/API/SQL) → clean it in Pandas → calculate metrics (revenue, churn, growth) → export results to a dashboard or database. Pandas is the tool for almost every one of those steps.

---

## 3. Essential Concepts (Beginner-Friendly)

### 3.1 The DataFrame — "your spreadsheet in Python"

It contains Horizontal rows and Vertical columns.

When we talk of the shape of the data, we're looking at how many rows & columns it has. Similar to the Cartesian graph, where we have the x and y axis usually written as (x,y) to get the coordinates, we also have (r,c) to visualize the shape of the data, which means the rows measure how long the data is, while the column measures how wide the data is.

Think of a DataFrame exactly like an Excel sheet:

```
        Department  Salary  Experience   Hired
0        Marketing   55000        3.5  2020-03-01   <- row 0  (a "record")
1             Sales   61000        5.0  2019-07-15   <- row 1
2             IT     82000        7.5  2017-01-10   <- row 2
     ^  row labels (index)
```

**Create a DataFrame from a dictionary:**

```python
import pandas as pd

# Each key becomes a COLUMN, each value a list of row values
df = pd.DataFrame({
    "Department": ["Marketing", "Sales", "IT", "Sales"],
    "Salary":     [55000, 61000, 82000, 48000],
    "Experience": [3.5, 5.0, 7.5, 1.0]
})

print(df)
```

**Output:**

```
  Department  Salary  Experience
0  Marketing   55000         3.5
1      Sales   61000         5.0
2         IT   82000         7.5
3      Sales   48000         1.0
```

### 3.2 The Series — one column of a DataFrame

```python
salary = df["Salary"]          # select one column -> a Series
print(type(salary))            # <class 'pandas.core.series.Series'>
print(salary.mean())           # 61500.0
```

### 3.3 Loading and Saving Data (huge time-saver)

```python
# Read
df = pd.read_csv("employees.csv")
df = pd.read_excel("sales.xlsx")
df = pd.read_json("logs.json")
df = pd.read_sql("SELECT * FROM orders", connection)

# Write / save
df.to_csv("cleaned.csv", index=False)
df.to_excel("report.xlsx", index=False)
```

`index=False` means "don't write the row-number column into the file".

### 3.4 Quick Look at Your Data (the first steps with ANY dataset)

```python
df.head()        # first 5 rows
df.tail(3)       # last 3 rows
df.shape         # (rows, columns) e.g. (4, 3)
df.info()        # column names, data types, non-null counts
df.describe()    # numeric summary: count, mean, std, min, 25%, 50%, 75%, max
df["Salary"].unique()    # distinct values
df["Department"].value_counts()   # how many rows per category
```

> 💡 **Industry habit:** whenever you open a new dataset, you ALWAYS run `head()`, `info()`, `describe()` first — this is called _exploratory data analysis_ (EDA).

### 3.5 Selecting Data

```python
# Select COLUMN(s)
df["Salary"]                      # one column -> Series
df[["Salary", "Experience"]]      # multiple columns -> DataFrame

# Select ROWS by index number
df.loc[0]             # row at index 0 (label-based)
df.iloc[1]            # row at position 1 (position-based)
df.iloc[0:2]          # first two rows
```

**Filtering rows with conditions** (like Excel filters):

```python
# Who earns more than 60000?
df[df["Salary"] > 60000]

# Who is in Sales?
df[df["Department"] == "Sales"]

# Combined conditions (use &, |, ~ and parentheses)
df[(df["Department"] == "Sales") & (df["Experience"] > 2)]
df[~(df["Department"] == "IT")]                      # NOT IT
df[df["Department"].isin(["Sales", "Marketing"])]     # IN a list
df[df["Department"].str.contains("Sa")]               # text contains
```

### 3.6 Adding / Renaming / Deleting Columns

```python
# New column from an existing one (vectorized — no loop needed!)
df["Monthly"] = df["Salary"] / 12

# New column with a fixed value
df["Employed"] = True

# Rename columns
df = df.rename(columns={"Salary": "Annual_Salary"})

# Delete a column
df = df.drop(columns=["Employed"])

# Drop a whole row
df = df.drop(index=0)
```

### 3.7 Handling Missing Data (very common in real data)

Real company data is almost always messy — missing salaries, blank names, etc. Pandas represents missing values as `NaN`.

```python
df.isna().sum()               # count missing per column
df.dropna()                   # drop rows with ANY missing value
df.dropna(subset=["Salary"])  # drop rows where Salary specifically is missing
df.fillna(0)                  # fill all missing with 0
df["Experience"].fillna(df["Experience"].mean(), inplace=True)  # fill with column average
```

### 3.8 Sorting

```python
df.sort_values("Salary", ascending=False)        # highest salary first
df.sort_values(["Department", "Salary"])         # sort by two columns
```

### 3.9 Grouping — the most valuable concept for business reporting

**GroupBy = "do this calculation separately for each group"** (like Excel Pivot Tables).

```python
# Average salary per department
df.groupby("Department")["Salary"].mean()

# Count employees per department
df.groupby("Department").size()

# Multiple stats at once
df.groupby("Department")["Salary"].agg(["mean", "min", "max", "count"])

# Filter within groups: departments with more than 1 employee
df.groupby("Department").filter(lambda g: len(g) > 1)
```

Output of the first example:

```
Department
IT         82000.0
Marketing  55000.0
Sales      54500.0
Name: Salary, dtype: float64
```

### 3.10 Working with Dates

```python
df["Hired"] = pd.to_datetime(df["Hired"])           # convert text -> datetime
df["HiredYear"] = df["Hired"].dt.year
df["HiredMonth"] = df["Hired"].dt.month
df["TenureDays"] = (pd.Timestamp.now() - df["Hired"]).dt.days
```

### 3.11 Merging DataFrames (like SQL JOIN)

Companies keep data in many tables (orders, customers, products). Pandas lets you combine them:

```python
# Imagine two tables:
# customers: CustomerID | Name
# orders:    OrderID | CustomerID | Amount

orders.merge(customers, on="CustomerID")                          # inner join
orders.merge(customers, on="CustomerID", how="left")              # left join
orders.merge(customers, on="CustomerID", how="outer")             # full join
pd.concat([df_jan, df_feb, df_mar], axis=0)                       # stack tables vertically
```

### 3.12 String Operations (`.str`)

```python
df["Name"] = ["  Ayesha Khan ", "Bilal Ahmed"]
df["Name"].str.strip()            # remove extra spaces
df["Name"].str.lower()
df["Name"].str.split().str[0]     # first word of each name
df["Name"].str.contains("Khan")   # boolean match
```

### 3.13 Aggregations at a Glance

```python
df["Salary"].sum()       # total
df["Salary"].mean()      # average
df["Salary"].median()    # middle value
df["Salary"].std()       # spread
df["Salary"].corr(df["Experience"])  # correlation (-1 to 1)
df["Salary"].rank()
```

---

## 4. Complete Mini Project: Company Sales Analysis

A realistic end-to-end example a junior analyst might do:

```python
import pandas as pd

# ---- 1. LOAD raw data (pretend this came from the warehouse) ----
df = pd.DataFrame({
    "Date":       ["2025-01-05", "2025-01-05", "2025-02-10", "2025-02-11",
                   "2025-03-01", None],
    "Product":    ["Laptop", "Mouse", "Laptop", "Monitor", "Mouse", "Laptop"],
    "Region":     ["North", "North", "South", "South", "East", "East"],
    "Quantity":   [10, 50, 8, None, 60, 12],
    "Unit_Price": [1200, 25, 1150, 220, 24, 1250]
})

# ---- 2. CLEAN ----
df["Date"] = pd.to_datetime(df["Date"])
df["Quantity"].fillna(df["Quantity"].mean(), inplace=True)   # fill missing qty with average
df = df.dropna(subset=["Date"])                              # can't sell with no date

# ---- 3. TRANSFORM ----
df["Revenue"] = df["Quantity"] * df["Unit_Price"]
df["Month"] = df["Date"].dt.month

# ---- 4. ANALYZE ----
print("Total revenue:", df["Revenue"].sum())

# Monthly revenue per region (pivot-style report)
monthly = df.pivot_table(values="Revenue", index="Product",
                         columns="Month", aggfunc="sum", fill_value=0)
print(monthly)

# Best region
best = df.groupby("Region")["Revenue"].sum().idxmax()
print("Best region:", best)
```

Output:

```
Total revenue: 125165.0
Month        NaN   1.0    2.0   3.0
Product
Laptop       0.0  12000  9200.0  15000.0
Monitor      0.0    0.0  1760.0     0.0
Mouse        0.0   1250    0.0  1440.0

Best region: North
```

This is the exact workflow used daily in business intelligence: **load → clean → transform → analyze → report**.

---

## 5. Common Pitfalls for Beginners

1. **SettingWithCopyWarning** — modifying a row of a filtered DataFrame may not work. Use `.loc[]` explicitly: `df.loc[df["Sales"] > 100, "Salary"] += 1000`.
2. **`NaN != NaN`** — missing values never equal themselves. Use `.isna()`, never `== None` or `== NaN`.
3. **Forgetting `inplace=True`** — most methods return a NEW DataFrame. `df.drop(columns=["x"])` does nothing unless you reassign or use `inplace=True`.
4. **Chained indexing** — `df[df["x"]>0]["y"] = 1` is unreliable; do `df.loc[df["x"]>0, "y"] = 1` instead.
5. **Looping over rows** — `for row in df.iterrows(): ...` is 100x slower than a vectorized operation like `df["x"] * 2`. Always look for the vectorized version.
6. **Integer columns with missing data** become `float64` or `Int64` — `df["qty"] = [1, None, 3]` gives `[1.0, NaN, 3.0]`.

---

## 6. Quick Reference Cheat Sheet

```text
Create:     pd.DataFrame(dict)    pd.Series(list)
Load:       pd.read_csv / read_excel / read_sql / read_json
Peek:       .head()  .info()  .describe()  .shape  .columns  .dtypes
Select:     df[cols]  df.loc[labels, cols]  df.iloc[positions, cols]
Filter:     df[condition]         df[df["x"].isin([...])]
New col:    df["new"] = df["x"] * 2
Missing:    .isna()  .dropna()  .fillna(value)
Clean text: .str.strip()  .str.lower()  .str.contains()
Sort:       .sort_values("col", ascending=False)
Group:      .groupby("col")["num"].mean()/sum()/count()
Combine:    .merge(other, on="key", how=...)   pd.concat([A, B])
Save:       .to_csv("f.csv", index=False)  .to_excel("f.xlsx")
Dates:      pd.to_datetime(col)  .dt.year  .dt.month
```

## 7. Where Pandas Sits in the Data Stack

```
 Raw Data (SQL, APIs, CSV, Excel, IoT sensors)
        |
        v
   PANDAS  (clean, reshape, calculate)   <-- today
        |
        v
   Visualization (Matplotlib, Seaborn, Plotly, Streamlit)
        |
        v
   Machine Learning (scikit-learn, XGBoost) / Databases / Dashboards
```

**One-liner takeaway:** Pandas is the "Swiss army knife" of data work — every company that touches structured data uses it daily to clean, combine, and summarize data before analysis or machine learning.
