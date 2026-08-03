# SETS

Outline all properties and methods of a Set and use cases.

> Python `set` — Properties, Methods, and Use Cases.

---

## 1. What is a `set`?

- **Description**: A `set` is an **unordered, mutable collection of unique, hashable items**. It is the Python implementation of the mathematical _set_ concept.
- **Uses**: Removing duplicates, fast membership testing, and performing mathematical set operations (union, intersection, difference, symmetric difference). Also used for tracking seen items, shared/unique elements, and tags/categories.
- **Uniqueness**: A set **cannot contain duplicates** — adding an item that already exists has no effect. This makes it ideal for deduplication.
- **Unordered**: Sets have **no defined order** and do **not support indexing or slicing**. `s[0]` raises a `TypeError`.
- **Hashable elements**: Every element must be **hashable** (immutable). You can store `int`, `str`, `float`, `tuple`, `frozenset`, but **not** `list`, `dict`, or another `set`.
- **Under the hood**: A set is implemented like a **hash table** (similar to a dict with only keys). This gives **O(1) average** membership, add, and remove operations, but iteration order is not guaranteed.
- **Set vs performance**: Membership testing with `in` on a set is O(1), whereas on a list/tuple it is O(n). This makes sets the go-to choice for large "is this present?" checks.

```python
tags = {"python", "data", "science"}
tags.add("ai")          # add in place
tags.add("python")      # duplicate — ignored, set unchanged
print(tags)             # {'python', 'data', 'science', 'ai'} (order not guaranteed)

# Unordered — no indexing
# tags[0]  -> TypeError: 'set' object is not subscriptable
```

---

## 2. Set Properties

| Property                | Description                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------- |
| **Unordered**           | No defined order; **not indexable or sliceable**; iteration order is not guaranteed   |
| **Mutable**             | Can be modified in place: add, remove, discard, update, clear                         |
| **Unique**              | No duplicate elements — adding an existing item is a no-op                            |
| **Hashable elements**   | Every element must be hashable (immutable); no `list`/`dict`/`set` elements           |
| **Not hashable itself** | A `set` cannot be a dict key or set element (use `frozenset` instead)                 |
| **Fast membership**     | O(1) average `in` / `not in` checks (hash-table based)                                |
| **Iterable**            | Can be looped over with `for item in s:` — yields each element once                   |
| **Length**              | `len(s)` returns the number of unique elements                                        |
| **Dynamic size**        | Grows/shrinks automatically with `add()`, `remove()`, `discard()`, `update()`         |
| **Set operations**      | `union`, `intersection`, `difference`, `symmetric_difference` (methods and operators) |
| **Comparable**          | `==` compares by contents (order-independent); `<`, `<=`, `>`, `>=` compare subsets   |

```python
s = {1, 2, 3}
print(len(s))          # 3
print(2 in s)          # True  — O(1) fast
print(99 not in s)     # True
print(len({1, 1, 2}))  # 2 — duplicates removed

# Equality ignores order
print({1, 2, 3} == {3, 2, 1})   # True

# Membership is dramatically faster than on a list
big_list = list(range(100_000))
big_set = set(big_list)
print(99_999 in big_set)   # True (O(1))
```

---

## 3. Set Creation

| Method                 | Syntax/Example                                    | Use Case                                       |
| ---------------------- | ------------------------------------------------- | ---------------------------------------------- |
| Curly braces (literal) | `{1, 2, 3}`, `{"a", "b"}`                         | Most common — from distinct elements           |
| `set()` constructor    | `set([1, 2, 2])`, `set("hello")`, `set(range(3))` | Converting any iterable; deduplicating a list  |
| `set()` empty          | `set()`                                           | **Empty set** (can't use `{}` — that's a dict) |
| Set comprehension      | `{x**2 for x in range(5)}`                        | Building a set with a transformation/filter    |
| `frozenset()`          | `frozenset([1, 2, 3])`                            | Immutable set (hashable, usable as dict key)   |
| From string characters | `set("banana")`                                   | Unique characters in a string                  |

```python
a = {1, 2, 3}                       # literal
b = set([1, 2, 2, 3, 3])            # {1, 2, 3} — deduplicates a list
c = set("banana")                   # {'a', 'b', 'n'} — unique letters
d = set(range(5))                   # {0, 1, 2, 3, 4}
e = {x % 3 for x in range(10)}      # {0, 1, 2} — set comprehension
f = set()                           # empty set  ({} is an empty dict!)
g = frozenset([1, 2, 3])            # immutable set

print(type({}))     # <class 'dict'>
print(type(set()))  # <class 'set'>
```

