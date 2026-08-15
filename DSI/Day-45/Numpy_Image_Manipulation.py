# -*- coding: utf-8 -*-
# Declares the file encoding as UTF-8, ensuring special characters are handled correctly.

import matplotlib.pyplot as plt
import numpy as np
from skimage import io

# Imports matplotlib's plotting module, aliased as plt, for displaying images.


# Imports the NumPy library, aliased as np, for numerical operations on arrays.

# Imports the 'io' module from scikit-image, which provides functions for reading and saving images.

camaro = io.imread("camaro.jpg")
# Reads the image file "camaro.jpg" from disk and loads it as a NumPy array into the variable 'camaro'.

print(camaro)
# Prints the raw NumPy array data to the console, showing the pixel values.

# structure of the image. This is just a collection of an array showing different intensities of the colour
# A comment explaining that the image is fundamentally a numerical array of colour intensities.

camaro.shape  # output (1200, 1600, 3)
# Accesses the 'shape' attribute of the array, which returns a tuple describing its dimensions.
# For this image, it means: 1200 rows (height), 1600 columns (width), and 3 colour channels (RGB).

# This tells us we have 1200 rows of pixel and 1600 cols of pixel and 3 shows it's a 3d array.
# The 3d further shows it is a coloured image.
# The image has an intensity which is an int value between 0-255 for each of the colour channel (RGB)
# Comments explaining that the 3 dimensions confirm it's a colour image,
# where each pixel's R, G, and B values range from 0 (dark) to 255 (bright).

plt.imshow(camaro)
# Displays the loaded image array using matplotlib's imshow() function.

plt.show()
# Renders and opens a window to actually display the image on screen.

# cropping the image with slice (y is cropped first)
# A comment indicating that cropping will begin by slicing the vertical (y) axis first.

cropped = camaro[0:500, :, :]  # 3d cropping (y,x,z dimensions)
# Crops the image by slicing the array:
# - Rows 0 to 499 (the top 500 pixels of height)
# - All columns (:)
# - All 3 colour channels (:)
# This keeps the full width but removes the bottom portion of the image.

plt.imshow(cropped)
# Displays the newly cropped image.

plt.show()
# Renders the cropped image in a window.

# crop x-horizontal
# A comment indicating the next crop will slice the horizontal (x) axis.

cropped = camaro[:, 400:1000, :]  # 3d cropping (y,x,z dimensions)
# Crops the image by slicing:
# - All rows (:)
# - Columns 400 to 999 (a horizontal slice in the middle)
# - All colour channels (:)
# This keeps the full height but trims the left and right edges.

plt.imshow(cropped)
# Displays the horizontally cropped image.

plt.show()
# Renders the image window.

# crop the vehicle
# A comment indicating the next crop will isolate the car itself.

cropped = camaro[350:1100, 200:1400, :]
# Crops a specific rectangular region:
# - Rows 350 to 1099 (vertical slice targeting the car)
# - Columns 200 to 1399 (horizontal slice targeting the car)
# - All colour channels (:)

plt.imshow(cropped)
# Displays the vehicle-cropped image.

plt.show()
# Renders the image window.

# Save image to disk
# A comment indicating the next step is file output.

io.imsave("camaro_cropped.jpg", cropped)
# Saves the current 'cropped' array to disk as a JPEG file named "camaro_cropped.jpg".

# Flip our image
# A comment introducing image flipping operations.

vertical_flip = camaro[::-1, :, :]
# Flips the image vertically (upside down) using NumPy slice notation:
# - ::-1 reverses the order of rows (y-axis)
# - : keeps all columns as-is
# - : keeps all colour channels as-is

plt.imshow(vertical_flip)
# Displays the vertically flipped image.

plt.show()
# Renders the flipped image.

io.imsave("camaro_vertical_flip.jpg", vertical_flip)
# Saves the vertically flipped image to disk.

horizontal_flip = camaro[:, ::-1, :]
# Flips the image horizontally (mirror image) using NumPy slice notation:
# - : keeps all rows as-is
# - ::-1 reverses the order of columns (x-axis)
# - : keeps all colour channels as-is

plt.imshow(horizontal_flip)
# Displays the horizontally flipped (mirrored) image.

plt.show()
# Renders the mirrored image.

io.imsave("camaro_horizontal_flip.jpg", horizontal_flip)
# Saves the horizontally flipped image to disk.

# Colour channels
# A comment introducing the section on isolating individual RGB colour channels.

# create an array which is the exact dimension of our camaro image
# A comment explaining the next step.

red = np.zeros(camaro.shape, dtype="uint8")
# Creates a new NumPy array filled entirely with zeros,
# with the exact same shape as the original 'camaro' image.
# dtype="uint8" sets the data type to unsigned 8-bit integer (0-255), matching image standards.

# Fill in values for only the red channel and leave the other channels az zeros
# A comment explaining the purpose of the next line.

red[:, :, 0] = camaro[:, :, 0]
# Copies only the RED channel (index 0) from the original image into the new array.
# The green (index 1) and blue (index 2) channels remain zero, so they appear black.

plt.imshow(red)
# Displays the red-channel-only image (appears red and black).

plt.show()
# Renders the red channel image.

# Green
# A comment indicating the next channel to isolate.

green = np.zeros(camaro.shape, dtype="uint8")
# Creates another zero-filled array with the same dimensions as the original image.

# Fill in values for only the red channel and leave the other channels az zeros
# A comment (with a typo — should say "green channel") explaining the approach.

green[:, :, 1] = camaro[:, :, 1]
# Copies only the GREEN channel (index 1) from the original image.
# The red (index 0) and blue (index 2) channels remain zero.

plt.imshow(green)
# Displays the green-channel-only image (appears green and black).

plt.show()
# Renders the green channel image.

# Blue
# A comment indicating the next channel to isolate.

blue = np.zeros(camaro.shape, dtype="uint8")
# Creates a third zero-filled array with the same dimensions.

# Fill in values for only the red channel and leave the other channels az zeros
# A comment (again with a typo — should say "blue channel").

blue[:, :, 2] = camaro[:, :, 2]
# Copies only the BLUE channel (index 2) from the original image.
# The red (index 0) and green (index 1) channels remain zero.

plt.imshow(blue)
# Displays the blue-channel-only image (appears blue and black).

plt.show()
# Renders the blue channel image.

# Vertically stack the 3 images on each other
# A comment introducing the final composition step.

camaro_rainbow = np.vstack((red, green, blue))
# Stacks the three channel-isolated images vertically (one on top of the other)
# using NumPy's vstack() function.
# The result is a tall image with red on top, green in the middle, and blue at the bottom.

plt.imshow(camaro_rainbow)
# Displays the vertically stacked composite image.

plt.show()
# Renders the final rainbow-stacked image.

io.imsave("camaro_rainbow.jpg", camaro_rainbow)
# Saves the stacked image to disk as "camaro_rainbow.jpg".


# Quick Reference Summary
"""

| Code | What It Does |
|------|-------------|
| `camaro[0:500, :, :]` | Crop top 500 pixels (height) |
| `camaro[:, 400:1000, :]` | Crop middle columns (width) |
| `camaro[::-1, :, :]` | Flip vertically (upside down) |
| `camaro[:, ::-1, :]` | Flip horizontally (mirror) |
| `camaro[:, :, 0]` | Red channel |
| `camaro[:, :, 1]` | Green channel |
| `camaro[:, :, 2]` | Blue channel |
| `np.vstack((a, b, c))` | Stack arrays vertically |
"""
