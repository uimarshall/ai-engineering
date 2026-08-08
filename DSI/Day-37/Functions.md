# FUNCTIONS

Reusable blocks of code in Python and their use cases.

> Python functions — definition, arguments, return values, scope, lambdas, higher-order functions, closures, decorators, recursion, and more.

> A function is a **named, reusable block of code** that performs a specific task. You define it once and call it as many times as you like.

---

## 1. What is a Function?

- **Description**: A function is a block of organized, reusable code that runs only when it is called. It can take **inputs** (arguments), perform work, and optionally **return** a result.
- **Uses**: Avoiding repetition (DRY — Don't Repeat Yourself), breaking complex problems into smaller steps, organizing code, testing logic in isolation, and building reusable utilities.
- **Core idea**: Write the logic **once**, then call it by name wherever you need it — with different inputs each time.
- **Syntax**: `def function_name(parameters):` followed by an indented block of statements.
- **Calling a function**: `function_name(arguments)` — the parentheses are what actually execute the function.

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))   # Hello, Alice!
print(greet("Bob"))     # Hello, Bob!
```

---

## 2. Defining & Calling Functions

### Basic definition

```python
def say_hello():
    print("Hello world!")

say_hello()          # Hello world!
say_hello()          # Hello world!  (call it again)
```

### With parameters and return

```python
def add(a, b):
    result = a + b
    return result

total = add(3, 5)
print(total)         # 8
```

### Docstrings — documenting the function

```python
def multiply(a, b):
    """Multiply two numbers and return the product."""
    return a * b

print(multiply.__doc__)   # Multiply two numbers and return the product.
help(multiply)            # shows the docstring in the interactive help
```

> **Note**: The function body is only executed when the function is **called** — defining it does nothing by itself.

---

## 3. Arguments vs Parameters

- **Parameter**: the name used inside the function definition (the "slot").
- **Argument**: the actual value you pass when calling the function.

```python
def subtract(a, b):   # a and b are parameters
    return a - b

print(subtract(10, 4))   # 10 and 4 are arguments  -> 6
```

### Positional arguments

Arguments are matched to parameters **by position** (left to right).

```python
def describe(name, age, city):
    print(f"{name} is {age} years old and lives in {city}.")

describe("Alice", 30, "Nairobi")
# Alice is 30 years old and lives in Nairobi.
```

### Keyword arguments

You can pass arguments by name — order no longer matters.

```python
describe(city="Nairobi", age=30, name="Alice")
# Alice is 30 years old and lives in Nairobi.
```

### Default parameter values

Parameters can have defaults, making them optional.

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))            # Hello, Alice!
print(greet("Bob", "Hi"))        # Hi, Bob!
print(greet("Carol", greeting="Hey"))   # Hey, Carol!
```

### Parameter ordering rules

Positional (required) → default parameters → `*args` → keyword-only → `**kwargs`.

```python
def order_demo(a, b=2, *args, flag=True, **kwargs):
    print("a:", a, "| b:", b, "| args:", args, "| flag:", flag, "| kwargs:", kwargs)

order_demo(1, 3, 4, 5, flag=False, name="x")
# a: 1 | b: 3 | args: (4, 5) | flag: False | kwargs: {'name': 'x'}
```

---

## 4. Return Values

### Single return value

```python
def square(x):
    return x ** 2

print(square(5))     # 25
```

### Multiple return values (a tuple)

Python functions can return several values at once — they come back as a **tuple**.

```python
def get_geo_coordinates():
    x = 2
    y = 5
    return x, y

coordinates = get_geo_coordinates()
print(coordinates)        # (2, 5)  — a tuple

x, y = get_geo_coordinates()   # unpack into separate variables
print(f"X: {x}, Y: {y}")       # X: 2, Y: 5
```

### Early `return` — break out of a function

`return` exits the function immediately. This lets you avoid nested `else` blocks.

