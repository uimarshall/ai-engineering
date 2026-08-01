# LISTS

Outline all properties and methods of a List and use cases.

> Python `list` — Properties, Methods, and Use Cases.

---

## 1. What is a `list`?

- **Description**: A `list` is an **ordered, mutable sequence** used to store a collection of items. Items can be of **any type** and can be mixed within the same list.
- **Uses**: Storing rows of data, user inputs, results of computations, temporary collections to sort/filter, implementing stacks & queues, and any collection that needs to grow, shrink, or change over time.
- **Mutability**: Unlike strings/tuples, lists **can be changed in place** — items can be added, removed, replaced, or reordered without creating a new object.
- **Under the hood**: A list is implemented as a **dynamic array** — it reserves extra capacity so `append()`/`pop()` at the end are **O(1)** amortized, while inserting/deleting at the front or middle is **O(n)** (items must shift).

```python
tasks = ["review", "write", "test"]
tasks.append("ship")        # add in place
tasks[0] = "re-review"      # replace in place — no new object
print(tasks)                # ['re-review', 'write', 'test', 'ship']
```

---

## 2. List Properties

| Property                | Description                                                                            |
| ----------------------- | -------------------------------------------------------------------------------------- |
| **Mutable**             | Can be modified in place: add, remove, replace, reorder items                          |
| **Ordered**             | Items have a defined insertion order; accessible by integer index                      |
| **Indexable**           | `lst[0]` returns the first item; negative indices count from the end (`lst[-1]`)       |
| **Sliceable**           | `lst[start:stop:step]` extracts sub-lists (returns a **new** list)                     |
| **Iterable**            | Can be looped over with `for item in lst:` — yields one item at a time                 |
| **Dynamic size**        | Grows/shrinks automatically with `append()`, `pop()`, `insert()`, `remove()`           |
| **Heterogeneous**       | Can hold mixed types: `[1, "a", 3.14, None, [1, 2]]` (including other lists)           |
| **Allows dupes**        | Duplicates are allowed: `[1, 1, 2]` is valid                                           |
| **Not hashable**        | Cannot be used as a dict key or set element (`hash(lst)` raises TypeError)             |
| **Length**              | `len(lst)` returns the number of items                                                 |
| **Membership**          | Supports `in` / `not in` for membership checks (O(n) for lists)                        |
| **Comparable**          | `==` compares item-by-item; `<`, `>` compare lexicographically                         |
| **Reference semantics** | Assigning/copying shares the **same object** unless you explicitly copy (see Pitfalls) |

```python
lst = [10, 20, 30, 40, 50]
print(lst[0])         # 10
print(lst[-1])        # 50
print(lst[1:4])       # [20, 30, 40]
print(lst[::-1])      # [50, 40, 30, 20, 10]  (reverse)
print(len(lst))       # 5
print(30 in lst)      # True
print(99 not in lst)  # True
```

---

## 3. List Creation

| Method                    | Syntax/Example                                  | Use Case                                            |
| ------------------------- | ----------------------------------------------- | --------------------------------------------------- |
| Square brackets (literal) | `[1, 2, 3]`, `[]`                               | Most common — fast and readable                     |
| `list()` constructor      | `list("abc")`, `list(range(3))`, `list((1, 2))` | Converting any iterable (string, tuple, set, range) |
| `range()` + `list()`      | `list(range(0, 10, 2))`                         | Numeric sequences                                   |
| Repetition `*`            | `[0] * 5`                                       | Pre-filling a fixed-size list                       |
| List comprehension        | `[x * x for x in range(5)]`                     | Building lists with a transformation/filter         |
| `split()` result          | `"a,b,c".split(",")`                            | Splitting text into a list                          |
| Nested literal            | `[[1, 2], [3, 4]]`                              | Matrices, grids, grouped data                       |

```python
a = [1, 2, 3]                      # literal
b = list("hello")                  # ['h', 'e', 'l', 'l', 'o']
c = list(range(5))                 # [0, 1, 2, 3, 4]
d = [0] * 4                        # [0, 0, 0, 0]
e = [x**2 for x in range(1, 6)]    # [1, 4, 9, 16, 25]
f = "red,green,blue".split(",")    # ['red', 'green', 'blue']
g = [[1, 2], [3, 4]]               # nested list (matrix)
```

