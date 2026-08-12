# Manipulating NumPy Arrays — A Beginner's Guide

NumPy is Python's library for working with **arrays** — fast, memory-efficient collections of numbers. Almost everything in data science (pandas, scikit-learn, TensorFlow) builds on NumPy, so learning to manipulate arrays is a core skill.

---

## 1. First Things First — Importing NumPy

```python
import numpy as np
```

By convention, we import NumPy as `np` so the code stays short.

---

## 2. Creating Arrays

| Function        | What it does                       | Example                                          |
| --------------- | ---------------------------------- | ------------------------------------------------ |
| `np.array()`    | Create from a Python list          | `np.array([1, 2, 3])`                            |
| `np.zeros()`    | Array of zeros                     | `np.zeros((2, 3))` → 2×3 grid of 0.0             |
| `np.ones()`     | Array of ones                      | `np.ones((2, 2))`                                |
| `np.arange()`   | Like `range()`, but gives an array | `np.arange(0, 10, 2)` → `[0 2 4 6 8]`            |
| `np.linspace()` | Evenly spaced numbers              | `np.linspace(0, 1, 5)` → `[0. 0.25 0.5 0.75 1.]` |
| `np.random`     | Random numbers                     | `np.random.rand(3)` → 3 random values            |

```python
a = np.array([1, 2, 3, 4])          # 1-D array
b = np.array([[1, 2], [3, 4]])      # 2-D array (matrix)
c = np.zeros((2, 3))                # 2 rows, 3 columns of zeros
d = np.arange(1, 13)                # [1 2 3 ... 12]

print(b)
# [[1 2]
#  [3 4]]
```

---

## 3. Array Attributes — Know Your Array

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print(arr.shape)      # (2, 3)  → 2 rows, 3 columns
print(arr.ndim)       # 2       → number of dimensions
print(arr.size)       # 6       → total elements
print(arr.dtype)      # int64   → data type of elements
print(arr.itemsize)   # 8       → bytes per element
```

> **Tip:** `shape` is the single most useful attribute. Everything else (reshaping, broadcasting) depends on it.

---

## 4. Indexing and Slicing

NumPy indexing is like list indexing, but with **one index per dimension**.

```python
arr = np.array([[10, 20, 30],
                [40, 50, 60]])

print(arr[0, 1])      # 20   → row 0, column 1
print(arr[1])         # [40 50 60]  → entire row 1
print(arr[1, :])      # same as above, ':' means "all columns"
print(arr[:, 2])      # [30 60]  → entire column 2

# Slicing
print(arr[:, 0:2])    # first two columns of every row
# [[10 20]
#  [40 50]]

# Negative indexing (from the end)
print(arr[-1, -1])    # 60 → last row, last column
```

### ⚠️ Important: Views vs. Copies

Slicing returns a **view** — it points to the same data. Changing it changes the original!

```python
sub = arr[:, 0]       # view of column 0
sub[0] = 999
print(arr)            # original ALSO changed!
# [[999  20  30]
#  [ 40  50  60]]
```

To get an independent copy, use `.copy()`:

```python
sub = arr[:, 0].copy()
sub[0] = 0            # original stays unchanged
```

---

## 5. Reshaping — Changing the Shape

```python
arr = np.arange(1, 13)        # [1 2 ... 12]

# Reshape into 3 rows × 4 columns
m = arr.reshape(3, 4)
print(m)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]

# Use -1 to let NumPy figure out a dimension
print(arr.reshape(2, -1))     # → 2 rows, 6 columns (auto)

# Flatten a 2-D array back into 1-D
print(m.flatten())            # [1 2 3 ... 12]

# Transpose: swap rows and columns
print(m.T)                    # becomes 4 rows × 3 columns

# Add a new axis (useful for broadcasting)
col = np.array([1, 2, 3])
print(col[:, np.newaxis])     # turns into a column vector
```

> `reshape` must match the total number of elements. `12` elements → `(3, 4)` works, but `(5, 3)` would raise an error.

---

## 6. Combining and Splitting Arrays

### Combining (joining)

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.concatenate([a, b]))        # [1 2 3 4 5 6]

x = np.array([[1, 2]])
y = np.array([[3, 4]])

print(np.vstack([x, y]))             # stack vertically (rows)
# [[1 2]
#  [3 4]]

print(np.hstack([x, y]))             # stack horizontally (columns)
# [[1 2 3 4]]
```

### Splitting

