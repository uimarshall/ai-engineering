# How a dictionary works in Python:
# A dictionary is a collection of key-value pairs. Each key is unique and maps to a value. Dictionaries are mutable, meaning you can change their contents after they are created.
# Internally, Python uses a hash table to implement dictionaries. When you add a key-value pair to a dictionary, Python computes a hash of the key to determine where to store the value in memory. This allows for fast lookups, as Python can quickly compute the hash and access the corresponding value.

# Creating a dictionary
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
print(my_dict)  # Output: {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Accessing values
print(my_dict["name"])  # Output: Alice
print(my_dict.get("age"))  # Output: 30
print(my_dict.get("country", "Unknown"))  # Output: Unknown (default value)
# Modifying values
my_dict["age"] = 31
print(my_dict)  # Output: {'name': 'Alice', 'age': 31, 'city': 'New York'}
# Adding new key-value pairs
my_dict["country"] = "USA"
print(
    my_dict
)  # Output: {'name': 'Alice', 'age': 31, 'city': 'New York', 'country': 'USA'}
# Removing key-value pairs
del my_dict["city"]
print(my_dict)  # Output: {'name': 'Alice', 'age': 31, 'country': 'USA'}
# Iterating over a dictionary
for key, value in my_dict.items():
    print(f"{key}: {value}")
# Output:
# name: Alice
# age: 31
# country: USA

# How does a dictionary literal work in Python?

# A dictionary literal in Python is a way to create a dictionary using a specific syntax. It consists of curly braces {} containing key-value pairs, where each key is separated from its corresponding value by a colon (:), and pairs are separated by commas (,). For example:
my_dict = {"name": "Alice", "age": 30, "city": "New York"}

# In this example, we create a dictionary with three key-value pairs: "name" maps to "Alice", "age" maps to 30, and "city" maps to "New York". The keys are strings, and the values can be of any data type (in this case, a string and an integer). The dictionary literal allows us to quickly and easily create a dictionary without needing to use the dict() constructor or add key-value pairs one at a time.

# When Python encounters a dictionary literal, it processes the key-value pairs and constructs a dictionary object in memory. The keys are hashed to determine their position in the underlying hash table, which allows for efficient retrieval of values based on their keys. The resulting dictionary can then be used to store and access data as needed.

################################################################

# How does a dictionary view compares to a dictionary literal in Python?

# A dictionary view in Python is a dynamic view of the dictionary's keys, values, or items. It is created using the dict.keys(), dict.values(), or dict.items() methods. These views are not static; they reflect changes made to the dictionary. For example:
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
keys_view = my_dict.keys()  # This creates a view of the dictionary's keys
print(keys_view)  # Output: dict_keys(['name', 'age', 'city'])
my_dict["country"] = "USA"  # Adding a new key-value pair to the dictionary
print(
    keys_view
)  # Output: dict_keys(['name', 'age', 'city', 'country']) - the view reflects the change
# In contrast, a dictionary literal is a static representation of a dictionary at the time it is created. It does not change unless you explicitly modify the dictionary it represents. For example:
my_dict_literal = {"name": "Alice", "age": 30, "city": "New York"}
print(my_dict_literal)  # Output: {'name': 'Alice', 'age': 30, 'city': 'New York'}
my_dict_literal["country"] = "USA"  # Modifying the dictionary literal
print(
    my_dict_literal
)  # Output: {'name': 'Alice', 'age': 30, 'city': 'New York', 'country': 'USA'} - the dictionary literal itself is modified, but it is not a view that reflects changes to another dictionary
# In summary, a dictionary view is a dynamic representation of a dictionary's keys, values, or items that reflects changes to the dictionary, while a dictionary literal is a static representation of a dictionary at the time it is created.