> **Watch out**: `[0] * 5` is fine for immutable items, but `[[]] * 3` creates **three references to the same inner list** — a classic bug (see Pitfalls).

---

## 4. List Operators

| Operator          | Example              | Result             | Use Case                                  |
| ----------------- | -------------------- | ------------------ | ----------------------------------------- |
| `+` (concat)      | `[1, 2] + [3, 4]`    | `[1, 2, 3, 4]`     | Combining lists (creates a **new** one)   |
| `*` (repeat)      | `["ab"] * 3`         | `['ab','ab','ab']` | Repeating patterns, padding               |
| `in`              | `3 in [1, 2, 3]`     | `True`             | Membership test                           |
| `not in`          | `5 not in [1, 2, 3]` | `True`             | Negated membership test                   |
| `==` / `!=`       | `[1, 2] == [1, 2]`   | `True`             | Item-by-item equality check               |
| `<`, `>`, ...     | `[1, 2] < [1, 3]`    | `True`             | Lexicographic comparison                  |
| `+=` (aug-assign) | `lst += [4]`         | in-place extend    | Appending multiple items to existing list |
| `*=` (aug-assign) | `lst *= 2`           | in-place repeat    | Repeating a list in place                 |

```python
print([1, 2] + [3, 4])       # [1, 2, 3, 4]
print([0] * 3)               # [0, 0, 0]
print(2 in [1, 2, 3])        # True

x = [1, 2]
x += [3, 4]                  # in-place extend — x is [1, 2, 3, 4]
x *= 2                       # x is [1, 2, 3, 4, 1, 2, 3, 4]
```

---

## 5. List Methods

All methods are called on a list object: `lst.method(...)`. Unlike strings, most mutating methods modify the list **in place** and return `None`.

### 5.1 Adding Items

| Method                | Description                                | Example               | Result      | Use Case                      |
| --------------------- | ------------------------------------------ | --------------------- | ----------- | ----------------------------- |
| `lst.append(item)`    | Add **one** item to the end                | `[1].append(2)`       | `[1, 2]`    | Building a list item-by-item  |
| `lst.extend(iter)`    | Add all items from an iterable to the end  | `[1].extend([2, 3])`  | `[1, 2, 3]` | Merging sequences             |
| `lst.insert(i, item)` | Insert item at index `i` (shifts the rest) | `[1, 3].insert(1, 2)` | `[1, 2, 3]` | Adding to a specific position |

```python
nums = [1]
nums.append(2)          # [1, 2]
nums.extend([3, 4])     # [1, 2, 3, 4]
nums.insert(0, 0)       # [0, 1, 2, 3, 4]
print(nums)

# append vs extend — the difference is important
a = [1, 2]
a.append([3, 4])        # [1, 2, [3, 4]]  — nested list added as ONE item
b = [1, 2]
b.extend([3, 4])        # [1, 2, 3, 4]    — each item added separately
```

### 5.2 Removing Items

| Method              | Description                                                          | Example               | Result             | Use Case                          |
| ------------------- | -------------------------------------------------------------------- | --------------------- | ------------------ | --------------------------------- |
| `lst.remove(item)`  | Remove **first** occurrence by value (raises `ValueError` if absent) | `[1, 2, 3].remove(2)` | `[1, 3]`           | Removing by value                 |
| `lst.pop(index=-1)` | Remove & **return** item at index (default last)                     | `[1, 2, 3].pop()`     | `3`, list `[1, 2]` | Stack behavior, getting last item |
| `lst.clear()`       | Remove **all** items                                                 | `[1, 2].clear()`      | `[]`               | Resetting a collection            |

```python
stack = [1, 2, 3]
last = stack.pop()          # last = 3, stack = [1, 2]
stack.remove(1)             # stack = [2]
print(stack)                # [2]
stack.clear()               # stack = []

# pop(index) removes from a specific position and returns it
fruits = ["apple", "banana", "cherry"]
item = fruits.pop(1)        # item = 'banana', fruits = ['apple', 'cherry']

# remove() raises if the value is missing
try:
    fruits.remove("mango")
except ValueError:
    print("mango not found")  # mango not found
```

