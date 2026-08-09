# LIST COMPREHENSION

A concise way to build lists in Python and its use cases.

> Python list comprehension — syntax, patterns, and how it compares to a `for` loop.

> A list comprehension is a **compact, one-line way to create a new list** by transforming and/or filtering an existing iterable. It's often faster and more readable than a traditional `for` loop.

---

## 1. What is a List Comprehension?

- **Description**: A list comprehension is a Pythonic shorthand that builds a new list in a single expression. It wraps a loop (and optional condition) inside square brackets `[]`.
- **Uses**: Transforming every item, filtering items by a condition, flattening nested lists, building lookup tables, and generating data.
- **Core idea**: Instead of writing `for` + `append()`, you describe the result directly: `[expression for item in iterable if condition]`.
- **Syntax**: `[expression for item in iterable if condition]`
  - `expression` — what to put in the new list (can transform `item`).
  - `item` — the variable that takes each value from the iterable.
  - `iterable` — any sequence/iterator (list, range, string, dict, etc.).
  - `if condition` — optional filter; only items that make it `True` are included.

```python
numbers = [1, 2, 3, 4, 5]
squared = [n ** 2 for n in numbers]
print(squared)          # [1, 4, 9, 16, 25]
```

---

## 2. Basic List Comprehension

### Transform every item

```python
# Square each number
squares = [n ** 2 for n in range(1, 6)]
print(squares)          # [1, 4, 9, 16, 25]

# Uppercase each word
words = ["apple", "banana", "cherry"]
caps = [w.upper() for w in words]
print(caps)             # ['APPLE', 'BANANA', 'CHERRY']

# Length of each word
lengths = [len(w) for w in words]
print(lengths)          # [5, 6, 6]
```

### Filter with `if`

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = [n for n in numbers if n % 2 == 0]
print(evens)            # [2, 4, 6]

# Only words longer than 4 characters
long_words = [w for w in ["apple", "kiwi", "fig"] if len(w) > 4]
print(long_words)       # ['apple']
```

### Transform AND filter together

```python
# Square only the even numbers
numbers = [1, 2, 3, 4, 5, 6]
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print(even_squares)     # [4, 16, 36]
```

> **Reading order matters**: The `if` comes _after_ the iterable, not before. `[n for n in numbers if n % 2 == 0]`, not `[n if ... for n in numbers]`.

---

## 3. Using a Function Inside a Comprehension

You can call any function as the `expression`.

```python
my_list = [1, 4, 9, 16, 25]

def square_root(num):
    return num ** 0.5

roots = [square_root(i) for i in my_list]
print(roots)            # [1.0, 2.0, 3.0, 4.0, 5.0]

# A built-in function works too
floats = [abs(x) for x in [-3, -1, 2, -8]]
print(floats)           # [3, 1, 2, 8]
```

---

## 4. Using Methods on the Item

```python
# Remove whitespace from each string
cleaned = [s.strip() for s in [" a ", "b ", " c"]]
print(cleaned)          # ['a', 'b', 'c']

# Swap case
swapped = [s.swapcase() for s in ["Hello", "World"]]
print(swapped)          # ['hELLO', 'wORLD']

# First character of each word
first_chars = [w[0] for w in ["apple", "banana", "cherry"]]
print(first_chars)      # ['a', 'b', 'c']
```

---

## 5. Nested List Comprehensions

### Flattening a 2D list

```python
two_dimensional_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten into a single list
flattened = [num for row in two_dimensional_list for num in row]
print(flattened)        # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Grab the first element of each row

```python
first_col = [row[0] for row in two_dimensional_list]
print(first_col)               # [1, 4, 7]
```

### Nested comprehension building a grid

```python
# Multiplication table (3x3)
table = [[row * col for col in range(1, 4)] for row in range(1, 4)]
print(table)            # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

> **Reading order**: The `for` clauses run left to right, exactly as nested `for` loops would. `[num for row in grid for num in row]` means `for row in grid: for num in row:`.

---

## 6. Comprehension vs `for` Loop

Both approaches build the same result — the difference is readability and speed.

```python
my_list = [1, 4, 9, 16, 25]

# Using a for loop + append
my_new_list = []
for i in my_list:
    if i % 2 == 0:
        my_new_list.append(i)
print(my_new_list)      # [4, 16]

# Using a comprehension (shorter)
my_new_list = [i for i in my_list if i % 2 == 0]
print(my_new_list)      # [4, 16]
```

### Side-by-side comparison

| Aspect            | `for` loop                             | List comprehension                               |
| ----------------- | -------------------------------------- | ------------------------------------------------ |
| **Lines of code** | More (init + loop + append)            | One line                                         |
| **Readability**   | Familiar to beginners                  | Compact; can be dense for complex logic          |
| **Speed**         | Slower (more bytecode)                 | Faster (optimized in C)                          |
| **Best for**      | Complex logic, side effects, debugging | Simple transforms/filters on an iterable         |
| **Memory**        | Builds list item by item               | Builds full list at once                         |
| **When to avoid** | Multiple statements per iteration      | Very long/nested expressions that get unreadable |

### The same logic, expanded

```python
# for loop version
result = []
for num in range(1, 11):
    if num % 2 == 0:
        result.append(num * num)