> **Watch out**: `{}` creates an **empty dict**, not an empty set. Use `set()` for an empty set.

---

## 4. Set Operators

Sets support both **operators** and the equivalent **methods** (see Section 5). These are the most distinctive feature of sets.

### Basic Operators

| Operator              | Description                            | Example               | Result      |
| --------------------- | -------------------------------------- | --------------------- | ----------- |
| `in`                  | Membership test (O(1))                 | `2 in {1, 2, 3}`      | `True`      |
| `not in`              | Negated membership test                | `5 not in {1, 2, 3}`  | `True`      |
| `==` / `!=`           | Content equality (order-independent)   | `{1, 2} == {2, 1}`    | `True`      |
| `\|` (union)          | All items from both sets               | `{1, 2} \| {2, 3}`    | `{1, 2, 3}` |
| `&` (intersection)    | Items common to both sets              | `{1, 2} & {2, 3}`     | `{2}`       |
| `-` (difference)      | Items in first set but not second      | `{1, 2, 3} - {2}`     | `{1, 3}`    |
| `^` (symmetric diff)  | Items in exactly one of the sets       | `{1, 2} ^ {2, 3}`     | `{1, 3}`    |
| `<=` (subset)         | First set is a subset of second        | `{1, 2} <= {1, 2, 3}` | `True`      |
| `<` (proper subset)   | First set is a strict subset of second | `{1, 2} < {1, 2, 3}`  | `True`      |
| `>=` (superset)       | First set contains second              | `{1, 2, 3} >= {1, 2}` | `True`      |
| `>` (proper superset) | First set strictly contains second     | `{1, 2, 3} > {1, 2}`  | `True`      |

```python
A = {1, 2, 3}
B = {2, 3, 4}

print(A | B)   # {1, 2, 3, 4}  union
print(A & B)   # {2, 3}        intersection
print(A - B)   # {1}           difference
print(B - A)   # {4}
print(A ^ B)   # {1, 4}        symmetric difference
print({1, 2} <= A)   # True   subset
print({1, 2} < A)    # True   proper subset
print(A >= {1, 2})   # True   superset
```

> **Augmented operators**: `|=`, `&=`, `-=`, `^=` mutate the set in place (like `update()`, `intersection_update()`, etc.).

```python
s = {1, 2}
s |= {2, 3}        # s = {1, 2, 3}
s &= {2, 3, 4}     # s = {2, 3}
s -= {3}           # s = {2}
s ^= {2, 5}        # s = {5}
print(s)           # {5}
```

---

## 5. Set Methods

### 5.1 Adding Items

| Method               | Description                                     | Example                | Result      | Use Case                      |
| -------------------- | ----------------------------------------------- | ---------------------- | ----------- | ----------------------------- |
| `s.add(item)`        | Add one item (no-op if already present)         | `{1}.add(2)`           | `{1, 2}`    | Building a set item-by-item   |
| `s.update(iterable)` | Add all items from an iterable (or another set) | `{1}.update([2, 3])`   | `{1, 2, 3}` | Merging multiple sources      |
| `s.update(a, b)`     | Add items from multiple iterables               | `{1}.update([2], [3])` | `{1, 2, 3}` | Combining several collections |

```python
s = {1}
s.add(2)            # {1, 2}
s.add(2)            # {1, 2} — duplicate ignored
s.update([3, 4])    # {1, 2, 3, 4}
s.update("ab")      # adds 'a', 'b' -> {1, 2, 3, 4, 'a', 'b'}
print(s)

# update() is equivalent to the |= operator
t = {10}
t |= {20, 30}       # {10, 20, 30}
```

### 5.2 Removing Items

| Method            | Description                                                        | Example              | Result              | Use Case                          |
| ----------------- | ------------------------------------------------------------------ | -------------------- | ------------------- | --------------------------------- |
| `s.remove(item)`  | Remove item; **raises `KeyError`** if absent                       | `{1, 2}.remove(1)`   | `{2}`               | Removing when absence is an error |
| `s.discard(item)` | Remove item; **no error** if absent                                | `{1, 2}.discard(99)` | `{1, 2}`            | Removing safely (no exception)    |
| `s.pop()`         | Remove & **return an arbitrary** item (raises `KeyError` if empty) | `{1, 2}.pop()`       | `1` or `2` (random) | Removing any element quickly      |
| `s.clear()`       | Remove **all** items                                               | `{1, 2}.clear()`     | `set()`             | Resetting a collection            |