```python
def content_moderation(age):
    if age < 18:
        return                    # early return -> None, nothing else runs
    print(f"Welcome! You are {age} years old and can view the content.")

content_moderation(15)            # prints nothing
content_moderation(21)            # Welcome! You are 21 years old and can view the content.
```

### Implicit `None`

If a function ends without a `return`, Python automatically returns `None` (the "no value" object).

```python
def do_nothing():
    pass

print(do_nothing())    # None

result = content_moderation(15)
print(result)          # None
```

> **Python `None` vs JavaScript**: Python's `None` is closest to JS `null` (explicit "no value"). JS also has `undefined` ("not set"). A Python function with no `return` gives `None` — like a JS function giving `undefined`.

---

## 5. `*args` and `**kwargs`

Tools for functions that accept a **variable number** of arguments.

### `*args` — arbitrary positional arguments (collected into a **tuple**)

```python
def add(*args):
    print("args:", args, "| type:", type(args))   # args is a tuple
    return sum(args)

print(add(1, 2))              # 3
print(add(1, 2, 3, 4, 5))     # 15
```

### `**kwargs` — arbitrary keyword arguments (collected into a **dict**)

```python
def greet(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

greet(name="Alice", age=30, city="Nairobi")
# name: Alice
# age: 30
# city: Nairobi
```

### Unpacking a list/dict into a call with `*` and `**`

The same symbols **unpack** a collection when calling a function.

```python
def power(base, exponent):
    return base ** exponent

values = [2, 10]
print(power(*values))          # 1024  — same as power(2, 10)

def create_user(name, role, active):
    return {"name": name, "role": role, "active": active}

config = {"name": "Carol", "role": "admin", "active": True}
print(create_user(**config))   # {'name': 'Carol', 'role': 'admin', 'active': True}
```

### Merging collections with `*` and `**`

```python
first = [1, 2, 3]
second = [4, 5, 6]
print([*first, *second])       # [1, 2, 3, 4, 5, 6]

defaults = {"theme": "dark", "lang": "en", "debug": False}
overrides = {"lang": "pt", "debug": True}
print({**defaults, **overrides})   # {'theme': 'dark', 'lang': 'pt', 'debug': True}
```

### Quick reference

| Symbol     | In function **definition**            | In function **call**                                                    |
| ---------- | ------------------------------------- | ----------------------------------------------------------------------- |
| `*args`    | collect extra positional args (tuple) | unpack list/tuple into positional args                                  |
| `**kwargs` | collect extra keyword args (dict)     | unpack dict into keyword args                                           |
| `*`        | —                                     | extended iterable unpacking in assignment (`first, *mid, last = [...]`) |

---

## 6. Variable Scope

Where a variable is **visible** depends on where it is defined.

### Local scope

Variables defined inside a function are **local** — they don't exist outside.

```python
def my_func():
    local_var = 10
    return local_var

print(my_func())          # 10
# print(local_var)        # NameError: local_var is not defined
```

### Global scope

Variables defined at the top level of a file are **global** and readable anywhere.

```python
x = 20
print("Global x:", x)     # Global x: 20

def show_x():
    print("Inside function, x:", x)   # can READ global x

show_x()                  # Inside function, x: 20
```

### The `global` keyword — modify a global inside a function

```python
x = 20

def modify_global_x():
    global x              # tell Python to use the global x
    x = 30

modify_global_x()
print("After modification, x:", x)   # After modification, x: 30
```

### Constants convention

Constants are defined at module level, written in **UPPERCASE**, and not meant to be changed.

```python
PI = 3.14159
SPEED_OF_LIGHT = 299792458   # meters per second

def circle_area(radius):
    return PI * radius ** 2

print(circle_area(2))        # 12.56636
```

### `nonlocal` — modify an outer (enclosing) function's variable

Used inside **nested functions** to modify a variable from the enclosing scope.

```python
def outer_function():
    y = 10

    def inner_function():
        nonlocal y            # allow modifying y from outer_function
        y = 15

    inner_function()
    print("y after inner:", y)   # y after inner: 15

outer_function()
```

