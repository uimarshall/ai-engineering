# STRINGS

Outline all properties and methods of a String and used cases.

> Python `str` — Properties, Methods, and Use Cases.

---

## 1. What is a `str`?

- **Description**: A `str` (string) is an **immutable sequence of Unicode characters** used to represent and store text.
- **Uses**: Storing names, messages, file contents, URLs, JSON, user input/output, text processing, and every kind of human-readable data.
- **Immutability**: Once created, a string **cannot be changed in place**. Any operation that appears to modify a string actually returns a **new** string.

```python
name = "Alice"
name = name.upper()   # Returns a NEW string "ALICE"; original "Alice" is untouched
```

```python
# Immutability demo — this raises a TypeError
s = "hello"
s[0] = "H"   # TypeError: 'str' object does not support item assignment
```

---

## 2. String Properties

| Property           | Description                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **Immutable**      | Cannot be modified in place; every "change" creates a new string                            |
| **Ordered**        | Characters have a defined left-to-right order and can be accessed by index                  |
| **Indexable**      | `s[0]` returns the first character; negative indices count from the end (`s[-1]`)           |
| **Sliceable**      | `s[start:stop:step]` extracts substrings                                                    |
| **Iterable**       | Can be looped over with `for char in s:` — yields one character at a time                   |
| **Hashable**       | Can be used as a dictionary key or set element (`hash(s)`)                                  |
| **Length**         | `len(s)` returns the number of characters                                                   |
| **Membership**     | Supports `in` / `not in` for substring checks                                               |
| **Unicode-aware**  | Handles any Unicode character (emoji, accented letters, CJK, etc.)                          |
| **Concatenatable** | Can be joined with `+` and repeated with `*`                                                |
| **Comparable**     | Supports ordering comparisons (`<`, `>`, `<=`, `>=`) using lexicographic (dictionary) order |

```python
s = "Hello"
print(s[0])          # H
print(s[-1])         # o
print(s[1:4])        # ell
print(s[::-1])       # olleH  (reverse)
print(len(s))        # 5
print("ell" in s)    # True
print("xyz" not in s)  # True
```

---

## 3. String Creation

| Method                       | Syntax/Example                       | Use Case                                    |
| ---------------------------- | ------------------------------------ | ------------------------------------------- |
| Single quotes                | `'hello'`                            | Short strings; avoid escaping double quotes |
| Double quotes                | `"hello"`                            | Strings that contain apostrophes (`"it's"`) |
| Triple quotes (multiline)    | `'''...'''` or `"""..."""`           | Multi-line text, docstrings, block comments |
| `str()` constructor          | `str(42)`, `str(3.14)`, `str([1,2])` | Converting numbers/objects to text          |
| f-string (formatted literal) | `f"value: {x:.2f}"`                  | **Modern** runtime text interpolation       |
| Raw string                   | `r"C:\Users\name"`                   | Paths & regex — backslashes are literal     |
| Bytes decode                 | `b"hello".decode("utf-8")`           | Converting bytes (e.g., from files/network) |

```python
name = "Alice"                              # double quotes
sentence = 'It is a "great" day'            # single quotes
multiline = """Line one
Line two
Line three"""
number_as_text = str(1000)                  # '1000'
formatted = f"Total: {10 + 5} items"        # 'Total: 15 items'
path = r"C:\Users\alice\Documents"          # raw string — no escape issues
```

---

## 4. String Operators

| Operator         | Example                | Result       | Use Case                                  |
| ---------------- | ---------------------- | ------------ | ----------------------------------------- |
| `+` (concat)     | `"a" + "b"`            | `'ab'`       | Joining text pieces                       |
| `*` (repeat)     | `"ab" * 3`             | `'ababab'`   | Generating separators/patterns            |
| `in`             | `"ell" in "hello"`     | `True`       | Substring membership test                 |
| `not in`         | `"x" not in "hello"`   | `True`       | Negated membership test                   |
| `==` / `!=`      | `"a" == "A"`           | `False`      | Case-sensitive equality check             |
| `<`, `>`, ...    | `"apple" < "banana"`   | `True`       | Lexicographic ordering / sorting          |
| `%`              | `"Hi %s" % "Bob"`      | `'Hi Bob'`   | Old-style `%` formatting (legacy)         |
| `f"..."`         | `f"Hi {name.upper()}"` | `'Hi ALICE'` | Modern inline formatting with expressions |
| `+` (aug-assign) | `s += "!"`             | (new string) | Accumulating text in a loop               |

