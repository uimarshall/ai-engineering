# Closures

# What is a closure?
# A closure is a function that retains access to variables from its enclosing scope, even after that scope has finished executing. Closures are often used to create functions with private variables or to maintain state between function calls.


def make_exercise(name):
    # This variable is captured by the closure, so it will be remembered even after make_exercise has finished executing.
    exercise_name = name.upper()

    # The inner function 'exercise' has access to the variable exercise_name from the enclosing scope of make_exercise.
    # This is the closure function (inner function). It can use the variable exercise_name even after make_exercise has returned.
    def exercise(frequency):
        return f"Let's do some {exercise_name} exercises! for {frequency} times."

    return exercise


def move_player(x, y):
    def move(dx, dy):
        nonlocal x, y  # Allows the inner function to modify the variables x and y from the enclosing scope
        x += dx
        y += dy
        return x, y

    return move


def main():
    create_exercise = make_exercise("push-ups")
    print(create_exercise(10))  # Output: Let's do some PUSH-UPS exercises
    # Example usage of the closure
    print("\n--- Closure Example ---")
    player_position = move_player(0, 0)  # Initial position (0, 0)
    print(player_position(5, 3))  # Move the player by (5, 3)
    print(player_position(-2, 4))  # Move the player by (-2, 4)


if __name__ == "__main__":
    main()
