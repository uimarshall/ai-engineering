# print("hello world")

# name = "John"
# age = 30
# print("Hello, " + name + str(age) + "!")

# marks = (85, 90, 78, 92)

# total_marks = sum(marks)
# average_marks = total_marks / len(marks)
# print("Total Marks:", total_marks)
# print("Average Marks:", average_marks)

# # Ternary operator
# status = "adult" if age >= 18 else "minor"
# print(status)

# a, b = 10, 20
# max_val = a if a > b else b
# print("Max:", max_val)

# is_valid = True
# print("yes" if is_valid else "no")

# Nested ternary with user input
score = int(input("Enter your score (0-100): "))
grade = (
    "A"
    if score >= 90
    else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
)
print(f"Grade: {grade}")

temperature = float(input("Enter temperature in Celsius: "))
weather = (
    "hot"
    if temperature > 30
    else "warm" if temperature > 20 else "cool" if temperature > 10 else "cold"
)
print(f"Weather is: {weather}")

num = int(input("Enter a number: "))
category = "positive" if num > 0 else "negative" if num < 0 else "zero"
parity = "even" if num % 2 == 0 else "odd"
print(f"{num} is {category} and {parity}")