```python
print("Hello" + " " + "World")     # Hello World
print("-" * 20)                    # --------------------
print("ell" in "hello")            # True
print("apple" < "banana")          # True  (a comes before b)
print(f"3 + 4 = {3 + 4}")          # 3 + 4 = 7
print("name: %s, age: %d" % ("Ann", 30))  # name: Ann, age: 30
```

---

## 5. String Methods

All methods are called on a string object: `s.method(...)`. Since strings are immutable, each method **returns a new string** (or another type where noted).

### 5.1 Case Conversion

| Method           | Description                            | Example                      | Result          | Use Case                                            |
| ---------------- | -------------------------------------- | ---------------------------- | --------------- | --------------------------------------------------- |
| `s.capitalize()` | First char uppercase, rest lowercase   | `"hello WORLD".capitalize()` | `'Hello world'` | Normalizing sentence case                           |
| `s.casefold()`   | Aggressive lowercase (handles Unicode) | `"Straße".casefold()`        | `'strasse'`     | Case-insensitive comparison (better than `lower()`) |
| `s.lower()`      | All characters lowercase               | `"HELLO".lower()`            | `'hello'`       | Standardizing input, search                         |
| `s.upper()`      | All characters uppercase               | `"hello".upper()`            | `'HELLO'`       | Display emphasis, normalization                     |
| `s.title()`      | First letter of each word uppercase    | `"hello world".title()`      | `'Hello World'` | Formatting headings/names                           |
| `s.swapcase()`   | Swap uppercase ↔ lowercase             | `"Hello".swapcase()`         | `'hELLO'`       | Toggling case (rarely used)                         |

```python
text = "hello WORLD"
print(text.capitalize())    # Hello world
print(text.lower())         # hello world
print(text.upper())         # HELLO WORLD
print(text.title())         # Hello World
print("Straße".casefold() == "strasse".casefold())  # True — Unicode-safe compare
```

### 5.2 Searching & Substring

| Method                 | Description                                           | Example                                  | Result | Use Case                            |
| ---------------------- | ----------------------------------------------------- | ---------------------------------------- | ------ | ----------------------------------- |
| `s.find(sub)`          | Lowest index where `sub` occurs; `-1` if not found    | `"hello".find("l")`                      | `2`    | Safe substring position lookup      |
| `s.rfind(sub)`         | Highest index where `sub` occurs; `-1` if not found   | `"hello".rfind("l")`                     | `3`    | Finding last occurrence             |
| `s.index(sub)`         | Like `find()` but **raises ValueError** if not found  | `"hello".index("l")`                     | `2`    | When absence is an error            |
| `s.rindex(sub)`        | Like `rfind()` but **raises ValueError** if not found | `"hello".rindex("l")`                    | `3`    | Last occurrence with error handling |
| `s.count(sub)`         | Count non-overlapping occurrences of `sub`            | `"ababa".count("aba")`                   | `1`    | Counting words/characters           |
| `s.startswith(prefix)` | `True` if starts with prefix (accepts tuple)          | `"report.pdf".startswith("report")`      | `True` | File-type / route matching          |
| `s.endswith(suffix)`   | `True` if ends with suffix (accepts tuple)            | `"photo.png".endswith((".png", ".jpg"))` | `True` | Extension checks                    |

```python
email = "alice@example.com"
print(email.find("@"))          # 5
print(email.index("@"))         # 5
print(email.count("e"))         # 2
print(email.startswith("alice"))  # True
print(email.endswith(".com"))   # True
print(email[email.index("@")+1:])  # example.com  (extract domain)
```

### 5.3 Validation / Character Classification

| Method             | Description                                        | Example                     | Result | Use Case                             |
| ------------------ | -------------------------------------------------- | --------------------------- | ------ | ------------------------------------ |
| `s.isalnum()`      | `True` if all chars alphanumeric (a–z, 0–9)        | `"abc123".isalnum()`        | `True` | Username/password validation         |
| `s.isalpha()`      | `True` if all chars alphabetic                     | `"hello".isalpha()`         | `True` | Name field validation                |
| `s.isascii()`      | `True` if all chars are ASCII                      | `"hello".isascii()`         | `True` | Encoding-compatibility checks        |
| `s.isdecimal()`    | `True` if all chars are decimal digits             | `"123".isdecimal()`         | `True` | Strict numeric string check          |
| `s.isdigit()`      | `True` if all chars are digits (incl. superscript) | `"12³".isdigit()`           | `True` | Numeric detection (broader)          |
| `s.isidentifier()` | `True` if valid Python identifier                  | `"var_name".isidentifier()` | `True` | Validating variable names / keywords |
| `s.islower()`      | `True` if ≥1 cased char and all are lowercase      | `"hello".islower()`         | `True` | Checking case conventions            |
| `s.isnumeric()`    | `True` if all chars are numeric (incl. ½, 万)      | `"½".isnumeric()`           | `True` | Detecting any numeric representation |
| `s.isprintable()`  | `True` if all chars are printable                  | `"hi".isprintable()`        | `True` | Sanitizing output                    |
| `s.isspace()`      | `True` if all chars are whitespace                 | `"  \t".isspace()`          | `True` | Detecting blank lines / padding      |
| `s.istitle()`      | `True` if title-cased (each word capitalized)      | `"Hello World".istitle()`   | `True` | Validating headings                  |
| `s.isupper()`      | `True` if ≥1 cased char and all are uppercase      | `"HELLO".isupper()`         | `True` | Checking shouting / all-caps flags   |

