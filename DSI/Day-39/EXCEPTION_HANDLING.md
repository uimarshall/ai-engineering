# EXCEPTION HANDLING

Handling errors gracefully in Python and its use cases.

> Python exception handling — `try`/`except`/`else`/`finally`, common error types, and code samples.

> An exception is an **error that occurs while a program is running**. Instead of letting the program crash, exception handling lets you **catch** the error and respond to it gracefully.

---

## 1. What is Exception Handling?

- **Description**: Exception handling is a mechanism that lets you detect runtime errors and take appropriate action — instead of the program stopping abruptly.
- **Uses**: Validating user input, handling file/network errors, retrying failed operations, giving friendly error messages, and keeping programs running even when something goes wrong.
- **Core idea**: Wrap risky code in a `try` block. If an error occurs, execution jumps to an `except` block where you decide what to do.
- **Syntax**: `try:` → `except <ErrorType>:` → (optional) `else:` → (optional) `finally:`.

```python
try:
    numerator = 10
    denominator = 0
    result = numerator / denominator
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

---

## 2. The `try` / `except` Block

### Basic structure

```python
try:
    # risky code that might raise an error
    x = 5 / 0
except ZeroDivisionError:
    # runs only if ZeroDivisionError happens
    print("You can't divide by zero!")
```

### Catching the error object

You can capture the exception to inspect it.

```python
try:
    print(10 / 0)
except ZeroDivisionError as error:
    print("Caught an error:", error)   # Caught an error: division by zero
```

### Catching multiple error types

```python
try:
    value = int("abc")          # raises ValueError
except (ValueError, TypeError):
    print("Invalid value or type provided.")
```

### Catching different errors separately

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Math error: division by zero")
except ValueError:
    print("Invalid value")
```

### Catching any error (bare `except`)

Use a bare `except` (or `except Exception`) as a **catch-all** — but be careful, it hides all errors.

```python
try:
    risky_operation()
except Exception:
    print("Something went wrong.")

# To see what actually happened
try:
    1 / 0
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
```

> **Tip**: Catch **specific** exceptions when you can. A bare `except` can hide bugs and make debugging harder.

---

## 3. Common Python Error Types

| Error               | When it happens                       | Example                       |
| ------------------- | ------------------------------------- | ----------------------------- |
| `TypeError`         | Wrong type used in an operation       | `"a" + 1`                     |
| `ValueError`        | Right type but invalid value          | `int("abc")`                  |
| `ZeroDivisionError` | Dividing by zero                      | `10 / 0`                      |
| `IndexError`        | Index out of range                    | `[1, 2][5]`                   |
| `KeyError`          | Missing dict key                      | `{"a": 1}["b"]`               |
| `NameError`         | Using an undefined variable           | `print(undefined_var)`        |
| `FileNotFoundError` | File doesn't exist                    | `open("missing.txt")`         |
| `AttributeError`    | Accessing a missing attribute/method  | `"abc".nonexistent()`         |
| `ImportError`       | Importing a non-existent module       | `import nonexistent_module`   |
| `StopIteration`     | Iterator has no more items            | `next(iter([]))`              |
| `RuntimeError`      | General runtime error                 | varies                        |
| `OverflowError`     | Numeric result too large to represent | `10 ** 1000` in some contexts |

### TypeError

```python
try:
    result = "5" + 5          # string + int -> TypeError
except TypeError as e:
    print("TypeError:", e)    # TypeError: can only concatenate str (not "int") to str
```

### ValueError

```python
try:
    number = int("hello")     # "hello" is not a valid number -> ValueError
except ValueError as e:
    print("ValueError:", e)   # ValueError: invalid literal for int() with base 10: 'hello'
```

### ZeroDivisionError

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)   # ZeroDivisionError: division by zero
```

### IndexError

```python
fruits = ["apple", "banana"]
try:
    print(fruits[5])
except IndexError as e:
    print("IndexError:", e)   # IndexError: list index out of range
```

### KeyError

```python
person = {"name": "Alice"}
try:
    print(person["age"])
except KeyError as e:
    print("KeyError:", e)     # KeyError: 'age'
```

### NameError

```python
try:
    print(not_defined)
except NameError as e:
    print("NameError:", e)    # NameError: name 'not_defined' is not defined
