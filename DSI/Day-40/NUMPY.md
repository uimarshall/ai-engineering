# NUMPY

Fast numerical computing in Python and its use cases.

> NumPy (Numerical Python) — the `ndarray`, vectorized operations, and why it's the foundation of data science in Python.

> NumPy is the **fundamental package for scientific computing** in Python. It provides the fast, memory-efficient `ndarray` object for working with large, multi-dimensional arrays — the backbone of pandas, scikit-learn, TensorFlow, and most AI/ML libraries.

---

## 1. What is NumPy?

- **Description**: NumPy is a Python library for numerical computing. Its core is the `ndarray` — an N-dimensional array that stores elements of the **same type** in contiguous memory, making operations 10–100x faster than pure Python lists.
- **Uses**: Math/statistics on large datasets, image processing, machine learning, simulations, and linear algebra — anywhere you crunch numbers fast.
- **Core idea**: Instead of looping over elements, NumPy applies operations to the **whole array at once** (vectorization).
- **Why not lists?** Python lists store pointers to objects scattered in memory; NumPy arrays store raw numbers contiguously — faster and far less memory.

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)        # [ 2  4  6  8 10] — no loop needed!
```

---

## 2. Installation & Import

```bash
pip install numpy
```

```python
import numpy as np      # the universal convention

print(np.__version__)   # e.g. '1.26.4'
```

---

## 3. Creating Arrays

### From Python lists

```python
a = np.array([1, 2, 3])              # 1D array
b = np.array([[1, 2], [3, 4]])       # 2D array (matrix)
print(a)   # [1 2 3]
print(b)   # [[1 2]
           #  [3 4]]
```

### Built-in creators

```python
np.zeros((2, 3))          # 2x3 array of 0.0
np.ones(3)                # [1. 1. 1.]
np.full((2, 2), 7)        # 2x2 filled with 7
np.arange(0, 10, 2)       # [0 2 4 6 8] — like range()
np.linspace(0, 1, 5)      # [0.   0.25 0.5  0.75 1.  ] — 5 evenly spaced
np.eye(3)                 # 3x3 identity matrix
np.random.rand(2, 2)      # random floats in [0, 1)
```

---

## 4. Array Attributes

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)    # (2, 3)  — rows, columns
print(arr.ndim)     # 2       — number of dimensions
print(arr.size)     # 6       — total elements
print(arr.dtype)    # int64   — data type of elements
```

---

## 5. Indexing & Slicing

Works like Python lists, extended to multiple dimensions.

```python
a = np.array([10, 20, 30, 40, 50])

print(a[0])         # 10
print(a[-1])        # 50
print(a[1:4])       # [20 30 40]

m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print(m[1, 2])      # 6       — row 1, column 2
print(m[0])         # [1 2 3] — entire first row
print(m[:, 1])      # [2 5 8] — entire second column
print(m[:2, 1:])    # [[2 3]
                    #  [5 6]] — sub-matrix
```

> **Note**: NumPy slices are **views**, not copies — modifying a slice changes the original array! Use `.copy()` if you need independence.

---

## 6. Vectorized Operations & Broadcasting

Operations apply element-by-element — no loops.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])

print(a + b)        # [11 22 33]
print(a * b)        # [10 40 90]
print(a ** 2)       # [1 4 9]
print(a + 100)      # [101 102 103] — scalar broadcast to all elements
```

### Broadcasting example (use case: centering data)

```python
data = np.array([[1, 2, 3],
                 [4, 5, 6]])

mean = data.mean(axis=0)      # column means: [2.5 3.5 4.5]
centered = data - mean        # broadcasts the (3,) row across both rows
print(centered)
# [[-1.5 -1.5 -1.5]
#  [ 1.5  1.5  1.5]]
```

---

## 7. Math & Statistics Functions

```python
arr = np.array([1, 2, 3, 4, 5])

print(arr.sum())     # 15
print(arr.mean())    # 3.0
print(arr.std())     # 1.4142135623730951
print(arr.max())     # 5
print(arr.min())     # 1
print(arr.argmax())  # 4 — index of the max value

# Axis-aware (use case: per-row / per-column stats)
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print(m.sum(axis=0))   # [5 7 9] — per column
print(m.sum(axis=1))   # [ 6 15] — per row
```

### Universal functions (ufuncs) — fast element-wise math

```python
x = np.array([0, 1, 4, 9])
print(np.sqrt(x))          # [0. 1. 2. 3.]
print(np.exp([0, 1]))      # [1.         2.71828183]
print(np.log([1, np.e]))   # [0. 1.]
```

---

## 8. Reshaping & Stacking

```python
a = np.arange(6)            # [0 1 2 3 4 5]
m = a.reshape(2, 3)         # 2 rows x 3 columns
print(m)
# [[0 1 2]
#  [3 4 5]]

print(m.flatten())          # back to 1D: [0 1 2 3 4 5]
print(m.T)                  # transpose: rows become columns

# Stacking arrays
x = np.array([1, 2])
y = np.array([3, 4])
print(np.vstack([x, y]))    # [[1 2]
                            #  [3 4]] — stack row-wise
print(np.hstack([x, y]))    # [1 2 3 4] — side by side
```

---

## 9. Boolean Indexing (Filtering)

One of the most powerful features — filter data with conditions, no loops.

```python
scores = np.array([55, 72, 90, 41, 88])

