# -*- coding: utf-8 -*-
import numpy as np

radii = np.array([2439.7, 6051.8, 6371, 3389.7, 69911, 58232, 25362, 24622])

# Formula for vol of a sphere => V = 4/3 * πr3

r = 10
volume = 4 / 3 * np.pi * r**3
print(volume)

volumes = 4 / 3 * np.pi * radii**3
print(volumes)

radii = np.random.randint(1, 1000, 1000000)


volumes = 4 / 3 * np.pi * radii**3
print(volumes)


# -*- coding: utf-8 -*-
# This line tells Python which character encoding to use for the file.
# "utf-8" supports almost every character/symbol in the world (like π and é).

import numpy as np

# This imports the NumPy library and gives it the short nickname "np".
# NumPy is a powerful toolbox for working with numbers and arrays efficiently.

radii = np.array([2439.7, 6051.8, 6371, 3389.7, 69911, 58232, 25362, 24622])
# Creates a NumPy "array" (a list of numbers) holding the radius of each planet in km.
# The order is: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.

# Formula for vol of a sphere => V = 4/3 * πr3
# A comment explaining the math: volume of a sphere = four-thirds times pi times radius cubed.
# (Note: this comment applies to the whole section, not just the next line.)

r = 10
# Creates a variable named "r" and stores the number 10 in it (a test radius).

volume = 4 / 3 * np.pi * r**3
# Calculates the volume of a sphere with radius 10.
# - "4 / 3" is the fraction four-thirds
# - "np.pi" is the value of π (about 3.14159) provided by NumPy
# - "r**3" means r raised to the power of 3 (r × r × r)
# The result is saved in a variable called "volume".

print(volume)
# Displays the calculated volume on the screen (about 4188.79).

volumes = 4 / 3 * np.pi * radii**3
# Calculates the volume for EVERY radius in the "radii" array at once.
# NumPy does this "element-wise" — it applies the formula to each of the 8 numbers.
# The result is a new array of 8 volumes, stored in a variable called "volumes".

print(volumes)
# Prints all 8 planet volumes to the screen at once.

radii = np.random.randint(1, 1000, 1000000)
# Replaces the old "radii" array with a brand-new one.
# np.random.randint(1, 1000, 1000000) generates 1,000,000 random whole numbers
# between 1 and 999 (the top value 1000 is excluded).

volumes = 4 / 3 * np.pi * radii**3
# Same volume formula as before, but now applied to all 1 million random radii.
# NumPy handles this huge calculation very fast — that's one of its biggest strengths!

print(volumes)
# Prints all 1 million calculated volumes to the screen.
# (This will flood your console with numbers — that's expected!)