```python
def is_valid_username(u):
    return u.isalnum() and not u.isdigit()

print(is_valid_username("alice_1"))    # False (underscore not alphanumeric)
print(is_valid_username("alice1"))     # True
print("  ".isspace())                  # True
print("Hello World".istitle())         # True
print("123".isnumeric())               # True
```

### 5.4 Splitting & Joining

| Method                    | Description                                                 | Example                     | Result              | Use Case                         |
| ------------------------- | ----------------------------------------------------------- | --------------------------- | ------------------- | -------------------------------- |
| `s.split(sep=None)`       | Split into list on `sep` (default: any whitespace)          | `"a,b,c".split(",")`        | `['a', 'b', 'c']`   | Parsing CSV/TSV, tokens          |
| `s.rsplit(sep, maxsplit)` | Split from the **right**                                    | `"a,b,c".rsplit(",", 1)`    | `['a,b', 'c']`      | Separating extension/domain      |
| `s.splitlines()`          | Split on line boundaries, keeping/removing breaks as needed | `"a\nb".splitlines()`       | `['a', 'b']`        | Reading multi-line text          |
| `sep.join(iterable)`      | Join an iterable of strings using `sep`                     | `"-".join(["a", "b", "c"])` | `'a-b-c'`           | Building CSV lines, paths, lists |
| `s.partition(sep)`        | Split into `(head, sep, tail)` at first occurrence          | `"a-b".partition("-")`      | `('a', '-', 'b')`   | Parsing key=value pairs          |
| `s.rpartition(sep)`       | Split at **last** occurrence into `(head, sep, tail)`       | `"a-b-c".rpartition("-")`   | `('a-b', '-', 'c')` | Splitting filename extension     |

```python
csv_line = "Alice,30,Engineer"
print(csv_line.split(","))              # ['Alice', '30', 'Engineer']

filename = "report_final.pdf"
name, sep, ext = filename.rpartition(".")
print(name, ext)                        # report_final pdf

print(", ".join(["red", "green", "blue"]))   # red, green, blue

text = "one\ntwo\nthree"
print(text.splitlines())                # ['one', 'two', 'three']
```

### 5.5 Trimming, Padding & Alignment

| Method                  | Description                                     | Example                | Result     | Use Case                      |
| ----------------------- | ----------------------------------------------- | ---------------------- | ---------- | ----------------------------- |
| `s.strip(chars=None)`   | Remove leading/trailing whitespace (or `chars`) | `"  hi  ".strip()`     | `'hi'`     | Cleaning user input           |
| `s.lstrip(chars)`       | Remove leading whitespace/chars                 | `"###hi".lstrip("#")`  | `'hi'`     | Stripping prefixes            |
| `s.rstrip(chars)`       | Remove trailing whitespace/chars                | `"hi   ".rstrip()`     | `'hi'`     | Cleaning file lines           |
| `s.center(width)`       | Center string in `width` padded with fillchar   | `"hi".center(6, "*")`  | `'**hi**'` | Table header formatting       |
| `s.ljust(width)`        | Left-justify in `width`                         | `"hi".ljust(4, "_")`   | `'hi__'`   | Fixed-width column alignment  |
| `s.rjust(width)`        | Right-justify in `width`                        | `"hi".rjust(4, "_")`   | `'__hi'`   | Right-aligning numbers        |
| `s.zfill(width)`        | Pad with zeros on the left                      | `"42".zfill(5)`        | `'00042'`  | Invoice IDs, order numbers    |
| `s.expandtabs(tabsize)` | Replace tabs with spaces                        | `"a\tb".expandtabs(4)` | `'a   b'`  | Normalizing tab-indented text |

