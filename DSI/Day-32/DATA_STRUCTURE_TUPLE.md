# TUPLES

Outline all properties and methods of a Tuple and use cases.

> Python `tuple` — Properties, Methods, and Use Cases.

---

## 1. What is a `tuple`?

- **Description**: A `tuple` is an **ordered, immutable sequence** used to store a collection of items. Items can be of **any type** and can be mixed within the same tuple.
- **Uses**: Storing fixed collections (coordinates, RGB values), returning multiple values from functions, protecting data from accidental modification, and serving as **dictionary keys / set elements** (because they are hashable when their contents are).
- **Immutability**: Unlike lists, tuples **cannot be changed in place** — no adding, removing, or replacing items after creation. Any operation that appears to modify a tuple actually creates a **new** tuple.
- **Under the hood**: A tuple is stored as a **fixed-size array**. It is **smaller and faster** than an equivalent list because it doesn't reserve extra capacity for growth.
- **Tuple vs List**: The two key differences are **mutability** (tuples are immutable, lists are mutable) and **hashability** (tuples can be dict keys, lists cannot). Everything else — ordering, indexing, slicing, iteration, membership — works identically.

|            | Tuple                      | List                    |
| ---------- | -------------------------- | ----------------------- |
| Mutability | **Immutable**              | Mutable                 |
| Hashable   | **Yes** (if contents are)  | No                      |
| Dict key   | **Allowed**                | Not allowed             |
| Methods    | Only `count()` / `index()` | Many mutating methods   |
| Memory     | Smaller, faster            | Larger (extra capacity) |
| Use case   | Fixed, protected data      | Dynamic, changing data  |

```python
point = (3, 4)
x, y = point                # unpacking
print(x, y)                 # 3 4

# Immutability demo — this raises a TypeError
t = (1, 2, 3)
t[0] = 99   # TypeError: 'tuple' object does not support item assignment
```

---

## 2. Tuple Properties

| Property          | Description                                                                           |
| ----------------- | ------------------------------------------------------------------------------------- |
| **Immutable**     | Cannot be modified in place; every "change" creates a new tuple                       |
| **Ordered**       | Items have a defined order; accessible by integer index                               |
| **Indexable**     | `t[0]` returns the first item; negative indices count from the end (`t[-1]`)          |
| **Sliceable**     | `t[start:stop:step]` extracts sub-tuples (returns a **new** tuple)                    |
| **Iterable**      | Can be looped over with `for item in t:` — yields one item at a time                  |
| **Fixed size**    | Length is set at creation and never changes                                           |
| **Heterogeneous** | Can hold mixed types: `(1, "a", 3.14, None, [1, 2])` (including other tuples/lists)   |
| **Allows dupes**  | Duplicates are allowed: `(1, 1, 2)` is valid                                          |
| **Hashable**      | Can be used as a dict key or set element **if all elements are hashable** (`hash(t)`) |
| **Length**        | `len(t)` returns the number of items                                                  |
| **Membership**    | Supports `in` / `not in` for membership checks (O(n))                                 |
| **Comparable**    | `==` compares item-by-item; `<`, `>` compare lexicographically                        |
| **Unpackable**    | Can be unpacked into variables: `a, b = t` (see Section 7)                            |

```python
t = (10, 20, 30, 40, 50)
print(t[0])         # 10
print(t[-1])        # 50
print(t[1:4])       # (20, 30, 40)
print(t[::-1])      # (50, 40, 30, 20, 10)  (reverse)
print(len(t))       # 5
print(30 in t)      # True
print(99 not in t)  # True
print(hash((1, 2))) # a hash value — usable as dict key
```

---

## 3. Tuple Creation

| Method                | Syntax/Example                                     | Use Case                                        |
| --------------------- | -------------------------------------------------- | ----------------------------------------------- |
| Parentheses (literal) | `(1, 2, 3)`, `()`                                  | Most common                                     |
| **No parentheses**    | `1, 2, 3` (comma makes the tuple)                  | Implicit tuples — function returns, assignments |
| Single-element tuple  | `(42,)` — **trailing comma is required**           | One-item tuples (`(42)` is just an int!)        |
| `tuple()` constructor | `tuple("abc")`, `tuple([1, 2])`, `tuple(range(3))` | Converting any iterable to a tuple              |
| Repetition `*`        | `(0,) * 4`                                         | Pre-filling a fixed tuple                       |
| Packing               | `t = 1, 2, 3` (comma-separated values)             | Building a tuple without parentheses            |
| `tuple(range(...))`   | `tuple(range(0, 10, 2))`                           | Numeric sequences                               |
| Nested literal        | `((1, 2), (3, 4))`                                 | Matrices, grids, grouped data                   |

