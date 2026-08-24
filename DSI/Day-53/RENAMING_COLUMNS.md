# 📊 Pandas: Renaming Columns — Complete Beginner's Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Why Rename Columns?](#why-rename)
3. [Loading Our Data](#setup)
4. [Method 1: `rename()` — Rename Specific Columns](#method1)
5. [Method 2: `df.columns = [...]` — Rename All Columns at Once](#method2)
6. [Method 3: `str.replace()` — Clean Column Names Programmatically](#method3)
7. [Practical Company Use Cases](#use-cases)
8. [Complete Code with Detailed Explanations](#complete-code)
9. [Common Mistakes to Avoid](#common-mistakes)
10. [Quick Reference Cheat Sheet](#cheat-sheet)

---

## 1. Introduction {#introduction}

When you load data from files (Excel, CSV, databases), the column names are often:

- ❌ Inconsistent (some uppercase, some lowercase)
- ❌ Contain spaces (which make coding harder)
- ❌ Use unclear abbreviations
- ❌ Have typos or special characters
- ❌ Don't match your company's naming conventions

**Renaming columns** is one of the first and most important steps in any data cleaning workflow. Clean, consistent column names make your code easier to read, write, and maintain.

> 💡 **Key Insight:** There are three main ways to rename columns in pandas:
>
> 1. **`rename()`** — Rename one or a few specific columns
> 2. **`df.columns = [...]`** — Replace ALL column names at once
> 3. **`df.columns.str.replace()`** — Clean column names programmatically (e.g., remove spaces)

---

## 2. Why Rename Columns? {#why-rename}

| Problem                 | Example                                      | Why It Matters                                  |
| ----------------------- | -------------------------------------------- | ----------------------------------------------- |
| **Spaces in names**     | `"Sales Cost"`                               | Can't use dot notation: `df.Sales Cost` fails   |
| **Inconsistent casing** | `"CustomerID"` vs `"customer_id"`            | Easy to make typos in code                      |
| **Unclear names**       | `"col1"`, `"var_x"`                          | Team members don't know what the data means     |
| **Typos**               | `"custmoer_id"`                              | Joins and merges fail because names don't match |
| **Special characters**  | `"sales$cost"`, `"qty#"`                     | Can cause syntax errors or unexpected behavior  |
| **Wrong context**       | `"customer_id"` when data is about suppliers | Misleading names lead to wrong analysis         |

> 🎯 **Best Practice:** Use `snake_case` (lowercase with underscores) for all column names. It's the standard in Python and data science.

---

## 3. Loading Our Data {#setup}

```python
# Import the pandas library - the standard tool for data manipulation in Python
import pandas as pd

# Load the Excel file into a DataFrame
# "grocery_database.xlsx" is our data file
# sheet_name="transactions" tells pandas which worksheet to read
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")
```

**Expected Output (first few rows):**

```
   customer_id transaction_date  transaction_id  product_area_id  num_items  sales_cost
0          642       2024-01-01               1                1          2        5.99
1          700       2024-01-01               2                3          1        2.49
2          642       2024-01-02               3                2          5       12.50
3          821       2024-01-02               4                1          3        8.75
4          642       2024-01-03               5                4          1        3.25
```

---

## 4. Method 1: `rename()` — Rename Specific Columns {#method1}

Use `rename()` when you want to change **only one or a few** column names while keeping the rest unchanged.

### 4.1 View Current Column Names

```python
# Convert the DataFrame's column names into a Python list
# This lets us see all current column names clearly
# It's helpful to run this BEFORE renaming so you know the exact current names
list(transactions)
```

**Expected Output:**

```python
['customer_id',
 'transaction_date',
 'transaction_id',
 'product_area_id',
 'num_items',
 'sales_cost']
```

> 📝 **Explanation:** `list(transactions)` converts the pandas Index object (which holds column names) into a plain Python list. This makes it easy to read, copy, and work with column names. You could also use `transactions.columns.tolist()` which does the same thing.

---

### 4.2 Rename a Single Column with `rename()`

```python
# Rename the column "customer_id" to "friend_id"
# columns={"old_name": "new_name"} creates a dictionary mapping old names to new names
# inplace=True means "modify the original DataFrame directly" instead of returning a copy
# Without inplace=True, the original DataFrame would NOT change!
transactions.rename(columns={"customer_id": "friend_id"}, inplace=True)
```

**Expected Output (no direct output, but the DataFrame is modified):**

> 📝 **Explanation:**
>
> - `rename()` is a pandas method that renames labels (columns or rows).
> - The `columns=` parameter takes a **dictionary** where:
>   - **Keys** = current column names you want to change
>   - **Values** = the new names you want to assign
> - `inplace=True` is **critical** here. By default, `rename()` returns a NEW DataFrame and leaves the original unchanged. With `inplace=True`, pandas modifies the existing `transactions` DataFrame directly, saving memory.

---

### 4.3 Verify the Rename Worked

```python
# Check the column names again to confirm the change
# "customer_id" should now appear as "friend_id"
list(transactions)
```

**Expected Output:**

```python
['friend_id',           # <-- Changed from 'customer_id'!
 'transaction_date',
 'transaction_id',
 'product_area_id',
 'num_items',
 'sales_cost']
```

> 📝 **Explanation:** Always verify your changes! Running `list(transactions)` after renaming confirms that `"customer_id"` has been successfully replaced with `"friend_id"`. This is a good habit to develop — verify every transformation step.

---

### 4.4 Renaming Multiple Columns at Once

```python
# You can rename multiple columns in one call by adding more key-value pairs
# This renames two columns simultaneously
transactions.rename(
    columns={
        "friend_id": "customer_id",      # Change it back
        "sales_cost": "revenue"           # Rename sales_cost to revenue
    },
    inplace=True
)
```

> 📝 **Explanation:** The dictionary can have as many entries as you need. Each `"old_name": "new_name"` pair renames one column. This is much more efficient than calling `rename()` multiple times.

---

## 5. Method 2: `df.columns = [...]` — Rename All Columns at Once {#method2}

Use this method when you want to **replace ALL column names** in one go. This is common when:

- You've imported data with generic names (col1, col2, col3...)
- You want to apply a consistent naming convention to the entire DataFrame
- You're building a DataFrame from scratch and need to name the columns

### 5.1 Define New Column Names

```python
# Create a Python list containing ALL the new column names
# The ORDER of names in this list MUST match the ORDER of columns in the DataFrame
# Column 0 gets the first name, Column 1 gets the second name, etc.
column_names = [
    'friend_id',           # Was: customer_id
    'transaction_date',    # Stays the same
    'purchase_id',         # Was: transaction_id
    'product_region_id',   # Was: product_area_id
    'num_items',           # Stays the same
    'sales_cost'           # Stays the same
]
```

> 📝 **Explanation:**
>
> - This list has **exactly 6 items** because our DataFrame has **6 columns**.
> - The **position** of each name in the list determines which column it gets assigned to.
> - If you have 6 columns but provide only 5 names, pandas will throw an error.
> - If you have 6 columns but provide 7 names, pandas will also throw an error.
> - **The count must match exactly!**

---

### 5.2 Assign the New Column Names

```python
# Replace ALL column names in the DataFrame with our new list
# This overwrites the existing column names completely
# Any column name NOT in your list will be lost/changed
transactions.columns = column_names
```

**Expected Output (no direct output, but columns are changed):**

> 📝 **Explanation:**
>
> - `transactions.columns` is a property that holds all column names as an Index object.
> - By assigning a new list to `transactions.columns`, you **completely replace** all existing names.
> - This is different from `rename()` which only changes the columns you specify.
> - **Warning:** This method is "all or nothing" — you must provide a name for EVERY column, even the ones you don't want to change.

---

### 5.3 Verify the Changes

```python
# Confirm all columns have been renamed correctly
list(transactions)
```

**Expected Output:**

```python
['friend_id',
 'transaction_date',
 'purchase_id',
 'product_region_id',
 'num_items',
 'sales_cost']
```

> 📝 **Explanation:** Notice how `transaction_id` became `purchase_id` and `product_area_id` became `product_region_id`. Even columns we didn't explicitly want to change (like `transaction_date`) had to be included in the list to maintain the correct order.

---

## 6. Method 3: `str.replace()` — Clean Column Names Programmatically {#method3}

Sometimes you don't want to rename columns individually — you want to **clean all names at once** using a pattern. The most common example is **replacing spaces with underscores**.

### 6.1 Why Spaces in Column Names Are Bad

```python
# Let's intentionally create column names WITH spaces
# This simulates data you might receive from Excel files or databases
column_names = [
    'friend id',           # Space between "friend" and "id"
    'transaction date',    # Space between "transaction" and "date"
    'purchase id',         # Space between "purchase" and "id"
    'product region id',   # Multiple spaces!
    'num items',           # Space between "num" and "items"
    'sales cost'           # Space between "sales" and "cost"
]

# Apply these messy names to our DataFrame
transactions.columns = column_names
```

**Expected Output (column names now have spaces):**

```python
['friend id',
 'transaction date',
 'purchase id',
 'product region id',
 'num items',
 'sales cost']
```

> 📝 **Explanation:**
>
> - Many real-world datasets (especially from Excel) have spaces in column names.
> - **Spaces cause problems** in Python because you can't use dot notation:
>   - ❌ `transactions.friend id` → SyntaxError (space is invalid in attribute names)
>   - ✅ `transactions["friend id"]` → Works, but annoying to type
> - It's much better to use underscores: `transactions.friend_id`

---

### 6.2 Replace Spaces with Underscores

```python
# Clean ALL column names by replacing every space with an underscore
# .str gives us access to string methods on the column names
# .replace(" ", "_") replaces each space character with an underscore
# The result is assigned back to transactions.columns, updating all names
transactions.columns = transactions.columns.str.replace(" ", "_")
```

**Expected Output:**

```python
['friend_id',
 'transaction_date',
 'purchase_id',
 'product_region_id',
 'num_items',
 'sales_cost']
```

> 📝 **Explanation:**
>
> - `transactions.columns` is an Index object containing all column names.
> - `.str` is a pandas **string accessor** that lets you apply string operations to EVERY element in the Index.
> - `.replace(" ", "_")` is a string method that replaces all occurrences of the first argument (space) with the second argument (underscore).
> - This is incredibly powerful because it processes **all column names at once** — no matter how many columns you have!
> - You can chain multiple `.str` operations: `transactions.columns.str.replace(" ", "_").str.lower()`

---

### 6.3 Other Common Cleaning Patterns

```python
# Convert ALL column names to lowercase
transactions.columns = transactions.columns.str.lower()

# Convert ALL column names to uppercase
transactions.columns = transactions.columns.str.upper()

# Remove leading/trailing whitespace
transactions.columns = transactions.columns.str.strip()

# Replace multiple patterns at once (using regex)
transactions.columns = transactions.columns.str.replace(r"[\s-]", "_", regex=True)

# Add a prefix to all columns
transactions.columns = "txn_" + transactions.columns

# Add a suffix to all columns
transactions.columns = transactions.columns + "_2024"
```

> 📝 **Explanation:** The `.str` accessor unlocks the full power of Python string methods for batch-processing column names. This is essential when dealing with messy data from external sources.

---

## 7. Practical Company Use Cases {#use-cases}

### 🏢 Use Case 1: Standardizing Column Names Across Multiple Datasets

**Scenario:** Your company receives monthly sales data from 5 different stores. Each store uses different column naming conventions.

```python
# Store A columns: ['CustID', 'Date', 'Qty', 'Amt']
# Store B columns: ['customer id', 'transaction date', 'quantity', 'amount']
# Store C columns: ['CUST_ID', 'TXN_DATE', 'NUM_ITEMS', 'SALES_COST']

# After loading each store's data, standardize them all:
standard_names = ['customer_id', 'transaction_date', 'num_items', 'sales_cost']

store_a.columns = standard_names
store_b.columns = standard_names
store_c.columns = standard_names

# Now you can concatenate them without issues
all_stores = pd.concat([store_a, store_b, store_c], ignore_index=True)
```

> 💼 **Business Value:** Enables seamless merging and analysis of data from multiple sources. Without standardization, `pd.concat()` would create a DataFrame with 12 columns instead of 4.

---

### 🏢 Use Case 2: Preparing Data for a Machine Learning Model

**Scenario:** The data science team needs clean column names for their Python ML pipeline.

```python
# Raw data from the database has spaces and mixed case
raw_data = pd.read_csv("raw_sales_data.csv")

# ML pipelines expect snake_case with no spaces
raw_data.columns = (
    raw_data.columns
    .str.strip()                    # Remove leading/trailing spaces
    .str.lower()                    # Convert to lowercase
    .str.replace(r"[^a-z0-9]", "_", regex=True)  # Replace special chars with _
    .str.replace(r"_+", "_", regex=True)         # Remove multiple consecutive _
    .str.strip("_")                # Remove leading/trailing underscores
)

# Save the cleaned data for the ML team
raw_data.to_csv("clean_sales_data.csv", index=False)
```

> 💼 **Business Value:** Prevents pipeline failures caused by invalid characters in column names. ML libraries like scikit-learn often struggle with spaces and special characters.

---

### 🏢 Use Case 3: Making Reports Readable for Stakeholders

**Scenario:** You need to export an Excel report for the Finance Director who prefers business-friendly column names.

```python
# Internal working names (developer-friendly)
internal_names = ['cust_id', 'txn_dt', 'prod_area', 'qty', 'rev']
report.columns = internal_names

# Before exporting, rename to business-friendly names
report.rename(columns={
    'cust_id': 'Customer ID',
    'txn_dt': 'Transaction Date',
    'prod_area': 'Product Category',
    'qty': 'Quantity Sold',
    'rev': 'Revenue ($)'
}, inplace=True)

# Export with pretty names
report.to_excel("monthly_sales_report.xlsx", index=False)
```

> 💼 **Business Value:** Reports with clear, descriptive headers are more professional and easier for non-technical stakeholders to understand. No one wants to see "cust_id" in a board presentation.

---

### 🏢 Use Case 4: Fixing Typos in Imported Data

**Scenario:** A CSV export from the legacy system has a typo in one column name.

```python
# Loaded data has a typo: "custmoer_id" instead of "customer_id"
print(list(df))
# ['custmoer_id', 'date', 'amount']  <-- Notice the typo!

# Fix just the typo without touching other columns
df.rename(columns={"custmoer_id": "customer_id"}, inplace=True)

# Now joins with the customer master table will work correctly
customer_master = pd.read_csv("customers.csv")
merged = df.merge(customer_master, on="customer_id")
```

> 💼 **Business Value:** A single typo in a column name can break data joins, causing missing data in reports. Fixing it early prevents downstream analysis errors.

---

### 🏢 Use Case 5: Adding Context with Prefixes/Suffixes

**Scenario:** You're merging two datasets with overlapping column names.

```python
# January data
jan = pd.read_excel("jan_sales.xlsx")
jan.columns = "jan_" + jan.columns  # jan_customer_id, jan_sales_cost, etc.

# February data
feb = pd.read_excel("feb_sales.xlsx")
feb.columns = "feb_" + feb.columns  # feb_customer_id, feb_sales_cost, etc.

# Now merge side-by-side without column name conflicts
comparison = pd.concat([jan, feb], axis=1)
```

> 💼 **Business Value:** Prevents column name collisions when combining datasets. Without prefixes, you'd have two "sales_cost" columns, and pandas would rename them to "sales_cost_x" and "sales_cost_y" automatically — which is confusing.

---

## 8. Complete Code with Detailed Explanations {#complete-code}

```python
# =============================================================================
# PANDAS - RENAMING COLUMNS: COMPLETE GUIDE
# =============================================================================
# This script demonstrates three methods for renaming columns in pandas:
#   1. rename()         - Rename specific columns
#   2. df.columns =     - Rename ALL columns at once
#   3. str.replace()    - Clean column names programmatically
# =============================================================================

# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------
# pandas: The primary library for data manipulation and analysis in Python.
import pandas as pd

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
# pd.read_excel(): Reads an Excel file into a pandas DataFrame.
#   - "grocery_database.xlsx": Path to the Excel file
#   - sheet_name="transactions": Which worksheet to read from the workbook
#   - Result stored in variable 'transactions'
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")

# ---------------------------------------------------------------------------
# VIEW CURRENT COLUMN NAMES
# ---------------------------------------------------------------------------
# list(transactions) converts the DataFrame's column Index into a Python list.
# This is the first thing you should do before renaming — you need to know
# the EXACT current names (including case and spelling).
# Running this before and after renaming helps you verify your changes.
list(transactions)

# ---------------------------------------------------------------------------
# METHOD 1: rename() — Rename Specific Columns
# ---------------------------------------------------------------------------
# transactions.rename() renames columns (or rows) by their labels.
#   - columns={"old_name": "new_name"}: A dictionary mapping old names to new
#   - inplace=True: Modifies the original DataFrame directly (no copy created)
#     WITHOUT inplace=True, rename() returns a NEW DataFrame and the original
#     remains unchanged — a common source of confusion for beginners!
#
# This method is best when you only need to rename a few columns.
transactions.rename(columns={"customer_id": "friend_id"}, inplace=True)

# Verify the change worked by viewing column names again
list(transactions)

# ---------------------------------------------------------------------------
# METHOD 2: df.columns = [...] — Rename ALL Columns at Once
# ---------------------------------------------------------------------------
# This method completely replaces ALL column names.
# You must provide a name for EVERY column, in the EXACT order they appear.
# If you have 6 columns, your list MUST have 6 items.
#
# Use this when:
#   - You want to rename most or all columns
#   - You're applying a consistent naming convention
#   - The original names are generic (col1, col2, col3...)

column_names = [
    'friend_id',           # Column 0: renamed from customer_id
    'transaction_date',    # Column 1: kept the same
    'purchase_id',         # Column 2: renamed from transaction_id
    'product_region_id',   # Column 3: renamed from product_area_id
    'num_items',           # Column 4: kept the same
    'sales_cost'           # Column 5: kept the same
]

# Assign the new list to transactions.columns
# This OVERWRITES all existing column names completely
transactions.columns = column_names

# Verify the changes
list(transactions)

# ---------------------------------------------------------------------------
# METHOD 3: str.replace() — Clean Column Names Programmatically
# ---------------------------------------------------------------------------
# This method is for cleaning up messy column names (e.g., removing spaces).
# It's especially useful when importing data from Excel or external systems.

# First, let's intentionally create messy column names with spaces
column_names = [
    'friend id',           # Has a space
    'transaction date',    # Has a space
    'purchase id',         # Has a space
    'product region id',   # Has multiple spaces
    'num items',           # Has a space
    'sales cost'           # Has a space
]

# Apply the messy names
transactions.columns = column_names

# View the messy names
list(transactions)

# Now clean them all at once using .str.replace()
# transactions.columns.str gives us access to string methods
# .replace(" ", "_") replaces every space with an underscore
# The result is assigned back, updating ALL column names in one line
transactions.columns = transactions.columns.str.replace(" ", "_")

# View the cleaned names — all spaces are now underscores
list(transactions)
```

---

## 9. Common Mistakes to Avoid {#common-mistakes}

| ❌ Mistake                                                            | ✅ Correct                                            | Why It Matters                                                  |
| --------------------------------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------- |
| `df.rename(columns={"old": "new"})` without `inplace=True`            | Add `inplace=True` or reassign: `df = df.rename(...)` | The original DataFrame doesn't change!                          |
| `df.columns = ["a", "b"]` when df has 3 columns                       | Provide exactly the right number of names             | pandas raises a `ValueError: Length mismatch`                   |
| `df.rename(columns={"customer_id": "friend_id"})` with wrong old name | Check spelling with `list(df)` first                  | If the old name doesn't exist, nothing happens — silently fails |
| `df.columns.str.replace(" ", "_")` without reassigning                | `df.columns = df.columns.str.replace(...)`            | The operation returns a new Index but doesn't modify df         |
| Using `df.rename({"old": "new"})` without `columns=`                  | `df.rename(columns={"old": "new"})`                   | Without `columns=`, pandas doesn't know what to rename          |
| Renaming after creating views/copies                                  | Rename immediately after loading                      | Changing names on a view may not affect the original DataFrame  |

---

## 10. Quick Reference Cheat Sheet {#cheat-sheet}

```python
# ========== METHOD 1: rename() ==========
# Rename ONE column
df.rename(columns={"old_name": "new_name"}, inplace=True)

# Rename MULTIPLE columns
df.rename(columns={
    "old1": "new1",
    "old2": "new2",
    "old3": "new3"
}, inplace=True)

# Rename without inplace (returns new DataFrame)
df_new = df.rename(columns={"old": "new"})

# ========== METHOD 2: Replace ALL names ==========
# Must provide exactly as many names as there are columns!
df.columns = ["col_a", "col_b", "col_c"]

# ========== METHOD 3: Clean programmatically ==========
# Replace spaces with underscores
df.columns = df.columns.str.replace(" ", "_")

# Convert to lowercase
df.columns = df.columns.str.lower()

# Convert to uppercase
df.columns = df.columns.str.upper()

# Remove leading/trailing whitespace
df.columns = df.columns.str.strip()

# Replace special characters with underscores (regex)
df.columns = df.columns.str.replace(r"[^a-zA-Z0-9]", "_", regex=True)

# Add prefix to all columns
df.columns = "prefix_" + df.columns

# Add suffix to all columns
df.columns = df.columns + "_suffix"

# Chain multiple operations
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ========== CHECKING COLUMN NAMES ==========
list(df)                    # All column names as a list
df.columns                  # All column names as an Index
df.columns.tolist()         # Same as list(df)
len(df.columns)             # Number of columns
```

---

## Summary

| Task                         | Method to Use                                     |
| ---------------------------- | ------------------------------------------------- |
| Rename 1-2 specific columns  | `df.rename(columns={"old": "new"}, inplace=True)` |
| Rename most/all columns      | `df.columns = ["name1", "name2", ...]`            |
| Remove spaces from all names | `df.columns = df.columns.str.replace(" ", "_")`   |
| Standardize casing           | `df.columns = df.columns.str.lower()`             |
| Add prefix/suffix to all     | `df.columns = "prefix_" + df.columns`             |
| Check current names          | `list(df)` or `df.columns.tolist()`               |

> 🎯 **Remember:** Clean column names are the foundation of clean code. Always rename columns as your FIRST step after loading data. It will save you hours of debugging typos and syntax errors later!