# comprehension version
result = [num * num for num in range(1, 11) if num % 2 == 0]
# [4, 16, 36, 64, 100]
```

> **Rule of thumb**: Use a comprehension when the logic fits comfortably on one line. If you need multiple steps, `if`/`elif` branches, `break`, or `continue`, a regular `for` loop is clearer.

---

## 7. Conditional Logic in the Expression (if/else)

You can use an **`if`/`else`** inside the _expression_ part — this is different from the trailing filter `if`. The `if` at the front picks one of two values; the `if` at the back decides whether to include the item.

```python
# Positive/negative labels (if/else in the expression)
numbers = [-3, 5, -1, 8]
labels = ["positive" if n > 0 else "negative" for n in numbers]
print(labels)           # ['negative', 'positive', 'negative', 'positive']

# Keep even numbers, replace odd with 0
numbers = [1, 2, 3, 4, 5]
result = [n if n % 2 == 0 else 0 for n in numbers]
print(result)           # [0, 2, 0, 4, 0]
```

### Filter `if` vs expression `if/else`

```python
# Trailing if -> filters (fewer items)
filtered = [n for n in range(6) if n % 2 == 0]
print(filtered)         # [0, 2, 4]

# if/else in expression -> same count, values change
changed = [n if n % 2 == 0 else -1 for n in range(6)]
print(changed)          # [0, -1, 2, -1, 4, -1]
```

---

## 8. Real-World Use Cases

### Extract data from a list of dicts (e.g. query results)

```python
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Carol", "age": 35},
]

names = [u["name"] for u in users]
print(names)            # ['Alice', 'Bob', 'Carol']

adults = [u["name"] for u in users if u["age"] >= 30]
print(adults)           # ['Alice', 'Carol']
```

### Clean and transform raw data

```python
raw_prices = ["$12.50", "$3.00", "$7.75"]
prices = [float(p.strip("$")) for p in raw_prices]
print(prices)           # [12.5, 3.0, 7.75]
```

### Filter valid entries

```python
values = ["1", "abc", "42", "", "7"]
valid = [int(v) for v in values if v.isdigit()]
print(valid)            # [1, 42, 7]
```

### Build a character lookup / quick table

```python
# ASCII codes for letters
codes = [(ch, ord(ch)) for ch in "abc"]
print(codes)            # [('a', 97), ('b', 98), ('c', 99)]
```

### Get indices meeting a condition

```python
scores = [55, 92, 78, 64, 88]
passing_positions = [i for i, s in enumerate(scores) if s >= 75]
print(passing_positions)   # [1, 2, 4]
```

### Prime filtering (related to Day-38)

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [n for n in range(2, 50) if is_prime(n)]
print(primes)
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

---

## 9. Related Comprehensions (set, dict, generator)

The same idea works for other collections.

### Set comprehension `{}` — deduplicates

```python
numbers = [1, 2, 2, 3, 3, 3]
unique_squares = {n ** 2 for n in numbers}
print(unique_squares)   # {1, 4, 9}
```

### Dict comprehension `{k: v}`

```python
words = ["apple", "banana", "cherry"]
length_map = {w: len(w) for w in words}
print(length_map)       # {'apple': 5, 'banana': 6, 'cherry': 6}
```

### Generator expression `()` — lazy, memory-efficient

```python
total = sum(n ** 2 for n in range(5))   # note: no extra list built
print(total)            # 30  (0 + 1 + 4 + 9 + 16)
```

> **Tip**: Prefer a generator expression over a comprehension when you only need to iterate once or pass to functions like `sum()`, `max()`, `any()`, `all()` — it avoids building an intermediate list.

---

## 10. Common Pitfalls

| Pitfall                                                              | Fix                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Wrong order of `for`/`if` (filter before iterable)                   | Keep `expression` → `for ... in ...` → `if ...` order               |
| Overly long/nested comprehension that's hard to read                 | Break into a helper function or a regular `for` loop                |
| Confusing filter `if` (trailing) with `if/else` (in expression)      | Trailing `if` filters items; `if/else` in expression changes values |
| Forgetting that comprehensions always return a full list             | Use a generator expression if you want lazy evaluation              |
| Mutating the original list inside a comprehension                    | Build a new list; don't side-effect the source                      |
| Using a comprehension when you need `break`/`continue`/complex logic | Use a regular `for` loop instead                                    |
| Reusing a variable name that shadows an outer variable               | Use distinct, descriptive names                                     |
| Nested comprehension order confusion                                 | Read `for` clauses left-to-right like nested loops                  |

---

## 11. Quick Reference

```python
# Basic: transform every item
[expr for item in iterable]

# Filter: keep only items matching a condition
[expr for item in iterable if condition]

# Transform + filter
[expr(item) for item in iterable if condition(item)]

# if/else in the expression (changes values, not count)
[a if cond else b for item in iterable]

# Nested / flattening
[item for row in grid for item in row]

# With a function
[my_func(i) for i in data]
```

---

> **Key Takeaway**: A list comprehension is Python's elegant, one-line alternative to a `for` loop + `append()` for building lists. It excels at **transforming** items (`[n ** 2 for n in ...]`) and **filtering** items (`[n for n in ... if ...]`). It's generally **faster** and more concise, but a regular `for` loop is the better choice when the logic is complex or has side effects. Master the core form `[expression for item in iterable if condition]`, remember the reading order (left to right), and when you need laziness or memory efficiency, reach for a **generator expression** `(expr for ...)` instead. The same pattern also extends to **set** and **dict** comprehensions, making it one of the most versatile tools in the Pythonic toolbox.
