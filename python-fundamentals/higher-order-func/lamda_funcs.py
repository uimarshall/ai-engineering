# Lambda Functions
# ─────────────────────────────────────────────────────────────

# What is a lambda function?
# A lambda function is a small anonymous function defined using the `lambda` keyword. It can take any number of arguments but can only have one expression. The expression is evaluated and returned when the lambda function is called.


def main():

    def add(x, y):
        return x + y

    # The above function can be rewritten as a lambda function:
    # The function is defined using the `lambda` keyword, followed by the parameters `x` and `y`, a colon, and the expression `x + y`.
    # Takes two arguments x and y, and returns their sum.
    add_lambda = lambda x, y: x + y

    # Example usage of the lambda function
    result = add_lambda(5, 3)
    print("\n--- Lambda Function Example ---")
    print("Result of add_lambda(5, 3):", result)  # Output: 8

    # Using lambda functions with built-in HOFs like map and filter
    numbers = [1, 2, 3, 4, 5]

    # The lambda function takes one argument x and returns its square.
    find_squares = lambda x: x**2

    # Using map with a lambda function to square each number
    squared_numbers = list(map(find_squares, numbers))
    print("\n--- Map with Lambda ---")
    print("Original numbers:", numbers)
    print("Squared numbers :", squared_numbers)

    # The lambda function takes one argument x and returns True if x is even, otherwise False.
    is_even = lambda x: x % 2 == 0

    # Using filter with a lambda function to get even numbers
    even_numbers = list(filter(is_even, numbers))
    print("\n--- Filter with Lambda ---")
    print("Original numbers:", numbers)
    print("Even numbers   :", even_numbers)

    # Using sorted with a lambda function as the key to sort by absolute value
    unsorted = [-5, 3, -1, 4, -2]
    sorted_by_abs = sorted(unsorted, key=lambda x: abs(x))
    print("\n--- Sorted with Lambda ---")
    print("Original list  :", unsorted)
    print("Sorted by abs  :", sorted_by_abs)

    # Using reduce with a lambda function to find the product of all numbers
    from functools import reduce

    product = reduce(lambda acc, x: acc * x, numbers)
    print("\n--- Reduce with Lambda ---")
    print("Numbers        :", numbers)
    print("Product        :", product)


if __name__ == "__main__":
    main()