```python
raw = "  Hello, World!  \n"
print(raw.strip())            # Hello, World!

print("Total".center(20, "="))   # ======Total=======
print("42".zfill(4))             # 0042

# Common: cleaning CSV/input data
values = [v.strip() for v in " Alice , Bob , Carol ".split(",")]
print(values)   # ['Alice', 'Bob', 'Carol']
```

### 5.6 Replacing, Removing & Translating

| Method                   | Description                                              | Example                                 | Result    | Use Case                        |
| ------------------------ | -------------------------------------------------------- | --------------------------------------- | --------- | ------------------------------- |
| `s.replace(old, new, n)` | Replace occurrences of `old` with `new` (optional count) | `"a-b-c".replace("-", "+")`             | `'a+b+c'` | Find-and-replace text           |
| `s.removeprefix(prefix)` | Remove `prefix` if present (else return copy)            | `"Report_2024".removeprefix("Report_")` | `'2024'`  | Stripping known prefixes (3.9+) |
| `s.removesuffix(suffix)` | Remove `suffix` if present (else return copy)            | `"file.txt".removesuffix(".txt")`       | `'file'`  | Stripping known suffixes (3.9+) |
| `str.maketrans(x, y, z)` | Build translation table (mapping/delete)                 | `str.maketrans("aeiou", "AEIOU")`       | table     | Mapping characters              |
| `s.translate(table)`     | Apply translation table to the string                    | `"hello".translate(t)`                  | `'hEllO'` | Efficient char-by-char mapping  |

```python
text = "The quick brown fox"
print(text.replace(" ", "_"))        # The_quick_brown_fox
print(text.replace("fox", "dog"))    # The quick brown dog

# Remove a known prefix safely
url = "https://example.com"
print(url.removeprefix("https://"))  # example.com

# Remove all vowels using translate
trans = str.maketrans("", "", "aeiou")
print("hello world".translate(trans))  # hll wrld
```

### 5.7 Formatting

| Method                  | Description                                     | Example                                  | Result       | Use Case                  |
| ----------------------- | ----------------------------------------------- | ---------------------------------------- | ------------ | ------------------------- |
| `s.format(*args, **kw)` | Substitute `{}` placeholders (positional/named) | `"{} is {}".format("Al", 30)`            | `'Al is 30'` | Dynamic text templates    |
| `s.format_map(mapping)` | Substitute using a mapping (e.g., dict)         | `"Hi {name}".format_map({"name": "Bo"})` | `'Hi Bo'`    | Formatting with dict data |

```python
print("Hello, {}! You have {} new messages.".format("Alice", 5))
# Hello, Alice! You have 5 new messages.

data = {"name": "Bob", "score": 92.456}
print("{name} scored {score:.1f}".format_map(data))
# Bob scored 92.5

# f-strings are the modern, preferred alternative:
print(f"{data['name']} scored {data['score']:.1f}")
```

### 5.8 Encoding

| Method          | Description                                | Example                  | Result           | Use Case                        |
| --------------- | ------------------------------------------ | ------------------------ | ---------------- | ------------------------------- |
| `s.encode(enc)` | Encode string to `bytes` using an encoding | `"café".encode("utf-8")` | `b'caf\xc3\xa9'` | Sending text over network/files |

```python
text = "café"
b = text.encode("utf-8")        # b'caf\xc3\xa9'
decoded = b.decode("utf-8")     # 'café'
print(decoded == text)          # True

# Handle unsupported characters gracefully
try:
    text.encode("ascii")        # raises UnicodeEncodeError
except UnicodeEncodeError:
    print("Not ASCII-safe!")    # Not ASCII-safe!
```

---

## 6. Related Built-in Functions

| Function            | Description                           | Example                    | Result  | Use Case                      |
| ------------------- | ------------------------------------- | -------------------------- | ------- | ----------------------------- |
| `len(s)`            | Number of characters                  | `len("hello")`             | `5`     | Limits, validation, counts    |
| `max(s)` / `min(s)` | Highest / lowest character            | `max("hello")`             | `'o'`   | Character extremes            |
| `sorted(s)`         | Returns sorted **list** of characters | `"".join(sorted("bca"))`   | `'abc'` | Sorting characters/letters    |
| `reversed(s)`       | Iterate characters in reverse         | `"".join(reversed("abc"))` | `'cba'` | Reversing text                |
| `ord(ch)`           | Unicode code point of a character     | `ord("A")`                 | `65`    | Character → number conversion |
| `chr(code)`         | Character from a Unicode code point   | `chr(65)`                  | `'A'`   | Number → character conversion |

