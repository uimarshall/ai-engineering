# WHILE LOOP

Repetition based on a condition in Python and use cases.
While some condition is true (`while count < 3`), do something (`print(count)`), test if the condition nis still true (`count += 1 `).

```python
count = 0
while count < 3:
    print(count)      # 0 / 1 / 2
    count += 1        # update the condition variable
```

> Python `while` loop — statements, patterns, and code samples.

---

## 1. What is a `while` loop?

- **Description**: A `while` loop repeatedly executes a block of code **as long as a condition is `True`**. It stops when the condition becomes `False`.
- **Uses**: Repeating until a certain condition is met, reading input until a valid value is given, game loops, retry logic, processing streams/live data, and counting loops where the number of iterations isn't known in advance.
- **Core idea**: Unlike a `for` loop (which iterates over a fixed collection), a `while` loop runs until a **condition is no longer true** — the number of iterations is determined at runtime.
- **Syntax**: `while condition:` followed by an indented block. The condition is re-checked before each iteration.
- **Risk of infinite loops**: If the condition never becomes `False`, the loop runs forever. Always ensure the loop body modifies something that affects the condition.

```python
count = 0
while count < 3:
    print(count)      # 0 / 1 / 2
    count += 1        # update the condition variable
```

---

## 2. Basic `while` Loop

The simplest form — repeat while a condition holds.

```python
# Count from 1 to 5
i = 1
while i <= 5:
    print(i)          # 1 2 3 4 5
    i += 1
```

```python
# Sum numbers from 1 to 10
total = 0
n = 1
while n <= 10:
    total += n
    n += 1
print(total)          # 55
```

---

## 3. `while` vs `for`

| `for` loop                                        | `while` loop                                         |
| ------------------------------------------------- | ---------------------------------------------------- |
| Iterates over a **known** sequence/iterable       | Runs until a **condition** becomes `False`           |
| Number of iterations is fixed by the collection   | Number of iterations is determined at runtime        |
| Index is managed automatically                    | You manage the loop variable / condition manually    |
| Best for: iterating lists, ranges, dicts, strings | Best for: unknown iteration counts, condition-driven |

```python
# for — good when iterating a known collection
for x in [1, 2, 3]:
    print(x)

# while — good when the stop condition is dynamic
n = 1
while n < 100:
    print(n)
    n = n * 2          # 1, 2, 4, 8, 16, 32, 64 (stops after 128)
```

---

## 4. The `break` Statement

`break` **exits the loop immediately**, regardless of the condition.

```python
# Stop when a number is even
n = 1
while n <= 10:
    if n % 2 == 0:
        print("Found even:", n)   # Found even: 2
        break                     # exit the loop
    print(n)
    n += 1

# Infinite loop controlled by break
count = 0
while True:               # runs forever until break
    count += 1
    if count >= 5:
        break
print(count)              # 5
```

---

## 5. The `continue` Statement

`continue` **skips the rest of the current iteration** and jumps back to the condition check.

```python
# Print only odd numbers (skip evens)
n = 0
while n < 6:
    n += 1
    if n % 2 == 0:
        continue        # skip even numbers
    print(n)            # 1 3 5
```

---

## 6. The `pass` Statement

`pass` is a **no-op** placeholder. In a `while` loop it does nothing and the loop proceeds normally.

```python
# Placeholder in an empty loop body
n = 0
while n < 3:
    pass              # do nothing yet (loop body cannot be empty)
    n += 1

# pass does not change flow — unlike break/continue
n = 0
while n < 5:
    n += 1
    if n == 3:
        pass          # no-op; prints 3 anyway
    print(n)          # 1 2 3 4 5
```

### `pass` vs `break` vs `continue` in a `while` loop

| Statement  | Effect on the loop                                  | Use case                                 |
| ---------- | --------------------------------------------------- | ---------------------------------------- |
| `break`    | Exits the loop entirely                             | Stop early when a condition is met       |
| `continue` | Skips the current iteration, goes back to condition | Skip an iteration but keep looping       |
| `pass`     | Does nothing — loop continues normally              | Placeholder for code to be written later |

```python
# Combined example
n = 0
while n < 6:
    n += 1
    if n == 2:
        continue       # skip 2
    if n == 5:
        break          # stop at 5
    if n == 3:
        pass           # no-op, prints 3 anyway
    print(n)           # 1 3 4
```

---

## 7. The `else` Clause on a `while` Loop

A `while` loop can have an `else` block that runs **only if the loop ends normally** (i.e., the condition becomes `False`) — it does **not** run if the loop is terminated by a `break`.

