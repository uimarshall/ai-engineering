# Joining and Merging Data in Pandas

> **Day 54 — Data Science Interview (DSI) Prep Series**  
> A beginner-friendly guide to combining datasets using `pd.merge()`, `DataFrame.join()`, and `pd.concat()`.

---

## Table of Contents

1. [Why Do We Need to Join/Merge Data?](#1-why-do-we-need-to-joinmerge-data)
2. [The Core Concept: Keys & Relationships](#2-the-core-concept-keys--relationships)
3. [`pd.merge()` — The Universal Tool](#3-pdmerge--the-universal-tool)
4. [Types of Joins Explained (With Diagrams)](#4-types-of-joins-explained-with-diagrams)
5. [Code Examples for Every Join Type](#5-code-examples-for-every-join-type)
6. [`DataFrame.join()` vs `pd.merge()`](#6-dataframejoin-vs-pdmerge)
7. [`pd.concat()` — Stacking DataFrames](#7-pdconcat--stacking-dataframes)
8. [Handling Duplicate Column Names](#8-handling-duplicate-column-names)
9. [Merging on Index](#9-merging-on-index)
10. [Real-World Company Use Cases](#10-real-world-company-use-cases)
11. [Common Mistakes & How to Avoid Them](#11-common-mistakes--how-to-avoid-them)
12. [Quick Reference Cheat Sheet](#12-quick-reference-cheat-sheet)

---

## 1. Why Do We Need to Join/Merge Data?

In the real world, data is **never** stored in one giant table. It's split across multiple tables for efficiency, security, and organization.

| Table       | Contains                             |
| ----------- | ------------------------------------ |
| `customers` | Customer names, emails, signup dates |
| `orders`    | Order IDs, amounts, dates            |
| `products`  | Product names, categories, prices    |
| `payments`  | Payment methods, statuses            |

**To answer business questions like:**

- "Which customers spent the most last month?"
- "What products are most popular in each region?"

**You MUST combine (join) these tables.**

---

## 2. The Core Concept: Keys & Relationships

Before merging, you need to understand **keys** — the column(s) that link two tables together.

### Types of Relationships

| Relationship     | Description                                             | Example                                              |
| ---------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| **One-to-One**   | One row in Table A matches exactly one row in Table B   | `employee_id` → `employee_details`                   |
| **One-to-Many**  | One row in Table A matches multiple rows in Table B     | `customer_id` → `orders` (one customer, many orders) |
| **Many-to-Many** | Multiple rows in Table A match multiple rows in Table B | `students` ↔ `courses`                               |

### Key Terminology

- **Left DataFrame**: The first DataFrame you provide (`df1`)
- **Right DataFrame**: The second DataFrame you provide (`df2`)
- **Join Key**: The column used to match rows (e.g., `customer_id`)
- **Indicator**: A column that tells you which table each row came from

---

## 3. `pd.merge()` — The Universal Tool

`pd.merge()` is the most flexible and commonly used function for joining DataFrames.

### Basic Syntax

```python
import pandas as pd

merged_df = pd.merge(
    left=df1,           # Left DataFrame
    right=df2,          # Right DataFrame
    how='inner',        # Type of join (inner, left, right, outer, cross)
    on='column_name',   # Column(s) to join on (must exist in both)
    left_on='col_a',    # Column in left DF to join on
    right_on='col_b',   # Column in right DF to join on
    left_index=False,   # Use left DF's index as join key
    right_index=False,  # Use right DF's index as join key
    suffixes=('_x', '_y'),  # Suffix for overlapping columns
    indicator=False,    # Add column showing source of each row
    validate=None       # Check merge type ('1:1', '1:m', 'm:1', 'm:m')
)
```

---

## 4. Types of Joins Explained (With Diagrams)

Imagine two circles (Venn diagrams). The **left circle** is `df1`, the **right circle** is `df2`.

### Visual Summary

```
INNER JOIN:     LEFT JOIN:      RIGHT JOIN:     OUTER JOIN:
   ___             ___             ___             ___
  /   \           /   |           |   \           /     \___/           \___|           |___/           \___/
  (overlap)       (all left)      (all right)     (all both)
```

| Join Type | What It Returns                                      | Analogy                                                           |
| --------- | ---------------------------------------------------- | ----------------------------------------------------------------- |
| **Inner** | Only rows that exist in **both** tables              | "Show me customers who BOTH signed up AND placed an order"        |
| **Left**  | **All** rows from left + matching from right         | "Show me ALL customers, and their orders if they have any"        |
| **Right** | **All** rows from right + matching from left         | "Show me ALL orders, and customer info if available"              |
| **Outer** | **All** rows from **both** tables                    | "Show me everything — customers and orders, match where possible" |
| **Cross** | Every row from left paired with every row from right | "Create all possible combinations"                                |

---

## 5. Code Examples for Every Join Type

### Setup: Create Sample DataFrames

```python
import pandas as pd

# Customers DataFrame
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
})

# Orders DataFrame
orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105, 106],
    'customer_id': [1, 1, 2, 3, 3, 99],  # Note: 99 doesn't exist in customers
    'amount': [250, 180, 320, 150, 200, 500],
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB Cable', 'Headphones']
})

print("=== CUSTOMERS ===")
print(customers)
print("\n=== ORDERS ===")
print(orders)
```

**Output:**

```
=== CUSTOMERS ===
   customer_id     name         city
0            1    Alice     New York
1            2      Bob  Los Angeles
2            3  Charlie      Chicago
3            4    Diana      Houston
4            5      Eve      Phoenix

=== ORDERS ===
   order_id  customer_id  amount     product
0       101            1     250      Laptop
1       102            1     180       Mouse
2       103            2     320    Keyboard
3       104            3     150     Monitor
4       105            3     200   USB Cable
5       106           99     500  Headphones
```

---

### 5.1 INNER JOIN

**Returns only rows where the key exists in BOTH DataFrames.**

```python
# Inner Join: Only customers who have placed orders
inner_result = pd.merge(
    customers,
    orders,
    on='customer_id',
    how='inner'
)

print("=== INNER JOIN ===")
print(inner_result)
```

**Output:**

```
=== INNER JOIN ===
   customer_id     name         city  order_id  amount   product
0            1    Alice     New York       101     250    Laptop
1            1    Alice     New York       102     180     Mouse
2            2      Bob  Los Angeles       103     320  Keyboard
3            3  Charlie      Chicago       104     150   Monitor
4            3  Charlie      Chicago       105     200  USB Cable
```

**What happened?**

- Customer 4 (Diana) and 5 (Eve) are **excluded** — they have no orders.
- Order 106 is **excluded** — customer_id 99 doesn't exist in customers.
- Only the "overlap" remains.

**Business Use Case:** _"Show me only active customers who have made purchases in the last 30 days."_

---

### 5.2 LEFT JOIN

**Returns ALL rows from the left DataFrame, and matching rows from the right. Missing values become `NaN`.**

```python
# Left Join: All customers, with their orders if any
left_result = pd.merge(
    customers,
    orders,
    on='customer_id',
    how='left'
)

print("=== LEFT JOIN ===")
print(left_result)
```

**Output:**

```
=== LEFT JOIN ===
   customer_id     name         city  order_id  amount   product
0            1    Alice     New York     101.0   250.0    Laptop
1            1    Alice     New York     102.0   180.0     Mouse
2            2      Bob  Los Angeles     103.0   320.0  Keyboard
3            3  Charlie      Chicago     104.0   150.0   Monitor
4            3  Charlie      Chicago     105.0   200.0  USB Cable
5            4    Diana      Houston       NaN     NaN       NaN
6            5      Eve      Phoenix       NaN     NaN       NaN
```

**What happened?**

- All 5 customers are kept.
- Diana and Eve have `NaN` for order columns — they haven't ordered anything.
- Order 106 is excluded because its customer_id (99) isn't in the left table.

**Business Use Case:** _"Show me all customers and their total spend. Include customers with $0 spend for retention campaigns."_

---

### 5.3 RIGHT JOIN

**Returns ALL rows from the right DataFrame, and matching rows from the left. Missing values become `NaN`.**

```python
# Right Join: All orders, with customer info if available
right_result = pd.merge(
    customers,
    orders,
    on='customer_id',
    how='right'
)

print("=== RIGHT JOIN ===")
print(right_result)
```

**Output:**

```
=== RIGHT JOIN ===
   customer_id     name         city  order_id  amount     product
0            1    Alice     New York       101     250      Laptop
1            1    Alice     New York       102     180       Mouse
2            2      Bob  Los Angeles       103     320    Keyboard
3            3  Charlie      Chicago       104     150     Monitor
4            3  Charlie      Chicago       105     200   USB Cable
5           99      NaN          NaN       106     500  Headphones
```

**What happened?**

- All 6 orders are kept.
- Order 106 has `NaN` for name and city — the customer_id 99 wasn't found.
- Diana and Eve are excluded because they have no orders.

**Business Use Case:** _"Show me all transactions from the payment gateway and match them to our customer database. Flag unmatched transactions for fraud review."_

---

### 5.4 OUTER JOIN (FULL OUTER JOIN)

**Returns ALL rows from BOTH DataFrames. Missing values become `NaN` where there's no match.**

```python
# Outer Join: Everything from both tables
outer_result = pd.merge(
    customers,
    orders,
    on='customer_id',
    how='outer'
)

print("=== OUTER JOIN ===")
print(outer_result)
```

**Output:**

```
=== OUTER JOIN ===
   customer_id     name         city  order_id  amount     product
0            1    Alice     New York     101.0   250.0      Laptop
1            1    Alice     New York     102.0   180.0       Mouse
2            2      Bob  Los Angeles     103.0   320.0    Keyboard
3            3  Charlie      Chicago     104.0   150.0     Monitor
4            3  Charlie      Chicago     105.0   200.0   USB Cable
5            4    Diana      Houston       NaN     NaN         NaN
6            5      Eve      Phoenix       NaN     NaN         NaN
7           99      NaN          NaN     106.0   500.0  Headphones
```

**What happened?**

- Every row from both tables is included.
- Diana & Eve have `NaN` order data.
- Order 106 has `NaN` customer data.
- This gives you the **complete picture**.

**Business Use Case:** _"Reconcile our CRM database with our sales records. I need to see all customers AND all orders to identify data gaps."_

---

### 5.5 CROSS JOIN

**Returns the Cartesian product — every row from left paired with every row from right.**

```python
# Cross Join: All combinations
# Note: Use 'cross' with caution on large datasets!
small_df1 = pd.DataFrame({'A': ['X', 'Y']})
small_df2 = pd.DataFrame({'B': [1, 2, 3]})

cross_result = pd.merge(small_df1, small_df2, how='cross')

print("=== CROSS JOIN ===")
print(cross_result)
```

**Output:**

```
=== CROSS JOIN ===
   A  B
0  X  1
1  X  2
2  X  3
3  Y  1
4  Y  2
5  Y  3
```

**What happened?**

- 2 rows × 3 rows = 6 rows total.
- Every combination of A and B is created.

**Business Use Case:** _"Generate all possible product-bundle combinations to calculate pricing scenarios."_

---

## 6. `DataFrame.join()` vs `pd.merge()`

| Feature             | `pd.merge()`            | `DataFrame.join()`        |
| ------------------- | ----------------------- | ------------------------- |
| Primary use         | General-purpose merging | Joining on index          |
| Default join type   | `inner`                 | `left`                    |
| Join key            | Any column(s)           | Primarily index           |
| Multiple DataFrames | Two at a time           | Can join multiple at once |

### `join()` Example

```python
# join() is best when your DataFrames are indexed by the key

customers_indexed = customers.set_index('customer_id')
orders_indexed = orders.set_index('customer_id')

# Left join using join() — joins on index by default
joined_result = customers_indexed.join(
    orders_indexed,
    how='left',
    rsuffix='_order'  # suffix for overlapping columns
)

print("=== USING .join() ===")
print(joined_result)
```

**When to use which?**

- Use **`pd.merge()`** when joining on columns (most common).
- Use **`.join()`** when your data is already indexed by the join key, or when joining multiple DataFrames at once.

---

## 7. `pd.concat()` — Stacking DataFrames

`concat()` is for **stacking** DataFrames vertically or horizontally, not for relational joining.

### Vertical Concatenation (Stacking Rows)

```python
# Combining data from multiple months
jan_sales = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02'],
    'revenue': [1000, 1500]
})

feb_sales = pd.DataFrame({
    'date': ['2024-02-01', '2024-02-02'],
    'revenue': [1200, 1800]
})

# Stack them vertically
all_sales = pd.concat([jan_sales, feb_sales], axis=0, ignore_index=True)
print(all_sales)
```

### Horizontal Concatenation (Side by Side)

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'C': [5, 6], 'D': [7, 8]})

# Place them side by side
combined = pd.concat([df1, df2], axis=1)
print(combined)
```

**Key difference:** `concat()` doesn't match on keys — it just sticks DataFrames together. Use `merge()` for relational joins.

---

## 8. Handling Duplicate Column Names

When both DataFrames have columns with the same name (other than the join key), pandas adds suffixes.

```python
df1 = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'status': ['active', 'active', 'inactive']
})

df2 = pd.DataFrame({
    'id': [1, 2, 3],
    'department': ['IT', 'HR', 'Finance'],
    'status': ['senior', 'junior', 'senior']  # Same column name!
})

# Default suffixes: _x and _y
merged = pd.merge(df1, df2, on='id', how='inner')
print(merged)
```

**Output:**

```
   id     name  status_x department status_y
0   1    Alice    active         IT   senior
1   2      Bob    active         HR   junior
2   3  Charlie  inactive    Finance   senior
```

### Custom Suffixes

```python
merged = pd.merge(
    df1, df2, on='id', how='inner',
    suffixes=('_employee', '_role')
)
print(merged)
```

**Output:**

```
   id     name status_employee department status_role
0   1    Alice          active         IT      senior
1   2      Bob          active         HR      junior
2   3  Charlie        inactive    Finance      senior
```

---

## 9. Merging on Index

Sometimes your join key is the DataFrame index, not a column.

```python
# Set customer_id as index
customers_idx = customers.set_index('customer_id')
orders_idx = orders.set_index('customer_id')

# Merge on index
result = pd.merge(
    customers_idx,
    orders_idx,
    left_index=True,      # Use left DF's index
    right_index=True,     # Use right DF's index
    how='inner'
)

print(result)
```

Or more simply:

```python
result = customers_idx.join(orders_idx, how='inner')
```

---

## 10. Real-World Company Use Cases

### Use Case 1: E-Commerce — Customer Lifetime Value (CLV) Analysis

**Scenario:** An online retailer wants to calculate how much each customer has spent.

```python
# customer_profiles.csv: customer_id, name, signup_date, segment
# transactions.csv: transaction_id, customer_id, amount, date

# Load data
customers = pd.read_csv('customer_profiles.csv')
transactions = pd.read_csv('transactions.csv')

# Calculate total spend per customer
customer_spend = pd.merge(
    customers,
    transactions.groupby('customer_id')['amount'].sum().reset_index(),
    on='customer_id',
    how='left'
)

# Fill customers with no transactions as $0
customer_spend['amount'] = customer_spend['amount'].fillna(0)

# Identify high-value customers for VIP program
vip_customers = customer_spend[customer_spend['amount'] > 5000]
print(f"VIP customers to target: {len(vip_customers)}")
```

**Business Impact:** Marketing team sends personalized offers to VIP customers, increasing retention by 15%.

---

### Use Case 2: SaaS — Churn Prediction

**Scenario:** A SaaS company wants to predict which customers are likely to cancel.

```python
# users.csv: user_id, signup_date, plan_type
# activity_log.csv: user_id, date, login_count, feature_usage_score
# support_tickets.csv: user_id, ticket_id, severity

users = pd.read_csv('users.csv')
activity = pd.read_csv('activity_log.csv')
tickets = pd.read_csv('support_tickets.csv')

# Merge user data with activity
user_activity = pd.merge(users, activity, on='user_id', how='left')

# Count support tickets per user
ticket_counts = tickets.groupby('user_id').size().reset_index(name='ticket_count')

# Merge ticket counts
churn_dataset = pd.merge(user_activity, ticket_counts, on='user_id', how='left')
churn_dataset['ticket_count'] = churn_dataset['ticket_count'].fillna(0)

# Flag at-risk users: low activity + high support tickets
at_risk = churn_dataset[
    (churn_dataset['feature_usage_score'] < 10) &
    (churn_dataset['ticket_count'] > 3)
]
print(f"At-risk users for intervention: {len(at_risk)}")
```

**Business Impact:** Customer success team proactively reaches out to at-risk users, reducing churn by 20%.

---

### Use Case 3: Retail — Inventory & Sales Reconciliation

**Scenario:** A retail chain needs to match warehouse inventory with store sales.

```python
# inventory.csv: store_id, product_id, stock_level, warehouse_location
# sales.csv: store_id, product_id, units_sold, date
# stores.csv: store_id, region, manager_name

inventory = pd.read_csv('inventory.csv')
sales = pd.read_csv('sales.csv')
stores = pd.read_csv('stores.csv')

# Step 1: Merge inventory with sales
inventory_sales = pd.merge(
    inventory,
    sales.groupby(['store_id', 'product_id'])['units_sold'].sum().reset_index(),
    on=['store_id', 'product_id'],
    how='outer'  # Catch products with no sales AND sales with no inventory record
)

# Step 2: Add store information
full_view = pd.merge(inventory_sales, stores, on='store_id', how='left')

# Identify stockouts (sold more than in stock)
full_view['stockout_risk'] = full_view['units_sold'] > full_view['stock_level']

# Identify phantom inventory (stock exists but no sales for 90 days)
full_view['phantom_inventory'] = (
    (full_view['stock_level'] > 0) &
    (full_view['units_sold'].fillna(0) == 0)
)

print(full_view[['store_id', 'product_id', 'stockout_risk', 'phantom_inventory']].head())
```

**Business Impact:** Operations team optimizes stock levels, reducing stockouts by 30% and clearing $2M in dead inventory.

---

### Use Case 4: Finance — Anti-Money Laundering (AML)

**Scenario:** A bank needs to flag suspicious transactions by cross-referencing multiple data sources.

```python
# accounts.csv: account_id, customer_id, open_date, risk_score
# transactions.csv: transaction_id, account_id, amount, destination_account, timestamp
# watchlist.csv: account_id, flag_reason, date_added

accounts = pd.read_csv('accounts.csv')
transactions = pd.read_csv('transactions.csv')
watchlist = pd.read_csv('watchlist.csv')

# Step 1: Flag transactions from watchlisted accounts
flagged_transactions = pd.merge(
    transactions,
    watchlist[['account_id', 'flag_reason']],
    left_on='account_id',
    right_on='account_id',
    how='inner'  # Only keep transactions from flagged accounts
)

# Step 2: Add account risk scores
flagged_with_risk = pd.merge(
    flagged_transactions,
    accounts[['account_id', 'risk_score']],
    on='account_id',
    how='left'
)

# High-priority alerts
high_priority = flagged_with_risk[
    (flagged_with_risk['risk_score'] > 7) |
    (flagged_with_risk['amount'] > 100000)
]

print(f"High-priority AML alerts: {len(high_priority)}")
```

**Business Impact:** Compliance team reviews high-priority alerts first, improving detection speed and meeting regulatory requirements.

---

### Use Case 5: Healthcare — Patient Outcome Analysis

**Scenario:** A hospital wants to analyze treatment effectiveness by combining patient demographics, treatments, and outcomes.

```python
# patients.csv: patient_id, age, gender, diagnosis_date
# treatments.csv: patient_id, treatment_type, start_date, dosage
# outcomes.csv: patient_id, recovery_time_days, readmitted

patients = pd.read_csv('patients.csv')
treatments = pd.read_csv('treatments.csv')
outcomes = pd.read_csv('outcomes.csv')

# Combine all three datasets
step1 = pd.merge(patients, treatments, on='patient_id', how='inner')
full_data = pd.merge(step1, outcomes, on='patient_id', how='inner')

# Analyze treatment effectiveness
effectiveness = full_data.groupby('treatment_type').agg({
    'recovery_time_days': 'mean',
    'readmitted': 'mean'
}).round(2)

print("Treatment Effectiveness:")
print(effectiveness)
```

**Business Impact:** Hospital administration identifies the most effective treatment protocols, improving patient outcomes and reducing readmission rates.

---

## 11. Common Mistakes & How to Avoid Them

### Mistake 1: Accidentally Creating a Cartesian Product (Many-to-Many)

```python
# BAD: Duplicate keys in BOTH tables cause explosive row growth
df1 = pd.DataFrame({'key': [1, 1], 'val': ['A', 'B']})
df2 = pd.DataFrame({'key': [1, 1], 'val': ['X', 'Y']})

# This creates 4 rows (2 x 2) instead of 2!
result = pd.merge(df1, df2, on='key')
print(result)  # 4 rows!
```

**Fix:** Use `validate` parameter to catch this.

```python
# This will raise an error if many-to-many merge occurs
try:
    result = pd.merge(df1, df2, on='key', validate='one_to_one')
except Exception as e:
    print(f"Merge validation failed: {e}")
```

---

### Mistake 2: Forgetting to Handle Missing Values After Left/Outer Joins

```python
merged = pd.merge(customers, orders, on='customer_id', how='left')

# BAD: NaN values will break calculations
# total = merged['amount'].sum()  # Works, but risky

# GOOD: Explicitly handle NaNs
merged['amount'] = merged['amount'].fillna(0)
merged['product'] = merged['product'].fillna('No Purchase')
```

---

### Mistake 3: Joining on the Wrong Column

```python
# BAD: Joining on 'id' when one table uses 'customer_id' and other uses 'user_id'
# result = pd.merge(df1, df2, on='id')  # Wrong!

# GOOD: Use left_on and right_on
result = pd.merge(df1, df2, left_on='customer_id', right_on='user_id')
```

---

### Mistake 4: Not Checking Row Count Before and After Merge

```python
print(f"Before merge: {len(df1)} rows")
result = pd.merge(df1, df2, on='key', how='inner')
print(f"After merge: {len(result)} rows")

# If row count explodes, you likely have duplicate keys!
```

---

### Mistake 5: Silent Data Loss with Inner Joins

```python
# Inner join silently drops non-matching rows!
# If you expected 1000 customers but only get 800, 200 were dropped.

# GOOD: Use indicator to see what was lost
result = pd.merge(df1, df2, on='key', how='outer', indicator=True)
print(result['_merge'].value_counts())
# Output: both 800, left_only 150, right_only 50
```

---

## 12. Quick Reference Cheat Sheet

```python
import pandas as pd

# ============================================
# CHEAT SHEET: Pandas Joins & Merges
# ============================================

# --- BASIC MERGES ---
pd.merge(df1, df2, on='key', how='inner')        # Keep only matches
pd.merge(df1, df2, on='key', how='left')         # Keep all from df1
pd.merge(df1, df2, on='key', how='right')        # Keep all from df2
pd.merge(df1, df2, on='key', how='outer')        # Keep all from both
pd.merge(df1, df2, how='cross')                  # Cartesian product

# --- MULTIPLE KEYS ---
pd.merge(df1, df2, on=['key1', 'key2'])

# --- DIFFERENT COLUMN NAMES ---
pd.merge(df1, df2, left_on='col_a', right_on='col_b')

# --- MERGE ON INDEX ---
pd.merge(df1, df2, left_index=True, right_index=True)

# --- CUSTOM SUFFIXES ---
pd.merge(df1, df2, on='key', suffixes=('_left', '_right'))

# --- ADD SOURCE INDICATOR ---
pd.merge(df1, df2, on='key', how='outer', indicator=True)

# --- VALIDATE MERGE TYPE ---
pd.merge(df1, df2, on='key', validate='one_to_one')   # 1:1
pd.merge(df1, df2, on='key', validate='one_to_many')  # 1:m
pd.merge(df1, df2, on='key', validate='many_to_one')  # m:1

# --- JOIN (Index-based) ---
df1.join(df2, how='left', rsuffix='_right')

# --- CONCAT (Stacking) ---
pd.concat([df1, df2], axis=0)   # Stack rows (vertical)
pd.concat([df1, df2], axis=1)   # Stack columns (horizontal)

# --- FILL NA AFTER JOIN ---
merged = pd.merge(df1, df2, how='left')
merged.fillna({'amount': 0, 'status': 'Unknown'}, inplace=True)
```

---

## Summary Table

| Join Type | Keeps Left        | Keeps Right      | Use When...                                 |
| --------- | ----------------- | ---------------- | ------------------------------------------- |
| `inner`   | Only matches      | Only matches     | You only care about complete data           |
| `left`    | All               | Only matches     | Left table is your "master" dataset         |
| `right`   | Only matches      | All              | Right table is your "master" dataset        |
| `outer`   | All               | All              | You need the complete picture, no data loss |
| `cross`   | All (× all right) | All (× all left) | You need all combinations                   |

---

> **Remember:** The art of data merging is knowing which questions you're trying to answer. The join type you choose directly shapes the story your data tells.

**Happy Merging! 🐼**