### 5.3 Searching & Counting

| Method            | Description                                                   | Example                 | Result | Use Case                    |
| ----------------- | ------------------------------------------------------------- | ----------------------- | ------ | --------------------------- |
| `lst.index(item)` | Index of **first** occurrence (raises `ValueError` if absent) | `["a", "b"].index("b")` | `1`    | Locating an item's position |
| `lst.count(item)` | Number of occurrences of `item`                               | `[1, 1, 2].count(1)`    | `2`    | Counting duplicates         |

```python
data = ["x", "y", "x", "z"]
print(data.index("y"))      # 1
print(data.index("x"))      # 0  — first occurrence only
print(data.count("x"))      # 2

# index() with start/stop bounds
nums = [1, 2, 1, 2, 1]
print(nums.index(1, 2))     # 2  — first 1 at or after index 2
print(nums.index(1, 3))     # 4
```

### 5.4 Reordering & Sorting

| Method                              | Description                             | Example                            | Result               | Use Case                  |
| ----------------------------------- | --------------------------------------- | ---------------------------------- | -------------------- | ------------------------- |
| `lst.sort(key=None, reverse=False)` | Sort in place (stable) — returns `None` | `[3, 1, 2].sort()`                 | `[1, 2, 3]`          | In-place sorting          |
| `lst.reverse()`                     | Reverse items in place — returns `None` | `[1, 2, 3].reverse()`              | `[3, 2, 1]`          | Reversing order           |
| `lst.sort(key=len)`                 | Sort using a key function               | `["bb", "a", "ccc"].sort(key=len)` | `['a', 'bb', 'ccc']` | Sorting by computed value |

```python
nums = [3, 1, 2]
nums.sort()                 # nums = [1, 2, 3]
nums.sort(reverse=True)     # nums = [3, 2, 1]

words = ["banana", "apple", "cherry"]
words.sort(key=len)         # by length: ['apple', 'banana', 'cherry']
words.sort(key=lambda w: w[-1])  # by last letter

nums.reverse()              # nums = [1, 2, 3]
```

> **Note**: `lst.sort()` sorts **in place** and returns `None`. `sorted(lst)` returns a **new** sorted list and leaves the original unchanged (see Built-ins).

### 5.5 Copying

| Method       | Description                                 | Example         | Result         | Use Case                      |
| ------------ | ------------------------------------------- | --------------- | -------------- | ----------------------------- |
| `lst.copy()` | Shallow copy of the list (same as `lst[:]`) | `[1, 2].copy()` | `[1, 2]` (new) | Independent copy for mutation |

```python
original = [1, [2, 3]]
shallow = original.copy()       # new outer list, SAME inner list
shallow.append(4)               # original unaffected -> [1, [2, 3]]
shallow[1][0] = 99              # original ALSO affected! inner list shared
print(original)                 # [1, [99, 3]]

# For nested lists, use deepcopy
import copy
deep = copy.deepcopy(original)
deep[1][0] = 0
print(original)                 # [1, [99, 3]]  — untouched
```

---

## 6. Indexing & Slicing

### Indexing

- `lst[0]` → first item; `lst[-1]` → last item; `lst[-2]` → second-to-last.
- Out-of-range positive/negative index raises `IndexError`.

```python
lst = [10, 20, 30, 40]
print(lst[0], lst[-1], lst[-2])     # 10 40 30

try:
    print(lst[10])
except IndexError:
    print("Index out of range")     # Index out of range
```

### Slicing — `lst[start:stop:step]`

- Returns a **new list** (a copy).
- `start` inclusive, `stop` exclusive.
- Negative `step` reverses direction.
- Omitting `start`/`stop` defaults to the full list.

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])        # [2, 3, 4]
print(nums[:4])         # [0, 1, 2, 3]   — first 4
print(nums[6:])         # [6, 7, 8, 9]   — from index 6 to end
print(nums[::2])        # [0, 2, 4, 6, 8]  — evens
print(nums[::-1])       # [9, 8, ..., 0]   — reversed copy
print(nums[-3:])        # [7, 8, 9]        — last 3

