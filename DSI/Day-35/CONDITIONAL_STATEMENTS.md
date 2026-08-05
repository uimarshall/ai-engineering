# CONDITIONAL STATEMENTS

Conditional logic in Python and use cases.

> Python conditional statements — `if`, `elif`, `else`, and more, with code samples.

---

## 1. What are Conditional Statements?

- **Description**: Conditional statements let a program make **decisions** by executing different blocks of code based on whether a condition is `True` or `False`.
- **Uses**: Validating input, branching logic, handling errors, applying rules, filtering choices, and controlling program flow.
- **Core idea**: Evaluate a **boolean expression** — if it is truthy, run one block; otherwise, run another (or do nothing).
- **Python keywords**: `if`, `elif`, `else`, plus the `match`/`case` (Python 3.10+) and the **ternary conditional expression**.
- **Indentation matters**: Python uses **indentation** (typically 4 spaces) to define which statements belong to a block — there are no braces or `end` keywords.

```python
age = 20
if age >= 18:
    print("Adult")      # indented block runs only if condition is True
```

---

## 2. Boolean Context & Truthiness

Before using conditions, understand what counts as `True`/`False`.

### Truthy and Falsy values

| Falsy (`False`)                             | Truthy (`True`)                                 |
| ------------------------------------------- | ----------------------------------------------- |
| `False`, `None`                             | `True`                                          |
| `0`, `0.0`, `0j`                            | any non-zero number (`1`, `-5`, `3.14`)         |
| empty string `""`                           | non-empty string `"hello"`                      |
| empty collections `[]`, `()`, `{}`, `set()` | non-empty collections `[1]`, `(0,)`, `{"a": 1}` |
| `range(0)`                                  | `range(1)`, any non-empty range                 |

```python
if "hello":          # truthy
    print("string is truthy")     # runs

if []:               # falsy
    print("never runs")
else:
    print("empty list is falsy")  # runs

if 0:
    print("never runs")
else:
    print("0 is falsy")           # runs
```

> **Golden rule**: Use `if value:` to check for "non-empty" rather than `if len(value) > 0:` — it's cleaner and idiomatic.

---

## 3. Comparison Operators

These produce boolean values (`True`/`False`) and are the building blocks of conditions.

| Operator | Description            | Example            | Result |
| -------- | ---------------------- | ------------------ | ------ |
| `==`     | Equal to               | `5 == 5`           | `True` |
| `!=`     | Not equal to           | `5 != 3`           | `True` |
| `<`      | Less than              | `3 < 5`            | `True` |
| `>`      | Greater than           | `5 > 3`            | `True` |
| `<=`     | Less than or equal     | `3 <= 3`           | `True` |
| `>=`     | Greater than or equal  | `5 >= 5`           | `True` |
| `is`     | Identity (same object) | `x is None`        | `True` |
| `is not` | Not identical          | `x is not None`    | `True` |
| `in`     | Membership             | `"a" in "cat"`     | `True` |
| `not in` | Not a member           | `"z" not in "cat"` | `True` |

```python
score = 85
print(score == 85)     # True
print(score != 90)     # True
print(score >= 80)     # True
print("ell" in "hello")  # True
```

> **Tip**: Use `==` for value equality and `is` only for identity checks (most commonly `is None` / `is not None`).

---

## 4. Logical Operators

Combine multiple conditions.

| Operator | Description                        | Example          | Result  |
| -------- | ---------------------------------- | ---------------- | ------- |
| `and`    | `True` only if **both** are true   | `True and False` | `False` |
| `or`     | `True` if **at least one** is true | `True or False`  | `True`  |
| `not`    | Negates a condition                | `not True`       | `False` |

```python
age = 25
has_license = True

if age >= 18 and has_license:
    print("Can drive")          # Can drive

if age < 18 or not has_license:
    print("Cannot drive")       # not printed

if not has_license:
    print("No license")         # not printed
```

### Short-circuit evaluation

`and` stops if the first operand is falsy; `or` stops if the first is truthy. This is useful for safe defaults.

```python
# or — picks the first truthy value
name = "" or "Guest"
print(name)          # Guest

# and — evaluates second only if first is truthy
user = {"admin": True}
is_admin = user.get("admin") and user["admin"]
```

---

## 5. The `if` Statement

The simplest form — run a block if a condition is `True`.

```python
temperature = 35

if temperature > 30:
    print("It's hot!")          # It's hot!
```

---

## 6. `if` / `else`

Runs one block if the condition is `True`, and a different block otherwise.

```python
age = 16

if age >= 18:
    print("Adult")
else:
    print("Minor")              # Minor
```

---

## 7. `if` / `elif` / `else`

For **multiple mutually exclusive** conditions. `elif` is evaluated in order; the first `True` branch runs, and the rest are skipped. `else` catches everything else.

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(grade)            # B
```

> **Note**: Order matters — `elif` conditions are checked top-to-bottom, so put the most specific/most restrictive checks first.

---

## 8. Nested Conditionals

You can place conditionals inside other conditionals to handle more complex logic.

```python
x = 5
y = 10

if x > 0:
    if y > 0:
        print("Both positive")      # Both positive
    else:
        print("x positive, y non-positive")
else:
    print("x non-positive")
