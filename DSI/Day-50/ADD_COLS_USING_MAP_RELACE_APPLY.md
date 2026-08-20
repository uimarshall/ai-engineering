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