```

### FileNotFoundError

```python
try:
    with open("missing_file.txt", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError as e:
    print("FileNotFoundError:", e)   # FileNotFoundError: [Errno 2] No such file or directory: 'missing_file.txt'
```

---

## 4. The `else` Clause

The `else` block runs **only if no exception was raised** in the `try` block.

```python
try:
    number = int("42")
except ValueError:
    print("That's not a valid number!")
else:
    print(f"Success! The number is {number}")   # runs because no error
```

### Practical example

```python
def safely_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    else:
        print(f"{a} / {b} = {result}")

safely_divide(10, 2)    # 10 / 2 = 5.0
safely_divide(10, 0)    # Cannot divide by zero.
```

> **Note**: `else` lets you keep "success" code separate from the risky code, so it isn't accidentally caught by the `except`.

---

## 5. The `finally` Clause

The `finally` block **always runs** — whether an exception occurred or not. It's used for cleanup (closing files, releasing resources).

```python
try:
    print("Opening file...")
    data = int("5")
except ValueError:
    print("Invalid value!")
finally:
    print("Cleanup always runs here.")

# Opening file...
# Cleanup always runs here.
```

### Even when an exception is raised

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Math error!")
finally:
    print("This runs no matter what.")

# Math error!
# This runs no matter what.
```

### Full structure: `try` / `except` / `else` / `finally`

```python
try:
    value = int("42")
except ValueError:
    print("Invalid number.")
else:
    print(f"Parsed: {value}")
finally:
    print("Done.")
# Parsed: 42
# Done.
```

---

## 6. Raising Exceptions with `raise`

You can **raise** your own exceptions to signal errors.

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    return age

try:
    set_age(-5)
except ValueError as e:
    print("Caught:", e)   # Caught: Age cannot be negative!
```

### Re-raising an exception

```python
try:
    1 / 0
except ZeroDivisionError:
    print("Handling...")
    raise                       # re-raises the same exception
```

---

## 7. Real-World Use Cases (with `input()`)

### Validating user input (repeatedly ask until valid)

```python
while True:
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 120:
            break
        print("Age must be between 0 and 120.")
    except ValueError:
        print("Please enter a valid number.")

print(f"Your age is {age}")
```

### Safe division calculator

```python
def safe_divide():
    try:
        a = float(input("First number: "))
        b = float(input("Second number: "))
        result = a / b
    except ValueError:
        print("Numbers only, please!")
    except ZeroDivisionError:
        print("You can't divide by zero!")
    else:
        print(f"Result: {result}")

safe_divide()
```

> **Note**: `input()` always returns a **string**. Calling `int()` or `float()` on it can raise `ValueError` if the user types something that isn't a number — so wrap it in a `try`/`except`.

### Reading a file that may not exist

```python
filename = input("Enter a filename: ")
try:
    with open(filename, encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print(f"Sorry, '{filename}' was not found.")
```

### Retry logic (with limited attempts)

```python
import random

def retry(max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        try:
            if random.random() < 0.5:
                raise ConnectionError("Network down")
            return f"Success on attempt {attempts}"
        except ConnectionError as e:
            print(f"Attempt {attempts} failed: {e}")
    return "Failed after all attempts"

print(retry())
```

### Classifying errors from a mixed list

```python
def process(value):
    try:
        result = 10 / value          # could be ZeroDivisionError or TypeError
        return result
    except ZeroDivisionError:
        return "Can't divide by zero"
    except TypeError:
        return "Need a number, not text"

print(process(2))     # 5.0
print(process(0))     # Can't divide by zero
print(process("x"))   # Need a number, not text
```

### Login / authentication stub

```python
def login(username, password):
    valid_user = ("alice", "secret123")
    if username != valid_user[0] or password != valid_user[1]:
        raise PermissionError("Invalid credentials")
    return "Welcome, Alice!"

try:
    username = input("Username: ")
    password = input("Password: ")
    print(login(username, password))
except PermissionError as e:
    print("Access denied:", e)
```

---

## 8. Common Pitfalls

| Pitfall                                                              | Fix                                                               |
| -------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Catching exceptions too broadly (bare `except`)                      | Catch specific exception types to avoid hiding bugs               |
| Swallowing errors silently (empty `except: pass`)                    | Log or print the error so you know it happened                    |
| Catching `Exception` but not handling cleanup                        | Use `finally` for resources that must be released                 |
| Putting too much code inside `try`                                   | Keep only the risky line(s) in `try`; move success code to `else` |
| Forgetting `input()` returns a string                                | Convert with `int()`/`float()` and catch `ValueError`             |
| Catching the wrong exception type (e.g. `ValueError` vs `TypeError`) | Check the actual error message and match the correct type         |
| Re-using a variable that may not exist outside `try`                 | Initialize it before `try` or handle the error path               |
| Not re-raising when you can't handle the error                       | Use bare `raise` to let the caller deal with it                   |
| Infinite loop in input validation without a `break` path             | Make sure the loop can exit when valid input is received          |

---

## 9. Quick Reference

```python
# Basic
try:
    risky_code()
except SomeError:
    handle_error()

# Multiple types
except (TypeError, ValueError):
    handle_multiple()

# Capture the error
except ZeroDivisionError as e:
    print(e)

# Separate handlers
except FileNotFoundError:
    ...
except KeyError:
    ...

# Success-only block
else:
    success_code()

# Always runs (cleanup)
finally:
    cleanup()

# Raise your own
raise ValueError("custom message")

# Re-raise current exception
raise
```

---

> **Key Takeaway**: Exception handling lets your Python programs **fail gracefully** instead of crashing. Use **`try`** to wrap risky code, **`except`** to catch specific error types (`TypeError`, `ValueError`, `ZeroDivisionError`, `IndexError`, `KeyError`, `FileNotFoundError`, and more), **`else`** to run code only on success, and **`finally`** for cleanup that always runs. When working with **`input()`**, remember it returns a string — always convert it inside a `try`/`except` to catch `ValueError` from bad input, and loop until the user provides something valid. Raise your own errors with **`raise`** to signal problems clearly. Catch specific exceptions rather than broad ones, and never swallow errors silently. Done well, exception handling makes your code robust, user-friendly, and much easier to debug.
