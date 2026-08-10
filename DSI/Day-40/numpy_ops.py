# -*- coding: utf-8 -*-

import numpy as np

my_1d_array = np.array([4,2,3])

type(my_1d_array)

my_1d_array.shape

my_1d_array[0]

my_1d_array[0:2]

my_1d_array[-1]

my_2d_array = np.array([[1,2,3,4,5],[6,7,8,9,10]])
print(my_2d_array)

# The shape is 2 rows & 5 cols

my_2d_array.shape

# First row

my_2d_array[0]

# Second row

my_2d_array[1]

# First row - second element

my_2d_array[0][1] # first method

my_2d_array[0,1] # second method

# second row - 3rd element

my_2d_array[1,2] # 8

# slicing

# 1st array slice 1 to 3

my_2d_array[0:1,1:3]

# slice a portion of the 2 arrays

my_2d_array[0:2,1:3]

# 3 dimensional arrays of zeroes and ones

np.zeros(3)
# 3x3 shape
np.zeros((3,3))

# 3x3x3 containing element 1

np.ones((3,3,3))

# specify shape and the elements(5)

np.full((3,3), 5)

# 1 dimensional array using arange

np.arange(10)
np.arange(2,10)
np.arange(2,10,2)

# This can be used to plot a linear graph- 20 nums spaced evenly from 1-5

np.linspace(1, 5, 20)

float_array = np.linspace(1, 5, 20)

# round to 2 dp.

np.round(float_array,2)

# create array of random nums

np.random.rand(5)

# 5 rows 2 cols

np.random.rand(5,2)

# 100 random int numbers between 20 and 80

np.random.randint(20,80,100)

# randint of shape 10x10

np.random.randint(20,80,(10,10))

# Reshaping an array

my_1d_array = np.random.randint(20,80,100)

# reshape to 2x2

my_2d_array = my_1d_array.reshape(10,10)

print(my_2d_array)

