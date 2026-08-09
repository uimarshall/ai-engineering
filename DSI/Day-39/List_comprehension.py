my_list = [
    1,
    4,
    9,
    16,
    25,
]
my_new_list = []

for i in my_list:
    if i % 2 == 0:
        my_new_list.append(i)


my_new_list = [i for i in my_list if i % 2 == 0]
print(my_new_list)


def square_root(num):
    return num**0.5


my_squared_list = [square_root(i) for i in my_list]
print(my_squared_list)

two_dimensional_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened_list = [num for row in two_dimensional_list for num in row]
print(flattened_list)

new_list = [i[0] for i in two_dimensional_list]
print(new_list)

another_list = [
    i[0]
    for i in two_dimensional_list
    if i[1] == max(i[1] for i in two_dimensional_list)
]
print(another_list)
