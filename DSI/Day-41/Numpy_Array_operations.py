# -*- coding: utf-8 -*-  # Tells Python this file uses UTF-8 text encoding (so special characters work correctly)

# Import the NumPy library and give it the short nickname "np" so we can type less
import numpy as np

# Generate 16 random integers btw 2 & 8

my_1d_array = np.random.randint(
    2, 8, 16
)  # Create a 1-D array (list) of 16 random whole numbers from 2 (included) up to 8 (excluded)

# Find max value in the array

np.max(
    my_1d_array
)  # Find the largest value in the array (method 1: using the np.max function)

# Another method

my_1d_array.max()  # Find the largest value in the array (method 2: calling .max() directly on the array itself)

my_1d_array.min()  # Find the smallest value in the array
my_1d_array.mean()  # Calculate the average (mean) of all the values in the array
my_1d_array.sum()  # Add up all the values in the array and return the total
my_1d_array.std()  # Calculate the standard deviation (how spread out the values are from the average)

# Reshape to 4x4

my_2d_array = my_1d_array.reshape(
    4, 4
)  # Rearrange the 16 values from the 1-D array into a 2-D grid with 4 rows and 4 columns
print(my_2d_array)  # Display the new 4x4 grid on the screen

my_2d_array.max()  # Find the largest value in the whole 4x4 grid
my_2d_array.max(
    axis=0
)  # Find the largest value of each COLUMN (axis=0 means compare down the rows)
my_2d_array.max(
    axis=1
)  # Find the largest value of each ROW (axis=1 means compare across the columns)
my_2d_array.min(axis=0)  # Find the smallest value of each COLUMN

# Get the index

my_2d_array.argmax(
    axis=0
)  # Find the POSITION (row index) of the largest value in each column
my_2d_array.argmax(
    axis=1
)  # Find the POSITION (column index) of the largest value in each row

np.sort(
    my_1d_array
)  # Sort the 1-D array in ascending order (from smallest to largest value)

# Math Operations on numpy array

a = np.array([1, 2, 3, 4, 5])  # Create a 1-D array containing the numbers 1, 2, 3, 4, 5

# Add 10 to each element of the array

a + 10  # Add 10 to EVERY element -> [11, 12, 13, 14, 15]
a - 10  # Subtract 10 from EVERY element -> [-9, -8, -7, -6, -5]
a * 10  # Multiply EVERY element by 10 -> [10, 20, 30, 40, 50]
a / 10  # Divide EVERY element by 10 -> [0.1, 0.2, 0.3, 0.4, 0.5]

# Adding corresponding elements of a to b

b = np.array(
    [5, 4, 7, 3, 1]
)  # Create a second 1-D array with the numbers 5, 4, 7, 3, 1

a + b  # Add the two arrays ELEMENT BY ELEMENT (1+5, 2+4, 3+7, ...) -> [6, 6, 10, 7, 6]

a = np.array([-2, -1, 0, 1, 2])  # Replace array "a" with new values: -2, -1, 0, 1, 2

np.square(
    a
)  # Square EVERY element (each value raised to the power of 2) -> [4, 1, 0, 1, 4]
np.sqrt(
    a
)  # Take the square root of EVERY element (note: square roots of negative numbers give NaN with a warning)
np.sign(a)  # Show the sign of each element: -1 for negative, 0 for zero, 1 for positive

np.sin(a)  # Calculate the sine of each element (values are treated as radians)
np.cos(a)  # Calculate the cosine of each element (values are treated as radians)
np.tan(a)  # Calculate the tangent of each element (values are treated as radians)

a = np.array([1, 2, 3])  # Create array "a" with the values 1, 2, 3
b = np.array([4, 5, 6])  # Create array "b" with the values 4, 5, 6

# Dot product
np.dot(
    a, b
)  # Compute the dot product: multiply matching elements and add the results: (1*4) + (2*5) + (3*6) = 32