### Scope summary

| Scope     | Where defined                                    | Keyword to modify |
| --------- | ------------------------------------------------ | ----------------- |
| Local     | Inside a function                                | — (just assign)   |
| Enclosing | Inside an outer function (nested functions)      | `nonlocal`        |
| Global    | Top level of a module/file                       | `global`          |
| Built-in  | Predefined names (`len`, `print`, `sum`, `None`) | —                 |

---

## 7. Lambda Functions

A **lambda** is a small, **anonymous** function — defined with the `lambda` keyword, it can take any number of arguments but contains only **one expression**. That expression is evaluated and returned automatically.

```python
# Regular function
def add(x, y):
    return x + y

# Same thing as a lambda
add_lambda = lambda x, y: x + y

print(add(5, 3))           # 8
print(add_lambda(5, 3))    # 8
```

### Typical use — short callbacks passed to other functions

```python
numbers = [1, 2, 3, 4, 5]

# map: square each number
squared = list(map(lambda x: x ** 2, numbers))
print(squared)             # [1, 4, 9, 16, 25]

# filter: keep even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)               # [2, 4]

# sorted: sort by absolute value
unsorted = [-5, 3, -1, 4, -2]
print(sorted(unsorted, key=lambda x: abs(x)))   # [-1, -2, 3, 4, -5]

# reduce: product of all numbers
from functools import reduce
print(reduce(lambda acc, x: acc * x, numbers))  # 120
```

> **Note**: Lambdas are best for **tiny, one-off** logic. If a function needs multiple statements or a docstring, use a normal `def`.

---

## 8. Higher-Order Functions (HOF)

A **higher-order function** either **takes a function as an argument** or **returns a function**. In Python, functions are **first-class citizens** — they can be passed around like any other object.

### Built-in HOFs: `map`, `filter`, `sorted`, `reduce`

```python
punches = [1, 2, 3, 4, 5]

def magnify(punch):
    return punch * 10

heavy = list(map(magnify, punches))
print(heavy)                 # [10, 20, 30, 40, 50]

scores = [55, 65, 75, 85, 95]

def is_distinction(score):
    return score >= 75

print(list(filter(is_distinction, scores)))   # [75, 85, 95]

words = ["banana", "kiwi", "apple", "cherry", "fig"]
print(sorted(words, key=len))       # ['fig', 'kiwi', 'apple', 'banana', 'cherry']
print(sorted(words, key=str.lower)) # ['apple', 'banana', 'cherry', 'fig', 'kiwi']
```

### HOF that accepts a function (strategy pattern)

```python
def pick_last(names):
    return names[-1]

def pick_first(names):
    return names[0]

def announce(picker_func, names):
    print(f"The chosen one is: {picker_func(names)}")

announce(pick_last, ["Alice", "Bob", "Charlie"])
# The chosen one is: Charlie
```

### HOF that returns a function (function factory)

```python
def make_multiplier(factor):
    """Returns a new function that multiplies any number by factor."""
    def multiplier(number):
        return number * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(10))     # 20
print(triple(10))     # 30
print(list(map(double, [1, 2, 3])))   # [2, 4, 6]
```

---

## 9. Closures

A **closure** is a function that **remembers** variables from its enclosing scope — even after that enclosing function has finished executing.

```python
def make_exercise(name):
    exercise_name = name.upper()       # captured by the inner function

    def exercise(frequency):           # closure
        return f"Let's do some {exercise_name} exercises! for {frequency} times."

    return exercise

push_ups = make_exercise("push-ups")
print(push_ups(10))   # Let's do some PUSH-UPS exercises! for 10 times.
print(push_ups(20))   # Let's do some PUSH-UPS exercises! for 20 times.
```

### Closures maintain state between calls

```python
def move_player(x, y):
    def move(dx, dy):
        nonlocal x, y          # modify the captured variables
        x += dx
        y += dy
        return x, y
    return move

player = move_player(0, 0)
print(player(5, 3))     # (5, 3)
print(player(-2, 4))    # (3, 7)
```

