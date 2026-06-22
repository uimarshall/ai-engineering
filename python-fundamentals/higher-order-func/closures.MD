In this code, the **enclosing scope** is the local scope of `make_exercise` — because `make_exercise` physically wraps (encloses) the inner function `exercise`.

Python resolves variable names using the **LEGB** rule:

| Scope         | What it means                                 | Example here                           |
| ------------- | --------------------------------------------- | -------------------------------------- |
| **L**ocal     | Inside the current function                   | `frequency` inside `exercise`          |
| **E**nclosing | Inside any outer function that wraps this one | `exercise_name` inside `make_exercise` |
| **G**lobal    | Module-level variables                        | anything at the top of the file        |
| **B**uilt-in  | Python's built-ins                            | `len`, `print`, etc.                   |

So from `exercise`'s point of view:

- `frequency` → **local** (its own parameter)
- `exercise_name` → **enclosing** (lives in `make_exercise`, which wraps `exercise`)

```python
def make_exercise(name):          # ← ENCLOSING function
    exercise_name = name.upper()  # ← lives in the ENCLOSING scope

    def exercise(frequency):      # ← inner function (the closure)
        return f"...{exercise_name}..."  # ← found in enclosing scope via LEGB

    return exercise
```

The key insight: even after `make_exercise` finishes executing, `exercise_name` is **retained** by the returned `exercise` function — that's exactly what makes it a closure.
