# FOR LOOPS

Iteration in Python and use cases.

> Python `for` loop — statements, patterns, and code samples.

> In `for` loop we say, for each element in a collection of elements, do something.

---

## 1. What is a `for` loop?

- **Description**: A `for` loop iterates over a **sequence or iterable** and executes a block of code for **each item**.
- **Uses**: Processing lists, tuples, strings, dictionaries, sets, files, ranges of numbers, and any iterable; building aggregations; applying transformations; repeated operations.
- **Core idea**: Unlike traditional counter-based loops, Python's `for` loop directly iterates over items — no manual index incrementing needed.
- **Syntax**: `for item in iterable:` followed by an indented block.
- **Guaranteed termination**: The loop naturally ends when the iterable is exhausted (no off-by-one index bugs).

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)     # apple / banana / cherry
```

---

## 2. Iterating Over Sequences

### Lists

```python
numbers = [10, 20, 30]
for n in numbers:
    print(n)          # 10 / 20 / 30
```

### Tuples

```python
colors = ("red", "green", "blue")
for color in colors:
    print(color)      # red / green / blue
```

### Strings (iterates over characters)

```python
word = "abc"
for ch in word:
    print(ch)         # a / b / c
```

### Sets (order not guaranteed)

```python
tags = {"python", "sql", "ai"}
for tag in tags:
    print(tag)        # order may vary
```

### Dictionaries (iterates over keys by default)

```python
person = {"name": "Alice", "age": 30}
for key in person:
    print(key, person[key])   # name Alice / age 30
```

---

## 3. The `range()` Function

`range()` generates a sequence of numbers — ideal for counting loops.

| Form                       | Description                       | Example           | Yields    |
| -------------------------- | --------------------------------- | ----------------- | --------- |
| `range(stop)`              | 0 to stop-1                       | `range(5)`        | 0,1,2,3,4 |
| `range(start, stop)`       | start to stop-1                   | `range(2, 6)`     | 2,3,4,5   |
| `range(start, stop, step)` | start to stop-1, stepping by step | `range(0, 10, 2)` | 0,2,4,6,8 |

```python
# Basic count
for i in range(5):
    print(i)          # 0 1 2 3 4

# Start and stop
for i in range(2, 6):
    print(i)          # 2 3 4 5

# With step
for i in range(0, 10, 2):
    print(i)          # 0 2 4 6 8

# Negative step (reverse)
for i in range(5, 0, -1):
    print(i)          # 5 4 3 2 1
```

> **Note**: `range()` is memory-efficient — it does not store all values at once; it generates them lazily.

---

## 4. Using an Index with `enumerate()`

When you need both the **index** and the **item**, use `enumerate()`.

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(index, fruit)
# 0 apple
# 1 banana
# 2 cherry

# Start the index at a custom value
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)
# 1 apple / 2 banana / 3 cherry
```

---

## 5. Iterating Multiple Sequences with `zip()`

Use `zip()` to loop over multiple same-length iterables in parallel.

```python
names = ["Alice", "Bob", "Carol"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Alice: 85 / Bob: 92 / Carol: 78
```

---

## 6. Iterating Over Dictionary Items

Use `.items()` to get both keys and values; `.keys()` and `.values()` for just keys or just values.

```python
person = {"name": "Alice", "age": 30, "city": "Nairobi"}

# Keys and values
for key, value in person.items():
    print(f"{key}: {value}")

# Keys only
for key in person.keys():
    print(key)          # name / age / city

# Values only
for value in person.values():
    print(value)        # Alice / 30 / Nairobi
```

---

## 7. The `break` Statement

`break` **exits the loop immediately** when a condition is met.

```python
for number in range(1, 10):
    if number == 5:
        break           # stop the loop entirely
    print(number)       # 1 2 3 4

# Example: find first item satisfying a condition
def find_first_divisible(items, divisor):
    for item in items:
        if item % divisor == 0:
            return item
    return None

print(find_first_divisible([7, 8, 9, 10], 3))   # 9
```

---

## 8. The `continue` Statement

`continue` **skips the rest of the current iteration** and moves to the next item.

```python
for number in range(1, 6):
    if number % 2 == 0:
        continue        # skip even numbers
    print(number)       # 1 3 5

# Example: skip blank lines
lines = ["a", "", "b", ""]
for line in lines:
    if not line:
        continue
    print(line.upper())   # A / B
```

---

## 9. The `pass` Statement

`pass` is a **no-op** (does nothing). It is used as a placeholder when a statement is **syntactically required** but you don't want to execute any code yet. Unlike `break` and `continue`, `pass` does **not** alter loop flow — execution simply continues to the next line.

```python
# Placeholder inside a loop (loop body cannot be empty)
for item in [1, 2, 3]:
    pass          # do nothing yet, but loop is valid
print("Loop done")   # runs after the loop

# Skipping a specific item without changing flow
for number in range(5):
    if number == 2:
        pass          # nothing happens; not like continue
    print(number)     # 0 1 2 3 4  (all printed)
```

### `pass` vs `break` vs `continue`

| Statement  | Effect on the loop                                 | Use case                                 |
| ---------- | -------------------------------------------------- | ---------------------------------------- |
| `break`    | Exits the loop entirely                            | Stop early when a condition is met       |
| `continue` | Skips the rest of the current iteration, goes next | Skip an item but keep looping            |
| `pass`     | Does nothing — loop continues normally             | Placeholder for code to be written later |