```python
print(len("hello"))              # 5
print("".join(reversed("abc")))  # cba  (also: "abc"[::-1])
print("".join(sorted("python"))) # hnopty
print(ord("A"), chr(66))         # 65 B
```

---

## 7. Full Summary Reference Table

| Category                 | Methods                                                                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Case conversion**      | `capitalize()`, `casefold()`, `lower()`, `upper()`, `title()`, `swapcase()`                                                                                             |
| **Searching**            | `find()`, `rfind()`, `index()`, `rindex()`, `count()`, `startswith()`, `endswith()`                                                                                     |
| **Validation**           | `isalnum()`, `isalpha()`, `isascii()`, `isdecimal()`, `isdigit()`, `isidentifier()`, `islower()`, `isnumeric()`, `isprintable()`, `isspace()`, `istitle()`, `isupper()` |
| **Split & Join**         | `split()`, `rsplit()`, `splitlines()`, `join()`, `partition()`, `rpartition()`                                                                                          |
| **Trim & Pad**           | `strip()`, `lstrip()`, `rstrip()`, `center()`, `ljust()`, `rjust()`, `zfill()`, `expandtabs()`                                                                          |
| **Replace & Translate**  | `replace()`, `removeprefix()`, `removesuffix()`, `maketrans()`, `translate()`                                                                                           |
| **Formatting**           | `format()`, `format_map()`                                                                                                                                              |
| **Encoding**             | `encode()`                                                                                                                                                              |
| **Properties/Operators** | immutable, ordered, indexable, sliceable, iterable, hashable; `+`, `*`, `in`, comparisons, f-strings                                                                    |
| **Built-ins**            | `len()`, `max()`, `min()`, `sorted()`, `reversed()`, `ord()`, `chr()`                                                                                                   |

---

## 8. Real-World Use Cases (Combined Example)

### Text cleaning pipeline (data science / NLP)

```python
def clean_text(raw: str) -> str:
    """Normalize messy text for downstream analysis."""
    return " ".join(
        word.lower().strip(".,!?;:")
        for word in raw.split()
        if word.strip(".,!?;:")      # drop empty tokens
    )

messy = "  Hello,   WORLD!!   This IS a   TEST.  "
print(clean_text(messy))
# 'hello world this is a test'
```

### Parsing key=value configuration

```python
config_line = "host=localhost;port=5432;db=analytics"
settings = {}
for pair in config_line.split(";"):
    key, _, value = pair.partition("=")
    settings[key] = value
print(settings)
# {'host': 'localhost', 'port': '5432', 'db': 'analytics'}
```

### Data validation

```python
def validate(phone: str) -> bool:
    return phone.startswith("+") and phone[1:].isdigit() and len(phone) == 13

print(validate("+254712345678"))   # True
print(validate("0712345678"))      # False — missing country code
```

### Building a CSV output row

```python
headers = ["name", "age", "city"]
row = ["Alice", 30, "Nairobi"]
print(",".join(headers))
print(",".join(str(item) for item in row))
# name,age,city
# Alice,30,Nairobi
```

---

## 9. Quick Reference: Common Pitfalls

| Pitfall                                           | Fix                                                                         |
| ------------------------------------------------- | --------------------------------------------------------------------------- |
| Trying to modify a string in place (`s[0] = "x"`) | Reassign: `s = "x" + s[1:]`                                                 |
| Using `index()` when substring may be absent      | Use `find()` (returns `-1`) or catch `ValueError`                           |
| Comparing `"Apple" == "apple"` expecting `True`   | Normalize both sides first: `.lower()` or `.casefold()`                     |
| `"".join(...)` vs `str(list)` confusion           | `join()` concatenates elements; `str(list)` gives `"['a', 'b']"`            |
| Forgetting `str()` when concatenating numbers     | `"Age: " + str(30)` (or use f-string) — cannot mix `str` and `int` with `+` |
| Relying on `replace()` for prefix removal         | Use `removeprefix()`/`removesuffix()` (cleaner, Python 3.9+)                |
| Slicing confusion `s[:n]` vs `s[n:]`              | `s[:n]` = first n chars; `s[n:]` = from index n to end                      |

---

> **Key Takeaway**: Strings are the most frequently used data type in Python — powering everything from user input handling to NLP pipelines. Understanding their properties (immutability, indexing, slicing) and mastering the method families (case conversion, searching, validation, splitting/joining, trimming/padding, formatting) lets you write concise, readable, and robust text-processing code. When in doubt, prefer **f-strings** for formatting and `.casefold()` for case-insensitive comparisons.
