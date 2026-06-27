# This function returns multiple values as a Tuple
def get_geo_coordinates():
    x = 2
    y = 5
    return x, y


coordinates = get_geo_coordinates()
print(coordinates)  # Output: (2, 5) - returns a Tuple
print(*coordinates)  # Output: 2 5 - unpacks the Tuple into separate values
x, y = get_geo_coordinates()  # Unpacks the returned Tuple into variables x and y
print(f"X: {x}, Y: {y}")  # Output: X: 2, Y: 5

# Using return to break out of a function early
age = int(input("Enter your age: "))


def content_moderation(age):
    if age < 18:
        return  # Early return if the user is a minor - breaks out of the function immediately - No need for else block.
    print(f"Welcome! You are {age} years old and can view the content.")


result = content_moderation(
    age
)  # If age < 18, the function will return None and not print the welcome message. If age >= 18, it will print the welcome message.
print(
    result
)  # Output: None if age < 18, otherwise it will print the welcome message and then print None.

# If age is 18 or more: it prints the welcome message, then ends.

# When a function ends without returning something, Python automatically returns `None`. This is why we see `None` when we print the result of `content_moderation(age)` if the age is less than 18 and also at the end in the terminal if the age is 18 or more.

"""
Python None vs JavaScript null and undefined:

In simple terms:

Python None is the “no value” object in Python.
JavaScript null is an explicit “no value” in JS.
JavaScript also has undefined, which means “not set” or “missing.”
So:

None is closest to JS null.
But Python combines ideas that JS splits into null and undefined.
Example idea:

Python function with no return gives None.
JavaScript function with no return gives undefined."""
