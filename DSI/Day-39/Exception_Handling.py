# Exception Handling in Python
# Demonstrates handling different error types with a practical age-input program.

# ---------------------------------------------------------------------------
# Example 1: Basic age input with ValueError handling
# input() always returns a string, so int() can raise a ValueError.
# ---------------------------------------------------------------------------

age = input("Enter your age: ")

try:
    age = int(age)  # may raise ValueError if the user didn't type a number
except ValueError as e:
    print("ValueError:", e)
    print("Please enter a valid number for your age.")
else:
    print(f"Your age is {age}.")
finally:
    print("Age input attempt finished.")

# ---------------------------------------------------------------------------
# Example 2: Loop until the user enters a valid age (validation loop)
# Keeps asking until a valid number between 0 and 120 is given.
# ---------------------------------------------------------------------------

while True:
    try:
        age = int(input("Enter your age: "))  # may raise ValueError
        if 0 <= age <= 120:
            break
        print("Age must be between 0 and 120.")
    except ValueError:
        print("That's not a valid number. Please try again.")

print(f"Age set to {age}.")

# ---------------------------------------------------------------------------
# Example 3: Applying age-based content moderation with early return
# ---------------------------------------------------------------------------


def content_moderation(age):
    if age < 18:
        return "Sorry, this content is for adults only."
    return f"Welcome! You are {age} years old and can view the content."


try:
    age = int(input("Enter your age: "))  # may raise ValueError
except ValueError:
    print("Invalid age entered.")
else:
    print(content_moderation(age))

# ---------------------------------------------------------------------------
# Example 4: Handling multiple error types (TypeError and ZeroDivisionError)
# ---------------------------------------------------------------------------

try:
    age = int(input("Enter your age: "))  # may raise ValueError
    result = 100 / age  # may raise ZeroDivisionError
except ValueError:
    print("ValueError: Please enter a number.")
except ZeroDivisionError:
    print("ZeroDivisionError: Age cannot be zero in this calculation.")
else:
    print(f"100 divided by your age is {result:.2f}.")

# ---------------------------------------------------------------------------
# Example 5: Raising a custom error with raise
# ---------------------------------------------------------------------------


def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    return age


try:
    age = int(input("Enter your age: "))  # may raise ValueError
    set_age(age)
except ValueError as e:
    print("Caught:", e)
else:
    print(f"Valid age: {age}")
