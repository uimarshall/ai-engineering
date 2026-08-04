# DICTIONARIES

Outline all properties and methods of a Dictionary and use cases.

> Python `dict` — Properties, Methods, and Use Cases.

---

## 1. What is a `dict`?

- **Description**: A `dict` (dictionary) is an **unordered\* (insertion-ordered in Python 3.7+) collection of **key-value pairs\*\*. Each key is mapped to a value, and values are retrieved by their key.
- **Uses**: Representing structured/record data (like JSON), lookup tables, configuration settings, caching/memoization, counting/tallying (frequency maps), grouping, and mapping from one value to another.
- **Key-value pairs**: A dictionary is written as `{key: value, ...}`. Keys must be **unique**, and values can be of **any type** (including other dicts, lists, etc.).
- **Hashable keys**: Every key must be **hashable** (immutable) — `int`, `str`, `float`, `tuple`, `frozenset` are allowed; `list`, `dict`, `set` are **not**.
- **Under the hood**: A dict is implemented as a **hash table**. This gives **O(1) average** lookup, insertion, and deletion by key — far faster than scanning a list.
- **Ordering**: Since Python 3.7, dictionaries **preserve insertion order** when iterating. Before that, order was not guaranteed.
- **Dict vs list**: Use a dict when you need fast lookup by a unique key; use a list when you need ordered, positional access.

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "Nairobi",
}
print(person["name"])      # Alice
person["age"] = 31         # update value in place
person["job"] = "Engineer" # add a new key-value pair
print(person)
```

---

## 2. Dict Properties

| Property                   | Description                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------- |
| **Key-value pairs**        | Each entry is a `key: value` pair; values are accessed via keys                         |
| **Unique keys**            | Keys cannot repeat — assigning an existing key **updates** its value                    |
| **Hashable keys**          | Keys must be hashable (immutable): `int`, `str`, `tuple`, `frozenset`; not `list`/`set` |
| **Ordered (3.7+)**         | Iteration preserves insertion order (Python 3.7+)                                       |
| **Mutable**                | Can add, remove, and update key-value pairs in place                                    |
| **Fast lookup**            | O(1) average get/insert/delete by key (hash table)                                      |
| **Dynamic size**           | Grows/shrinks automatically as pairs are added/removed                                  |
| **Iterable**               | Iterating a dict yields its **keys** by default; use `.items()` for pairs               |
| **Values can be any type** | Values may be `int`, `str`, `list`, `dict`, `None`, objects, etc.                       |
| **Length**                 | `len(d)` returns the number of key-value pairs                                          |
| **Membership**             | `in` / `not in` checks **keys** (not values) — O(1)                                     |
| **Not orderable**          | Dictionaries cannot be compared with `<`/`>` (only `==`/`!=` by contents)               |

```python
d = {"a": 1, "b": 2}
print(len(d))          # 2
print("a" in d)        # True  — checks keys
print(1 in d)          # False — does NOT check values
print(d["a"])          # 1

# Iteration yields keys
for k in d:
    print(k)           # a / b
