## Breaking Down the Decorator

### The Big Picture

A **decorator** wraps a function to add behavior before/after it runs — like a gift wrapper around a present. The present (your function) is still inside, unchanged.

---

### Step-by-Step Walkthrough

```python
def penalty_kick_decorator(func):   # 1. Takes a function as input
    def wrapper(*args, **kwargs):   # 2. Defines a "wrapper" function
        print("Preparing...")       # 3. Runs BEFORE the original function
        result = func(*args, **kwargs)  # 4. Calls the original function
        print("Kick completed!")    # 5. Runs AFTER the original function
        return result               # 6. Returns whatever the original returned

    return wrapper                  # 7. Returns the wrapper (not its result!)
```

When you write `@penalty_kick_decorator` above `penalty_kick`, Python essentially does this behind the scenes:

```python
penalty_kick = penalty_kick_decorator(penalty_kick)
```

So `penalty_kick` is now the `wrapper` function, with the original `penalty_kick` "trapped" inside it.

---

### What are `*args` and `**kwargs`?

The wrapper doesn't know in advance what arguments the original function needs, so it uses these to **accept anything**.

**`*args` — positional arguments** (the `*` collects them into a tuple)

```python
def example(*args):
    print(args)

example(1, 2, 3)        # → (1, 2, 3)
example("hello", True)  # → ('hello', True)
```

**`**kwargs`— keyword arguments** (the`\*\*` collects them into a dict)

```python
def example(**kwargs):
    print(kwargs)

example(name="Alice", age=25)  # → {'name': 'Alice', 'age': 25}
```

**Together**, they mean: _"accept any combination of arguments, no matter what"_

---

### Why Does the Wrapper Need Them?

Your `penalty_kick` takes `player_name`. But the wrapper must be **reusable** for ANY function — some might take 0 args, some 5, some keyword args:

```python
# The wrapper needs to handle ALL of these:
penalty_kick("Alice")              # 1 positional arg → *args = ("Alice",)
some_other_func(5, 10, mode="fast") # *args=(5,10), **kwargs={"mode":"fast"}
no_args_func()                     # *args=(), **kwargs={}
```

When `func(*args, **kwargs)` is called, Python **unpacks** them back into the original function's expected format:

```
*args = ("Alice",)   →   func("Alice")   →   penalty_kick("Alice") ✓
```

---

### The Full Execution Flow

```
penalty_kick("Alice")
    │
    ▼
wrapper("Alice")              ← you're actually calling this now
    │
    ├─ print("Preparing...")
    ├─ result = original_penalty_kick("Alice")
    │       └─ print("Alice is taking the penalty kick!")
    │       └─ returns "Goal scored by Alice!"
    ├─ print("Kick completed!")
    └─ return "Goal scored by Alice!"
```

The key insight: `*args` and `**kwargs` make the wrapper a **universal pass-through** — it catches all arguments and forwards them to the real function untouched.