```python
arr = np.arange(1, 11)               # [1 2 ... 10]

left, right = np.split(arr, [5])     # split after index 5
print(left)   # [1 2 3 4 5]
print(right)  # [6 7 8 9 10]
```

---

## 7. Arithmetic — Element-wise by Default

Unlike Python lists, NumPy operations apply **element by element**:

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

print(a + b)      # [11 22 33]
print(a * b)      # [10 40 90]
print(a ** 2)     # [1 4 9]
print(a + 100)    # [101 102 103]  (scalar broadcasts)

# Comparison gives boolean arrays
print(a > 1)      # [False  True  True]
```

### Broadcasting — different shapes, same operation

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])
col = np.array([10, 20])          # one value per row

print(m + col[:, np.newaxis])     # add a column to each row
# [[11 12 13]
#  [24 25 26]]
```

---

## 8. Aggregations — Summarizing Data

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])

print(arr.sum())          # 21          → total of all elements
print(arr.mean())         # 3.5         → average
print(arr.min())          # 1
print(arr.max())          # 6

# Along one axis:
print(arr.sum(axis=0))    # [5 7 9]     → column sums
print(arr.sum(axis=1))    # [6 15]      → row sums

# Cumulative sum
print(np.cumsum(np.array([1, 2, 3])))   # [1 3 6]
```

---

## 9. Filtering with Boolean Masks

A **mask** is a boolean array used to pick elements:

```python
arr = np.array([5, 12, 3, 18, 7])

mask = arr > 10
print(mask)                 # [False  True False  True False]
print(arr[mask])            # [12 18]  → filtered values

# One-liner:
print(arr[arr > 10])        # [12 18]
print(arr[(arr > 5) & (arr < 15)])   # [12 7]

# Using np.where to get indices
print(np.where(arr > 10))   # (array([1, 3]),)  → index positions
```

---

## 10. Adding and Removing Elements

```python
arr = np.array([1, 2, 3])

# Append / insert / delete (returns a NEW array)
print(np.append(arr, 4))            # [1 2 3 4]
print(np.insert(arr, 1, 99))        # [1 99 2 3]
print(np.delete(arr, 0))            # [2 3]

# Unique values and sorting
nums = np.array([3, 1, 2, 1, 3])
print(np.unique(nums))              # [1 2 3]
print(np.sort(nums))                # [1 1 2 3 3]

# Sorting a 2-D array by a column
data = np.array([[3, 9],
                 [1, 5],
                 [2, 7]])
print(data[data[:, 0].argsort()])   # sort rows by column 0
# [[1 5]
#  [2 7]
#  [3 9]]
```

---

## 11. Quick Cheat Sheet

| Task         | Code                                      |
| ------------ | ----------------------------------------- |
| Create array | `np.array([...])`                         |
| Get shape    | `arr.shape`                               |
| Reshape      | `arr.reshape(r, c)`                       |
| Flatten      | `arr.flatten()`                           |
| Transpose    | `arr.T`                                   |
| Stack        | `np.vstack([a, b])` / `np.hstack([a, b])` |
| Join 1-D     | `np.concatenate([a, b])`                  |
| Sum          | `arr.sum()` or `arr.sum(axis=0)`          |
| Filter       | `arr[arr > 10]`                           |
| Find index   | `np.where(arr > 10)`                      |
| Sort         | `np.sort(arr)`                            |
| Unique       | `np.unique(arr)`                          |
| Safe copy    | `arr.copy()`                              |

---

## 12. Common Beginner Mistakes

1. **Confusing shape with size** — `shape` is the dimensions, `size` is the total count.
2. **Slicing creates a view** — if you don't want side effects, use `.copy()`.
3. **Using `=` instead of `.copy()`** — `b = a` just makes another name for the _same_ array.
4. **Forgetting axis meaning** — `axis=0` goes _down_ rows, `axis=1` goes _across_ columns.
5. **Mixing Python lists and arrays** — `[1, 2, 3] * 2` repeats the list; `np.array([1, 2, 3]) * 2` multiplies each element.

```python
# The copy pitfall
a = np.array([1, 2, 3])
b = a                # NOT a copy!
b[0] = 999
print(a)             # [999 2 3]  ← original changed!
```

---

**Next steps:** practice by creating a random array with `np.random.rand(5, 5)` and try reshaping, filtering, and summing it along both axes. Then move on to pandas, which uses NumPy arrays under the hood.