```

---

## 3. Dict Creation

| Method                    | Syntax/Example                       | Use Case                                    |
| ------------------------- | ------------------------------------ | ------------------------------------------- |
| Curly braces (literal)    | `{"name": "Alice", "age": 30}`       | Most common — explicit key-value pairs      |
| `{}` empty                | `{}`                                 | **Empty dict**                              |
| `dict()` constructor      | `dict(name="Alice", age=30)`         | Building from keyword arguments             |
| `dict(iterable_of_pairs)` | `dict([("a", 1), ("b", 2)])`         | From a list of `(key, value)` tuples        |
| `dict(zip(keys, values))` | `dict(zip(["a", "b"], [1, 2]))`      | Building from parallel key/value lists      |
| `dict(mapping)`           | `dict(other_dict)`, `dict(**kwargs)` | Copying or merging                          |
| Dict comprehension        | `{x: x**2 for x in range(5)}`        | Building dictionaries with a transformation |
| `fromkeys()`              | `{}.fromkeys(["a", "b"], 0)`         | Creating a dict with default values         |

```python
a = {"name": "Alice", "age": 30}          # literal
b = {}                                    # empty dict
c = dict(name="Bob", age=25)              # {'name': 'Bob', 'age': 25}
d = dict([("x", 1), ("y", 2)])            # {'x': 1, 'y': 2}
keys = ["name", "age"]
vals = ["Carol", 35]
e = dict(zip(keys, vals))                 # {'name': 'Carol', 'age': 35}
f = {x: x**2 for x in range(4)}           # {0: 0, 1: 1, 2: 4, 3: 9}
g = {}.fromkeys(["a", "b", "c"], 0)       # {'a': 0, 'b': 0, 'c': 0}
```

> **Note**: The `{}` literal creates a **dict**, not a set. Use `set()` for an empty set.

---

## 4. Dict Operators

| Operator             | Description                                     | Example                        | Result             |
| -------------------- | ----------------------------------------------- | ------------------------------ | ------------------ |
| `d[key]`             | Get value for key (raises `KeyError` if absent) | `{"a": 1}["a"]`                | `1`                |
| `d[key] = value`     | Set / update value for a key                    | `{"a": 1}["a"] = 2`            | `{'a': 2}`         |
| `del d[key]`         | Remove a key-value pair (raises `KeyError`)     | `d = {"a": 1}; del d["a"]`     | `{}`               |
| `key in d`           | Test if a **key** exists (O(1))                 | `"a" in {"a": 1}`              | `True`             |
| `key not in d`       | Negated key test                                | `"b" not in {"a": 1}`          | `True`             |
| `==` / `!=`          | Content equality (order-independent)            | `{"a": 1} == {"a": 1}`         | `True`             |
| `\|` (merge, 3.9+)   | Merge two dicts into a new one                  | `{"a": 1} \| {"b": 2}`         | `{'a': 1, 'b': 2}` |
| `\|=` (update, 3.9+) | Merge another dict into this one in place       | `d = {"a": 1}; d \|= {"b": 2}` | `{'a': 1, 'b': 2}` |

```python
d = {"a": 1, "b": 2}
print(d["a"])            # 1
d["c"] = 3               # add -> {'a': 1, 'b': 2, 'c': 3}
d["a"] = 10              # update -> {'a': 10, 'b': 2, 'c': 3}
del d["b"]               # remove -> {'a': 10, 'c': 3}
print("a" in d)          # True
print("b" in d)          # False

# Merge operator (Python 3.9+)
merged = {"a": 1} | {"b": 2, "a": 99}   # {'a': 99, 'b': 2} — later wins
print(merged)
```

> **Note**: Using `d[key]` when the key is absent raises `KeyError`. Use `.get(key, default)` if you want a safe default instead (see Section 5).

---

## 5. Dict Methods

### 5.1 Accessing Values

| Method                       | Description                                                 | Example                   | Result       | Use Case                          |
| ---------------------------- | ----------------------------------------------------------- | ------------------------- | ------------ | --------------------------------- |
| `d[key]`                     | Get value; raises `KeyError` if absent                      | `{"a": 1}["a"]`           | `1`          | Direct access when key is present |
| `d.get(key, default=None)`   | Get value; returns `default` if absent (no error)           | `{"a": 1}.get("b", 0)`    | `0`          | Safe lookup with a fallback       |
| `d.setdefault(key, default)` | Get value, or set it to `default` if absent, then return it | `{}.setdefault("a", 5)`   | `5`          | Insert-if-missing pattern         |
| `d.keys()`                   | View of all keys (dict_keys)                                | `list({"a": 1}.keys())`   | `['a']`      | Iterating / checking keys         |
| `d.values()`                 | View of all values (dict_values)                            | `list({"a": 1}.values())` | `[1]`        | Iterating / aggregating values    |
| `d.items()`                  | View of all `(key, value)` pairs (dict_items)               | `list({"a": 1}.items())`  | `[('a', 1)]` | Looping over key-value pairs      |

```python
d = {"name": "Alice", "age": 30}

print(d.get("city"))            # None (default)
print(d.get("city", "Unknown")) # Unknown
print(d.get("age", 0))          # 30

# setdefault — insert only if missing
d.setdefault("city", "Nairobi")
d.setdefault("age", 99)         # already present -> unchanged
print(d)                        # {'name': 'Alice', 'age': 30, 'city': 'Nairobi'}

