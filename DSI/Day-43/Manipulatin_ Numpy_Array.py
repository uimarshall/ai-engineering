# -*- coding: utf-8 -*-
# Import the numpy library and give it the short nickname "np" so we can use it easily
import numpy as np

# Create a 1-dimensional array (a simple list) of 10 items, all set to 0.0 (zeros)
my_1d_array = np.zeros(10)

# Print the array to the screen so we can see it
print(my_1d_array)

# Change the value at position 0 (the very first item) to 50
my_1d_array[0] = 50
# Print the array again to see the change (first item is now 50)
print(my_1d_array)

# Change the values at positions 3, 4, and 5 (slice 3:6 means "from index 3 up to but NOT including index 6") to 50
my_1d_array[3:6] = 50
# Print the array again to see the changes
print(my_1d_array)

# Find the positions (indexes) of all items in the array that are equal to 50
# (Note: the result is not stored or printed here, so nothing shows on screen)
np.where(my_1d_array == 50)

# Create a 2-dimensional array (like a table with rows and columns) from a list of lists
# Row 1 = [1, 5, 9], Row 2 = [8, 5, 5]
my_2d_array = np.array([[1, 5, 9], [8, 5, 5]])
# Print the 2D array so we can see the table
print(my_2d_array)

# Find the positions of all items that are equal to 5
np.where(my_2d_array == 5)
# Find the positions of all items that are less than 5
np.where(my_2d_array < 5)
# Find the positions of all items that are greater than or equal to 5
np.where(my_2d_array >= 5)
# Find the positions of all items that are less than or equal to 5
np.where(my_2d_array <= 5)
# Find the positions of all items that are NOT equal to 5
np.where(my_2d_array != 5)

# Similar to np.where, but returns the positions as (row, column) pairs, which is easier to read for 2D arrays
np.argwhere(my_2d_array == 5)

# Find the positions of all items greater than 5 and save the result in a variable called "index"
index = np.where(my_2d_array > 5)
# Print those positions (e.g., which rows and which columns)
print(index)

# Use the saved positions to look up the actual values at those spots (the values that are greater than 5)
my_2d_array[index]

# Use the saved positions to CHANGE all those values (the ones greater than 5) to 100
my_2d_array[index] = 100
# Print the 2D array again to see the updated values
print(my_2d_array)

# Check if ALL items in the 1D array are "truthy" (non-zero). Returns False because the array still contains some zeros
np.all(my_1d_array)

# Check if ALL items in the array are greater than or equal to 0. Returns True
np.all(my_1d_array >= 0)
# Check if ALL items in the array are greater than 5. Returns False (some are 0)
np.all(my_1d_array > 5)

# Check if AT LEAST ONE item in the array is "truthy" (non-zero). Returns True because there are some 50s
np.any(my_1d_array)

# combining arrays

# Create a 2x2 array (2 rows, 2 columns) called "a"
a = np.array([[1, 2], [3, 4]])

# Create another 2x2 array called "b"
b = np.array([[5, 6], [7, 8]])
# Print array "a"
print(a)
# Print array "b"
print(b)

# Stack the two arrays vertically (place "b" directly below "a") to make one bigger 4x2 array
v = np.vstack(((a, b)))
# Print the combined array so we can see the result
print(v)

np.vstack((a, b, a, b))

# Horizontal stack

h = np.hstack(((a, b)))
print(h)

np.hstack((a, b, a, b))

print(my_2d_array)
my_2d_array.flatten()


# ============================================================
# NUMPY STACKING & FLATTENING — EXPLAINED FOR BEGINNERS
# ============================================================

# Before we can stack anything, we need arrays to stack.
# A 1D NumPy array is like a list of numbers.

a = np.array([1, 2, 3])  # first array  -> [1 2 3]
b = np.array([4, 5, 6])  # second array -> [4 5 6]

# ------------------------------------------------------------
# VERTICAL STACK (vstack) — stacks arrays ON TOP of each other
# ------------------------------------------------------------
# np.vstack((a, b, a, b)) stacks the arrays as ROWS, one below the other.
# The result is a 2D array with 4 rows and 3 columns:
#   [1 2 3]   <- a
#   [4 5 6]   <- b
#   [1 2 3]   <- a again
#   [4 5 6]   <- b again
np.vstack((a, b, a, b))
# ⚠️ IMPORTANT: this line alone does NOT save the result anywhere!
# The stacked array is created and then immediately thrown away,
# because nothing is assigned to a variable. To keep it, you'd write:
#   result = np.vstack((a, b, a, b))
# ...and then use `result` later in your code.

# ------------------------------------------------------------
# HORIZONTAL STACK (hstack) — stacks arrays SIDE BY SIDE
# ------------------------------------------------------------
# hstack joins arrays along the columns (left to right),
# producing ONE single row (1D array).
h = np.hstack(((a, b)))  # <-- the DOUBLE parentheses are a common beginner trap!
print(h)  # prints: [1 2 3 4 5 6]
# Why does it still work? ((a, b)) is just a tuple (a, b) wrapped in
# one extra pair of parentheses — valid but unnecessary.
# The cleaner version is:  h = np.hstack((a, b))

# Same operation again, but this time WITHOUT saving to a variable.
# Just like the vstack line above, the result is computed and discarded,
# so you won't see any output from this line.
np.hstack((a, b, a, b))
# (If saved, the result would be: [1 2 3 4 5 6 1 2 3 4 5 6])

# ------------------------------------------------------------
# FLATTEN — turns a 2D array into a single 1D row
# ------------------------------------------------------------
print(my_2d_array)  # shows the 2D array, for example:
# [[1 2 3]
#  [4 5 6]]

my_2d_array.flatten()  # creates a NEW 1D copy: [1 2 3 4 5 6]
# ⚠️ IMPORTANT: flatten() does NOT modify the original array —
# it returns a brand-new array. To keep the flattened version,
# you must assign it:
#   flat = my_2d_array.flatten()
# (If you instead want a flattened "view" that shares memory with the
# original, use my_2d_array.ravel() — but for beginners, flatten() is
# usually the safer choice.)

"""
**Key takeaways for a beginner:**
1. **`vstack` = vertical** (stacks rows on top of each other → more rows)
2. **`hstack` = horizontal** (stacks columns side by side → wider row)
3. **`flatten()` doesn't change the original array** — always assign its result to a variable if you want to use it.
4. **Undefined names** — in your original snippet, `a`, `b`, and `my_2d_array` were never created, so running it would raise a `NameError`. The setup lines I added at the top fix that.
"""
