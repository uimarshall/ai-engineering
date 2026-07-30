## LIST ALL PYTHON DATATYPES AND VARIABLES.

> Python Data Types and their Uses.

---

## 1. **Numeric Types**

### `int` (Integer)

- **Description**: Represents whole numbers (positive, negative, or zero) without a decimal point.
- **Uses**: Counting, indexing, mathematical operations, loop counters.
- **Examples**: `42`, `-7`, `0`, `1000000`
- **Python 3 Note**: Integers have unlimited precision (can be arbitrarily large).

```python
age = 25
population = 8_000_000_000  # Underscores improve readability
```

### `float` (Floating-Point Number)

- **Description**: Represents real numbers with a decimal point or in scientific notation.
- **Uses**: Scientific calculations, measurements, percentages, any value requiring precision.
- **Examples**: `3.14`, `-0.001`, `1.5e10` (1.5 × 10¹⁰)
- **Note**: Subject to floating-point arithmetic limitations (e.g., `0.1 + 0.2` is not exactly `0.3`).

```python
pi = 3.14159
speed_of_light = 3.0e8
```

### `complex` (Complex Number)

- **Description**: Represents numbers in the form `a + bj`, where `a` is the real part and `b` is the imaginary part.
- **Uses**: Engineering, physics, signal processing, quantum computing.
- **Examples**: `3 + 4j`, `-2j`, `complex(1, 2)`

```python
z = 3 + 4j
print(z.real)  # 3.0
print(z.imag)  # 4.0
```

---

## 2. **Text Type**

### `str` (String)

- **Description**: Represents a sequence of Unicode characters (text). Strings are **immutable**.
- **Uses**: Storing and manipulating text, user input/output, file contents, data serialization.
- **Creation**: Single quotes `'...'`, double quotes `"..."`, triple quotes `'''...'''` or `"""..."""`.
- **Features**: Slicing, concatenation, formatting (f-strings, `.format()`, `%`), methods (`.upper()`, `.split()`, `.join()`, etc.).

```python
name = "Alice"
greeting = f"Hello, {name}!"
multiline = """This is a
multi-line string."""
```

---

## 3. **Sequence Types**

### `list` (List)

- **Description**: An ordered, **mutable** collection of items (can contain mixed types).
- **Uses**: Storing collections of items that need frequent modification, implementing stacks/queues, iteration.
- **Features**: Indexing, slicing, appending, extending, inserting, removing, sorting.
- **Complexity**: O(1) append/pop at end, O(n) insert/delete at beginning.

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
fruits[0] = "apricot"  # Mutable
```

### `tuple` (Tuple)

- **Description**: An ordered, **immutable** collection of items (can contain mixed types).
- **Uses**: Fixed collections (e.g., coordinates, RGB values), function return values, dictionary keys, data integrity.
- **Features**: Indexing, slicing, unpacking, hashable (can be used as dict keys).
- **Note**: Often used for heterogeneous data where position implies meaning.

```python
coordinates = (40.7128, -74.0060)  # (latitude, longitude)
rgb_red = (255, 0, 0)
```

### `range` (Range)

- **Description**: Represents an immutable sequence of numbers, commonly used in loops.
- **Uses**: Iterating a specific number of times, generating arithmetic progressions.
- **Parameters**: `range(stop)`, `range(start, stop)`, `range(start, stop, step)`
- **Memory Efficiency**: Does not store all values; generates them on demand (lazy evaluation).

```python
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

evens = range(0, 10, 2)   # 0, 2, 4, 6, 8
```

---

## 4. **Mapping Type**

### `dict` (Dictionary)

- **Description**: An unordered (ordered in Python 3.7+) collection of **key-value pairs**. Keys must be immutable and hashable.
- **Uses**: Storing structured data, lookup tables, caching/memoization, configuration settings, JSON-like data.
- **Features**: Fast O(1) average lookup, insertion, deletion; dictionary comprehensions; methods (`.keys()`, `.values()`, `.items()`, `.get()`, `.update()`).

```python
person = {
    "name": "Bob",
    "age": 30,
    "city": "New York"
}
print(person["name"])  # Bob
person["age"] = 31     # Update value
```

---

## 5. **Set Types**

### `set` (Set)

- **Description**: An unordered, **mutable** collection of **unique, hashable** items.
- **Uses**: Removing duplicates, mathematical set operations (union, intersection, difference), membership testing.
- **Features**: O(1) average membership testing; set comprehensions; methods: `.add()`, `.remove()`, `.union()`, `.intersection()`, `.difference()`, `.symmetric_difference()`.
- **Note**: No indexing (unordered).

```python
unique_ids = {101, 102, 103, 101}  # {101, 102, 103} — duplicates removed
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)  # {2, 3}  intersection
print(a | b)  # {1, 2, 3, 4}  union
```

### `frozenset` (Frozen Set)

- **Description**: An **immutable** version of a set. Hashable, so it can be used as a dictionary key or set element.
- **Uses**: When you need a set that should not change, or as a key in a dictionary.
- **Features**: Same set operations as `set`, but no methods that modify the set.

```python
immutable_set = frozenset([1, 2, 3, 2])  # frozenset({1, 2, 3})
```

---

## 6. **Boolean Type**

### `bool` (Boolean)

- **Description**: Represents truth values — either `True` or `False`.
- **Uses**: Conditional statements, loop control, flags, function return values for checks.
- **Note**: `bool` is a subclass of `int`; `True` behaves like `1`, `False` behaves like `0`.
- **Truthy/Falsy**: Empty sequences, `0`, `None`, empty collections evaluate to `False`; non-empty values evaluate to `True`.

```python
is_active = True
if is_active:
    print("Active!")

