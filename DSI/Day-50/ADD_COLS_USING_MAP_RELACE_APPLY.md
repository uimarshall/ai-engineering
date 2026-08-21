# Adding and Transforming Columns Using `map`, `replace`, `apply`, and `applymap`

> **Day 50 — Data Science Interview Prep**  
> This guide explains how to transform and add columns in pandas using `map`, `replace`, `apply`, and `applymap`, with detailed explanations for beginners and real-world company use cases.

---

## Table of Contents

- [Adding and Transforming Columns Using `map`, `replace`, `apply`, and `applymap`](#adding-and-transforming-columns-using-map-replace-apply-and-applymap)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [The `map()` Method](#the-map-method)
    - [Mapping Values with a Dictionary](#mapping-values-with-a-dictionary)
    - [Mapping with a Function](#mapping-with-a-function)
    - [Handling Unmapped Values (NaN)](#handling-unmapped-values-nan)
  - [The `replace()` Method](#the-replace-method)
    - [Replacing Single Values](#replacing-single-values)
    - [Replacing Multiple Values](#replacing-multiple-values)
    - [Replacing Values in a DataFrame](#replacing-values-in-a-dataframe)
    - [Using Regular Expressions with Replace](#using-regular-expressions-with-replace)
  - [The `apply()` Method](#the-apply-method)
    - [Applying a Function to a Series (Column)](#applying-a-function-to-a-series-column)
    - [Applying a Function to a DataFrame (Row-wise or Column-wise)](#applying-a-function-to-a-dataframe-row-wise-or-column-wise)
    - [Using Lambda Functions with Apply](#using-lambda-functions-with-apply)
    - [Apply vs Vectorized Operations](#apply-vs-vectorized-operations)
  - [The `applymap()` Method](#the-applymap-method)
    - [Applying a Function Element-wise to a DataFrame](#applying-a-function-element-wise-to-a-dataframe)
    - [When to Use applymap vs apply](#when-to-use-applymap-vs-apply)
  - [Quick Comparison Table](#quick-comparison-table)
  - [Practical Company Use Cases](#practical-company-use-cases)
    - [1. **Retail: Product Category Encoding with `map()`**](#1-retail-product-category-encoding-with-map)
    - [2. **Healthcare: Cleaning Patient Data with `replace()`**](#2-healthcare-cleaning-patient-data-with-replace)
    - [3. **Finance: Calculating Risk Scores with `apply()`**](#3-finance-calculating-risk-scores-with-apply)
    - [4. **E-Commerce: Formatting Prices with `applymap()`**](#4-e-commerce-formatting-prices-with-applymap)
    - [5. **HR: Salary Band Classification with `map()` and `apply()`**](#5-hr-salary-band-classification-with-map-and-apply)
  - [Summary Cheat Sheet](#summary-cheat-sheet)
  - [Key Takeaways for Beginners](#key-takeaways-for-beginners)
  - [Adding Columns in Pandas: `map()`, `replace()`, `apply()`, and `applymap()`](#adding-columns-in-pandas-map-replace-apply-and-applymap)
    - [1. `map()` — Element-wise Mapping Using a Dictionary or Function](#1-map--element-wise-mapping-using-a-dictionary-or-function)
    - [2. `replace()` — Substitute Values (In-place or Copy)](#2-replace--substitute-values-in-place-or-copy)
    - [3. `apply()` — Apply a Function Along an Axis](#3-apply--apply-a-function-along-an-axis)
    - [4. `applymap()` — Element-wise Function on Entire DataFrame](#4-applymap--element-wise-function-on-entire-dataframe)
    - [Quick Comparison Table](#quick-comparison-table-1)
    - [Pro Tips](#pro-tips)

---

## Introduction

When working with data, you often need to **transform** existing values into new ones. For example:

- Convert country codes to full country names
- Replace incorrect or outdated values
- Calculate new columns based on existing ones
- Clean or format every cell in a table

Pandas provides four powerful methods for these transformations:

| Method       | What It Does                                   | Works On               |
| ------------ | ---------------------------------------------- | ---------------------- |
| `map()`      | Transforms each value using a dict or function | Series (single column) |
| `replace()`  | Substitutes specific values with new ones      | Series or DataFrame    |
| `apply()`    | Applies a function along an axis               | Series or DataFrame    |
| `applymap()` | Applies a function to every single element     | DataFrame only         |

Think of it this way:

- **`map()`** is like a translator (word → word)
- **`replace()`** is like find-and-replace in Word
- **`apply()`** is like a calculator (process a whole column or row at once)
- **`applymap()`** is like a spell-checker (check every single cell individually)

---

## The `map()` Method

### Mapping Values with a Dictionary

The `map()` method is used on a **Series** (single column) to transform each value based on a lookup dictionary.

```python
import pandas as pd
import numpy as np

# Create a DataFrame with country codes
data = pd.DataFrame({
    "food": ["bacon", "pulled pork", "bacon", "Pastrami", "corned beef", "Bacon", "pastrami", "honey ham", "nova lox"],
    "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6],
    "animal": ["pig", "pig", "pig", "cow", "cow", "pig", "cow", "pig", "salmon"]
})

print("Original DataFrame:")
print(data)

# Map animal names to a numeric code
meat_to_animal = {
    "bacon": "pig",
    "pulled pork": "pig",
    "pastrami": "cow",
    "corned beef": "cow",
    "honey ham": "pig",
    "nova lox": "salmon"
}

# Wait — let's do a better example: map animals to category numbers
animal_to_code = {"pig": 1, "cow": 2, "salmon": 3}

# map() looks up each value in the Series in the dictionary
data["animal_code"] = data["animal"].map(animal_to_code)
print("
After mapping animals to codes:")
print(data)
```

**Detailed Explanation for Beginners:**

- `data["animal"]` selects the "animal" column, which is a **Series**.
- `.map(animal_to_code)` looks at each value in that Series and tries to find it in the dictionary.
- `"pig"` → `1`, `"cow"` → `2`, `"salmon"` → `3`.
- The result is a new Series of numbers, which we assign to a new column `"animal_code"`.
- `map()` is like using a phone book — you look up a name and get a number back.

**Output:**

```
Original DataFrame:
          food  ounces  animal
0        bacon     4.0     pig
1  pulled pork     3.0     pig
2        bacon    12.0     pig
3     Pastrami     6.0     cow
4  corned beef     7.5     cow
5        Bacon     8.0     pig
6     pastrami     3.0     cow
7    honey ham     5.0     pig
8     nova lox     6.0  salmon

After mapping animals to codes:
          food  ounces  animal  animal_code
0        bacon     4.0     pig            1
1  pulled pork     3.0     pig            1
2        bacon    12.0     pig            1
3     Pastrami     6.0     cow            2
4  corned beef     7.5     cow            2
5        Bacon     8.0     pig            1
6     pastrami     3.0     cow            2
7    honey ham     5.0     pig            1
8     nova lox     6.0  salmon            3
```

---

### Mapping with a Function

Instead of a dictionary, you can pass a function to `map()`.

```python
# Create a Series of numbers
s = pd.Series([1, 2, 3, 4, 5])

# Map each number to its square
squared = s.map(lambda x: x ** 2)
print("Original:", s.tolist())
print("Squared:", squared.tolist())

# Or use a named function
def add_ten(x):
    return x + 10

s_plus_ten = s.map(add_ten)
print("Plus ten:", s_plus_ten.tolist())
```

**Detailed Explanation for Beginners:**

- `lambda x: x ** 2` is a **lambda function** — a small, unnamed function that takes `x` and returns `x` squared.
- `.map()` applies this function to **every single value** in the Series.
- `1` → `1`, `2` → `4`, `3` → `9`, etc.
- You can also define a regular function (like `add_ten`) and pass it to `map()`.
- This is useful when the transformation is too complex for a simple dictionary lookup.

---

### Handling Unmapped Values (NaN)

If a value in your Series is **not found** in the dictionary, it becomes `NaN` (missing).

```python
s = pd.Series(["apple", "banana", "cherry", "date"])

fruit_map = {"apple": "red", "banana": "yellow"}

# 'cherry' and 'date' are NOT in the dictionary
mapped = s.map(fruit_map)
print(mapped)
```

**Output:**

```
0       red
1    yellow
2       NaN
3       NaN
dtype: object
```

**Detailed Explanation for Beginners:**

- `"apple"` is in the dictionary → becomes `"red"`.
- `"banana"` is in the dictionary → becomes `"yellow"`.
- `"cherry"` and `"date"` are **not** in the dictionary → they become `NaN` (Not a Number / missing value).
- **Important:** `map()` does NOT keep the original value if it's not found — it replaces it with `NaN`.
- If you want to keep original values for unmapped items, use `.replace()` instead, or fill NaN afterward with `.fillna()`.

```python
# Keep original values for unmapped items
mapped_with_fallback = s.map(fruit_map).fillna(s)
print(mapped_with_fallback)
```

---

## The `replace()` Method

### Replacing Single Values

`replace()` substitutes one or more values with new values, and **keeps unmapped values unchanged** (unlike `map()`).

```python
s = pd.Series([1, -999, 2, -999, -1000, 3])

# Replace -999 with NaN (common for missing data codes)
s_replaced = s.replace(-999, np.nan)
print("Original:", s.tolist())
print("Replaced:", s_replaced.tolist())
```

**Detailed Explanation for Beginners:**

- In many datasets, `-999` is used as a code for "missing data" (because early databases couldn't store empty values).
- `.replace(-999, np.nan)` finds every `-999` and changes it to `NaN` (pandas' way of saying "empty").
- Unlike `map()`, the values `1`, `2`, `-1000`, and `3` are **left alone** because they weren't specified for replacement.
- This is like using Find & Replace in Microsoft Word — it only changes what you tell it to change.

**Output:**

```
Original: [1, -999, 2, -999, -1000, 3]
Replaced: [1.0, nan, 2.0, nan, -1000.0, 3.0]
```

---

### Replacing Multiple Values

You can replace multiple values at once using lists or a dictionary.

```python
s = pd.Series([1, -999, 2, -999, -1000, 3])

# Method 1: Replace multiple values with the same replacement
s_replaced = s.replace([-999, -1000], np.nan)
print("Multiple replaced with NaN:", s_replaced.tolist())

# Method 2: Replace different values with different replacements
s_replaced2 = s.replace({-999: np.nan, -1000: 0})
print("Different replacements:", s_replaced2.tolist())
```

**Detailed Explanation for Beginners:**

- Method 1: Pass a **list** of values to find, and a single replacement value. Both `-999` and `-1000` become `NaN`.
- Method 2: Pass a **dictionary** where keys are values to find, and values are what to replace them with.
  - `-999` → `NaN`
  - `-1000` → `0`
- The dictionary approach is more flexible when different values need different replacements.

---

### Replacing Values in a DataFrame

`replace()` works on entire DataFrames too, not just Series.

```python
df = pd.DataFrame({
    "A": [1, -999, 3],
    "B": [-999, 2, -1000],
    "C": [4, 5, 6]
})

print("Original DataFrame:")
print(df)

# Replace -999 and -1000 with NaN across the entire DataFrame
df_clean = df.replace([-999, -1000], np.nan)
print("
After replacement:")
print(df_clean)
```

**Detailed Explanation for Beginners:**

- When called on a DataFrame, `replace()` scans **every single cell** in the entire table.
- Any cell containing `-999` or `-1000` gets replaced with `NaN`.
- Values like `1`, `2`, `3`, `4`, `5`, `6` are untouched.
- This is perfect for cleaning datasets where missing data is coded as specific numbers across all columns.

**Output:**

```
Original DataFrame:
     A      B  C
0    1   -999  4
1 -999      2  5
2    3  -1000  6

After replacement:
     A    B  C
0  1.0  NaN  4
1  NaN  2.0  5
2  3.0  NaN  6
```

---

### Using Regular Expressions with Replace

You can use `regex=True` to match patterns, not just exact values.

```python
df = pd.DataFrame({
    "name": ["Mr. John", "Ms. Sarah", "Dr. Mike", "Mrs. Emma"]
})

# Remove titles using regex
df["name_clean"] = df["name"].replace(r"^(Mr\.|Ms\.|Mrs\.|Dr\.)\s*", "", regex=True)
print(df)
```

**Detailed Explanation for Beginners:**

- `regex=True` tells pandas to treat the first argument as a **regular expression pattern**, not a literal string.
- The pattern `r"^(Mr\.|Ms\.|Mrs\.|Dr\.)\s*"` means:
  - `^` = start of the string
  - `(Mr\.|Ms\.|Mrs\.|Dr\.)` = match any of these titles
  - `\s*` = any spaces after the title
- The replacement is `""` (empty string), so the titles are removed.
- **Warning:** Regular expressions are powerful but tricky. Test your pattern carefully!

---

## The `apply()` Method

### Applying a Function to a Series (Column)

`apply()` calls a function on each **value** in a Series, similar to `map()` but more flexible.

```python
s = pd.Series([1, 2, 3, 4, 5])

# Apply a lambda function
doubled = s.apply(lambda x: x * 2)
print("Doubled:", doubled.tolist())

# Apply a more complex function
def categorize(x):
    if x < 3:
        return "low"
    elif x < 5:
        return "medium"
    else:
        return "high"

categorized = s.apply(categorize)
print("Categorized:", categorized.tolist())
```

**Detailed Explanation for Beginners:**

- `apply()` on a Series works very similarly to `map()` with a function.
- The key difference: `apply()` is more general-purpose and can handle functions that use **conditional logic** (if/else statements).
- In the example above, each number is checked: less than 3 → `"low"`, less than 5 → `"medium"`, otherwise → `"high"`.
- `apply()` is like giving a set of instructions to a worker who processes each item one by one.

---

### Applying a Function to a DataFrame (Row-wise or Column-wise)

This is where `apply()` really shines — it can process entire rows or columns at once!

```python
df = pd.DataFrame({
    "math": [85, 90, 78, 92],
    "science": [88, 85, 90, 78],
    "english": [82, 88, 85, 90]
}, index=["Alice", "Bob", "Charlie", "David"])

print("Original:")
print(df)

# Apply along axis=0 (columns) — calculate mean of each column
col_means = df.apply(lambda col: col.mean())
print("
Column means:")
print(col_means)

# Apply along axis=1 (rows) — calculate mean of each row
row_means = df.apply(lambda row: row.mean(), axis=1)
print("
Row means (student averages):")
print(row_means)
```

**Detailed Explanation for Beginners:**

- When `apply()` is used on a DataFrame, it processes either **columns** or **rows** as a whole.
- `axis=0` (default): The function receives each **column** as a Series. `col.mean()` calculates the average of each subject across all students.
- `axis=1`: The function receives each **row** as a Series. `row.mean()` calculates the average of all subjects for each student.
- Think of `axis=0` as looking **down** each column, and `axis=1` as looking **across** each row.
- This is incredibly powerful for creating summary statistics or custom calculations per row/column.

**Output:**

```
Original:
         math  science  english
Alice      85       88       82
Bob        90       85       88
Charlie    78       90       85
David      92       78       90

Column means:
math       86.25
science    85.25
english    86.25
dtype: float64

Row means (student averages):
Alice      85.000000
Bob        87.666667
Charlie    84.333333
David      86.666667
dtype: float64
```

---

### Using Lambda Functions with Apply

Lambda functions are short, inline functions perfect for quick transformations.

```python
df = pd.DataFrame({
    "price": [100, 200, 300],
    "quantity": [2, 3, 1]
})

# Calculate total revenue per row using a lambda
df["total"] = df.apply(lambda row: row["price"] * row["quantity"], axis=1)
print(df)
```

**Detailed Explanation for Beginners:**

- `lambda row: row["price"] * row["quantity"]` is a function that:
  1. Receives a row (which is like a small Series with column names as labels)
  2. Accesses the `"price"` and `"quantity"` values from that row
  3. Multiplies them and returns the result
- `axis=1` is **critical** here — without it, pandas would try to pass columns instead of rows, and the code would fail.
- This is how you create calculated columns that depend on multiple other columns.

**Output:**

```
   price  quantity  total
0    100         2    200
1    200         3    600
2    300         1    300
```

---

### Apply vs Vectorized Operations

**Important:** `apply()` loops over data in Python, which is **slow**. For simple math, use vectorized operations instead.

```python
df = pd.DataFrame({
    "A": [1, 2, 3, 4, 5],
    "B": [10, 20, 30, 40, 50]
})

# SLOW way: using apply
# df["C"] = df.apply(lambda row: row["A"] + row["B"], axis=1)

# FAST way: vectorized operation (uses C under the hood)
df["C"] = df["A"] + df["B"]
print(df)
```

**Detailed Explanation for Beginners:**

- **Vectorized operations** (like `df["A"] + df["B"]`) are written in C (a fast programming language) and operate on entire columns at once.
- **`apply()`** calls Python code for each row, which is much slower — sometimes 10x to 100x slower!
- **Rule of thumb:** If you can do it with basic math (`+`, `-`, `*`, `/`, `**`) or built-in pandas methods, do that instead of `apply()`.
- Use `apply()` only when you need **complex logic** that can't be expressed with simple operations.

---

## The `applymap()` Method

### Applying a Function Element-wise to a DataFrame

`applymap()` applies a function to **every single element** (cell) in a DataFrame.

```python
df = pd.DataFrame({
    "A": [1.25, 2.50, 3.75],
    "B": [4.10, 5.20, 6.30]
})

print("Original:")
print(df)

# Format each number to 1 decimal place
formatted = df.applymap(lambda x: f"{x:.1f}")
print("
Formatted to 1 decimal:")
print(formatted)

# Check if each value is greater than 3
greater_than_3 = df.applymap(lambda x: x > 3)
print("
Is each value > 3?")
print(greater_than_3)
```

**Detailed Explanation for Beginners:**

- `applymap()` visits **every cell** in the DataFrame one by one.
- `lambda x: f"{x:.1f}"` formats each number to show 1 decimal place.
- `lambda x: x > 3` checks each value and returns `True` or `False`.
- Unlike `apply()`, `applymap()` does NOT have an `axis` parameter — it always works element by element.
- **Use case:** Formatting, rounding, or type-checking every cell in a table.

**Output:**

```
Original:
      A     B
0  1.25  4.10
1  2.50  5.20
2  3.75  6.30

Formatted to 1 decimal:
     A    B
0  1.2  4.1
1  2.5  5.2
2  3.8  6.3

Is each value > 3?
       A     B
0  False  True
1  False  True
2   True  True
```

---

### When to Use applymap vs apply

```python
df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6]
})

# applymap: element-wise (each cell individually)
print("applymap (element-wise):")
print(df.applymap(lambda x: x ** 2))

# apply on axis=0: column-wise (each column as a Series)
print("
apply axis=0 (column-wise):")
print(df.apply(lambda col: col.sum()))

# apply on axis=1: row-wise (each row as a Series)
print("
apply axis=1 (row-wise):")
print(df.apply(lambda row: row.sum(), axis=1))
```

**Detailed Explanation for Beginners:**

| Method          | Scope                  | Example Result                                       |
| --------------- | ---------------------- | ---------------------------------------------------- |
| `applymap()`    | Each individual cell   | `1→1`, `2→4`, `3→9` (every cell squared)             |
| `apply(axis=0)` | Each column as a group | `A: 6`, `B: 15` (sum of each column)                 |
| `apply(axis=1)` | Each row as a group    | `Row 0: 5`, `Row 1: 7`, `Row 2: 9` (sum of each row) |

- Use `applymap()` when you need to transform **each value independently**.
- Use `apply()` when you need to perform a calculation using **multiple values** from a row or column.

---

## Quick Comparison Table

| Method                          | Input            | Output    | Keeps Unmapped?    | Best For                           |
| ------------------------------- | ---------------- | --------- | ------------------ | ---------------------------------- |
| `Series.map(dict)`              | Series           | Series    | No → NaN           | Lookup tables, encoding categories |
| `Series.map(func)`              | Series           | Series    | Yes (func decides) | Simple value transformations       |
| `Series.replace()`              | Series/DataFrame | Same type | Yes                | Cleaning data, fixing typos        |
| `Series.apply(func)`            | Series           | Series    | Yes                | Complex logic per value            |
| `DataFrame.apply(func, axis=0)` | DataFrame        | Series    | Yes                | Column-wise aggregations           |
| `DataFrame.apply(func, axis=1)` | DataFrame        | Series    | Yes                | Row-wise calculations              |
| `DataFrame.applymap(func)`      | DataFrame        | DataFrame | Yes                | Cell-by-cell formatting            |

---

## Practical Company Use Cases

### 1. **Retail: Product Category Encoding with `map()`**

**Scenario:** A retail company needs to convert product category names into numeric codes for machine learning models.

```python
products = pd.DataFrame({
    "product_id": ["P001", "P002", "P003", "P004", "P005"],
    "product_name": ["T-Shirt", "Laptop", "Sneakers", "Coffee Maker", "Jeans"],
    "category": ["Clothing", "Electronics", "Footwear", "Appliances", "Clothing"]
})

# Map categories to numeric codes for ML models
category_map = {
    "Clothing": 1,
    "Electronics": 2,
    "Footwear": 3,
    "Appliances": 4
}

products["category_code"] = products["category"].map(category_map)
print(products[["product_name", "category", "category_code"]])
```

**Business Value:**

- Machine learning algorithms require numeric inputs, not text.
- `map()` provides a clean, readable way to encode categorical variables.
- The mapping dictionary serves as documentation — anyone can see what number represents what category.

---

### 2. **Healthcare: Cleaning Patient Data with `replace()`**

**Scenario:** A hospital receives patient data where missing values are coded as `-1` and unknown values as `"UNK"`. These need to be standardized to `NaN`.

```python
patients = pd.DataFrame({
    "patient_id": ["P001", "P002", "P003", "P004", "P005"],
    "age": [45, -1, 32, 58, -1],
    "blood_pressure": ["120/80", "UNK", "140/90", "UNK", "110/70"],
    "cholesterol": [200, 180, -1, 220, 190]
})

print("Before cleaning:")
print(patients)

# Replace -1 and "UNK" with NaN across the entire DataFrame
patients_clean = patients.replace([-1, "UNK"], pd.NA)
print("
After cleaning:")
print(patients_clean)
```

**Business Value:**

- Standardizes missing data representation for consistent analysis.
- Prevents `-1` from being treated as a real age in statistical calculations.
- Ensures data quality before feeding into diagnostic algorithms or reports.

---

### 3. **Finance: Calculating Risk Scores with `apply()`**

**Scenario:** A bank needs to calculate a custom risk score for each loan applicant based on multiple factors.

```python
applicants = pd.DataFrame({
    "applicant_id": ["A001", "A002", "A003", "A004", "A005"],
    "credit_score": [720, 680, 750, 620, 700],
    "income": [75000, 52000, 95000, 45000, 60000],
    "debt": [15000, 25000, 10000, 35000, 18000],
    "employment_years": [5, 2, 8, 1, 4]
})

# Custom risk scoring function
def calculate_risk_score(row):
    # Lower credit score = higher risk
    credit_risk = max(0, (850 - row["credit_score"]) / 850 * 40)

    # Higher debt-to-income = higher risk
    dti = row["debt"] / row["income"]
    dti_risk = min(40, dti * 100)

    # Less employment history = higher risk
    employment_risk = max(0, (10 - row["employment_years"]) / 10 * 20)

    total_risk = credit_risk + dti_risk + employment_risk
    return round(total_risk, 2)

# Apply the function row-wise
applicants["risk_score"] = applicants.apply(calculate_risk_score, axis=1)

# Categorize risk level
applicants["risk_level"] = applicants["risk_score"].apply(
    lambda x: "High" if x > 50 else "Medium" if x > 25 else "Low"
)

print(applicants[["applicant_id", "risk_score", "risk_level"]].sort_values("risk_score", ascending=False))
```

**Business Value:**

- Automates loan risk assessment using a custom formula.
- `apply()` allows complex, multi-column logic that can't be expressed with simple math.
- Risk levels help loan officers prioritize applications and set interest rates.

---

### 4. **E-Commerce: Formatting Prices with `applymap()`**

**Scenario:** An e-commerce platform needs to format all prices in a product catalog for display on the website.

```python
products = pd.DataFrame({
    "product": ["Widget A", "Widget B", "Widget C"],
    "cost_price": [12.50, 25.00, 8.75],
    "sale_price": [19.99, 39.99, 14.99],
    "profit_margin": [0.37, 0.38, 0.42]
})

print("Original:")
print(products)

# Format all numeric values: prices as currency, margins as percentages
formatted = products.copy()
formatted[["cost_price", "sale_price"]] = products[["cost_price", "sale_price"]].applymap(lambda x: f"${x:.2f}")
formatted["profit_margin"] = products["profit_margin"].apply(lambda x: f"{x:.0%}")

print("
Formatted for display:")
print(formatted)
```

**Business Value:**

- `applymap()` formats every price cell consistently across the catalog.
- Prepares data for direct export to web pages, reports, or Excel sheets.
- Ensures professional presentation of financial data to customers and stakeholders.

---

### 5. **HR: Salary Band Classification with `map()` and `apply()`**

**Scenario:** An HR department needs to classify employees into salary bands and calculate bonus eligibility.

```python
employees = pd.DataFrame({
    "employee_id": ["E001", "E002", "E003", "E004", "E005"],
    "department": ["Engineering", "Sales", "HR", "Engineering", "Sales"],
    "salary": [95000, 75000, 55000, 110000, 82000],
    "performance_rating": [4.5, 3.8, 4.2, 4.8, 3.5],
    "years_at_company": [3, 5, 2, 7, 1]
})

# Map departments to department codes
dept_codes = {"Engineering": "ENG", "Sales": "SAL", "HR": "HRM"}
employees["dept_code"] = employees["department"].map(dept_codes)

# Classify salary into bands using apply
employees["salary_band"] = employees["salary"].apply(
    lambda s: "Band A" if s >= 100000 else "Band B" if s >= 70000 else "Band C"
)

# Calculate bonus using row-wise apply (based on multiple factors)
def calculate_bonus(row):
    base_bonus = row["salary"] * 0.05
    performance_multiplier = row["performance_rating"] / 5.0
    tenure_bonus = row["years_at_company"] * 500
    return round(base_bonus * performance_multiplier + tenure_bonus, 2)

employees["bonus"] = employees.apply(calculate_bonus, axis=1)

print(employees[["employee_id", "dept_code", "salary_band", "bonus"]])
```

**Business Value:**

- `map()` standardizes department names into short codes for reporting systems.
- `apply()` on a single column creates salary bands for compensation analysis.
- `apply()` on rows calculates bonuses using a complex, multi-factor formula.
- Enables automated payroll processing and compensation benchmarking.

---

## Summary Cheat Sheet

| Task                                            | Method                                                  | Example                                     |
| ----------------------------------------------- | ------------------------------------------------------- | ------------------------------------------- |
| Convert categories to codes                     | `Series.map(dict)`                                      | `df["cat"].map({"A": 1, "B": 2})`           |
| Transform each value with a function            | `Series.map(func)` or `Series.apply(func)`              | `s.map(lambda x: x*2)`                      |
| Replace specific values                         | `Series.replace(old, new)`                              | `s.replace(-999, np.nan)`                   |
| Replace multiple values at once                 | `Series.replace([a, b], c)` or `Series.replace({a: b})` | `s.replace({"old": "new"})`                 |
| Clean missing data codes across DataFrame       | `DataFrame.replace([codes], np.nan)`                    | `df.replace([-1, -999], np.nan)`            |
| Calculate per-row values using multiple columns | `DataFrame.apply(func, axis=1)`                         | `df.apply(lambda r: r["a"]+r["b"], axis=1)` |
| Aggregate per-column values                     | `DataFrame.apply(func, axis=0)`                         | `df.apply(lambda c: c.mean())`              |
| Format every cell in a DataFrame                | `DataFrame.applymap(func)`                              | `df.applymap(lambda x: f"{x:.2f}")`         |

---

## Key Takeaways for Beginners

1. **`map()`** is best for **lookup transformations** (dictionary-based). It replaces values NOT found in the dictionary with `NaN`.
2. **`replace()`** is best for **cleaning data** (fixing typos, standardizing missing value codes). It leaves unmatched values alone.
3. **`apply()`** on a Series = transform each value (like `map()`). On a DataFrame = process entire rows or columns.
4. **`applymap()`** touches every single cell. Use it for formatting or type conversion, not for math.
5. **Performance matters:** For simple math, use vectorized operations (`df["A"] + df["B"]`) instead of `apply()` — it's 10-100x faster.
6. **`axis=1`** means "across the row" (left to right). **`axis=0`** means "down the column" (top to bottom). This is the #1 source of confusion!
7. When using `apply()` with a lambda on rows, always remember to reference columns by name: `row["column_name"]`.

---

_Happy Learning! Practice these methods with real datasets to build intuition for when to use each one._

## Adding Columns in Pandas: `map()`, `replace()`, `apply()`, and `applymap()`

### 1. `map()` — Element-wise Mapping Using a Dictionary or Function

**Best for:** Converting categorical values to other values (e.g., encoding labels, mapping codes to names).

```python
import pandas as pd

df = pd.DataFrame({
    'department_code': ['HR', 'FIN', 'IT', 'OPS', 'HR']
})

# Using a dictionary
dept_map = {'HR': 'Human Resources', 'FIN': 'Finance', 'IT': 'Information Tech', 'OPS': 'Operations'}
df['department_name'] = df['department_code'].map(dept_map)

# Using a function
df['dept_upper'] = df['department_code'].map(lambda x: x.upper())
```

**Practical Use Cases:**

- Converting country codes to full country names
- Mapping product SKUs to product categories
- Encoding gender ('M'/'F' → 'Male'/'Female')
- Converting letter grades to GPA points

**⚠️ Note:** `map()` on a Series returns `NaN` for values not found in the mapping. Use `.fillna()` to handle unmatched values.

---

### 2. `replace()` — Substitute Values (In-place or Copy)

**Best for:** Cleaning data by replacing specific values across the DataFrame or Series.

```python
df = pd.DataFrame({
    'status': ['active', 'inactive', 'pending', 'active', 'banned'],
    'score': [85, -1, 92, -1, 78]
})

# Replace specific values in a column
df['status_clean'] = df['status'].replace({'banned': 'suspended', 'pending': 'under_review'})

# Replace across entire DataFrame (e.g., sentinel values)
df_clean = df.replace(-1, pd.NA)
```

**Practical Use Cases:**

- Standardizing inconsistent entries ('USA', 'U.S.', 'United States' → 'USA')
- Replacing sentinel/missing values (-999, -1, 'N/A') with `NaN`
- Normalizing text casing inconsistencies
- Replacing outdated category labels

**💡 Tip:** `replace()` supports regex when `regex=True` — great for pattern-based cleaning.

---

### 3. `apply()` — Apply a Function Along an Axis

**Best for:** Row-wise or column-wise computations that involve multiple columns.

```python
df = pd.DataFrame({
    'price': [100, 200, 150],
    'tax_rate': [0.08, 0.10, 0.08],
    'discount': [5, 10, 0]
})

# Row-wise operation (axis=1)
df['final_price'] = df.apply(
    lambda row: row['price'] * (1 + row['tax_rate']) - row['discount'],
    axis=1
)

# Column-wise operation (axis=0) — less common for creating new columns
df['price_doubled'] = df['price'].apply(lambda x: x * 2)
```

**Practical Use Cases:**

- Calculating BMI from height and weight columns
- Deriving full names from first + last name columns
- Computing custom scoring formulas across multiple features
- Applying conditional logic too complex for a simple vectorized operation

**⚠️ Performance Warning:** `apply()` with `axis=1` is slower than vectorized operations. Prefer direct arithmetic when possible:

```python
# Faster vectorized alternative
df['final_price_fast'] = df['price'] * (1 + df['tax_rate']) - df['discount']
```

---

### 4. `applymap()` — Element-wise Function on Entire DataFrame

**Best for:** Formatting or transforming all elements in a DataFrame uniformly.

```python
df = pd.DataFrame({
    'A': [1.234, 2.567, 3.891],
    'B': [4.123, 5.678, 6.901]
})

# Format all floats to 2 decimal places
df_rounded = df.applymap(lambda x: round(x, 2))

# Convert all values to strings with a prefix
df_str = df.applymap(lambda x: f"val_{x}")
```

**Practical Use Cases:**

- Rounding all numeric values in a DataFrame
- Adding currency symbols to all monetary columns
- Converting all values to strings for export
- Applying string methods (strip, lower) across mixed text columns

**⚠️ Note:** `applymap()` operates on the entire DataFrame. For a single column, use `Series.map()` or `Series.apply()` instead.

---

### Quick Comparison Table

| Method       | Scope                                   | Input            | Best For                         |
| ------------ | --------------------------------------- | ---------------- | -------------------------------- |
| `map()`      | Single Series                           | dict/function    | Label encoding, category mapping |
| `replace()`  | Series/DataFrame                        | dict/list/scalar | Cleaning, standardizing values   |
| `apply()`    | Series (element) or DataFrame (row/col) | function         | Complex row-wise calculations    |
| `applymap()` | Entire DataFrame                        | function         | Uniform formatting of all cells  |

---

### Pro Tips

1. **Vectorization First:** Always try vectorized operations before `apply()`. `df['c'] = df['a'] + df['b']` is 10-100x faster than `df.apply(lambda row: row['a'] + row['b'], axis=1)`.

2. **Handling Missing Mappings:** Use `.map(d).fillna('Unknown')` to avoid silent `NaN` insertion.

3. **Chaining:** These methods work great in method chains:

   ```python
   df.assign(
       dept_name=lambda d: d['code'].map(dept_map),
       status_clean=lambda d: d['status'].replace({'x': 'y'})
   )
   ```

4. **Type Safety:** `apply()` can infer return types poorly. Explicitly specify `dtype` when creating the new column if needed.
