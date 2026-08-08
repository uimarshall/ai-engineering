# -*- coding: utf-8 -*-

"""
A prime number is a number that is only divisible by itself and one.
"""

# Version 1

n = 20
number_range = set(range(2, n + 1))
primes_list = []

prime = number_range.pop()
primes_list.append(prime)
multiples = set(range(prime * 2, n + 1, prime))

# difference_update is an inbuilt set function
number_range.difference_update(multiples)

# Version 2

# upper bound
n = 100

# Number range to be checked
number_range = set(range(2, n + 1))

# empty list to append discovered primes to
primes_list = []


# while loop
while number_range:
    prime = number_range.pop()
    primes_list.append(prime)
    multiples = set(range(prime * 2, n + 1, prime))

    # difference_update is an inbuilt set function
    number_range.difference_update(multiples)

# print our list of primes
print(primes_list)

# number of primes that were found

prime_count = len(primes_list)

# Largest prime
largest_prime = max(primes_list)

# summary
print(
    f"There are {prime_count} prime numbers between 2 and {n}, the largest being {largest_prime}"
)

# Version 3


def primes_finder(n):
    # Number range to be checked
    number_range = set(range(2, n + 1))

    # empty list to append discovered primes to
    primes_list = []

    # while loop
    while number_range:
        # prime = number_range.pop()
        prime = min(sorted(number_range))

        number_range.remove(prime)
        primes_list.append(prime)
        multiples = set(range(prime * 2, n + 1, prime))

        # difference_update is an inbuilt set function
        number_range.difference_update(multiples)

    # print our list of primes
    print(primes_list)

    # number of primes that were found

    prime_count = len(primes_list)

    # Largest prime
    largest_prime = max(primes_list)

    # summary
    print(
        f"There are {prime_count} prime numbers between 2 and {n}, the largest being {largest_prime}"
    )
    return primes_list


primes_finder(100)
# print(primes_list)