print(list(d.keys()))           # ['name', 'age', 'city']
print(list(d.values()))         # ['Alice', 30, 'Nairobi']
print(list(d.items()))          # [('name','Alice'), ('age',30), ('city','Nairobi')]

for key, value in d.items():
    print(key, "=", value)
```

### 5.2 Adding & Updating

| Method                    | Description                                               | Example                    | Result             |
| ------------------------- | --------------------------------------------------------- | -------------------------- | ------------------ |
| `d[key] = value`          | Add a new pair or update an existing key                  | `{}["a"] = 1`              | `{'a': 1}`         |
| `d.update(iterable)**kw)` | Add/update multiple pairs from a dict, pairs, or keywords | `{}.update({"a": 1}, b=2)` | `{'a': 1, 'b': 2}` |
| `d.setdefault(key, def)`  | Insert key with default only if missing                   | `{}.setdefault("a", 5)`    | `{'a': 5}`         |

```python
d = {"a": 1}
d["b"] = 2                    # add          -> {'a': 1, 'b': 2}
d.update({"c": 3, "a": 10})   # add c, update a -> {'a': 10, 'b': 2, 'c': 3}
d.update(d=None, e=4)         # hmm, use keywords: d.update(f=5)
print(d)

# Common merge pattern
config = {"host": "localhost"}
config.update({"port": 5432, "debug": True})
print(config)                 # {'host': 'localhost', 'port': 5432, 'debug': True}
```

### 5.3 Removing Items

| Method                     | Description                                                      | Example                    | Result     | Use Case                    |
| -------------------------- | ---------------------------------------------------------------- | -------------------------- | ---------- | --------------------------- |
| `d.pop(key, default=None)` | Remove key and **return its value**; return `default` if absent  | `{"a": 1}.pop("a")`        | `1`        | Remove-and-get (safe)       |
| `d.popitem()`              | Remove & return the **last** inserted `(key, value)` pair (LIFO) | `{"a": 1}.popitem()`       | `('a', 1)` | Iteratively draining a dict |
| `del d[key]`               | Remove a key (raises `KeyError` if absent)                       | `d = {"a": 1}; del d["a"]` | `{}`       | Direct removal              |
| `d.clear()`                | Remove all items                                                 | `{"a": 1}.clear()`         | `{}`       | Resetting a mapping         |

```python
d = {"a": 1, "b": 2, "c": 3}

value = d.pop("b")          # value = 2, d = {'a': 1, 'c': 3}
value = d.pop("z", -1)      # value = -1 (default, no error)

key, value = d.popitem()    # removes & returns ('c', 3) (last inserted)
print(d)                    # {'a': 1}

del d["a"]                  # d = {}
d.clear()                   # d = {}
```

### 5.4 Copying

| Method     | Description                       | Example           | Result           | Use Case                      |
| ---------- | --------------------------------- | ----------------- | ---------------- | ----------------------------- |
| `d.copy()` | Shallow copy of the dict          | `{"a": 1}.copy()` | `{'a': 1}` (new) | Independent copy for mutation |
| `dict(d)`  | Construction-based copy (shallow) | `dict({"a": 1})`  | `{'a': 1}`       | Another way to copy           |

```python
original = {"a": [1, 2], "b": 3}
shallow = original.copy()       # new outer dict, SAME inner list
shallow["c"] = 4                # original unaffected
shallow["a"].append(99)         # original ALSO affected! inner list shared
print(original)                 # {'a': [1, 2, 99], 'b': 3}

# For nested containers, use deepcopy
import copy
deep = copy.deepcopy(original)
deep["a"].append(0)
print(original)                 # {'a': [1, 2, 99], 'b': 3}  — untouched
```

---

## 6. Dict Comprehensions

A concise way to build a dictionary from an iterable.

```python
# Square of each number as a key -> value map
squares = {x: x**2 for x in range(5)}           # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# With a condition — only even numbers
evens = {x: x**2 for x in range(10) if x % 2 == 0}

# Transforming a list of words into word-length map
words = ["apple", "banana", "cherry"]
lengths = {w: len(w) for w in words}            # {'apple': 5, 'banana': 6, 'cherry': 6}

# Building from a list of pairs
pairs = [("a", 1), ("b", 2), ("a", 3)]
dedup = {k: v for k, v in pairs}                # {'a': 3, 'b': 2} — last wins