```python
a = (1, 2, 3)             # literal with parentheses
b = 1, 2, 3               # packing — same as (1, 2, 3)
c = ()                    # empty tuple
d = (42,)                 # single-element tuple — NOTE the comma!
e = (42)                  # just the int 42, NOT a tuple
f = tuple("hello")        # ('h', 'e', 'l', 'l', 'o')
g = tuple([1, 2, 3])      # (1, 2, 3)
h = (0,) * 4              # (0, 0, 0, 0)
i = ((1, 2), (3, 4))      # nested tuple

print(type((42)))         # <class 'int'>
print(type((42,)))        # <class 'tuple'>
```

> **Watch out**: The **comma** creates the tuple, not the parentheses. `(42)` is an integer; `(42,)` is a tuple. An empty tuple is the only exception — it uses `()`.

---

## 4. Tuple Operators

| Operator          | Example              | Result             | Use Case                                   |
| ----------------- | -------------------- | ------------------ | ------------------------------------------ |
| `+` (concat)      | `(1, 2) + (3, 4)`    | `(1, 2, 3, 4)`     | Combining tuples (creates a **new** tuple) |
| `*` (repeat)      | `("ab",) * 3`        | `('ab','ab','ab')` | Repeating patterns, padding                |
| `in`              | `3 in (1, 2, 3)`     | `True`             | Membership test                            |
| `not in`          | `5 not in (1, 2, 3)` | `True`             | Negated membership test                    |
| `==` / `!=`       | `(1, 2) == (1, 2)`   | `True`             | Item-by-item equality check                |
| `<`, `>`, ...     | `(1, 2) < (1, 3)`    | `True`             | Lexicographic comparison                   |
| `+=` (aug-assign) | `t += (4,)`          | new tuple          | Concatenation — rebinds to a **new** tuple |

```python
print((1, 2) + (3, 4))       # (1, 2, 3, 4)
print(("x",) * 3)            # ('x', 'x', 'x')
print(2 in (1, 2, 3))        # True
print((1, 2) < (1, 3))       # True  — 2 < 3 at the second position

t = (1, 2)
t += (3,)                    # creates a NEW tuple (1, 2, 3) and rebinds t
print(t)                     # (1, 2, 3)
```

> **Note**: Unlike lists, `+=` on a tuple does **not** mutate in place — it creates a new tuple (immutability). There is no in-place `extend`, `append`, or `sort` because none of these exist for tuples.

---

## 5. Tuple Methods

Tuples expose only **two methods** — both are non-mutating (they return a value and leave the tuple unchanged). All other sequence behaviors come from operators and built-ins.

| Method          | Description                                                   | Example                 | Result | Use Case                    |
| --------------- | ------------------------------------------------------------- | ----------------------- | ------ | --------------------------- |
| `t.count(item)` | Number of occurrences of `item`                               | `(1, 1, 2).count(1)`    | `2`    | Counting duplicates         |
| `t.index(item)` | Index of **first** occurrence (raises `ValueError` if absent) | `("a", "b").index("b")` | `1`    | Locating an item's position |

```python
data = (1, 2, 1, 3, 1)
print(data.count(1))        # 3
print(data.index(2))        # 1
print(data.index(1))        # 0  — first occurrence only

# index() with start/stop bounds
print(data.index(1, 1))     # 2  — first 1 at or after index 1
print(data.index(1, 3))     # 4

# index() raises if the item is missing
try:
    data.index(99)
except ValueError:
    print("99 not found")   # 99 not found
```

> **Why so few methods?** Because tuples are immutable, all mutating list methods (`append`, `extend`, `insert`, `remove`, `pop`, `clear`, `sort`, `reverse`) are **absent** by design. If you need those operations, convert with `list(t)` or use a list from the start.

---

## 6. Indexing & Slicing

### Indexing

- `t[0]` → first item; `t[-1]` → last item; `t[-2]` → second-to-last.
- Out-of-range positive/negative index raises `IndexError`.

```python
t = (10, 20, 30, 40)
print(t[0], t[-1], t[-2])   # 10 40 30

try:
    print(t[10])
except IndexError:
    print("Index out of range")   # Index out of range
```

### Slicing — `t[start:stop:step]`

- Returns a **new tuple** (a copy).
- `start` inclusive, `stop` exclusive.
- Negative `step` reverses direction.
- Omitting `start`/`stop` defaults to the full tuple.

```python
nums = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
print(nums[2:5])        # (2, 3, 4)
print(nums[:4])         # (0, 1, 2, 3)   — first 4
print(nums[6:])         # (6, 7, 8, 9)   — from index 6 to end
print(nums[::2])        # (0, 2, 4, 6, 8)  — evens
print(nums[::-1])       # (9, 8, ..., 0)   — reversed copy
print(nums[-3:])        # (7, 8, 9)        — last 3

# Unlike lists, there is NO slice assignment for tuples:
# nums[2:5] = ... raises TypeError ('tuple' object does not support item assignment)
```