# Slice assignment — replace a slice in place
nums[2:5] = [20, 30]    # [0, 1, 20, 30, 5, 6, 7, 8, 9]
```

---

## 7. Related Built-in Functions

| Function                    | Description                                | Example                         | Result              | Use Case                    |
| --------------------------- | ------------------------------------------ | ------------------------------- | ------------------- | --------------------------- |
| `len(lst)`                  | Number of items                            | `len([1, 2, 3])`                | `3`                 | Counts, validation          |
| `max(lst)` / `min(lst)`     | Highest / lowest item (must be comparable) | `max([3, 1, 2])`                | `3`                 | Extremes                    |
| `sum(lst)`                  | Sum of items (numeric)                     | `sum([1, 2, 3])`                | `6`                 | Aggregation                 |
| `sorted(lst, key, reverse)` | Returns a **new** sorted list              | `sorted([3, 1, 2])`             | `[1, 2, 3]`         | Non-destructive sorting     |
| `reversed(lst)`             | Iterator over items in reverse order       | `list(reversed([1, 2, 3]))`     | `[3, 2, 1]`         | Reversing without modifying |
| `enumerate(lst)`            | Yields `(index, item)` pairs               | `list(enumerate(["a", "b"]))`   | `[(0,'a'),(1,'b')]` | Looping with index          |
| `zip(lst1, lst2, ...)`      | Pairs up items across multiple lists       | `list(zip([1, 2], ["a", "b"]))` | `[(1,'a'),(2,'b')]` | Combining columns           |
| `all(lst)` / `any(lst)`     | `True` if all / any item is truthy         | `all([True, 1, "x"])`           | `True`              | Validations, flags          |
| `list(iterable)`            | Convert any iterable to a list             | `list("abc")`                   | `['a','b','c']`     | Conversion                  |

```python
scores = [80, 92, 75, 88]
print(sum(scores))                  # 335
print(max(scores), min(scores))     # 92 75
print(sorted(scores, reverse=True)) # [92, 88, 80, 75]  (original unchanged)

for i, name in enumerate(["alice", "bob"]):
    print(i, name)                  # 0 alice / 1 bob

names = ["alice", "bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(name, age)                # alice 30 / bob 25
```

---

## 8. List Comprehensions

A concise way to build lists by transforming/filtering an iterable.

```python
# Basic — square of each number
squares = [x**2 for x in range(5)]           # [0, 1, 4, 9, 16]

# With condition — only even squares
evens = [x**2 for x in range(10) if x % 2 == 0]   # [0, 4, 16, 36, 64]

# With transformation on strings
words = ["apple", "banana", "cherry"]
lengths = [len(w) for w in words]            # [5, 6, 6]

# Nested comprehension (flattening a matrix)
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]      # [1, 2, 3, 4, 5, 6]

# With a conditional expression (ternary)
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']
```

> List comprehensions are generally **faster and more readable** than building a list with a manual `for` + `append()` loop.

---

## 9. Lists as Stacks & Queues

### Stack (LIFO — Last In, First Out)

Use `append()` to push and `pop()` to pop. Both are **O(1)** at the end.

```python
stack = []
stack.append("a")       # push
stack.append("b")
print(stack.pop())      # 'b'
print(stack.pop())      # 'a'
```

### Queue (FIFO — First In, First Out)

A list works for small queues using `append()` + `pop(0)`, but `pop(0)` is **O(n)** because items shift.

```python
queue = []
queue.append("first")
queue.append("second")
print(queue.pop(0))     # 'first' — works, but O(n) shifting
```

For performance-critical queues, use `collections.deque` — **O(1)** on both ends.

```python
from collections import deque

