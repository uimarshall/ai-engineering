# Decorators

# What is a decorator?
# A decorator is a design pattern in Python that allows you to modify the behavior of a function or class. Decorators are a powerful tool that can be used to add functionality to existing code in a clean and readable way. They are often used for logging, access control, memoization, and other cross-cutting concerns.

# Real-world uses of a decorator:
# - Logging: Decorators can be used to log the execution of functions, including their input arguments and return values.

# @require_auth (checks if the user is authenticated before allowing access to a function)

# @validate_input (validates the input arguments of a function before executing it)

# @precondition_check (checks if certain conditions are met before executing a function)

# @preprocess_data (preprocesses the input data before passing it to a function)
# - Access control: Decorators can be used to restrict access to certain functions based on user roles or permissions.


def penalty_kick_decorator(func):
    def wrapper(*args, **kwargs):
        print("Preparing for the penalty kick...")
        result = func(*args, **kwargs)
        print("Penalty kick completed!")
        return result

    return wrapper


@penalty_kick_decorator
def penalty_kick(player_name):
    print(f"{player_name} is taking the penalty kick!")
    return f"Goal scored by {player_name}!"


def main():
    # Example usage of the decorated function
    print("\n--- Penalty Kick Decorator Example ---")
    result = penalty_kick("Alice")
    print(result)

    # Example of a simple decorator that logs the execution of a function
    def log_decorator(func):
        def wrapper(*args, **kwargs):
            print(
                f"Executing {func.__name__} with arguments: {args} and keyword arguments: {kwargs}"
            )
            result = func(*args, **kwargs)
            print(f"{func.__name__} returned: {result}")
            return result

        return wrapper

    @log_decorator
    def add(x, y):
        return x + y

    @log_decorator
    def multiply(x, y):
        return x * y

    # Example usage of the decorated functions
    print("\n--- Decorator Example ---")
    add_result = add(5, 3)
    multiply_result = multiply(4, 2)


if __name__ == "__main__":
    main()
