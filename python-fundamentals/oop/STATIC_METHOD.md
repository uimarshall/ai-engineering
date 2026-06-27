A static method is called "static" because it belongs **statically to the class itself**, not to any instance. The word comes from the idea that its binding is fixed/resolved at compile/definition time — it doesn't depend on runtime object state.

Key reasons for the name:

- **No dynamic dispatch** — unlike instance methods, it doesn't receive `self` (no reference to an instance), so there's nothing dynamic to resolve at runtime.
- **Fixed to the class** — it's permanently attached to the class namespace, not to objects that come and go.
- **No access to instance or class state** — it can't access `self` or `cls`, making its behavior unchanging ("static") regardless of what instances exist.

```python
class MathUtils:
    @staticmethod
    def add(a, b):   # no self, no cls — pure function attached to the class
        return a + b

MathUtils.add(2, 3)  # called on the class, not an instance
```

The contrast is with **instance methods** (dynamic — behavior depends on `self`) and **class methods** (semi-dynamic — depend on `cls`, which can vary with inheritance).

`cls` is the first parameter of a **class method** — it refers to the **class itself** (not an instance).

```python
class Dog:
    species = "Canis familiaris"

    def __init__(self, name):
        self.name = name

    @classmethod
    def describe_species(cls):
        return f"All dogs are {cls.species}"  # cls is Dog

Dog.describe_species()  # "All dogs are Canis familiaris"
```

- `cls` is a convention (like `self`), you could name it anything, but `cls` is standard.
- It receives the **class** as the first argument automatically when the method is called.
- Through `cls` you can access class-level attributes and even create instances:

```python
@classmethod
def create(cls, name):
    return cls(name)  # same as Dog(name), but works with subclasses too
```

**The key difference:**

|                 | First param | Has access to    |
| --------------- | ----------- | ---------------- |
| Instance method | `self`      | instance + class |
| Class method    | `cls`       | class only       |
| Static method   | none        | neither          |

The main advantage of `cls` over hardcoding the class name is **inheritance** — if a subclass calls the method, `cls` will be that subclass, not the parent.
