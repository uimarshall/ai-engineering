"""
Created on Thu Aug  6 12:36:33 2026

@author: uimar


# Version 1

CORRECT_NUMBER = 26
user_guess = int(input("What is your Guess? "))

if user_guess == CORRECT_NUMBER:
    print("Wow, You got it right, Great guess!")
else:
    print("Sorry! your guess is incorrect")

# Version 2

CORRECT_NUMBER = 26

while True:
    user_guess = int(input("What is your Guess? "))

    if user_guess == CORRECT_NUMBER:
        print("Wow, You got it right, Great guess!")
        break
    else:
        print("Sorry! your guess is incorrect")

"""

# Version 3

import random

random.randint(1, 10)

LOWER_BOUND = 1
UPPER_BOUND = 100
GUESS_LIMIT = 5
GUESS_COUNTER = 0
CORRECT_NUMBER = random.randint(LOWER_BOUND, UPPER_BOUND)

print(
    f"Try guessing the number I'm thinking. It is between {LOWER_BOUND} and {UPPER_BOUND}. Good luck, you have {GUESS_LIMIT} guesses!"
)

while True:
    user_guess = int(input("What is your Guess? "))
    GUESS_COUNTER += 1
    remaining_guesses = GUESS_LIMIT - GUESS_COUNTER

    if LOWER_BOUND <= user_guess <= UPPER_BOUND:
        if user_guess == CORRECT_NUMBER:
            print(f"Wow, You got it right in {GUESS_COUNTER} guesses, Great guess!")
            break
        elif user_guess < CORRECT_NUMBER:
            print(
                f"Your guess is too low, try again! Guess remaining: {remaining_guesses}"
            )
        else:
            print(
                f"Your guess is too high, try again! Guess remaining: {remaining_guesses}"
            )

    else:
        print(
            f"Your guess is outside the range, try a guess between {LOWER_BOUND} and {UPPER_BOUND}! Guess remaining: {remaining_guesses}"
        )

    if remaining_guesses == 0:
        print(
            f"Sorry, you're out of guesses. The number you're after is {CORRECT_NUMBER}"
        )
        break
