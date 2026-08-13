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
