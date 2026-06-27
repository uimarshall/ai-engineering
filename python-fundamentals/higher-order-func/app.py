# Higher order functions are functions that can take other functions as arguments or return functions as their result. In Python, functions are first-class citizens, which means they can be passed around and used as arguments just like any other object (string, int, float, list, and so on).
# This allows for a functional programming style, where you can create more abstract and reusable code.

# ─────────────────────────────────────────────────────────────
# EXAMPLE 1: Eeny Meeny Miny Moe — HOF that accepts a function
# ─────────────────────────────────────────────────────────────


from unicodedata import name


def eeny(name):
    return f"Eeny   -> {name}"


def meeny(name):
    return f"Meeny  -> {name}"


def miny(name):
    return f"Miny   -> {name}"


def moe(name):
    return f"Moe    -> {name} << YOU'RE IT!"


def pick_chant(chant_func, name):
    """Higher-order function: receives a chant function and applies it."""
    return chant_func(name)


def eeny_meeny_miny_moe(names: list, picker_func):
    """
    Higher-order function: cycles through chant steps using a picker function
    to decide the final chosen name.
    """
    chants = [eeny, meeny, miny, moe]
    print("\n--- Eeny Meeny Miny Moe ---")
    for i, name in enumerate(names):
        step = chants[i % len(chants)]
        print(pick_chant(step, name))
    chosen = picker_func(names)
    print(f"\nFinal pick: {chosen}")
    return chosen


def pick_last(names):
    """Picker strategy: always pick the last name."""
    return names[-1]


def pick_first(names):
    """Picker strategy: always pick the first name."""
    return names[0]


players = ["Alice", "Bob", "Charlie", "Diana"]

eeny_meeny_miny_moe(players, pick_last)
eeny_meeny_miny_moe(players, pick_first)


def run_errand(action_taken, times):
    """A simple function to simulate running an errand."""
    return action_taken(name="James", times=times)
    # return f"Running errand: {action_taken} for {times} times."


def errand(name, times):
    return f"{name} is running an errand {times} times."


errand_result = run_errand(errand, 3)
print("\n--- Running Errand ---")
print(errand_result)


# ─────────────────────────────────────────────────────────────
# EXAMPLE 2: HOF that RETURNS a function (function factory)
# ─────────────────────────────────────────────────────────────


def make_multiplier(factor):
    """
    Higher-order function: returns a new function that multiplies
    any number by the given factor.
    """

    def multiplier(number):
        return number * factor

    return multiplier


double = make_multiplier(2)
triple = make_multiplier(3)
tenfold = make_multiplier(10)

numbers = [1, 2, 3, 4, 5]

print("\n--- Function Factory (make_multiplier) ---")
print("Originals :", numbers)
print("Doubled   :", list(map(double, numbers)))
print("Tripled   :", list(map(triple, numbers)))
print("Tenfold   :", list(map(tenfold, numbers)))

# Using filter (another built-in HOF) with a lambda
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("\nEvens from", numbers, "->", evens)

# Using sorted with a key function (HOF receiving a function)
words = ["banana", "kiwi", "apple", "cherry", "fig"]
by_length = sorted(words, key=len)
by_alpha = sorted(words, key=str.lower)

print("\n--- sorted() as HOF ---")
print("By length :", by_length)
print("By alpha  :", by_alpha)
