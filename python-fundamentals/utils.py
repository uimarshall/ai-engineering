def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b


def power(a, b):
    return a**b


def square(a):
    return a**2


def say_hello():
    print("Hello from the main function!")


print("This is the utils.py file, and it has been imported successfully!")
print(
    __name__
)  # This will print the name of the module, which is 'utils' when imported, and '__main__' when run directly.
print(
    __name__ == "__main__"
)  # This will print True if the file is run directly, and False if it is imported as a module.


def main():
    print(
        "Hello from inside the main function!, but only if this file is run directly from the utils.py file"
    )


if __name__ == "__main__":
    main()