```

> Nested `if` can often be flattened with `and` for readability:
>
> ```python
> if x > 0 and y > 0:
>     print("Both positive")
> ```

---

## 9. The Ternary Conditional Expression

A one-line `if`/`else` that returns a value. Syntax: `value_if_true if condition else value_if_false`.

```python
age = 20
status = "Adult" if age >= 18 else "Minor"
print(status)          # Adult

# Equivalent verbose version:
if age >= 18:
    status = "Adult"
else:
    status = "Minor"
```

```python
# Useful for quick assignments
temperature = 12
weather = "Cold" if temperature < 15 else "Warm"
print(weather)         # Cold

# Nested ternary (avoid for complex logic)
num = 0
sign = "positive" if num > 0 else ("negative" if num < 0 else "zero")
print(sign)            # zero
```

> Use ternaries for **simple** cases only. For multiple conditions, prefer `if`/`elif`/`else` for readability.

---

## 10. `match` / `case` (Python 3.10+)

Python's **structural pattern matching** — a powerful alternative to long `if`/`elif` chains for matching patterns.

```python
def describe_command(command):
    match command:
        case "start":
            return "Starting..."
        case "stop":
            return "Stopping..."
        case "restart":
            return "Restarting..."
        case _:
            return "Unknown command"

print(describe_command("start"))   # Starting...
print(describe_command("quit"))    # Unknown command
```

### Matching with patterns and guards

```python
def classify(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On x-axis at {x}"
        case (0, y):
            return f"On y-axis at {y}"
        case (x, y) if x == y:
            return "On diagonal"
        case (x, y):
            return f"({x}, {y})"

print(classify((0, 0)))    # Origin
print(classify((5, 0)))    # On x-axis at 5
print(classify((3, 3)))    # On diagonal
```

---

## 11. Checking Containers & Membership

Conditionals frequently check whether items exist in lists, dicts, strings, or sets.

```python
# Membership in a list
fruits = ["apple", "banana", "cherry"]
if "banana" in fruits:
    print("Banana available")       # Banana available

# Checking a dict key
config = {"debug": True, "port": 8080}
if "debug" in config:
    print("debug key present")      # debug key present

# Checking a dict value safely
port = config.get("port", 3000)
if port:
    print(f"Port: {port}")          # Port: 8080

# Empty container check
items = []
if not items:
    print("No items")               # No items
```

---

## 12. Real-World Use Cases (Combined Example)

### Input validation

```python
def validate_age(age):
    if age < 0:
        return "Invalid: negative"
    elif age < 18:
        return "Minor"
    elif age < 65:
        return "Adult"
    else:
        return "Senior"

print(validate_age(-5))   # Invalid: negative
print(validate_age(20))   # Adult
```

### Categorizing data (data science)

```python
def categorize_score(score):
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 50:
        return "Pass"
    return "Fail"

scores = [95, 80, 60, 30]
print([categorize_score(s) for s in scores])
# ['Excellent', 'Good', 'Pass', 'Fail']
```

### Menu / routing logic

```python
choice = input("Choose (view/edit/delete): ").strip().lower()

if choice == "view":
    print("Showing item")
elif choice == "edit":
    print("Editing item")
elif choice == "delete":
    print("Deleting item")
else:
    print("Invalid choice")
```

### Safe division with checks

```python
def safe_divide(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # Error: division by zero
```

### Applying business rules

```python
def shipping_cost(weight, is_express=False):
    if weight <= 0:
        return 0
    base = 5 + weight * 0.5
    if is_express:
        base += 10
    return round(base, 2)

print(shipping_cost(2))           # 6.0
print(shipping_cost(2, True))     # 16.0
```

---

## 13. Common Pitfalls

| Pitfall                                                    | Fix                                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Forgetting the colon `:` after `if`/`elif`/`else`          | Always add `:` at the end of the condition line                                 |
| Inconsistent indentation (mixing spaces/tabs, wrong block) | Use 4 spaces consistently; keep nested blocks aligned                           |
| Using `=` instead of `==` in a condition                   | `=` is assignment; use `==` for comparison (`if x == 5:`)                       |
| Checking membership with `if list:` when you mean length   | `if items:` tests non-empty; use `if len(items) == n:` for an exact count       |
| `elif` after `else` (invalid order)                        | `else` must come last; use `elif` between `if` and `else`                       |
| Using a mutable default / side effects in a condition      | Keep conditions as pure boolean expressions; avoid assignment inside conditions |
| Comparing floats with `==` (precision issues)              | Use a tolerance: `abs(a - b) < 1e-9`                                            |
| Over-nesting with deep `if` blocks                         | Flatten with `and`/`or`, or use early returns / guard clauses                   |
| `match`/`case` requires Python 3.10+                       | Use `if`/`elif` for older Python versions                                       |
| Ternary for complex multi-branch logic                     | Use `if`/`elif`/`else` for readability when there are more than 2 branches      |

---

> **Key Takeaway**: Conditional statements give programs the power to make decisions. Master the core forms — `if`, `if/else`, `if/elif/else` — plus the **ternary expression** for simple one-liners and **`match`/`case`** (Python 3.10+) for clean pattern matching. Remember: **indentation defines blocks**, **`:` is required** after each condition, **`==` compares while `=` assigns**, and a value's **truthiness** (not just `True`/`False`) determines whether a branch runs. Use `and`/`or`/`not` to combine conditions, and prefer readable `if`/`elif` chains over deeply nested or convoluted ternaries. When in doubt, check for "non-empty" with `if value:` and for "none" with `if value is None:`.
> </content>