# Inverting a dict (swap keys and values)
orig = {"a": 1, "b": 2}
inverted = {v: k for k, v in orig.items()}      # {1: 'a', 2: 'b'}
```

> Dict comprehensions are concise and **faster** than building a dict with a manual `for` loop.

---

## 7. Iterating a Dictionary

There are several ways to iterate a dict, depending on whether you need keys, values, or both.

```python
d = {"name": "Alice", "age": 30, "city": "Nairobi"}

# Keys only (default)
for k in d:
    print(k)                     # name / age / city

# Keys explicitly
for k in d.keys():
    print(k)

# Values
for v in d.values():
    print(v)                     # Alice / 30 / Nairobi

# Key-value pairs (most common)
for k, v in d.items():
    print(f"{k}: {v}")

# Sorted keys
for k in sorted(d):
    print(k, d[k])
```

---

## 8. Related Built-in Functions

| Function            | Description                         | Example                         | Result       | Use Case                   |
| ------------------- | ----------------------------------- | ------------------------------- | ------------ | -------------------------- |
| `len(d)`            | Number of key-value pairs           | `len({"a": 1, "b": 2})`         | `2`          | Counts, validation         |
| `dict(iterable)`    | Build a dict from pairs / keywords  | `dict([("a", 1)])`, `dict(a=1)` | `{'a': 1}`   | Conversion / construction  |
| `list(d)`           | List of keys                        | `list({"a": 1})`                | `['a']`      | Getting keys as a list     |
| `sorted(d)`         | Sorted list of keys                 | `sorted({"b": 1, "a": 2})`      | `['a', 'b']` | Deterministic key ordering |
| `zip(keys, values)` | Pair up keys and values             | `dict(zip(["a"], [1]))`         | `{'a': 1}`   | Building dicts from lists  |
| `any(d)` / `all(d)` | `True` if any / all keys are truthy | `any({"a": 1})`                 | `True`       | Validating keys            |

```python
d = {"b": 1, "a": 2}
print(len(d))              # 2
print(list(d))             # ['b', 'a']  (insertion order)
print(sorted(d))           # ['a', 'b']  (sorted keys)

# Rebuilding from parallel lists
keys = ["name", "age"]
values = ["Alice", 30]
person = dict(zip(keys, values))
print(person)              # {'name': 'Alice', 'age': 30}
```

---

## 9. `defaultdict` and `Counter` (from `collections`)

### `defaultdict` — automatic default values

`collections.defaultdict` provides a default value for missing keys, avoiding manual `setdefault` checks.

```python
from collections import defaultdict

# Grouping items by first letter
words = ["apple", "avocado", "banana", "blueberry"]
groups = defaultdict(list)
for w in words:
    groups[w[0]].append(w)
print(groups)
# defaultdict(<class 'list'>, {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']})

# Counting with a default of int (0)
counts = defaultdict(int)
for ch in "banana":
    counts[ch] += 1
print(counts)   # defaultdict(int, {'b': 1, 'a': 3, 'n': 2})
```

### `Counter` — counting hashable items

`collections.Counter` is a dict subclass specialized for counting.

```python
from collections import Counter

freq = Counter("banana")
print(freq)             # Counter({'a': 3, 'n': 2, 'b': 1})
print(freq["a"])        # 3
print(freq.most_common(2))  # [('a', 3), ('n', 2)]
```

---

## 10. Full Summary Reference Table

| Category            | Methods / Operators                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------- |
| **Accessing**       | `d[key]`, `get()`, `setdefault()`, `keys()`, `values()`, `items()`                        |
| **Adding/Updating** | `d[key] = value`, `update()`, `setdefault()`, `\|` (merge, 3.9+), `\|=` (update, 3.9+)    |
| **Removing**        | `pop()`, `popitem()`, `del d[key]`, `clear()`                                             |
| **Copying**         | `copy()`, `dict(d)`, `copy.deepcopy()` for nested                                         |
| **Membership**      | `in`, `not in` (checks **keys**, O(1))                                                    |
| **Comprehensions**  | `{k: v for item in iterable if condition}`                                                |
| **Built-ins**       | `len()`, `dict()`, `list()`, `sorted()`, `zip()`, `any()`, `all()`                        |
| **`collections`**   | `defaultdict`, `Counter` for counting                                                     |
| **Properties**      | key-value pairs, unique/hashable keys, ordered (3.7+), mutable, O(1) lookup, dynamic size |

---

## 11. Real-World Use Cases (Combined Example)

### Representing structured data (record / JSON-like)

```python
user = {
    "id": 101,
    "name": "Alice",
    "email": "alice@example.com",
    "roles": ["admin", "editor"],
    "active": True,
}
print(user["name"])                    # Alice
print(user["roles"][0])                # admin
```

### Counting / frequency map

```python
words = "the cat sat on the mat the".split()
freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1
print(freq)   # {'the': 3, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}
```

### Grouping / aggregating

```python
people = [
    {"name": "Alice", "team": "A"},
    {"name": "Bob", "team": "B"},
    {"name": "Carol", "team": "A"},
]
by_team = {}
for p in people:
    by_team.setdefault(p["team"], []).append(p["name"])
