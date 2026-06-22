import main_function

# This is namespaced as utils, so we can access its functions using utils.function_name()
import utils

#  import a single function - This imports the subtract function directly into the current namespace, so we can use subtract() without the utils. prefix
from utils import square, subtract

print("Running app2.py")
main_function.say_hello()
result = utils.add(5, 3)
print(f"The result of adding 5 and 3 is: {result}")

subtract_result = subtract(
    10, 4
)  # We can use subtract directly because we imported it from utils
print(f"The result of subtracting 4 from 10 is: {subtract_result}")


"""

In this context, namespacing means:

`import utils` creates a namespace called `utils` that contains everything defined in utils.py.

So in your file app2.py, when you write:

- `utils.add(5, 3)`
- `utils.subtract(...)`
- `utils.square(...)`

you’re saying “use `add` from the `utils` namespace/module.”

Why this is useful:
- Avoids name conflicts (you might have another `add` somewhere else).
- Makes code clearer (`utils.add` tells you where it came from).

In your project, `add` is defined in utils.py, and accessed through the module namespace in app2.py.

Good practice to avoid namespace pollution:

- Prefer import utils and call utils.add()
- Import specific names explicitly when needed: from utils import add
- Keep variables as local as possible and avoid unnecessary globals
In short:

Namespace = organization and separation of names.
Namespace pollution = overcrowding that separation until names clash or become unclear.
"""