```python
s = {1, 2, 3}
s.remove(2)          # {1, 3}
# s.remove(99)       # KeyError: 99

s.discard(99)        # no error — safe
s.discard(1)         # {3}

item = s.pop()       # returns an arbitrary element (3)
print(s)             # set()

# remove vs discard comparison
s = {1, 2}
try:
    s.remove(99)
except KeyError:
    print("99 not found")   # 99 not found
s.discard(99)               # silent no-op
```

### 5.3 Set Operations (Methods)

| Method                      | Description                 | Example                            | Result      | Equivalent Operator |
| --------------------------- | --------------------------- | ---------------------------------- | ----------- | ------------------- |
| `s.union(other)`            | All items from both sets    | `{1, 2}.union({2, 3})`             | `{1, 2, 3}` | `\|`                |
| `s.intersection(other)`     | Items common to both sets   | `{1, 2}.intersection({2, 3})`      | `{2}`       | `&`                 |
| `s.difference(other)`       | Items in `s` not in `other` | `{1, 2}.difference({2})`           | `{1}`       | `-`                 |
| `s.symmetric_difference(o)` | Items in exactly one set    | `{1, 2}.symmetric_difference({2})` | `{1}`       | `^`                 |
| `s.issubset(other)`         | `s` is a subset of `other`  | `{1, 2}.issubset({1, 2, 3})`       | `True`      | `<=`                |
| `s.issuperset(other)`       | `s` contains all of `other` | `{1, 2, 3}.issuperset({1, 2})`     | `True`      | `>=`                |
| `s.isdisjoint(other)`       | `True` if no common items   | `{1, 2}.isdisjoint({3, 4})`        | `True`      | —                   |

```python
A = {1, 2}
B = {2, 3}

print(A.union(B))                # {1, 2, 3}
print(A.intersection(B))         # {2}
print(A.difference(B))           # {1}
print(A.symmetric_difference(B)) # {1, 3}
print(A.issubset({1, 2, 3}))     # True
print({1, 2, 3}.issuperset(A))   # True
print(A.isdisjoint({5, 6}))      # True
```

### 5.4 In-Place Update Methods

| Method                                 | Description                    | Equivalent |
| -------------------------------------- | ------------------------------ | ---------- |
| `s.update(other)`                      | Add all items from `other`     | `\|=`      |
| `s.intersection_update(other)`         | Keep only items common to both | `&=`       |
| `s.difference_update(other)`           | Remove items found in `other`  | `-=`       |
| `s.symmetric_difference_update(other)` | Keep items in exactly one set  | `^=`       |

```python
s = {1, 2, 3}
s.intersection_update({2, 3, 4})   # s = {2, 3}
s.difference_update({3})           # s = {2}
s.symmetric_difference_update({2, 9})  # s = {9}
print(s)                           # {9}
```

### 5.5 Copying

| Method     | Description             | Example         | Result         | Use Case                      |
| ---------- | ----------------------- | --------------- | -------------- | ----------------------------- |
| `s.copy()` | Shallow copy of the set | `{1, 2}.copy()` | `{1, 2}` (new) | Independent copy for mutation |

```python
original = {1, 2, 3}
shallow = original.copy()   # separate set
shallow.add(99)
print(original)   # {1, 2, 3}  — unchanged
print(shallow)    # {1, 2, 3, 99}
```

---

## 6. Comparison & Membership

### Membership (`in`)

The most common use of a set — fast O(1) membership testing.

```python
allowed = {"admin", "editor", "viewer"}
role = "editor"
print(role in allowed)       # True
print("owner" in allowed)    # False

# Compare with a list — O(n) vs O(1)
roles_list = ["admin", "editor", "viewer"]
print("editor" in roles_list)   # True but O(n) scan
```

### Subset / Superset / Equality

```python
admins = {"alice", "bob"}
all_users = {"alice", "bob", "carol"}

print(admins.issubset(all_users))   # True
print(admins < all_users)           # True — proper subset
print(all_users.issuperset(admins)) # True
print(admins == {"bob", "alice"})   # True — order-independent
```

---

## 7. Set Comprehensions