print(by_team)   # {'A': ['Alice', 'Carol'], 'B': ['Bob']}
```

### Lookup table / configuration

```python
REGION_CODES = {
    "KE": "Kenya",
    "UG": "Uganda",
    "TZ": "Tanzania",
}
code = "UG"
print(REGION_CODES.get(code, "Unknown"))   # Uganda
```

### Caching / memoization

```python
cache = {}
def factorial(n):
    if n in cache:
        return cache[n]
    result = 1
    for i in range(2, n + 1):
        result *= i
    cache[n] = result
    return result

print(factorial(5))   # 120
print(factorial(5))   # 120 (from cache)
```

### Building a dict with `zip` (mapping columns to rows)

```python
headers = ["name", "age", "city"]
row = ["Alice", 30, "Nairobi"]
record = dict(zip(headers, row))
print(record)   # {'name': 'Alice', 'age': 30, 'city': 'Nairobi'}
```

---

## 12. Common Pitfalls

| Pitfall                                                        | Fix                                                                            |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `d[key]` raises `KeyError` when the key is missing             | Use `d.get(key, default)` or check `if key in d` first                         |
| `{}` creates a dict, not a set (or empty set)                  | For an empty set use `set()`, for an empty dict use `{}`                       |
| Using a `list`/`set` as a key raises `TypeError`               | Only use hashable (immutable) keys; convert to `tuple`/`frozenset` if needed   |
| Assuming dict order is random — it's insertion-ordered in 3.7+ | Rely on insertion order in 3.7+; use `sorted(d)` for a deterministic key order |
| `d.get("key")` returns `None` for missing keys                 | Provide an explicit default: `d.get("key", 0)`                                 |
| `.keys()`/`.values()`/`.items()` return **views**, not lists   | Convert with `list(...)` if you need a list (e.g., to index or re-sort)        |
| Mutating a dict while iterating over it                        | Iterate over a copy: `for k in list(d):` or collect keys first                 |
| `pop()` without default raises `KeyError`                      | Use `d.pop(key, default)` for a safe removal                                   |
| Shallow copy shares nested mutable values (list/dict)          | Use `copy.deepcopy(d)` for fully independent nested copies                     |
| `d.update(k=v)` treats `k` as a string literal                 | Use a dict or pairs for non-string keys: `d.update({1: "one"})`                |
| Forgetting that `in` checks **keys**, not values               | To check a value, use `v in d.values()`                                        |

---

> **Key Takeaway**: Dictionaries are Python's powerhouse mapping type — key-value storage with **O(1) lookup** and insertion-order preservation (3.7+). They are indispensable for structured/record data, lookups, counting, grouping, caching, and configuration. Master the essentials: **`get()` for safe reads**, **`setdefault()`/`defaultdict` for insert-if-missing**, **`.items()` for iteration**, **`.update()`/`|` for merging**, and **dict comprehensions** for building maps. Remember the cardinal rules: **keys must be hashable**, **`in` checks keys (not values)**, **`.keys()`/`.values()`/`.items()` are views**, and **assignment/shallow copy shares nested mutable values** — use `copy.deepcopy()` when you need full independence. When you need counting or group-by behavior, `collections.Counter` and `collections.defaultdict` are your best friends.