# Keep only passing scores (>= 50)
passed = scores[scores >= 50]
print(passed)                 # [55 72 90 88]

# Replace values conditionally (use case: clean bad sensor readings)
data = np.array([10, 999, 30, 999, 50])
clean = np.where(data == 999, 0, data)
print(clean)                  # [10  0 30  0 50]

# Count matches
print((scores >= 80).sum())   # 2
```

---

## 10. Common Use Cases

### Use case 1: Data analysis — quick statistics

```python
temperatures = np.array([22.5, 24.0, 19.8, 23.3, 25.1])
print(f"Average: {temperatures.mean():.1f} C")        # Average: 22.9 C
print(f"Coldest day: day {temperatures.argmin() + 1}")  # Coldest day: day 3
```

### Use case 2: Image processing (images ARE arrays!)

A grayscale image is just a 2D array of pixel values (0–255).

```python
image = np.random.randint(0, 256, size=(100, 100))
brightened = np.clip(image + 50, 0, 255)   # increase brightness, cap at 255
inverted = 255 - image                     # negative of the image
print(image.shape)                         # (100, 100)
```

### Use case 3: Machine learning — vector math

```python
# Dot product: prediction = inputs . weights
inputs = np.array([1.5, 2.0, 3.0])
weights = np.array([0.2, 0.4, 0.1])
prediction = inputs @ weights        # same as np.dot(inputs, weights)
print(round(prediction, 1))          # 1.4
```

### Use case 4: Simulation — Monte Carlo

```python
rng = np.random.default_rng(seed=42)
dice_rolls = rng.integers(1, 7, size=10_000)
print(f"P(rolling a 6) ~ {(dice_rolls == 6).mean():.3f}")   # ~ 0.163 (theory: 1/6 = 0.167)
```

### Use case 5: Linear algebra — solving equations

```python
# Solve:  2x + y = 5
#          x + 3y = 10
A = np.array([[2, 1],
              [1, 3]])
b = np.array([5, 10])

x = np.linalg.solve(A, b)
print(x)                      # [1. 3.] — x=1, y=3
```

---

## 11. NumPy Array vs Python List

| Feature       | Python list                | NumPy array                  |
| ------------- | -------------------------- | ---------------------------- |
| Element types | Mixed types allowed        | Single type (`dtype`)        |
| Speed         | Slow (Python loops)        | Fast (C underneath)          |
| Memory        | High (object overhead)     | Low (contiguous storage)     |
| Math ops      | `[1,2] * 2` → `[1,2,1,2]`  | `arr * 2` → element-wise     |
| Best for      | General-purpose storage    | Numerical data & computation |

---

## 12. Common Pitfalls

| Pitfall                                                        | Fix                                                        |
| -------------------------------------------------------------- | ---------------------------------------------------------- |
| Expecting slices to be copies (they're **views**)              | Use `arr[a:b].copy()` when you need independence           |
| Mixing types — one string turns the whole array into strings   | Keep arrays numeric: `np.array([1, 2, 3])` not `[1, "2"]`  |
| `list * 2` repeats but `array * 2` multiplies                  | Remember operators are element-wise on arrays              |
| Shape mismatch errors when broadcasting                        | Check `.shape` of both arrays before operating             |
| `reshape()` total size must match element count                | Use `reshape(-1, n)` to auto-infer one dimension           |
| Forgetting `axis` — `sum()` flattens everything                | Use `axis=0` (per column) or `axis=1` (per row) explicitly |
| Integer arrays can't hold `NaN` or float results               | Create with `dtype=float` when you expect decimals/NaN     |
| Using legacy `np.random.*` functions in new code               | Prefer `rng = np.random.default_rng()` for reproducibility |

---

## 13. Quick Reference

```python
import numpy as np

# Creation
np.array([1, 2, 3])              # from a list
np.zeros((2, 3)); np.ones(3)     # pre-filled arrays
np.arange(0, 10, 2)              # range-like
np.linspace(0, 1, 5)             # evenly spaced values

# Attributes
arr.shape; arr.ndim; arr.dtype; arr.size

# Indexing & filtering
arr[1:4]; m[1, 2]; m[:, 0]; arr[arr > 5]

# Math
arr + 10; arr * arr2; arr.sum(); arr.mean(axis=0)
np.sqrt(arr); arr @ weights      # matrix/vector multiply

# Shape
arr.reshape(2, 3); arr.flatten(); arr.T

# Random
rng = np.random.default_rng(42)
rng.integers(1, 10, size=5); rng.random((2, 2))
```

---

> **Key Takeaway**: NumPy is the foundation of numerical computing in Python. Its `ndarray` replaces slow Python loops with **vectorized operations** that run at C speed — `arr * 2` instead of `[x * 2 for x in arr]`. Master the essentials: **create** arrays (`array`, `arange`, `linspace`, `zeros`), **inspect** them (`shape`, `dtype`, `ndim`), **index and slice** them (including boolean masks for filtering), run **math and stats** with `axis` control, and use **broadcasting** to combine arrays of different shapes. Whether you're analyzing data, processing images, training ML models, or running simulations, NumPy is almost always the first import — and pandas, scikit-learn, and TensorFlow are all built on top of it.


