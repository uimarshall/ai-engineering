x = 20
print("Global variable x before modification (global scope):", x)

# Constants are typically defined at the module level and are not meant to be changed. They are often written in uppercase letters to indicate that they are constants. For example:
PI = 3.14159
SPEED_OF_LIGHT = 299792458  # in meters per second


# A function that modifies the global variable 'x' using the 'global' keyword


def modify_global_x():
    global x  # This tells Python that we want to use the global variable 'x'
    x = 30  # Modifying the global variable 'x'
    PI = 3.14  # This is a local variable that shadows the global constant PI
    print(
        "Inside modify_global_x, PI:", PI
    )  # This will print the local variable PI, not the global constant
    print("Inside modify_global_x (local scope), x:", x)


modify_global_x()
print(
    "Outside modify_global_x (global changes), x:", x
)  # This will reflect the modified value of x


print("********************" * 2)

print("Demonstrating nested functions and variable scope:")

print("********************" * 2)


def outer_function():
    y = 10
    PI = 3.14  # This is a local variable that shadows the global constant PI
    print("Inside outer_function, x:", x)
    print("Inside outer_function before variable modification, y:", y)

    def inner_function():
        # This allows us to modify the 'y' variable from the outer function by using the 'nonlocal' keyword
        nonlocal y
        # Modifying the 'y' variable from the outer function
        y = 15
        z = 5
        print("Inside inner_function, x:", x)
        print("Inside inner_function, y:", y)
        print("Inside inner_function, z:", z)

    inner_function()
    print("Inside outer_function after inner_function modification, y:", y)


outer_function()