---

## 7. Tuple Unpacking

One of the most powerful tuple features — the ability to "unpack" values into variables.

### Parallel assignment

```python
point = (3, 4)
x, y = point                # x = 3, y = 4
print(x, y)                 # 3 4
```

### Swapping variables without a temporary

```python
a, b = 1, 2
a, b = b, a                 # a = 2, b = 1
print(a, b)                 # 2 1
```

### Starred unpacking (`*rest`)

```python
first, *middle, last = (1, 2, 3, 4, 5)
print(first)                # 1
print(middle)               # [2, 3, 4]   — rest is a list
print(last)                 # 5
```

### Returning multiple values from a function

```python
def min_max(numbers):
    return min(numbers), max(numbers)   # returns a tuple

lo, hi = min_max([3, 1, 4, 1, 5])
print(lo, hi)               # 1 5
```

### Unpacking in loops

```python
pairs = [(1, "a"), (2, "b"), (3, "c")]
for num, letter in pairs:
    print(num, letter)
# 1 a / 2 b / 3 c
```

> **Requirement**: The number of variables must match the number of items, unless you use `*rest` to capture the leftover items.

```python
x, y = (1, 2, 3)   # ValueError: too many values to unpack
```

---

## 8. Related Built-in Functions

| Function            | Description                                | Example                         | Result              | Use Case                             |
| ------------------- | ------------------------------------------ | ------------------------------- | ------------------- | ------------------------------------ |
| `len(t)`            | Number of items                            | `len((1, 2, 3))`                | `3`                 | Counts, validation                   |
| `max(t)` / `min(t)` | Highest / lowest item (must be comparable) | `max((3, 1, 2))`                | `3`                 | Extremes                             |
| `sum(t)`            | Sum of items (numeric)                     | `sum((1, 2, 3))`                | `6`                 | Aggregation                          |
| `sorted(t)`         | Returns a **new list** sorted              | `sorted((3, 1, 2))`             | `[1, 2, 3]`         | Sorting (tuples can't sort in place) |
| `reversed(t)`       | Iterator over items in reverse order       | `tuple(reversed((1, 2, 3)))`    | `(3, 2, 1)`         | Reversing without modifying          |
| `enumerate(t)`      | Yields `(index, item)` pairs               | `list(enumerate(("a", "b")))`   | `[(0,'a'),(1,'b')]` | Looping with index                   |
| `zip(t1, t2, ...)`  | Pairs up items across multiple sequences   | `list(zip((1, 2), ("a", "b")))` | `[(1,'a'),(2,'b')]` | Combining columns                    |
| `tuple(iterable)`   | Convert any iterable to a tuple            | `tuple("abc")`                  | `('a','b','c')`     | Conversion                           |

```python
scores = (80, 92, 75, 88)
print(sum(scores))                  # 335
print(max(scores), min(scores))     # 92 75
print(sorted(scores, reverse=True)) # [92, 88, 80, 75]  (returns a list!)
print(tuple(reversed(scores)))      # (88, 75, 92, 80)

for i, name in enumerate(("alice", "bob")):
    print(i, name)                  # 0 alice / 1 bob

names = ("alice", "bob")
ages = (30, 25)
for name, age in zip(names, ages):
    print(name, age)                # alice 30 / bob 25
```

> **Note**: `sorted(t)` returns a **list**, not a tuple. Convert back if needed: `tuple(sorted(t))`.

---

## 9. Hashability & Uses as Dict Keys / `namedtuple`

### When can a tuple be a dict key?

A tuple is hashable **only if all of its elements are hashable** (immutable). A tuple containing a list is **not** hashable.

```python
good = (1, 2, "a", (3, 4))       # all elements immutable -> hashable
bad = (1, 2, ["a", "b"])         # contains a list -> NOT hashable

print(hash(good))                # a hash value
# hash(bad) -> TypeError: unhashable type: 'list'
```

### Tuple as dictionary key

```python
locations = {
    (40.7128, -74.0060): "New York",   # (lat, lon) as a key
    (51.5074, -0.1278): "London",
    (35.6762, 139.6503): "Tokyo",
}
print(locations[(51.5074, -0.1278)])   # London

# Also works with tuples of strings
phonebook = {("Alice", "Smith"): "555-0100"}
print(phonebook[("Alice", "Smith")])   # 555-0100
```

### `namedtuple` — tuples with named fields

`collections.namedtuple` gives tuples the readability of objects while keeping tuple features (immutability, unpacking, ordering).

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)