Like list/dict comprehensions, but produce a `set`. They automatically drop duplicates.

```python
# Square of each number 0-9
squares = {x**2 for x in range(10)}        # {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}

# With a condition — squares of even numbers only
evens = {x**2 for x in range(10) if x % 2 == 0}   # {0, 4, 16, 36, 64}

# Unique first letters of words
words = ["apple", "banana", "cherry", "avocado"]
first_letters = {w[0] for w in words}      # {'a', 'b', 'c'}

# Normalize + deduplicate user input
raw = ["Alice", "alice", "BOB", "bob"]
unique = {name.lower() for name in raw}    # {'alice', 'bob'}
```

> Set comprehensions are concise and **faster** than building a set with a manual `for` + `add()` loop.

---

## 8. Related Built-in Functions

| Function              | Description                                   | Example             | Result              | Use Case                      |
| --------------------- | --------------------------------------------- | ------------------- | ------------------- | ----------------------------- |
| `len(s)`              | Number of unique elements                     | `len({1, 2, 2, 3})` | `3`                 | Counts, validation            |
| `set(iterable)`       | Convert any iterable to a set (dedup)         | `set([1, 1, 2])`    | `{1, 2}`            | Deduplication                 |
| `frozenset(iterable)` | Immutable set                                 | `frozenset([1, 2])` | `frozenset({1, 2})` | Hashable set for dict keys    |
| `max(s)` / `min(s)`   | Highest / lowest element (must be comparable) | `max({3, 1, 2})`    | `3`                 | Extremes                      |
| `sum(s)`              | Sum of elements (numeric)                     | `sum({1, 2, 3})`    | `6`                 | Aggregation                   |
| `sorted(s)`           | Returns a **new sorted list**                 | `sorted({3, 1, 2})` | `[1, 2, 3]`         | Getting a deterministic order |
| `any(s)` / `all(s)`   | `True` if any / all elements are truthy       | `any({0, 1})`       | `True`              | Validations, flags            |

```python
nums = {3, 1, 2, 1}          # {1, 2, 3}
print(len(nums))             # 3
print(max(nums), min(nums))  # 3 1
print(sum(nums))             # 6
print(sorted(nums))          # [1, 2, 3]  — a list, in sorted order
```

> **Note**: `sorted(s)` returns a **list** (sets are unordered). A set itself has no order you can rely on.

---

## 9. `frozenset` — The Immutable Set

`frozenset` is the immutable version of a set. It supports all the same set operations but **cannot be modified** (no `add`, `remove`, `discard`, `update`, `clear`). Because it is hashable, it can be used as a dict key or a set element.

```python
frozen = frozenset([1, 2, 3])
print(frozen)               # frozenset({1, 2, 3})
print(2 in frozen)          # True
print(frozen | {3, 4})      # frozenset({1, 2, 3, 4}) — new frozenset

# frozen.add(4)  -> AttributeError: 'frozenset' object has no attribute 'add'

# Usable as a dict key (unlike a set)
cache = {frozenset([1, 2]): "pair"}
print(cache[frozenset([1, 2])])   # pair

# A set of frozensets is valid (a set of sets is not)
s = {frozenset([1, 2]), frozenset([3, 4])}
print(s)   # {frozenset({1, 2}), frozenset({3, 4})}
```

---

## 10. Full Summary Reference Table

| Category             | Methods / Operators                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Adding items**     | `add()`, `update()`, `\|=`                                                                                                |
| **Removing items**   | `remove()` (raises), `discard()` (safe), `pop()` (arbitrary), `clear()`                                                   |
| **Set operations**   | `union()`/`\|`, `intersection()`/`&`, `difference()`/`-`, `symmetric_difference()`/`^`                                    |
| **Relationships**    | `issubset()`/`<=`, `issuperset()`/`>=`, `isdisjoint()`, `==` (content equality)                                           |
| **In-place updates** | `update()`, `intersection_update()`, `difference_update()`, `symmetric_difference_update()` (and `\|=`, `&=`, `-=`, `^=`) |
| **Copying**          | `copy()`                                                                                                                  |
| **Membership**       | `in`, `not in` (O(1))                                                                                                     |
| **Built-ins**        | `len()`, `max()`, `min()`, `sum()`, `sorted()`, `set()`, `frozenset()`, `any()`, `all()`                                  |
| **Comprehensions**   | `{expr for item in iterable if condition}`                                                                                |
| **Properties**       | unordered, mutable, unique elements, hashable elements, not hashable itself, O(1) membership, dynamic size                |