> **Use cases**: creating functions with private data, counters, configurable factories, and maintaining state without a class.

---

## 10. Decorators

A **decorator** is a function that **wraps** another function to modify or extend its behavior — without changing the original function's code. Use the `@decorator_name` syntax above a function.

### A simple decorator (logging)

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_decorator
def add(x, y):
    return x + y

add(5, 3)
# Calling add with (5, 3)
# add returned: 8
```

### A timing decorator

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper

@timer
def slow_add(a, b):
    time.sleep(0.01)
    return a + b

slow_add(3, 7)   # slow_add took 0.01xxxx s
```

### Real-world uses of decorators

- **Logging** — record function calls, arguments, and return values.
- **Access control** — e.g. `@require_auth` checks if a user is authenticated before running a function.
- **Input validation** — e.g. `@validate_input` validates arguments before execution.
- **Timing / performance** — measure how long a function takes.
- **Memoization / caching** — remember results to avoid recomputation.
- **Retry logic** — retry a function a number of times on failure.

> **Key idea**: `@decorator` is just sugar for `func = decorator(func)`. The decorator receives the function and returns a wrapper that usually uses `*args, **kwargs` so it works with **any** function signature.

---

## 11. Recursion

**Recursion** is when a function **calls itself**. Every recursive function needs a **base case** (a stopping condition) to avoid infinite recursion.

```python
def factorial(n):
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))     # 120  (5 * 4 * 3 * 2 * 1)
```

```python
def fibonacci(n):
    if n <= 1:          # base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(7))     # 13
```

> **Note**: Every recursive call uses stack memory. Deep recursion can raise `RecursionError` — set a safe limit with `sys.setrecursionlimit()` or prefer an iterative loop when performance matters.

---

## 12. The `main()` Function & `if __name__ == "__main__":`

Every Python file has two possible uses:

1. **Run directly**: `python main_function.py` → `__name__` becomes `"__main__"`.
2. **Imported by another file**: `import main_function` → `__name__` becomes the module name (`"main_function"`).

```python
def say_hello():
    print("Hello from say_hello()")

def main():
    print("Running main_function.py directly")
    say_hello()

if __name__ == "__main__":
    main()
```

### Why it matters

- Reusable functions stay in the file.
- You can still run/test the file by itself.
- Importing the file does **not** accidentally run demo/test code.

> **Analogy**: The file is a shop. `main()` is "open the shop now." `if __name__ == "__main__":` is the key check — **only open if this file is the one started by the user.**

---

## 13. Useful Built-in Functions

Python ships with many ready-made functions:

| Function       | Purpose                        | Example                         | Result                 |
| -------------- | ------------------------------ | ------------------------------- | ---------------------- |
| `print()`      | Output to console              | `print("hi")`                   | `hi`                   |
| `len()`        | Length of a collection         | `len([1, 2, 3])`                | `3`                    |
| `type()`       | Type of an object              | `type(5)`                       | `<class 'int'>`        |
| `sum()`        | Sum of an iterable             | `sum([1, 2, 3])`                | `6`                    |
| `max()`        | Largest value                  | `max([4, 9, 2])`                | `9`                    |
| `min()`        | Smallest value                 | `min([4, 9, 2])`                | `2`                    |
| `abs()`        | Absolute value                 | `abs(-7)`                       | `7`                    |
| `round()`      | Round a float                  | `round(3.14159, 2)`             | `3.14`                 |
| `range()`      | Generate a sequence of numbers | `list(range(3))`                | `[0, 1, 2]`            |
| `sorted()`     | Return a sorted list           | `sorted([3, 1, 2])`             | `[1, 2, 3]`            |
| `enumerate()`  | Index + item pairs             | `list(enumerate(["a", "b"]))`   | `[(0, 'a'), (1, 'b')]` |
| `zip()`        | Combine iterables element-wise | `list(zip([1, 2], ["a", "b"]))` | `[(1, 'a'), (2, 'b')]` |
| `input()`      | Read user input as a string    | `input("Name? ")`               | user text              |
| `isinstance()` | Check an object's type         | `isinstance(5, int)`            | `True`                 |

