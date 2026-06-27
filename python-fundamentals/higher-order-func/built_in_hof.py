# Built-in HOF

# 1. map() - applies a function to all items in an iterable and returns a map object (which is an iterator).

punches = [1, 2, 3, 4, 5]


def magnify_punches(punch):
    return punch * 10


# The `map()` function applies the `magnify_punches` function to each item in the `punches` list, resulting in a new list of "heavy punches."
heavy_punches = map(magnify_punches, punches)
print(type(heavy_punches))  # <class 'map'>
# To see the results, we can convert the map object to a list.
heavy_punches_list = list(heavy_punches)

print("\n--- Map Example ---")
print("Original punches:", punches)
print("Heavy punches   :", heavy_punches_list)

# 2. filter() - filters items in an iterable based on a function that returns True or False

scores = [55, 65, 75, 85, 95]


# The `filter()` function applies the `is_distinction` function to each item in the `scores` list, returning only those scores that meet the distinction criteria (i.e., scores >= 75).
def is_distinction(score):
    return score >= 75


# Only scores that are 75 or above will return True and will be included in the result.
distinctions = filter(is_distinction, scores)
distinctions_list = list(distinctions)

print("\n--- Filter Example ---")
print("Original scores :", scores)
print("Scores with Distinctions    :", distinctions_list)