print(p.x, p.y)         # 3 4   — access by name
print(p[0], p[1])       # 3 4   — access by index (still a tuple)
x, y = p                # 3 4   — unpacking still works
print(p._asdict())      # {'x': 3, 'y': 4}
print(p._replace(x=10)) # Point(x=10, y=4) — returns a NEW namedtuple
```

---

## 10. Full Summary Reference Table

| Category         | Methods / Operators                                                                             |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| **Methods**      | `count()`, `index()` (only two — no mutating methods)                                           |
| **Operators**    | `+`, `*`, `in`, `not in`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `+=` (rebinds to new tuple)         |
| **Accessing**    | indexing `t[i]`, negative indices, slicing `t[start:stop:step]`                                 |
| **Unpacking**    | parallel assignment, starred `*rest`, function returns, loop unpacking                          |
| **Built-ins**    | `len()`, `max()`, `min()`, `sum()`, `sorted()`, `reversed()`, `enumerate()`, `zip()`, `tuple()` |
| **Hashable**     | dict keys / set elements when all elements are hashable                                         |
| **`namedtuple`** | `namedtuple("Name", ["field1", "field2"])` from `collections`                                   |
| **Properties**   | immutable, ordered, heterogeneous, allows duplicates, fixed size, hashable                      |

---

## 11. Real-World Use Cases (Combined Example)

### Coordinates / fixed records

```python
# (latitude, longitude) — never changes, and works as a dict key
city = ("Nairobi", 1.2921, 36.8219)
name, lat, lon = city
print(f"{name}: ({lat}, {lon})")    # Nairobi: (1.2921, 36.8219)
```

### Function returning multiple values

```python
def divide(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder      # returns a tuple

q, r = divide(17, 5)
print(q, r)                         # 3 2
```

### Database / CSV rows

```python
rows = [
    (1, "Alice", 30, "Nairobi"),
    (2, "Bob", 25, "Mombasa"),
    (3, "Carol", 35, "Kisumu"),
]
for user_id, name, age, city in rows:
    print(f"{user_id}: {name}, {age}, {city}")
```

### Grouping / aggregating with `zip`

```python
names = ("Alice", "Bob", "Carol")
scores = (85, 92, 78)
grades = ("B", "A", "C")

report = [f"{n}: {s} ({g})" for n, s, g in zip(names, scores, grades)]
for line in report:
    print(line)
# Alice: 85 (B)
# Bob: 92 (A)
# Carol: 78 (C)
```

### Safe dictionary keys for a config / lookup table

```python
# Cache results keyed by immutable parameters
cache = {}
def fib(n):
    if n in cache:
        return cache[n]
    if n < 2:
        return n
    cache[n] = fib(n - 1) + fib(n - 2)
    return cache[n]

print(fib(10))      # 55
```

### Old-style string formatting with a tuple

```python
print("Name: %s, Age: %d" % ("Alice", 30))   # Name: Alice, Age: 30
# .format() and f-strings work too:
print("{} — {}".format(*("Alice", 30)))      # Alice — 30
```

---

## 12. Common Pitfalls

| Pitfall                                                           | Fix                                                                              |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `(42)` is an **int**, not a tuple — forgetting the trailing comma | Use `(42,)` for a single-element tuple                                           |
| `t = (1, 2)` then trying `t[0] = 99`                              | Tuples are immutable — rebuild a new tuple or use a list                         |
| Tuple **containing a list** is unhashable (dict key fails)        | Use a tuple of immutable elements, or convert the inner list to a tuple          |
| `t += (4,)` seems to "mutate" — it actually creates a new tuple   | Understand rebinding: the original object is unchanged, `t` now points elsewhere |
| Calling `t.sort()` (list habit)                                   | Tuples have no `sort()` — use `sorted(t)` (returns a list) or `tuple(sorted(t))` |
| `x, y = (1, 2, 3)` — too many values to unpack                    | Match variable count, or use starred unpacking `x, *rest = (1, 2, 3)`            |
| Forgetting `namedtuple` `_replace` returns a **new** object       | Reassign the result: `p = p._replace(x=10)`                                      |
| Using a mutable default in a function that returns a tuple        | Tuples can contain lists — keep elements immutable for hashability               |
| Confusing tuples with lists in APIs                               | Lists = dynamic/changing; tuples = fixed/protected records                       |
| `sorted(t)` returns a **list**, not a tuple                       | Wrap with `tuple(sorted(t))` if a tuple is required                              |

---

> **Key Takeaway**: Tuples are Python's way of saying "this data is fixed" — ordered, immutable, and lightweight. They excel at representing fixed records, returning multiple values, enabling parallel unpacking, and serving as hashable dictionary keys. Master the two methods (`count()`, `index()`), slicing, and unpacking, and remember the cardinal rules: **the comma creates the tuple** (`(42,)` not `(42)`), **`sorted()` returns a list**, **`+=` rebinds to a new tuple**, and **a tuple is hashable only if every element is hashable**. When you need named fields on top of tuple behavior, reach for `collections.namedtuple`.