---

## 14. Real-World Use Cases (Combined Examples)

### Email validation

```python
def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]

print(is_valid_email("alice@example.com"))   # True
print(is_valid_email("bob@localhost"))       # False
```

### Shopping cart total

```python
def cart_total(prices, tax_rate=0.16):
    subtotal = sum(prices)
    return round(subtotal * (1 + tax_rate), 2)

print(cart_total([1200, 300, 450, 800]))     # 3190.0
print(cart_total([1000, 500], tax_rate=0.1)) # 1650.0
```

### Grading system

```python
def grade(score):
    if score >= 75:
        return "Distinction"
    if score >= 60:
        return "Merit"
    if score >= 50:
        return "Pass"
    return "Fail"

print(grade(82))   # Distinction
print(grade(45))   # Fail
```

### Flexible report builder with `*args` / `**kwargs`

```python
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
```

### Function that summarizes any list

```python
def summarize(numbers):
    return {
        "count": len(numbers),
        "total": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "max": max(numbers),
        "min": min(numbers),
    }

print(summarize([10, 20, 30, 40]))
# {'count': 4, 'total': 100, 'average': 25.0, 'max': 40, 'min': 10}
```

### Retry wrapper (decorator)

```python
import random

def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
            raise RuntimeError("All attempts failed")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable():
    if random.random() < 0.5:
        raise ValueError("Network error")
    return "Success"

print(unreliable())
```

---

## 15. Set Methods: `difference_update()` and In-Place Set Operations

Sets come with **in-place** methods that modify the original set directly instead of returning a new one. They are the mutating counterparts of the read-only operations (`difference`, `intersection`, `union`, `symmetric_difference`) and all return `None`.

### `difference_update()` — remove elements found in another set/iterable

Removes from the set **any element that also appears in the passed iterable**, changing the set **in place**. This is the mutating version of `difference()`.

```python
available = {"python", "java", "c++", "ruby", "go"}
taken = {"java", "go"}

available.difference_update(taken)
print(available)   # {'python', 'c++', 'ruby'}
```

> **Note**: `difference_update()` returns `None` and mutates the original set. If you want a **new** set without touching the original, use `difference()` instead.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

result = a.difference(b)     # difference() -> NEW set, 'a' unchanged
print(result)                # {1, 2}

a.difference_update(b)       # difference_update() -> mutates 'a' in place
print(a)                     # {1, 2}
```

### `update()` — add all elements from another iterable (in-place union)

The mutating version of `union()` — adds every element from the given iterable(s) to the set.

```python
team_a = {"alice", "bob"}
team_b = {"carol", "dave"}

team_a.update(team_b)
print(team_a)   # {'alice', 'bob', 'carol', 'dave'}
```

### `intersection_update()` — keep only elements present in both sets

The mutating version of `intersection()` — removes anything **not** shared with the given iterable(s).

```python
all_users = {"alice", "bob", "carol", "dave"}
premium = {"bob", "dave", "erin"}

premium.intersection_update(all_users)
print(premium)   # {'bob', 'dave'}  (only users who are in both)
```

### `symmetric_difference_update()` — keep elements in exactly one set

The mutating version of `symmetric_difference()` — keeps elements that appear in **only one** of the two sets (removes shared ones).

```python
likes_football = {"alice", "bob", "carol"}
likes_tennis = {"bob", "dave"}

likes_football.symmetric_difference_update(likes_tennis)
print(likes_football)   # {'alice', 'carol', 'dave'}  (shared 'bob' removed)
```

### Combined example — cleaning up a shopping list

```python
cart = {"apple", "milk", "bread", "eggs", "butter"}
out_of_stock = {"milk", "butter"}