q = deque()
q.append("first")
q.append("second")
print(q.popleft())      # 'first' — O(1)
```

---

## 10. Full Summary Reference Table

| Category               | Methods / Operators                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Adding items**       | `append()`, `extend()`, `insert()`, `+`, `+=`, `*`, `*=`                                                         |
| **Removing items**     | `remove()`, `pop()`, `clear()`                                                                                   |
| **Searching/Counting** | `index()`, `count()`, `in`, `not in`                                                                             |
| **Reordering**         | `sort()`, `reverse()`                                                                                            |
| **Copying**            | `copy()`, `[:]`, `copy.deepcopy()` for nested lists                                                              |
| **Accessing**          | indexing `lst[i]`, negative indices, slicing `lst[start:stop:step]`, slice assignment                            |
| **Built-ins**          | `len()`, `max()`, `min()`, `sum()`, `sorted()`, `reversed()`, `enumerate()`, `zip()`, `all()`, `any()`, `list()` |
| **Comprehensions**     | `[expr for item in iterable if condition]`                                                                       |
| **Properties**         | mutable, ordered, heterogeneous, allows duplicates, dynamic size, not hashable                                   |

---

## 11. Real-World Use Cases (Combined Example)

### Cleaning & transforming data (data science / ETL)

```python
raw = ["  Alice ", "", "Bob", "alice", "  "]
cleaned = [name.strip() for name in raw if name.strip()]     # drop blanks
unique = list(dict.fromkeys(cleaned))                        # preserve order, drop dupes
print(cleaned)   # ['Alice', 'Bob', 'alice']
print(unique)    # ['Alice', 'Bob', 'alice']
```

### Aggregating multiple columns with `zip`

```python
names = ["Alice", "Bob", "Carol"]
scores = [85, 92, 78]
grades = ["B", "A", "C"]

report = [f"{n}: {s} ({g})" for n, s, g in zip(names, scores, grades)]
for line in report:
    print(line)
# Alice: 85 (B)
# Bob: 92 (A)
# Carol: 78 (C)
```

### Building a CSV output row

```python
headers = ["name", "age", "city"]
row = ["Alice", 30, "Nairobi"]
print(",".join(headers))                     # name,age,city
print(",".join(str(item) for item in row))   # Alice,30,Nairobi
```

### Implementing a simple stack (undo history)

```python
history = []
def do(action):
    history.append(action)
    print(f"Done: {action}")

def undo():
    if history:
        print(f"Undo: {history.pop()}")
    else:
        print("Nothing to undo")

do("edit title"); do("change color"); undo()   # Undo: change color
```

### Batch processing with slicing (chunking)

```python
items = list(range(1, 11))          # [1..10]
chunk_size = 3
chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
print(chunks)  # [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
```

---

## 12. Common Pitfalls

| Pitfall                                                         | Fix                                                                              |
| --------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Assigning `b = a` and mutating `b` — `a` changes too (aliasing) | `b = a.copy()` or `b = a[:]` for a shallow copy; `copy.deepcopy(a)` for nested   |
| `[[]] * 3` creates 3 references to the **same** inner list      | Use a comprehension: `[[] for _ in range(3)]`                                    |
| Mutating a list while iterating over it (skips/shifts items)    | Iterate over a copy: `for x in lst[:]:` or build a new list with a comprehension |
| Using `lst.sort()` and expecting the return value               | `sort()` returns `None` and sorts in place; use `sorted(lst)` to get a new list  |
| `lst.append([1, 2])` vs `lst.extend([1, 2])` confusion          | `append` adds one nested item; `extend` adds each element separately             |
| `index()`/`remove()` on an absent value raises `ValueError`     | Guard with `if item in lst:` or catch `ValueError`                               |
| `pop()` vs `pop(0)` on big lists                                | `pop(0)` is O(n); use `collections.deque` for front-removal-heavy workloads      |
| Default argument `def f(lst=[])` shares state across calls      | Use `def f(lst=None): lst = lst or []`                                           |
| Slice confusion `lst[:n]` vs `lst[n:]`                          | `lst[:n]` = first n items; `lst[n:]` = from index n to the end                   |
| Treating lists as hashable (using as dict key)                  | Convert to `tuple(lst)` if the contents are immutable                            |

---

> **Key Takeaway**: Lists are Python's workhorse data structure — ordered, mutable, and flexible enough to hold anything. Master the method families (adding, removing, searching, sorting), slicing, and comprehensions to write clean, efficient collection-handling code. Remember the golden rules: **`sort()` mutates in place, `sorted()` returns new**, **`append` vs `extend` are not the same**, and **assignment copies references, not data** — use `.copy()` or `copy.deepcopy()` when you need independence. When you need speed on both ends of a queue, reach for `collections.deque`.