```python
# Combine all three
for number in range(1, 8):
    if number == 4:
        break          # stop entirely at 4
    if number == 2:
        continue       # skip 2
    if number == 3:
        pass           # no-op, prints 3 anyway
    print(number)      # 1 3
```

> **Tip**: `pass` is also commonly used as a placeholder for empty function/class bodies: `def upcoming(): pass`.

---

## 10. The `else` Clause on a Loop

A `for` loop can have an `else` block that runs **only if the loop completes without `break`**.

```python
# else runs (no break)
for i in range(3):
    print(i)            # 0 1 2
else:
    print("Loop finished normally")   # runs

# else does NOT run (loop was broken)
for i in range(3):
    if i == 1:
        break
else:
    print("Never reached")   # skipped because of break

# Real-world: search without a flag
def contains_negative(numbers):
    for n in numbers:
        if n < 0:
            print("Found a negative:", n)
            break
    else:
        print("No negatives found")

contains_negative([1, -2, 3])   # Found a negative: -2
contains_negative([1, 2, 3])    # No negatives found
```

---

## 11. Nested Loops

Loops inside loops — useful for 2D data, combinations, and grids.

```python
# 2D grid
for i in range(3):
    row = ""
    for j in range(3):
        row += f"({i},{j}) "
    print(row)
# (0,0) (0,1) (0,2)
# (1,0) (1,1) (1,2)
# (2,0) (2,1) (2,2)

# Matrix sum
matrix = [[1, 2], [3, 4]]
total = 0
for row in matrix:
    for value in row:
        total += value
print(total)            # 10
```

---

## 12. List Comprehensions (Loop Shortcut)

A concise way to build a list from a loop — often favored over a manual `for` + `append()`.

```python
# Manual loop
squares = []
for x in range(5):
    squares.append(x**2)
print(squares)          # [0, 1, 4, 9, 16]

# Equivalent comprehension
squares = [x**2 for x in range(5)]
print(squares)          # [0, 1, 4, 9, 16]

# With a condition
evens = [x for x in range(10) if x % 2 == 0]
print(evens)            # [0, 2, 4, 6, 8]
```

---

## 13. Real-World Use Cases (Combined Example)

### Summation / aggregation

```python
prices = [1200, 300, 450, 800]
total = 0
for price in prices:
    total += price
print(total)            # 2750
```

### Filtering

```python
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = []
for n in numbers:
    if n % 2 == 0:
        even_numbers.append(n)
print(even_numbers)     # [2, 4, 6]
```

### Processing file lines

```python
with open("my_files/example.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

### Building strings

```python
words = ["python", "is", "awesome"]
sentence = ""
for word in words:
    sentence += word + " "
print(sentence.strip())    # python is awesome
```

### Running a fixed number of times

```python
for attempt in range(3):
    print(f"Attempt {attempt + 1}")
# Attempt 1 / Attempt 2 / Attempt 3
```

### Table of values (data processing)

```python
temps_c = [20, 25, 30, 35]
print("C\tF")
for c in temps_c:
    f = c * 9 / 5 + 32
    print(f"{c}\t{f:.1f}")
# C	F
# 20	68.0
# 25	77.0
# 30	86.0
# 35	95.0
```

---

## 14. Common Pitfalls

| Pitfall                                                          | Fix                                                                                 |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Forgetting the colon `:` after the `for` line                    | Always add `:` after the iterable                                                   |
| Missing/incorrect indentation for the loop block                 | Indent the loop body consistently (4 spaces)                                        |
| Modifying a list while iterating over it (skips elements)        | Iterate over a copy: `for x in lst[:]:` or build a new list                         |
| Using `range(len(lst))` when you could iterate directly          | Iterate items directly: `for item in lst:`; use `enumerate()` if you need the index |
| `for` loop `else` runs even when you expected it not to          | Remember `else` runs only if the loop completes **without `break`**                 |
| Infinite-loop thinking with `for` (it's bounded by the iterable) | `for` is safe; use `while` only when the count is unknown                           |
| Mismatched `zip()` lengths (truncates to shortest)               | Use `itertools.zip_longest()` if you need to pad                                    |
| Reusing a variable name that shadows the loop variable           | Use clear, distinct variable names                                                  |
| `range()` confusion with `stop` being exclusive                  | `range(stop)` yields `0..stop-1`; adjust bounds accordingly                         |
| Forgetting `enumerate()` and manually tracking an index          | Use `for i, item in enumerate(items):`                                              |

---

> **Key Takeaway**: Python's `for` loop is the cleanest way to iterate over any sequence or iterable — no manual index arithmetic required. Master the core patterns: **`range()` for counting**, **`enumerate()` for index+item**, **`zip()` for parallel iteration**, **`.items()` for dicts**, and **comprehensions** for building collections concisely. Use **`break`** to exit early, **`continue`** to skip an iteration, and the **`else` clause** to run code only when the loop completes without breaking. Remember: **don't mutate a list while iterating over it**, **`range`'s stop is exclusive**, and **`for`/`else` only fires when there's no `break`**. When you find yourself writing `for i in range(len(lst))`, ask whether `for item in lst` or `for i, item in enumerate(lst)` is cleaner.
> </content>