# Remove out-of-stock items in place
cart.difference_update(out_of_stock)
print(cart)   # {'apple', 'bread', 'eggs'}

# Add freshly restocked items
cart.update({"juice", "cheese"})
print(cart)   # {'apple', 'bread', 'eggs', 'juice', 'cheese'}
```

### Quick reference — read-only vs in-place

| Read-only (returns new set)           | In-place (mutates, returns `None`) | Effect                           |
| ------------------------------------- | ---------------------------------- | -------------------------------- |
| `a \| b` / `a.union(b)`               | `a.update(b)`                      | add all elements from `b`        |
| `a - b` / `a.difference(b)`           | `a.difference_update(b)`           | remove elements found in `b`     |
| `a & b` / `a.intersection(b)`         | `a.intersection_update(b)`         | keep elements present in both    |
| `a ^ b` / `a.symmetric_difference(b)` | `a.symmetric_difference_update(b)` | keep elements in exactly one set |

> **Key idea**: The in-place `*_update()` methods modify the set they are called on and return `None`. Use the read-only operators when you need to keep the original set intact, and the `*_update()` methods when mutating the original is fine.

---

## 16. Common Pitfalls

| Pitfall                                                           | Fix                                                                             |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Forgetting the colon `:` after the `def` line                     | Always end the `def` line with `:`                                              |
| Missing/incorrect indentation for the function body               | Indent the body consistently (4 spaces)                                         |
| Defining a function but never **calling** it (missing `()`)       | Call it: `greet("Alice")` — `greet` alone just references the function          |
| Forgetting to `return` (function silently gives `None`)           | Add `return value` explicitly if the function should produce a result           |
| Using a mutable default argument (e.g. `def f(lst=[])`)           | Use `def f(lst=None)` and set `lst = lst if lst is not None else []` inside     |
| Reordering/omitting required positional arguments                 | Pass them in order, or use keyword arguments                                    |
| Modifying a global without `global` (silently creates a local)    | Declare `global x` inside the function before assigning                         |
| Naming a variable the same as a built-in (`list`, `sum`, `input`) | Use descriptive names like `items`, `total`, `user_input`                       |
| Wrong order: positional after keyword in a call                   | Put all positional arguments **before** keyword arguments                       |
| Unbounded recursion (no base case)                                | Always define a base case; watch `RecursionError` for deep recursion            |
| Shadowing a parameter with a same-named local variable            | Use distinct variable names                                                     |
| Assuming functions can change caller's int/str (immutables)       | Immutables are passed by value; reassignment inside only affects the local name |

---

## 17. Function Definitions — Quick Reference

```python
def basic():                      # no parameters, returns None
    pass

def with_default(a, b=10):        # default value
    return a + b

def with_args(*args):             # any number of positional args
    return sum(args)

def with_kwargs(**kwargs):        # any number of keyword args
    return kwargs

def combined(a, *args, flag=True, **kwargs):   # full combo
    return a, args, flag, kwargs

def returns_multiple():
    return 1, 2, 3                # returns a tuple (1, 2, 3)

def early_return(x):
    if x < 0:
        return None
    return x
```

---

> **Key Takeaway**: Functions are the building blocks of clean, reusable Python code. Master **defining and calling** (`def` + `()`), **arguments** (positional, keyword, defaults, `*args`, `**kwargs`), **return values** (single, multiple via tuple, early `return`, implicit `None`), and **scope** (`global`/`nonlocal`). Then level up with **lambdas** for tiny anonymous functions, **higher-order functions** (`map`/`filter`/`sorted`/`reduce`) for functional style, **closures** for remembering state, **decorators** for wrapping behavior, and **recursion** for problems that decompose into identical sub-problems. Guard the `main` entry point with `if __name__ == "__main__":` so imported modules never run demo code unexpectedly. Follow the **DRY** principle — write a function once, call it everywhere, and your code stays readable, testable, and maintainable.
