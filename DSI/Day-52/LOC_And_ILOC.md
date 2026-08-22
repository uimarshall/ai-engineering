# 📊 Pandas: Selecting Rows & Columns with `loc` and `iloc`

## Table of Contents

1. [Introduction](#introduction)
2. [The Difference Between `loc` and `iloc`](#the-difference)
3. [Setting Up Our Data](#setup)
4. [`iloc` - Index-Based Selection](#iloc-section)
5. [`loc` - Label-Based Selection](#loc-section)
6. [Conditional Logic & Filtering](#conditional-logic)
7. [Practical Company Use Cases](#use-cases)
8. [Complete Code with Detailed Explanations](#complete-code)
9. [Common Mistakes to Avoid](#common-mistakes)
10. [Quick Reference Cheat Sheet](#cheat-sheet)

---

## 1. Introduction {#introduction}

When working with real-world data in pandas, you'll often deal with DataFrames containing **thousands or millions of rows** and **dozens of columns**. For any specific analysis task, you rarely need ALL the data — you only need the **relevant rows and columns**.

Think of it like searching through a massive filing cabinet:

- **`iloc`** = "I want the 5th folder from the top" (position-based)
- **`loc`** = "I want the folder labeled 'Customer 642'" (name-based)

> 💡 **Key Insight:** Both methods follow the same pattern: `DataFrame.loc[rows, columns]` and `DataFrame.iloc[rows, columns]`. The first argument always specifies which **rows** you want, and the second (optional) argument specifies which **columns** you want.

---

## 2. The Difference Between `loc` and `iloc` {#the-difference}

| Feature               | `loc`                                 | `iloc`                                             |
| --------------------- | ------------------------------------- | -------------------------------------------------- |
| **Stands for**        | Location (by label)                   | Integer Location (by index position)               |
| **Selection Method**  | Uses **labels/names**                 | Uses **integer positions** (0, 1, 2...)            |
| **Row Selection**     | Row labels (e.g., customer_id values) | Row index positions (e.g., 0, 1, 2)                |
| **Column Selection**  | Column names (e.g., "sales_cost")     | Column index positions (e.g., 0, 1, 2)             |
| **Slicing Behavior**  | **Inclusive** of end point            | **Exclusive** of end point                         |
| **Boolean Filtering** | ✅ Yes                                | ❌ No (use `.iloc` with boolean arrays indirectly) |

> ⚠️ **Important:** `iloc[0:4]` returns rows 0, 1, 2, 3 (4 is EXCLUDED). But `loc[0:4]` returns rows labeled 0, 1, 2, 3, 4 (4 is INCLUDED)!

---

## 3. Setting Up Our Data {#setup}

```python
# Import the pandas library - this is the standard data manipulation library in Python
import pandas as pd

# Import numpy for numerical operations (often used alongside pandas)
import numpy as np

# Load the Excel file into a DataFrame
# "grocery_database.xlsx" is our data file
# sheet_name="transactions" tells pandas which sheet to read from the Excel workbook
# The result is stored in the variable 'transactions'
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# Let's see what our data looks like (this line isn't in the original file but is helpful)
print(transactions.head())
print(transactions.shape)  # Shows (number_of_rows, number_of_columns)
```

**Expected Output:**

```
   transaction_id  customer_id  product_area_id  num_items  sales_cost
0               1          642                1          2        5.99
1               2          700                3          1        2.49
2               3          642                2          5       12.50
3               4          821                1          3        8.75
4               5          642                4          1        3.25

(100, 5)  # 100 rows, 5 columns (example values)
```

---

## 4. `iloc` - Index-Based Selection {#iloc-section}

The **`I`** in `iloc` stands for **Integer/Index**. You select data based on its **numerical position** in the DataFrame, just like Python list indexing.

### 4.1 Selecting a Single Row by Position

```python
# Select the FIRST row (index position 0)
# Python uses 0-based indexing, so 0 = first row, 1 = second row, etc.
transactions.iloc[0]
```

**Expected Output:**

```
transaction_id      1
customer_id       642
product_area_id     1
num_items           2
sales_cost       5.99
Name: 0, dtype: object
```

> 📝 **Explanation:** When you select a single row, pandas returns a **Series** object (a one-dimensional labeled array). The "Name: 0" tells you this Series came from row index 0. Each value is paired with its column name.

---

### 4.2 Selecting Multiple Rows with Slicing

```python
# Select rows from position 0 UP TO (but NOT including) position 4
# This returns rows at positions 0, 1, 2, and 3
# REMEMBER: iloc slicing is EXCLUSIVE of the end point
transactions.iloc[0:4]
```

**Expected Output:**

```
   transaction_id  customer_id  product_area_id  num_items  sales_cost
0               1          642                1          2        5.99
1               2          700                3          1        2.49
2               3          642                2          5       12.50
3               4          821                1          3        8.75
```

> 📝 **Explanation:** Notice that row 4 is NOT included! This is the same behavior as Python list slicing: `my_list[0:4]` gives you elements at indices 0, 1, 2, 3. The result is a **DataFrame** (since multiple rows are selected).

---

### 4.3 Selecting Specific Rows by Index List

```python
# Select rows at positions 0, 30, and 51 ONLY
# We use DOUBLE square brackets [[ ]] to pass a LIST of index positions
# This is like saying: "Give me the 1st, 31st, and 52nd rows"
transactions.iloc[[0, 30, 51]]
```

**Expected Output:**

```
    transaction_id  customer_id  product_area_id  num_items  sales_cost
0                1          642                1          2        5.99
30              31          900                2          4        9.99
51              52          642                3          1        1.99
```

> 📝 **Explanation:** The inner brackets `[0, 30, 51]` create a Python list. The outer brackets `.iloc[...]` pass that list to the indexer. This is useful when you need **non-consecutive rows** — for example, sampling specific records for audit.

---

### 4.4 Selecting Both Rows AND Columns

```python
# Select rows 0 to 3 (positions 0,1,2,3) AND specific columns by position
# Column positions: 0 = transaction_id, 3 = num_items, -1 = last column (sales_cost)
# Negative indexing (-1) means "count from the end" - very useful for large DataFrames!
transactions.iloc[0:4, [0, 3, -1]]
```

**Expected Output:**

```
   transaction_id  num_items  sales_cost
0               1          2        5.99
1               2          1        2.49
2               3          5       12.50
3               4          3        8.75
```

> 📝 **Explanation:** Now we're using **both dimensions** of `iloc`:
>
> - First argument `0:4` = rows at positions 0, 1, 2, 3
> - Second argument `[0, 3, -1]` = columns at positions 0, 3, and the last one (-1)
>
> The comma separates "what rows I want" from "what columns I want."

---

### 4.5 Selecting ALL Rows with Specific Columns

```python
# The colon (:) by itself means "select ALL rows"
# This is useful when you want specific columns but ALL rows
transactions.iloc[:, [0, 3, -1]]
```

**Expected Output:**

```
     transaction_id  num_items  sales_cost
0                 1          2        5.99
1                 2          1        2.49
2                 3          5       12.50
3                 4          3        8.75
4                 5          1        3.25
..              ...        ...         ...
95               96          2        4.50
96               97          1        1.99
97               98          3        7.25
98               99          4       10.00
99              100          2        5.50

[100 rows x 3 columns]
```

> 📝 **Explanation:** `:` is Python's "slice everything" operator. When used alone, it means "give me everything in this dimension." This is perfect when you need to extract a subset of columns (like creating a summary report) while keeping all rows.

---

## 5. `loc` - Label-Based Selection {#loc-section}

`loc` uses **labels/names** instead of numbers. If your row index has meaningful labels (like customer IDs), `loc` becomes incredibly intuitive.

### 5.1 Selecting a Single Row by Default Index

```python
# When you first load data, pandas automatically assigns a default index: 0, 1, 2, 3...
# So initially, the row labels ARE the same as the row positions
# This selects the row with LABEL 0 (which happens to be the first row)
transactions.loc[0]
```

**Expected Output:**

```
transaction_id      1
customer_id       642
product_area_id     1
num_items           2
sales_cost       5.99
Name: 0, dtype: object
```

> 📝 **Explanation:** Right now, `loc[0]` and `iloc[0]` give the same result because the default index labels (0, 1, 2...) match the positions. But this changes once we set a custom index!

---

### 5.2 Setting a Custom Index

```python
# Change the row index from default numbers (0, 1, 2...) to the 'customer_id' column values
# inplace=True means "modify the original DataFrame" instead of creating a copy
# Now each row is labeled by its customer_id instead of 0, 1, 2...
transactions.set_index("customer_id", inplace=True)
```

**Expected Output (showing the index change):**

```
Before:                    After:
   transaction_id...           transaction_id...
0              1           642              1
1              2           700              2
2              3           642              3
```

> 📝 **Explanation:** `set_index()` transforms a column into the DataFrame's index (row labels). Now instead of saying "give me row 0," you can say "give me the row for customer 642." The `inplace=True` parameter is memory-efficient because it modifies the existing DataFrame rather than creating a new one.

---

### 5.3 Selecting Rows by Custom Index Label

```python
# Now that customer_id is our index, we can select ALL rows for customer 642
# This returns ALL transactions made by customer 642
transactions.loc[642]
```

**Expected Output:**

```
            transaction_id  product_area_id  num_items  sales_cost
customer_id
642                      1                1          2        5.99
642                      3                2          5       12.50
642                      8                4          1        3.25
642                     15                1          3        8.50
```

> 📝 **Explanation:** This is where `loc` shines! Instead of remembering that customer 642 is at row position 0 (and maybe other positions too), you simply use their ID. Notice that customer 642 appears **multiple times** (they made multiple transactions), so `loc` returns ALL matching rows.

---

### 5.4 Resetting the Index

```python
# Convert the index back into a regular column
# This undoes the set_index() operation
# customer_id becomes a normal column again, and the default numeric index (0, 1, 2...) returns
transactions.reset_index(inplace=True)
```

**Expected Output:**

```
   customer_id  transaction_id  product_area_id  num_items  sales_cost
0          642               1                1          2        5.99
1          700               2                3          1        2.49
2          642               3                2          5       12.50
```

> 📝 **Explanation:** `reset_index()` is the opposite of `set_index()`. It turns the current index back into a regular column and restores the default 0-based numeric index. You typically do this when you're done with label-based operations and want to return to the standard format.

---

### 5.5 Viewing Column Names

```python
# Convert the column names into a Python list
# This is helpful to see exactly what columns exist, especially in large DataFrames
# You can copy-paste these names into your loc[] selections
list(transactions)
```

**Expected Output:**

```
['customer_id', 'transaction_id', 'product_area_id', 'num_items', 'sales_cost']
```

> 📝 **Alternative:** You can also use `transactions.columns` to see column names, but `list(transactions)` converts them to a plain Python list that's easier to work with programmatically.

---

### 5.6 Selecting Rows and a Single Column

```python
# Select rows with labels 0 through 10 (INCLUSIVE of 10!)
# AND only the 'customer_id' column
# REMEMBER: loc slicing is INCLUSIVE of both endpoints
transactions.loc[0:10, "customer_id"]
```

**Expected Output:**

```
0     642
1     700
2     642
3     821
4     642
5     900
6     700
7     821
8     642
9     900
10    700
Name: customer_id, dtype: int64
```

> 📝 **Explanation:** Notice the difference from `iloc`! `loc[0:10]` includes row 10. Also notice we use the **column name** `"customer_id"` instead of its position. The result is a Series (single column of data).

---

### 5.7 Selecting Rows and Multiple Columns

```python
# Select rows 0 through 10 (inclusive)
# AND only these three specific columns, in this exact order
transactions.loc[0:10, ["customer_id", "product_area_id", "sales_cost"]]
```

**Expected Output:**

```
    customer_id  product_area_id  sales_cost
0           642                1        5.99
1           700                3        2.49
2           642                2       12.50
3           821                1        8.75
4           642                4        3.25
5           900                2        9.99
6           700                3        1.99
7           821                4        7.25
8           642                1        4.50
9           900                2       10.00
10          700                3        5.50
```

> 📝 **Explanation:** Pass a **list of column names** as the second argument. The columns appear in the order you specify them. This is incredibly useful for creating reports with columns in a specific order.

---

### 5.8 Reordering Columns

```python
# Select the same rows, but REORDER the columns
# sales_cost appears FIRST, then customer_id, then product_area_id
# The original DataFrame is NOT modified - this just returns a new view
transactions.loc[0:10, ["sales_cost", "customer_id", "product_area_id"]]
```

**Expected Output:**

```
    sales_cost  customer_id  product_area_id
0        5.99          642                1
1        2.49          700                3
2       12.50          642                2
3        8.75          821                1
4        3.25          642                4
5        9.99          900                2
6        1.99          700                3
7        7.25          821                4
8        4.50          642                1
9       10.00          900                2
10       5.50          700                3
```

> 📝 **Explanation:** `loc` doesn't just filter columns — it lets you **reorder them**! This is perfect for creating presentation-ready DataFrames where the most important column (like sales_cost) should appear first in a report.

---

## 6. Conditional Logic & Filtering {#conditional-logic}

This is where pandas becomes truly powerful. You can select rows based on **conditions** (rules) rather than specific positions or labels.

### 6.1 Creating a Boolean Mask

```python
# Check which rows have customer_id equal to 642
# This returns a Series of True/False values (a Boolean mask)
# True = this row meets the condition, False = it doesn't
transactions["customer_id"] == 642
```

**Expected Output:**

```
0      True      # Row 0: customer_id is 642 ✓
1     False      # Row 1: customer_id is 700 ✗
2      True      # Row 2: customer_id is 642 ✓
3     False      # Row 3: customer_id is 821 ✗
4      True      # Row 4: customer_id is 642 ✓
      ...
95    False
96     True
97    False
98    False
99    False
Name: customer_id, Length: 100, dtype: bool
```

> 📝 **Explanation:** A **Boolean mask** is like a filter screen. Each row gets a True or False label. When you pass this mask to `loc`, pandas keeps only the rows marked True. This is the foundation of all data filtering in pandas.

---

### 6.2 Filtering Rows with a Condition

```python
# Select ONLY the rows where customer_id equals 642
# Pass the Boolean mask directly into loc as the row selector
# No second argument means "return all columns"
transactions.loc[transactions["customer_id"] == 642]
```

**Expected Output:**

```
    customer_id  transaction_id  product_area_id  num_items  sales_cost
0           642               1                1          2        5.99
2           642               3                2          5       12.50
4           642               5                4          1        3.25
8           642               9                1          3        4.50
15          642              16                2          4        9.99
...         ...             ...              ...        ...         ...
```

> 📝 **Explanation:** `transactions["customer_id"] == 642` creates a mask, and `loc[mask]` applies it. Only rows where the condition is True are returned. This is how you answer questions like "Show me all transactions for a specific customer."

---

### 6.3 Filtering Rows AND Selecting Specific Columns

```python
# Filter rows where customer_id = 642
# AND return only these three columns
transactions.loc[transactions["customer_id"] == 642,
                 ["customer_id", "sales_cost", "product_area_id"]]
```

**Expected Output:**

```
    customer_id  sales_cost  product_area_id
0           642        5.99                1
2           642       12.50                2
4           642        3.25                4
8           642        4.50                1
15          642        9.99                2
```

> 📝 **Explanation:** Now we're combining everything:
>
> - First argument: Boolean mask to filter rows (customer_id == 642)
> - Second argument: List of column names to keep
>
> This is extremely common in real work — you rarely want ALL columns when filtering.

---

### 6.4 Multiple Conditions with AND (`&`)

```python
# Select rows where customer_id = 642 AND num_items > 5
# BOTH conditions must be True for a row to be selected
# IMPORTANT: Each condition must be wrapped in parentheses ()
# The & operator means "AND" (both must be true)
transactions.loc[(transactions["customer_id"] == 642) & (transactions["num_items"] > 5)]
```

**Expected Output:**

```
    customer_id  transaction_id  product_area_id  num_items  sales_cost
2           642               3                2          5       12.50
25          642              26                3          8       15.99
```

> 📝 **Explanation:** The `&` operator requires **both** conditions to be True. Parentheses are **mandatory** because `&` has higher operator precedence than `==`. Without parentheses, Python would evaluate incorrectly. Think of this as: "Show me customer 642's transactions where they bought more than 5 items."

---

### 6.5 Multiple Conditions with OR (`|`)

```python
# Select rows where customer_id = 642 OR num_items > 5
# EITHER condition being True is enough for selection
# The | operator (pipe symbol) means "OR"
transactions.loc[(transactions["customer_id"] == 642) | (transactions["num_items"] > 5)]
```

**Expected Output:**

```
    customer_id  transaction_id  product_area_id  num_items  sales_cost
0           642               1                1          2        5.99
2           642               3                2          5       12.50
4           642               5                4          1        3.25
8           642               9                1          3        4.50
11          700              12                2          7       18.50
...         ...             ...              ...        ...         ...
```

> 📝 **Explanation:** The `|` operator is inclusive OR — a row is selected if **either** condition is True (or both). This answers: "Show me all transactions by customer 642, PLUS any transaction where more than 5 items were bought (regardless of customer)."

---

### 6.6 Checking Membership with `isin()`

```python
# Select rows where customer_id is IN the list [642, 700]
# This is cleaner than writing: (customer_id == 642) | (customer_id == 700)
# isin() checks if each value exists in the provided list
transactions.loc[transactions["customer_id"].isin([642, 700])]
```

**Expected Output:**

```
    customer_id  transaction_id  product_area_id  num_items  sales_cost
0           642               1                1          2        5.99
1           700               2                3          1        2.49
2           642               3                2          5       12.50
6           700               7                3          2        4.99
8           642               9                1          3        4.50
```

> 📝 **Explanation:** `isin()` is much more readable and efficient than chaining multiple OR conditions. It's perfect when you have a list of values to match against — like "show me transactions for our top 10 VIP customers."

---

### 6.7 Negating a Condition with `~` (Tilde)

```python
# The tilde (~) means "NOT" or "opposite of"
# Select rows where customer_id is NOT in [642, 700]
# This returns ALL customers EXCEPT 642 and 700
transactions.loc[~transactions["customer_id"].isin([642, 700])]
```

**Expected Output:**

```
    customer_id  transaction_id  product_area_id  num_items  sales_cost
3           821               4                1          3        8.75
5           900               6                2          4        9.99
7           821               8                4          2        5.50
9           900              10                2          1        2.99
10          555              11                3          3        6.75
...         ...             ...              ...        ...         ...
```

> 📝 **Explanation:** The `~` (tilde) operator **inverts** a Boolean mask. Where `isin()` returns True, `~isin()` returns False, and vice versa. This is how you exclude data. Example: "Show me all transactions EXCEPT those from our two biggest customers."

---

## 7. Practical Company Use Cases {#use-cases}

### 🏢 Use Case 1: Sales Performance Analysis

**Scenario:** The Sales Director needs a monthly report showing high-value transactions.

```python
# Select transactions over $100 from the last 30 days
# Only show customer, date, and amount columns
high_value = transactions.loc[
    (transactions["sales_cost"] > 100) &
    (transactions["transaction_date"] >= "2024-01-01"),
    ["customer_id", "transaction_date", "sales_cost"]
]

# Export for the Sales Director
high_value.to_excel("high_value_transactions.xlsx", index=False)
```

> 💼 **Business Value:** Identifies top revenue-generating transactions for follow-up and customer relationship management.

---

### 🏢 Use Case 2: Customer Segmentation

**Scenario:** Marketing wants to analyze spending patterns of VIP customers.

```python
# VIP customer list
vip_customers = [642, 700, 821, 900]

# Get all transactions for VIPs, focusing on product preferences
vip_data = transactions.loc[
    transactions["customer_id"].isin(vip_customers),
    ["customer_id", "product_area_id", "num_items", "sales_cost"]
]

# Group by customer to see total spending
vip_summary = vip_data.groupby("customer_id")["sales_cost"].sum()
```

> 💼 **Business Value:** Helps marketing create personalized campaigns based on what VIP customers actually buy.

---

### 🏢 Use Case 3: Inventory Management

**Scenario:** The warehouse manager needs to know which product areas have low stock movement.

```python
# Products with low sales (less than 5 items sold in a transaction)
# Focus on product_area_id and quantity
low_movement = transactions.loc[
    transactions["num_items"] < 5,
    ["product_area_id", "num_items", "sales_cost"]
]

# Count transactions per product area
product_counts = low_movement["product_area_id"].value_counts()
```

> 💼 **Business Value:** Identifies slow-moving inventory areas that may need promotions or discontinuation.

---

### 🏢 Use Case 4: Fraud Detection

**Scenario:** The finance team flags unusually large transactions.

```python
# Flag transactions where quantity OR amount is unusually high
suspicious = transactions.loc[
    (transactions["num_items"] > 20) | (transactions["sales_cost"] > 500),
    ["transaction_id", "customer_id", "num_items", "sales_cost"]
]

# Add a flag column
suspicious.loc[:, "flag"] = "REVIEW_REQUIRED"
```

> 💼 **Business Value:** Automated fraud detection by identifying transactions that deviate significantly from normal patterns.

---

### 🏢 Use Case 5: Weekly Reporting

**Scenario:** Generate a standard weekly report with specific column ordering.

```python
# Standard weekly report format: Customer first, then what they bought, then cost
weekly_report = transactions.loc[
    transactions["transaction_date"] >= "2024-01-15",
    ["customer_id", "product_area_id", "num_items", "sales_cost", "transaction_date"]
]

# Reorder by sales cost (highest first) for the report
weekly_report = weekly_report.sort_values("sales_cost", ascending=False)
```

> 💼 **Business Value:** Consistent, automated reporting saves hours of manual Excel work every week.

---

## 8. Complete Code with Detailed Explanations {#complete-code}

```python
# =============================================================================
# PANDAS - LOC & ILOC: COMPLETE GUIDE
# =============================================================================
# This script demonstrates how to select specific rows and columns from a
# DataFrame using loc (label-based) and iloc (index-based) selection.
# =============================================================================

# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
# pandas: The primary library for data manipulation and analysis in Python.
#         Provides DataFrame and Series data structures.
import pandas as pd

# numpy: A library for numerical computing. Often used alongside pandas for
#        mathematical operations, though not directly used in this script.
import numpy as np

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
# pd.read_excel(): Reads an Excel file (.xlsx) into a pandas DataFrame.
#   - First argument: Path to the Excel file ("grocery_database.xlsx")
#   - sheet_name="transactions": Specifies which worksheet to read from the
#     Excel workbook. Excel files can contain multiple sheets.
#   - The result is a DataFrame stored in the variable 'transactions'.
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# ---------------------------------------------------------------------------
# BASIC SYNTAX OVERVIEW
# ---------------------------------------------------------------------------
# Both loc and iloc follow the same pattern:
#   DataFrame.loc[row_selection, column_selection]   <- Uses LABELS/NAMES
#   DataFrame.iloc[row_selection, column_selection]  <- Uses INDEX POSITIONS
#
# row_selection:    Which rows you want (required)
# column_selection: Which columns you want (optional - omit for all columns)
# ---------------------------------------------------------------------------

transactions.loc[row_labels, column_labels]      # Label-based
transactions.iloc[row_indexes, column_indexes]   # Index-based


# =============================================================================
# ILOC - INTEGER/INDEX BASED SELECTION
# =============================================================================
# "I" in iloc = "Index" (integer position)
# Use iloc when you know the NUMERICAL POSITION of what you want.
# Think of it like array indexing in programming.
# =============================================================================

# ---------------------------------------------------------------------------
# Select a single row by position
# ---------------------------------------------------------------------------
# .iloc[0] selects the FIRST row (position 0).
# Python uses 0-based indexing: 0 = first, 1 = second, etc.
# Returns a Series (single row with column labels as the index).
transactions.iloc[0]

# ---------------------------------------------------------------------------
# Select multiple consecutive rows with slicing
# ---------------------------------------------------------------------------
# .iloc[0:4] selects rows at positions 0, 1, 2, and 3.
# IMPORTANT: iloc slicing is EXCLUSIVE of the end point (4 is NOT included).
# This is the same behavior as Python list slicing.
# Returns a DataFrame (multiple rows).
transactions.iloc[0:4]

# ---------------------------------------------------------------------------
# Select specific non-consecutive rows
# ---------------------------------------------------------------------------
# .iloc[[0, 30, 51]] selects rows at positions 0, 30, and 51 ONLY.
# Double brackets [[ ]] create a list and pass it to iloc.
# This is useful for sampling or checking specific records.
transactions.iloc[[0, 30, 51]]

# ---------------------------------------------------------------------------
# Select specific rows AND specific columns
# ---------------------------------------------------------------------------
# .iloc[0:4, [0, 3, -1]] does TWO things:
#   - First part (0:4): Select rows at positions 0, 1, 2, 3
#   - Second part ([0, 3, -1]): Select columns at positions 0, 3, and -1
#     - 0 = first column
#     - 3 = fourth column
#     - -1 = LAST column (negative indexing counts from the end)
# The comma separates row selection from column selection.
transactions.iloc[0:4, [0, 3, -1]]

# ---------------------------------------------------------------------------
# Select ALL rows and specific columns
# ---------------------------------------------------------------------------
# .iloc[:, [0, 3, -1]] uses a colon (:) for the row dimension.
# The colon alone means "select everything in this dimension."
# So: ALL rows, but ONLY columns at positions 0, 3, and -1.
# Great for extracting a subset of columns while keeping all rows.
transactions.iloc[:, [0, 3, -1]]


# =============================================================================
# LOC - LABEL BASED SELECTION
# =============================================================================
# loc uses LABELS (names) instead of numbers.
# By default, row labels are 0, 1, 2, 3... (same as positions initially).
# But loc becomes powerful when you set custom labels (like customer IDs).
# =============================================================================

# ---------------------------------------------------------------------------
# Select a single row by label (default index)
# ---------------------------------------------------------------------------
# .loc[0] selects the row with LABEL 0.
# With default indexing, this is the same as .iloc[0].
# Returns a Series.
transactions.loc[0]

# ---------------------------------------------------------------------------
# Set a custom index (making row labels meaningful)
# ---------------------------------------------------------------------------
# .set_index("customer_id") makes the 'customer_id' column the new row index.
# inplace=True modifies the original DataFrame instead of returning a copy.
# After this, rows are labeled by customer_id values, not 0, 1, 2...
# Example: Row label 642 contains all transactions for customer 642.
transactions.set_index("customer_id", inplace=True)

# ---------------------------------------------------------------------------
# Select rows by custom label
# ---------------------------------------------------------------------------
# .loc[642] selects ALL rows where the index label is 642.
# Since customer_id is now the index, this returns ALL transactions for
# customer 642 (there may be multiple rows if they made multiple purchases).
# This is much more intuitive than remembering row positions!
transactions.loc[642]

# ---------------------------------------------------------------------------
# Reset the index back to default
# ---------------------------------------------------------------------------
# .reset_index() undoes set_index().
# The current index (customer_id) becomes a regular column again.
# The default numeric index (0, 1, 2...) is restored.
# inplace=True modifies the original DataFrame.
transactions.reset_index(inplace=True)

# ---------------------------------------------------------------------------
# View all column names
# ---------------------------------------------------------------------------
# list(transactions) converts the column names into a Python list.
# Useful for seeing available columns, especially in large DataFrames.
# You can then copy-paste these names into your loc selections.
list(transactions)

# ---------------------------------------------------------------------------
# Select rows and a single column
# ---------------------------------------------------------------------------
# .loc[0:10, "customer_id"] does TWO things:
#   - 0:10 selects rows with labels 0 through 10 (INCLUSIVE of 10!)
#   - "customer_id" selects only that column
# NOTE: Unlike iloc, loc slicing is INCLUSIVE of both endpoints.
# Returns a Series (single column).
transactions.loc[0:10, "customer_id"]

# ---------------------------------------------------------------------------
# Select rows and multiple columns
# ---------------------------------------------------------------------------
# .loc[0:10, ["customer_id", "product_area_id", "sales_cost"]]
#   - Rows 0 through 10 (inclusive)
#   - Only these three columns, in this exact order
# Returns a DataFrame (multiple rows, multiple columns).
transactions.loc[0:10, ["customer_id", "product_area_id", "sales_cost"]]

# ---------------------------------------------------------------------------
# Reorder columns
# ---------------------------------------------------------------------------
# By specifying columns in a different order, you REORDER them.
# sales_cost appears first, then customer_id, then product_area_id.
# The original DataFrame is NOT modified - this returns a new view.
# Perfect for creating reports with columns in a specific order.
transactions.loc[0:10, ["sales_cost", "customer_id", "product_area_id"]]


# =============================================================================
# CONDITIONAL LOGIC & FILTERING
# =============================================================================
# This is the most powerful feature of loc - selecting data based on RULES.
# You create a Boolean mask (True/False for each row) and pass it to loc.
# =============================================================================

# ---------------------------------------------------------------------------
# Create a Boolean mask
# ---------------------------------------------------------------------------
# transactions["customer_id"] == 642 compares every row's customer_id to 642.
# Returns a Series of True/False values.
# True = this row's customer_id is 642.
# False = this row's customer_id is NOT 642.
# This mask can be used to filter rows.
transactions["customer_id"] == 642

# ---------------------------------------------------------------------------
# Filter rows based on a condition
# ---------------------------------------------------------------------------
# Pass the Boolean mask directly into loc's row selector.
# Only rows where the condition is True are returned.
# No second argument means "return all columns."
# This answers: "Show me all transactions for customer 642."
transactions.loc[transactions["customer_id"] == 642]

# ---------------------------------------------------------------------------
# Filter rows AND select specific columns
# ---------------------------------------------------------------------------
# Combine filtering (first argument) with column selection (second argument).
# Only rows where customer_id = 642 are returned,
# and only the three specified columns are shown.
# This is extremely common in real-world data analysis.
transactions.loc[transactions["customer_id"] == 642,
                 ["customer_id", "sales_cost", "product_area_id"]]

# ---------------------------------------------------------------------------
# Multiple conditions with AND (&)
# ---------------------------------------------------------------------------
# (condition1) & (condition2) requires BOTH to be True.
# Parentheses are MANDATORY because & has higher precedence than ==.
# This answers: "Show me customer 642's transactions with more than 5 items."
transactions.loc[(transactions["customer_id"] == 642) & (transactions["num_items"] > 5)]

# ---------------------------------------------------------------------------
# Multiple conditions with OR (|)
# ---------------------------------------------------------------------------
# (condition1) | (condition2) requires EITHER to be True (or both).
# The | symbol means "OR".
# Parentheses are again mandatory.
# This answers: "Show me transactions by customer 642 OR any transaction
#                 where more than 5 items were bought."
transactions.loc[(transactions["customer_id"] == 642) | (transactions["num_items"] > 5)]

# ---------------------------------------------------------------------------
# Check membership with isin()
# ---------------------------------------------------------------------------
# .isin([642, 700]) checks if each row's customer_id is in the list [642, 700].
# Much cleaner than: (customer_id == 642) | (customer_id == 700)
# Perfect for filtering by a list of values (e.g., VIP customers).
transactions.loc[transactions["customer_id"].isin([642, 700])]

# ---------------------------------------------------------------------------
# Negate a condition with ~ (tilde)
# ---------------------------------------------------------------------------
# ~ means "NOT" or "opposite of".
# ~transactions["customer_id"].isin([642, 700]) returns True for rows where
# customer_id is NOT in [642, 700].
# This answers: "Show me all transactions EXCEPT those from customers 642 and 700."
transactions.loc[~transactions["customer_id"].isin([642, 700])]
```

---

## 9. Common Mistakes to Avoid {#common-mistakes}

| ❌ Mistake                                 | ✅ Correct                                               | Why It Matters                      |
| ------------------------------------------ | -------------------------------------------------------- | ----------------------------------- | ------------------------------------------- |
| `df.loc[0:4]` thinking 4 is excluded       | Remember: `loc` is **inclusive**                         | You'll get 5 rows instead of 4      |
| `df.iloc[0:4]` thinking 4 is included      | Remember: `iloc` is **exclusive**                        | You'll get 4 rows instead of 5      |
| `df.loc[df['col'] == 1 & df['col2'] == 2]` | `df.loc[(df['col'] == 1) & (df['col2'] == 2)]`           | Missing parentheses causes errors   |
| `df.iloc[0, 'column_name']`                | `df.iloc[0, 0]` or `df.loc[0, 'column_name']`            | `iloc` needs numbers, not names     |
| `df.loc[0, 0]`                             | `df.loc[0, 'column_name']`                               | `loc` needs names, not numbers      |
| Using `and`/`or` instead of `&`/`          | `                                                        | Always use `&` and `\|` with pandas | Python's `and`/`or` don't work element-wise |
| Forgetting `inplace=True`                  | Add `inplace=True` or reassign: `df = df.set_index(...)` | Changes don't persist otherwise     |

---

## 10. Quick Reference Cheat Sheet {#cheat-sheet}

```python
# ========== ILOC (Integer Position) ==========
transactions.iloc[0]                    # First row
transactions.iloc[-1]                   # Last row
transactions.iloc[0:5]                  # Rows 0,1,2,3,4 (5 excluded)
transactions.iloc[[0, 5, 10]]          # Rows 0, 5, and 10
transactions.iloc[:, 0]                 # First column, all rows
transactions.iloc[0:5, 0:3]             # Rows 0-4, columns 0-2
transactions.iloc[:, [0, 2, -1]]        # All rows, columns 0, 2, and last

# ========== LOC (Label/Name) ==========
transactions.loc[0]                     # Row with label 0
transactions.loc[0:5]                   # Rows with labels 0,1,2,3,4,5 (5 INCLUDED!)
transactions.loc[:, "column_name"]      # One column, all rows
transactions.loc[0:5, ["col1", "col2"]] # Rows 0-5, specific columns
transactions.loc[df["col"] > 5]         # Rows where condition is True
transactions.loc[df["col"].isin([...])] # Rows where value is in list
transactions.loc[~df["col"].isin([...])] # Rows where value is NOT in list

# ========== COMMON PATTERNS ==========
# Filter + select columns
df.loc[condition, ["col1", "col2"]]

# Multiple AND conditions
df.loc[(cond1) & (cond2) & (cond3)]

# Multiple OR conditions
df.loc[(cond1) | (cond2)]

# Between two values
df.loc[df["col"].between(10, 20)]

# Not null values
df.loc[df["col"].notna()]

# Null values
df.loc[df["col"].isna()]
```

---

## Summary

| Task                            | Use This                       |
| ------------------------------- | ------------------------------ |
| Select by position (0, 1, 2...) | `iloc`                         |
| Select by name/label            | `loc`                          |
| Filter by conditions            | `loc` with Boolean mask        |
| Check multiple values           | `.isin()`                      |
| Exclude values                  | `~` (tilde)                    |
| Reorder columns                 | `loc` with ordered column list |
| Custom row labels               | `.set_index()`                 |

> 🎯 **Remember:** `iloc` is for **positions** (like an array), `loc` is for **labels** (like a dictionary). Master both, and you'll be able to slice and dice any DataFrame with confidence!
