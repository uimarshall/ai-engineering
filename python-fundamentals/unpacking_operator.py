# use *args, and **kwargs to unpack arguments in function calls.

# use *args,  to accept any number of positional arguments in function calls.

# use **kwargs (key word arguments) to accept any number of keyword arguments in function calls.
#
# *args — arbitrary positional arguments. The * is the unpacking operator; args is just a convention. It collects extra positional arguments into a tuple.
# **kwargs — arbitrary keyword arguments. The ** unpacks mappings; kwargs is convention. It collects extra keyword arguments into a dict.
# =============================================================================
# *args  -> arbitrary positional arguments  (collected into a TUPLE)
# **kwargs -> arbitrary keyword arguments   (collected into a DICT)
#
# The names "args" and "kwargs" are conventions; the * and ** are what matter.
# =============================================================================


# -----------------------------------------------------------------------------
# 1. Basic *args — accept any number of positional arguments
# -----------------------------------------------------------------------------
def add(*args):
    print(
        "Received args:", args, "(type:", type(args), ")-packed into a tuple"
    )  # args is a tuple of all positional arguments, e.g. (1, 2, 3) - this is just a regular tuple, you can iterate over it, index it, etc.
    # Tuple = packed state;
    # we can unpack it with * when calling another function, e.g. sum(*args) would unpack the tuple into individual arguments for sum()
    print(
        "Received unpacked args into a list:",
        *args,
        "- unpacked into individual arguments and printed as a list",
        "type:",
        type(args),
    )  # This will unpack the tuple into individual arguments, which will be printed as a list
    return sum(args)


print(add(1, 2))  # 3
print(add(1, 2, 3, 4, 5))  # 15


# -----------------------------------------------------------------------------
# 2. Basic **kwargs — accept any number of keyword arguments
# -----------------------------------------------------------------------------
def greet(**kwargs):
    print(
        "Received kwargs:", kwargs
    )  # kwargs is a dict of all keyword arguments,kwargs always return a dict: e.g. {'name': 'Alice', 'age': 30, 'city': 'New York'}
    print("Type of kwargs:", type(kwargs))
    # kwargs.items(): always returns a view of the dictionary's items, which is an iterable of (key, value) pairs. It does not return a list, but you can convert it to a list if needed, e.g. list(kwargs.items()) would give you a list of tuples.
    for key, value in kwargs.items():
        print(f"{key}: {value}")


greet(name="Alice", age=30, city="New York")
# name: Alice
# age: 30
# city: New York


# -----------------------------------------------------------------------------
# 3. Combining normal params, *args, and **kwargs
#    Order rule: positional -> *args -> keyword-only -> **kwargs
# -----------------------------------------------------------------------------
def describe(title, *args, separator="-", **kwargs):
    print(f"\n{title}")
    print(separator * 20)
    print("Positional extras:", args)
    print("Keyword extras:   ", kwargs)


describe("Report", "item1", "item2", separator="=", author="Bob", year=2024)
# Report
# ====================
# Positional extras: ('item1', 'item2')
# Keyword extras:    {'author': 'Bob', 'year': 2024}


# -----------------------------------------------------------------------------
# 4. Forwarding / passing args and kwargs to another function
# -----------------------------------------------------------------------------
def log(func, *args, **kwargs):
    print(f"Calling {func.__name__} ...")
    result = func(*args, **kwargs)
    print(f"Result: {result}")
    return result


def multiply(a, b):
    return a * b


log(multiply, 4, 5)  # Calling multiply ... Result: 20


# -----------------------------------------------------------------------------
# 5. Unpacking a list/tuple into a function with *
# -----------------------------------------------------------------------------
def power(base, exponent):
    return base**exponent


values = [2, 10]
print(power(*values))  # 1024  — same as power(2, 10)


# -----------------------------------------------------------------------------
# 6. Unpacking a dict into a function with **
# -----------------------------------------------------------------------------
def create_user(name, role, active):
    return {"name": name, "role": role, "active": active}


config = {"name": "Carol", "role": "admin", "active": True}
user = create_user(**config)
print(user)  # {'name': 'Carol', 'role': 'admin', 'active': True}


# -----------------------------------------------------------------------------
# 7. Merging lists/tuples with *
# -----------------------------------------------------------------------------
first = [1, 2, 3]
second = [4, 5, 6]
merged = [*first, *second]
print(merged)  # [1, 2, 3, 4, 5, 6]


# -----------------------------------------------------------------------------
# 8. Merging dicts with **  (Python 3.5+)
# -----------------------------------------------------------------------------
defaults = {"theme": "dark", "lang": "en", "debug": False}
overrides = {"lang": "pt", "debug": True}
final_config = {**defaults, **overrides}
print(final_config)  # {'theme': 'dark', 'lang': 'pt', 'debug': True}


# -----------------------------------------------------------------------------
# 9. *args in a class constructor — flexible initialisation
# -----------------------------------------------------------------------------
class ShoppingCart:
    def __init__(self, owner, *items):
        self.owner = owner
        self.items = list(items)
        print("Received items:", items)  # items is a tuple of all positional arguments

    def add(self, *new_items):
        self.items.extend(new_items)
        print(
            "Added items:", new_items
        )  # new_items is a tuple of all positional arguments

    def __repr__(self):
        return f"Cart({self.owner}): {self.items}"


cart = ShoppingCart("Alice", "apple", "bread")
cart.add("milk", "eggs")
print(cart)  # Cart(Alice): ['apple', 'bread', 'milk', 'eggs']


# -----------------------------------------------------------------------------
# 10. **kwargs for optional configuration / builder pattern
# -----------------------------------------------------------------------------
def build_query(table, **filters):
    conditions = " AND ".join(f"{k}='{v}'" for k, v in filters.items())
    query = f"SELECT * FROM {table}"
    if conditions:
        query += f" WHERE {conditions}"
    return query


print(build_query("users"))
# SELECT * FROM users

print(build_query("users", role="admin", active="true"))
# SELECT * FROM users WHERE role='admin' AND active='true'


# -----------------------------------------------------------------------------
# 11. Decorator pattern — the classic *args/**kwargs use case
# -----------------------------------------------------------------------------
import time


def timer(func):
    def wrapper(*args, **kwargs):  # captures ANY call signature
        start = time.perf_counter()
        result = func(*args, **kwargs)  # forwards everything unchanged
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result

    return wrapper


@timer
def slow_add(a, b):
    time.sleep(0.01)
    return a + b


slow_add(3, 7)  # slow_add took 0.01xxxx s


# -----------------------------------------------------------------------------
# 12. Extended iterable unpacking with * in assignments
# -----------------------------------------------------------------------------
first, *middle, last = [10, 20, 30, 40, 50]
print(first)  # 10
print(middle)  # [20, 30, 40]
print(last)  # 50


# =============================================================================
# QUICK REFERENCE
# =============================================================================
# Symbol  | In function DEFINITION       | In function CALL
# --------|------------------------------|---------------------------------
# *args   | collect extra positionals    | unpack list/tuple into args
# **kwargs| collect extra keywords       | unpack dict into keyword args
# * (assign) | catch middle elements     | N/A
# =============================================================================