---

## 11. Real-World Use Cases (Combined Example)

### Removing duplicates from a list

```python
emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]
unique_list = list(set(emails))          # order not preserved
print(unique_list)                        # e.g. ['c@x.com', 'a@x.com', 'b@x.com']

# Preserve order with a set + list comprehension
seen = set()
ordered_unique = [e for e in emails if not (e in seen or seen.add(e))]
print(ordered_unique)                     # ['a@x.com', 'b@x.com', 'c@x.com']
```

### Fast membership testing / filtering

```python
# Which words appear in a document? (dedup + membership)
words = "the cat sat on the mat".split()
unique_words = set(words)
print(unique_words)                       # {'cat', 'on', 'mat', 'sat', 'the'}

stopwords = {"the", "on", "a"}
content = {w for w in unique_words if w not in stopwords}
print(content)                            # {'cat', 'mat', 'sat'}
```

### Comparing two groups (users in two systems)

```python
system_a = {"alice", "bob", "carol"}
system_b = {"bob", "dave", "erin"}

print("In both:", system_a & system_b)        # {'bob'}
print("Only in A:", system_a - system_b)      # {'alice', 'carol'}
print("Only in B:", system_b - system_a)      # {'dave', 'erin'}
print("Either (not both):", system_a ^ system_b)  # {'alice', 'carol', 'dave', 'erin'}
```

### Tracking seen items (e.g., in a loop)

```python
def unique_words_in_order(text):
    seen = set()
    result = []
    for word in text.split():
        if word not in seen:
            seen.add(word)
            result.append(word)
    return result

print(unique_words_in_order("the cat sat the cat"))  # ['the', 'cat', 'sat']
```

### Finding tags / shared interests

```python
alice = {"python", "sql", "tableau"}
bob = {"python", "machine-learning", "sql"}

common = alice & bob
print("Shared:", common)                      # {'python', 'sql'}
print("Combined:", alice | bob)               # all unique skills
```

### Using `frozenset` as a dict key (e.g., grouping)

```python
orders = [
    ("a", "b", "a"),
    ("b", "a"),
    ("c", "c"),
]
counts = {}
for order in orders:
    key = frozenset(order)          # dedupe + make hashable
    counts[key] = counts.get(key, 0) + 1
print(counts)   # {frozenset({'a', 'b'}): 2, frozenset({'c'}): 1}
```

---

## 12. Common Pitfalls

| Pitfall                                                         | Fix                                                                           |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `{}` creates a **dict**, not an empty set                       | Use `set()` for an empty set                                                  |
| `{1, 2, [3]}` — adding a `list`/`dict`/`set` raises `TypeError` | Only store **hashable** elements (immutable); use `frozenset` for nested sets |
| Indexing `s[0]` or slicing `s[1:2]` — sets are unordered        | Sets have no order; convert to a list `list(s)` if you need positional access |
| `s.remove(x)` raises `KeyError` if `x` is absent                | Use `s.discard(x)` for a safe no-op removal                                   |
| Assuming iteration order is stable                              | Sets are unordered — use `sorted(s)` for a deterministic order                |
| `s.pop()` returns an **arbitrary** element, not "first"         | Only use `pop()` when any element is fine; do not rely on the order           |
| Using a set as a dict key or set element                        | Use `frozenset` instead (sets are unhashable)                                 |
| `{1, 2, 3}` ordering after operations                           | Don't rely on order — use `sorted()` or a list if order matters               |
| Mutating a set while iterating over it                          | Iterate over a copy: `for x in s.copy():` or build a new set                  |
| Adding a mutable element like a list                            | Convert to a tuple for hashable contents, or use `frozenset` for nested sets  |

---

> **Key Takeaway**: Sets are Python's answer to "unique, unordered, and fast" — perfect for removing duplicates, lightning-fast membership checks, and mathematical set logic. Master the core operations (`add`, `discard`, `remove`, `union`/`|`, `intersection`/`&`, `difference`/`-`, `symmetric_difference`/`^`) and the subset/superset relationships. Remember the cardinal rules: **`{}` is a dict, `set()` is an empty set**, **elements must be hashable**, **order is never guaranteed**, and **`frozenset` is the hashable, immutable counterpart**. When you just need to know "is it in there?" quickly, a set is almost always the right tool.
> </content>