# Truthy examples
bool("hello")  # True
bool([])       # False
bool(42)       # True
bool(0)        # False
```

---

## 7. **Binary Types**

### `bytes` (Bytes)

- **Description**: An **immutable** sequence of bytes (integers in range 0–255).
- **Uses**: Binary data handling, network communication, file I/O (especially binary files), encoding/decoding.
- **Creation**: `b"hello"`, `bytes([104, 101, 108])`, `"hello".encode()`

```python
data = b"hello"
print(data[0])  # 104 (ASCII value of 'h')
```

### `bytearray` (Byte Array)

- **Description**: A **mutable** sequence of bytes (integers in range 0–255).
- **Uses**: Same as `bytes` but when you need to modify the binary data in-place.
- **Features**: Indexing, slicing, append, extend, insert, remove.

```python
buffer = bytearray(b"hello")
buffer[0] = 72  # ASCII 'H'
print(buffer)   # bytearray(b"Hello")
```

### `memoryview` (Memory View)

- **Description**: Provides a view into the memory of another binary object (`bytes`, `bytearray`, or other objects supporting the buffer protocol).
- **Uses**: Efficiently accessing and slicing large binary data without copying.
- **Performance**: Avoids memory copies when slicing large buffers.

```python
data = bytearray(b"Hello World")
view = memoryview(data)
print(view[0])    # 72 ('H')
print(view[0:5])  # <memory at ...> — no copy
```

---

## 8. **None Type**

### `NoneType` (`None`)

- **Description**: Represents the **absence of a value** or **null value**. There is only one instance: `None`.
- **Uses**: Default return value for functions, placeholder for optional values, indicating missing or undefined data.
- **Note**: `None` evaluates to `False` in boolean contexts. Always compare with `is` (not `==`) for identity: `x is None`.

```python
result = None  # No value yet
value = some_function()  # Might return None
if value is None:
    print("No value returned")
```

---

## Summary Table

| Type         | Category | Mutable? | Ordered?   | Hashable? | Common Use Case        |
| ------------ | -------- | -------- | ---------- | --------- | ---------------------- |
| `int`        | Numeric  | —        | —          | Yes       | Whole numbers          |
| `float`      | Numeric  | —        | —          | Yes       | Decimal numbers        |
| `complex`    | Numeric  | —        | —          | Yes       | Complex math           |
| `str`        | Text     | No       | Yes        | No        | Text data              |
| `list`       | Sequence | Yes      | Yes        | No        | Dynamic collections    |
| `tuple`      | Sequence | No       | Yes        | Yes       | Fixed collections      |
| `range`      | Sequence | No       | Yes        | No        | Numeric sequences      |
| `dict`       | Mapping  | Yes      | Yes (3.7+) | No        | Key-value pairs        |
| `set`        | Set      | Yes      | No         | No        | Unique items           |
| `frozenset`  | Set      | No       | No         | Yes       | Immutable unique items |
| `bool`       | Boolean  | —        | —          | Yes       | True/False values      |
| `bytes`      | Binary   | No       | Yes        | No        | Binary data            |
| `bytearray`  | Binary   | Yes      | Yes        | No        | Mutable binary data    |
| `memoryview` | Binary   | Views    | Yes        | No        | Zero-copy buffer views |
| `NoneType`   | Special  | —        | —          | —         | Null/absent value      |

---

## Quick Reference: Type Checking

```python
# Check type
type(42)          # <class 'int'>
isinstance(42, int)  # True

# Common type checks
isinstance(x, (int, float))   # Numeric
isinstance(x, str)             # String
isinstance(x, (list, tuple))   # Sequence
isinstance(x, dict)            # Dictionary
isinstance(x, (set, frozenset))  # Set
isinstance(x, bytes)           # Bytes
```

---

## Practice Examples

```python
# Integer
count = 100

# Float
price = 19.99

# Complex
impedance = 50 + 25j

# String
name = "Python"

# List
colors = ["red", "green", "blue"]

# Tuple
dimensions = (1920, 1080)

# Range
numbers = range(1, 11)

# Dictionary
config = {"host": "localhost", "port": 8080}

# Set
tags = {"python", "data", "science"}

# Frozenset
immutable_tags = frozenset(["a", "b", "c"])

# Boolean
is_valid = True

# Bytes
binary = b"\x00\xFF\xA0"

# Bytearray
buffer = bytearray(binary)

# None
result = None
```

---

> **Key Takeaway**: Choosing the right data type is crucial for writing efficient, readable, and bug-free Python code. Each type has specific strengths and use cases — use them appropriately!