```python
# else runs (condition becomes False naturally)
n = 0
while n < 3:
    print(n)            # 0 1 2
    n += 1
else:
    print("Loop finished")   # runs

# else does NOT run (loop was broken)
n = 0
while n < 10:
    if n == 3:
        break
    n += 1
else:
    print("Not reached")   # skipped because of break

# Real-world: search without a flag
def find_vowel(text):
    i = 0
    while i < len(text):
        if text[i] in "aeiou":
            print("Found vowel:", text[i])
            break
        i += 1
    else:
        print("No vowel found")

find_vowel("hello")     # Found vowel: e
find_vowel("cry")       # No vowel found
```

---

## 8. Infinite Loops & How to Avoid Them

An infinite loop runs forever because the condition never becomes `False`. Always make sure the loop body moves toward making the condition false.

```python
# DANGEROUS — never updates the condition
# n = 0
# while n < 5:
#     print(n)      # n never changes -> infinite loop

# SAFE — updates the condition variable
n = 0
while n < 5:
    print(n)
    n += 1          # n changes each iteration
```

### Common causes & fixes

| Cause                                                   | Fix                                                 |
| ------------------------------------------------------- | --------------------------------------------------- |
| Forgetting to increment the loop variable               | Update the variable inside the loop body            |
| Condition never becomes `False`                         | Ensure the loop body changes the condition's inputs |
| Using `while True:` without a `break`                   | Add a `break` statement to exit when appropriate    |
| Logic error (wrong comparison, e.g. `>` instead of `<`) | Double-check the condition logic                    |
| Modifying the wrong variable                            | Track the variable that controls the condition      |

```python
# Safe pattern: use while True with a break
attempts = 0
while True:
    attempts += 1
    print(f"Attempt {attempts}")
    if attempts >= 3:
        break          # guarantees termination
```

> **Tip**: If you can know the number of iterations upfront, prefer a `for` loop. Use `while` when the stop condition is genuinely runtime-dependent.

---

## 9. Real-World Use Cases (Combined Example)

### Reading input until valid (validation loop)

```python
while True:
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 120:
            break
        print("Age must be between 0 and 120.")
    except ValueError:
        print("Please enter a number.")
print(f"Age set to {age}")
```

### Retry logic (with limited attempts)

```python
import random

def retry(n, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        if random.random() < 0.5:
            return f"Success on attempt {attempts}"
    return "Failed after all attempts"

print(retry(1))
```

### Menu / interactive loop

```python
choice = ""
while choice != "q":
    choice = input("Enter command (start/stop/quit): ").strip().lower()
    if choice == "start":
        print("Starting...")
    elif choice == "stop":
        print("Stopping...")
    elif choice == "quit":
        print("Goodbye")
    else:
        print("Unknown command")
```

### Processing a stream of items until empty

```python
queue = ["task1", "task2", "task3"]
while queue:
    item = queue.pop(0)      # remove from front
    print(f"Processing {item}")
# Processing task1 / task2 / task3
```

### Countdown timer

```python
seconds = 5
while seconds > 0:
    print(seconds)
    seconds -= 1
print("Blast off!")          # 5 4 3 2 1 Blast off!
```

### Game loop (state-based)

```python
health = 100
while health > 0:
    health -= 25
    print(f"Health: {health}")
    if health <= 0:
        print("Game over")
# Health: 75 / 50 / 25 / 0 / Game over
```

---

## 10. Common Pitfalls

| Pitfall                                                         | Fix                                                                               |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| **Infinite loop** — condition never becomes `False`             | Always update the loop variable; add a `break` if using `while True:`             |
| Forgetting to initialize the loop variable before the loop      | Set the variable before `while` so the condition is meaningful on first check     |
| `while` with no `break` and a condition that stays true         | Audit the condition and ensure the body changes its inputs                        |
| `else` clause runs when you expected it not to                  | `else` runs only if the loop ends naturally (no `break`)                          |
| Using `==` in the condition instead of `<=`/`<` (off-by-one)    | Double-check comparison operators and boundaries                                  |
| Modifying a list while iterating with indices in a `while` loop | Iterate over a copy or adjust indices carefully                                   |
| `continue` skipping the update step, causing an infinite loop   | Update the loop variable **before** `continue`, or use a `for` loop               |
| Confusing `while` with `for` when iteration count is known      | Use `for` + `range()` when the count is known; use `while` for dynamic conditions |
| `while True` with no escape path (no `break`/`return`)          | Always provide a `break` or `return` to exit                                      |

---

> **Key Takeaway**: The `while` loop is Python's tool for **condition-driven repetition** — run until a condition is no longer true. It's ideal for input validation, retries, menus, game loops, and any scenario where the iteration count isn't known in advance. Master **`break`** to exit early, **`continue`** to skip an iteration, **`pass`** as a placeholder, and the **`else` clause** which runs only when the loop ends without `break`. Above all, **guard against infinite loops** — always update the variable that controls the condition, and prefer `while True` + `break` when you need a guaranteed exit. When the number of iterations is known, a `for` loop is usually the cleaner choice.
