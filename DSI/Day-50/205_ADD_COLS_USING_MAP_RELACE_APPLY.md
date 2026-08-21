# Day 50 — Adding & Dropping Columns Using `map`, `replace`, `apply`, and `applymap`

> **File:** `205_Map_Replace_Apply_ApplyMap.py`  
> **Dataset:** `grocery_database.xlsx` (sheets: `customer_details`, `product_areas`)  
> **Goal:** Learn how to transform, replace, and calculate new columns in pandas.

---

## Table of Contents

1. [Setup & Data Loading](#setup--data-loading)
2. [`map()` — Transforming Series Values](#map--transforming-series-values)
3. [`replace()` — Substituting Values While Preserving Others](#replace--substituting-values-while-preserving-others)
4. [`apply()` — Calling Functions on Series & DataFrames](#apply--calling-functions-on-series--dataframes)
5. [`applymap()` — Element-wise DataFrame Operations](#applymap--element-wise-dataframe-operations)
6. [Side-by-Side Comparison](#side-by-side-comparison)
7. [Practical Company Use Cases](#practical-company-use-cases)
8. [Common Mistakes & Tips](#common-mistakes--tips)

---

## Setup & Data Loading

```python
# -*- coding: utf-8 -*-
```

**Explanation:** This tells Python that the file can contain special characters (like accented letters). It's good practice but not strictly necessary in Python 3.

```python
import pandas as pd
```

**Explanation:** We import the **pandas** library and nickname it `pd`. This is the industry standard nickname. Pandas is the main tool we use for data tables in Python.

```python
customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")
product_areas = pd.read_excel("grocery_database.xlsx", sheet_name="product_areas")
```

**Explanation:**

- `pd.read_excel()` reads an Excel file into a pandas DataFrame (a table).
- `"grocery_database.xlsx"` is the name of the Excel file.
- `sheet_name="customer_details"` tells pandas which tab (sheet) inside the Excel file to read.
- We load **two** sheets into two separate DataFrames:
  - `customer_details` — likely contains info about customers (name, gender, distance from store, credit score, etc.)
  - `product_areas` — likely contains info about product categories (name, profit margin, etc.)

> **Beginner Tip:** Think of an Excel file as a binder with multiple sheets. `pd.read_excel()` lets you pick which sheet to work with.

---

## `map()` — Transforming Series Values

### What is `map()`?

`map()` is used on a **single column** (called a Series in pandas) to transform each value into something else using a **dictionary** as a lookup table.

### Code 1: Mapping Gender to Numbers

```python
customer_details["gender_numeric"] = customer_details["gender"].map({"M" : 0, "F" : 1})
```

**Line-by-Line Explanation:**

1. `customer_details["gender"]` — selects the `"gender"` column from the `customer_details` DataFrame. This is a **Series** (a single column of data).
2. `.map({"M" : 0, "F" : 1})` — uses a **dictionary** to transform values:
   - Every `"M"` (Male) becomes `0`
   - Every `"F"` (Female) becomes `1`
3. `customer_details["gender_numeric"] = ...` — creates a **brand new column** called `"gender_numeric"` and stores the transformed values there.

**Why do this?**
Machine learning models and some statistical tools only work with numbers, not text. Converting `"M"`/`"F"` to `0`/`1` makes the data usable for analysis.

**Visual Example:**

| customer_id | gender | →   | gender_numeric |
| ----------- | ------ | --- | -------------- |
| 1           | M      | →   | 0              |
| 2           | F      | →   | 1              |
| 3           | M      | →   | 0              |
| 4           | F      | →   | 1              |

---

### Code 2: Incomplete Mapping — The NaN Trap

```python
customer_details["gender_numeric"] = customer_details["gender"].map({"M" : 0})
```

**Line-by-Line Explanation:**

1. Here, the dictionary only maps `"M"` → `0`.
2. There is **no mapping** for `"F"` (Female).
3. When `map()` encounters a value it doesn't recognize, it replaces it with **`NaN`** (Not a Number), which means "missing data" in pandas.

**What happens to the data?**

| gender | gender_numeric |
| ------ | -------------- |
| M      | 0              |
| F      | NaN            |
| M      | 0              |
| F      | NaN            |

> **⚠️ CRITICAL WARNING:** `map()` is **all-or-nothing**. If a value isn't in your dictionary, it becomes `NaN`. Always check that your dictionary covers ALL possible values in the column, or be prepared to handle NaN values afterward.

---

### Code 3: Map Only Works on Series

```python
# NB: Map is only applicable to the Series Data structure. It will throw error for DF.
```

**Explanation:**

- `map()` can only be used on a **single column** (Series).
- If you try `customer_details.map({...})` on the entire DataFrame, pandas will throw an error.
- This is because `map()` doesn't know which column you want to transform when given multiple columns.

> **Beginner Tip:** If you need to transform multiple columns, use `applymap()` or transform each column individually.

---

## `replace()` — Substituting Values While Preserving Others

### What is `replace()`?

`replace()` is similar to `map()`, but with one big difference: **values not mentioned in the dictionary are left unchanged** (they do NOT become NaN).

### Code 4: Replacing Gender Values

```python
customer_details["gender_numeric"] = customer_details["gender"].replace({"M" : 0, "F" : 1})
```

**Line-by-Line Explanation:**

1. `customer_details["gender"]` — selects the gender column (a Series).
2. `.replace({"M" : 0, "F" : 1})` — uses a dictionary to substitute values:
   - `"M"` → `0`
   - `"F"` → `1`
3. The result is stored in a new column `"gender_numeric"`.

**How is this different from `map()`?**

- If there were an unexpected value like `"U"` (Unknown) in the gender column:
  - `map()` would convert `"U"` → `NaN`
  - `replace()` would keep `"U"` as `"U"`

> **Rule of Thumb:** Use `map()` when you want to **encode** a column (convert all values to a new set). Use `replace()` when you want to **fix specific values** while leaving everything else alone.

---

### Code 5: Incomplete Replace — Safe Behavior

```python
customer_details["gender_numeric"] = customer_details["gender"].replace({"M" : 0})
```

**Line-by-Line Explanation:**

1. The dictionary only says `"M"` → `0`.
2. `"F"` is NOT in the dictionary.
3. Unlike `map()`, `replace()` **leaves `"F"` unchanged** — it stays as `"F"`.

**What happens to the data?**

| gender | gender_numeric |
| ------ | -------------- |
| M      | 0              |
| F      | F              |
| M      | 0              |
| F      | F              |

> **Key Difference:** `replace()` = "change what I tell you to change, leave the rest alone." `map()` = "change everything according to my dictionary, make everything else NaN."

---

## `apply()` — Calling Functions on Series & DataFrames

### What is `apply()`?

`apply()` lets you run a **function** on every value in a Series, or on every row/column in a DataFrame. It's like a factory assembly line — each item goes through a machine (your function) and comes out transformed.

---

### Code 6: Applying a Built-in Function (`len`)

```python
product_areas["product_area_name"].apply(len)
```

**Line-by-Line Explanation:**

1. `product_areas["product_area_name"]` — selects the `product_area_name` column. This might contain values like `"Fresh Food"`, `"Bakery"`, `"Dairy"`, etc.
2. `.apply(len)` — applies Python's built-in `len()` function to **every single value** in that column.
3. `len("Fresh Food")` = 10, `len("Bakery")` = 6, etc.
4. This returns a new Series with the length of each string.

**Why is this useful?**

- You might want to check if product names are too long for a display label.
- You might want to filter out names that exceed a certain character limit.

**Visual Example:**

| product_area_name | →   | length |
| ----------------- | --- | ------ |
| Fresh Food        | →   | 10     |
| Bakery            | →   | 6      |
| Dairy             | →   | 5      |

> **Note:** The result is NOT saved to a new column here. If you want to keep it, you'd write:  
> `product_areas["name_length"] = product_areas["product_area_name"].apply(len)`

---

### Code 7: Custom Function with `apply()`

```python
def update_profit_margin(profit_margins):
    if profit_margins > 0.2:
        return profit_margins * 1.2
    else:
        return profit_margins * 0.8
```

**Line-by-Line Explanation:**

1. We define a **custom function** called `update_profit_margin`.
2. It takes one input: `profit_margins` (a single number).
3. **If** the profit margin is greater than `0.2` (20%):
   - Increase it by 20% (`* 1.2`). This might simulate a successful product getting a bonus markup.
4. **Else** (profit margin is 20% or less):
   - Decrease it by 20% (`* 0.8`). This might simulate a discount or price reduction for low-margin items.

```python
product_areas["profit_margin_updated"] = product_areas["profit_margin"].apply(update_profit_margin)
```

**Line-by-Line Explanation:**

1. `product_areas["profit_margin"]` — selects the profit margin column (e.g., values like `0.15`, `0.25`, `0.30`).
2. `.apply(update_profit_margin)` — runs our custom function on **every single value** in that column.
3. The result is saved to a new column called `"profit_margin_updated"`.

**Visual Example:**

| profit_margin | →   | profit_margin_updated | Reason          |
| ------------- | --- | --------------------- | --------------- |
| 0.15          | →   | 0.12                  | ≤ 0.2, so × 0.8 |
| 0.25          | →   | 0.30                  | > 0.2, so × 1.2 |
| 0.30          | →   | 0.36                  | > 0.2, so × 1.2 |

> **Beginner Tip:** This is a powerful pattern — define your logic in a function, then `apply()` it to an entire column. You can use `if/else`, loops, or any Python logic inside the function.

---

### Code 8: `apply()` on a DataFrame — Column-wise (Default)

```python
x = pd.DataFrame({"A" : [1,2], "B" : [3,4], "C" : [5,6]})
```

**Line-by-Line Explanation:**

1. We create a small DataFrame `x` with 3 columns (`A`, `B`, `C`) and 2 rows.

**The DataFrame looks like this:**

|     | A   | B   | C   |
| --- | --- | --- | --- |
| 0   | 1   | 3   | 5   |
| 1   | 2   | 4   | 6   |

```python
x.apply(max)
```

**Line-by-Line Explanation:**

1. `.apply(max)` applies the `max()` function to the DataFrame.
2. By default, `axis=0`, which means it processes **each column** (top to bottom).
3. For column `A`: `max(1, 2)` = `2`
4. For column `B`: `max(3, 4)` = `4`
5. For column `C`: `max(5, 6)` = `6`

**Result:**

```
A    2
B    4
C    6
dtype: int64
```

> **Beginner Tip:** `axis=0` means "down the columns." Imagine dropping a ball down each column — it travels from top to bottom. That's what `apply()` does when `axis=0`.

---

### Code 9: `apply()` on a DataFrame — Row-wise

```python
x.apply(max, axis=1)
```

**Line-by-Line Explanation:**

1. `.apply(max, axis=1)` applies the `max()` function **across each row** (left to right).
2. `axis=1` tells pandas to process horizontally, not vertically.
3. For row 0: `max(1, 3, 5)` = `5`
4. For row 1: `max(2, 4, 6)` = `6`

**Result:**

```
0    5
1    6
dtype: int64
```

> **Beginner Tip:** `axis=1` means "across the rows." Imagine reading a book left to right — that's what `apply()` does when `axis=1`.

**Memory Trick:**

- `axis=0` = **0** looks like a vertical line ↓ = columns
- `axis=1` = **1** looks like a horizontal line → = rows

---

## `applymap()` — Element-wise DataFrame Operations

### What is `applymap()`?

`applymap()` applies a function to **every single cell** (element) in a DataFrame. Unlike `apply()`, which works on rows or columns as groups, `applymap()` visits each cell individually.

### Code 10: Defining a Function for applymap

```python
def square(n):
    return n ** 2
```

**Line-by-Line Explanation:**

1. We define a function called `square`.
2. It takes a number `n` and returns `n` squared (`n ** 2` means "n to the power of 2").
3. `square(3)` returns `9`, `square(4)` returns `16`, etc.

```python
x.apply(square)
```

**Line-by-Line Explanation:**

1. Wait — this code says `x.apply(square)`, not `x.applymap(square)`!
2. On a DataFrame, `.apply(square)` with `axis=0` (default) passes **each column** as a Series to the `square` function.
3. However, `square()` expects a single number, not a Series. **This would actually raise an error** because you can't square a Series!
4. The **intended code** should be:

```python
x.applymap(square)
```

**Corrected Explanation:**

1. `x.applymap(square)` visits **every single cell** in DataFrame `x`.
2. It applies `square()` to each value individually.
3. `1` → `1`, `2` → `4`, `3` → `9`, `4` → `16`, `5` → `25`, `6` → `36`.

**Result:**

|     | A   | B   | C   |
| --- | --- | --- | --- |
| 0   | 1   | 9   | 25  |
| 1   | 4   | 16  | 36  |

> **⚠️ Important Note:** The original code has `x.apply(square)` which would fail on a DataFrame. The correct method for element-wise operations is `applymap()`. `apply()` is for row/column-wise operations; `applymap()` is for cell-by-cell operations.

---

## Side-by-Side Comparison

| Method       | Works On            | Scope                                              | Unmapped Values | Best For                           |
| ------------ | ------------------- | -------------------------------------------------- | --------------- | ---------------------------------- |
| `map()`      | Series only         | Each value                                         | Become `NaN`    | Encoding categories (M→0, F→1)     |
| `replace()`  | Series or DataFrame | Each value                                         | Stay unchanged  | Cleaning data, fixing typos        |
| `apply()`    | Series or DataFrame | Each value (Series) or each row/column (DataFrame) | Stay unchanged  | Custom calculations, complex logic |
| `applymap()` | DataFrame only      | Each individual cell                               | Stay unchanged  | Formatting, math on every cell     |

---

## Practical Company Use Cases

### Use Case 1: Grocery Store — Customer Gender Encoding for Loyalty Analysis

**Scenario:** A grocery chain wants to analyze shopping patterns by gender but their ML model requires numeric inputs.

```python
# The exact code from the file:
customer_details["gender_numeric"] = customer_details["gender"].map({"M" : 0, "F" : 1})
```

**Business Value:**

- Marketing teams can segment customers by gender for targeted promotions.
- Data science teams can feed the numeric gender into predictive models (e.g., "which gender is more likely to buy organic products?").
- `map()` provides a clean, readable way to document the encoding: `0 = Male`, `1 = Female`.

**What happens if you forget a mapping?**

```python
# DON'T DO THIS — it will make all females NaN!
customer_details["gender_numeric"] = customer_details["gender"].map({"M" : 0})
```

This would destroy your data quality. Always verify your dictionary covers all unique values:

```python
print(customer_details["gender"].unique())  # Check before mapping!
```

---

### Use Case 2: Grocery Store — Cleaning Inconsistent Product Area Names with `replace()`

**Scenario:** The `product_areas` sheet has inconsistent naming — some entries say `"Bakery"`, others say `"bakery"` or `"BAKERY"`. You need to standardize them.

```python
# Standardize various spellings to one correct spelling
product_areas["product_area_name"] = product_areas["product_area_name"].replace({
    "bakery": "Bakery",
    "BAKERY": "Bakery",
    "dairy": "Dairy"
})
```

**Business Value:**

- Ensures reports group "Bakery" sales correctly instead of splitting them across multiple spellings.
- `replace()` is perfect here because you only want to fix specific misspellings — you don't want to turn everything else into NaN (which `map()` would do).
- Inventory managers can trust that their category reports are accurate.

---

### Use Case 3: Grocery Store — Dynamic Profit Margin Adjustment with `apply()`

**Scenario:** The grocery store wants to adjust profit margins based on performance. High-margin areas get a boost; low-margin areas get reduced to remain competitive.

```python
def update_profit_margin(profit_margins):
    if profit_margins > 0.2:
        return profit_margins * 1.2  # High performers get 20% boost
    else:
        return profit_margins * 0.8  # Low performers get 20% reduction

product_areas["profit_margin_updated"] = product_areas["profit_margin"].apply(update_profit_margin)
```

**Business Value:**

- Category managers can simulate pricing strategies before implementing them.
- High-performing areas (like premium organic sections with >20% margin) get increased investment.
- Low-performing areas get price reductions to drive volume and clear shelf space.
- The `apply()` method allows complex business rules (if/else logic) that simple math can't express.

**Visual Example:**

| product_area_name | profit_margin | profit_margin_updated | Action         |
| ----------------- | ------------- | --------------------- | -------------- |
| Fresh Food        | 0.15          | 0.12                  | Reduce price   |
| Organic Produce   | 0.25          | 0.30                  | Increase price |
| Bakery            | 0.18          | 0.144                 | Reduce price   |
| Premium Meats     | 0.30          | 0.36                  | Increase price |

---

### Use Case 4: Grocery Store — Product Name Length Validation with `apply(len)`

**Scenario:** The store's receipt printers can only display 20 characters for product area names. You need to check which names are too long.

```python
name_lengths = product_areas["product_area_name"].apply(len)
print(name_lengths)

# Find names that are too long for receipts
long_names = product_areas[product_areas["product_area_name"].apply(len) > 20]
print(long_names)
```

**Business Value:**

- IT teams can identify product names that will be truncated on receipts.
- Marketing teams can create shorter alternative names for POS systems.
- Prevents customer confusion when "International Specialty Foods" prints as "International Specialty Fo" on a receipt.

---

### Use Case 5: Grocery Store — Bulk Price Calculation with `applymap()`

**Scenario:** The store needs to create a bulk pricing matrix where every price is discounted by 10% for wholesale customers.

```python
# Assume we have a price matrix DataFrame
price_matrix = pd.DataFrame({
    "small": [1.99, 2.49, 3.99],
    "medium": [3.49, 4.99, 6.99],
    "large": [5.99, 7.99, 9.99]
}, index=["Apple", "Banana", "Orange"])

# Apply 10% discount to EVERY price
wholesale_prices = price_matrix.applymap(lambda x: round(x * 0.9, 2))
print(wholesale_prices)
```

**Business Value:**

- `applymap()` efficiently transforms every price in the entire catalog.
- Wholesale buyers get consistent 10% discounts across all products and sizes.
- Pricing analysts can generate multiple pricing tiers (retail, wholesale, VIP) by reusing the same `applymap()` pattern with different multipliers.

---

## Common Mistakes & Tips

### Mistake 1: Using `map()` When You Should Use `replace()`

```python
# BAD: Will turn unexpected values into NaN
customer_details["gender_clean"] = customer_details["gender"].map({"M": "Male", "F": "Female"})
# If there's a "U" for Unknown, it becomes NaN!

# GOOD: Keeps unexpected values as-is
customer_details["gender_clean"] = customer_details["gender"].replace({"M": "Male", "F": "Female"})
# "U" stays as "U" — you can see it and handle it later
```

### Mistake 2: Forgetting `axis=1` for Row-wise Operations

```python
# This finds the max of each COLUMN (default axis=0)
max_per_column = x.apply(max)

# This finds the max of each ROW (must specify axis=1)
max_per_row = x.apply(max, axis=1)
```

### Mistake 3: Using `apply()` Instead of `applymap()` for Element-wise Operations

```python
# This will FAIL on a DataFrame
def square(n):
    return n ** 2
x.apply(square)  # ❌ ERROR — passes entire columns, not single numbers

# This works correctly
x.applymap(square)  # ✅ Passes each cell individually
```

### Tip: Check Unique Values Before Mapping

```python
# Always check what values exist before using map()
print(customer_details["gender"].unique())
# Output: ['M' 'F' 'U']  ← Oh! There's also 'U' for Unknown!

# Now you can include it in your map:
customer_details["gender_numeric"] = customer_details["gender"].map({"M": 0, "F": 1, "U": 2})
```

### Tip: Vectorized Operations Are Faster Than `apply()`

```python
# SLOW — uses Python loop under the hood
product_areas["profit_doubled"] = product_areas["profit_margin"].apply(lambda x: x * 2)

# FAST — uses optimized C code
product_areas["profit_doubled"] = product_areas["profit_margin"] * 2
```

> **Rule of Thumb:** If you can do it with simple math (`+`, `-`, `*`, `/`), do that instead of `apply()`. Use `apply()` only when you need `if/else` logic or complex calculations.

---

## Summary

| Method                        | Syntax                           | Use When                                                                                 |
| ----------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------- |
| `map()`                       | `series.map({"old": "new"})`     | You want to encode/convert ALL values in a column. Remember: unmapped values become NaN! |
| `replace()`                   | `series.replace({"old": "new"})` | You want to fix specific values while leaving the rest untouched.                        |
| `apply()` (Series)            | `series.apply(func)`             | You need custom logic (if/else) for each value in a column.                              |
| `apply()` (DataFrame, axis=0) | `df.apply(func)`                 | You want to aggregate or process each column as a group.                                 |
| `apply()` (DataFrame, axis=1) | `df.apply(func, axis=1)`         | You want to calculate something using multiple columns for each row.                     |
| `applymap()`                  | `df.applymap(func)`              | You want to transform every single cell in a DataFrame individually.                     |

---

_Master these four methods, and you'll be able to transform any dataset to fit your business needs!_
