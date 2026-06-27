from pathlib import Path

path = Path(__file__).parent / "food.json"

import json

food = {
    "menu": [
        {
            "name": "Pizza",
            "price": 10.99,
            "ingredients": ["dough", "tomato sauce", "cheese"],
        },
        {
            "name": "Burger",
            "price": 8.99,
            "ingredients": ["bun", "beef patty", "lettuce", "tomato", "cheese"],
        },
        {
            "name": "Salad",
            "price": 6.99,
            "ingredients": ["lettuce", "tomato", "cucumber", "carrot"],
        },
    ]
}


def write_json(data, file_path):

    with open(file_path, "w", encoding="utf-8") as file:
        # The json.dump() function is used to write the Python dictionary (data) to a file in JSON format. The indent=4 argument is used to pretty-print the JSON with an indentation of 4 spaces, making it easier to read.
        # It serializes the Python object (in this case, the food dictionary) into a JSON formatted string and writes it to the specified file. If the file does not exist, it will be created. If it already exists, it will be overwritten.
        json.dump(data, file, indent=4)
    print(f"Data written to {file_path}")


def read_json(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        # The json.load() function is used to read the JSON data from a file and convert it back into a Python dictionary.
        data = json.load(file)
    print(f"Data read from {file_path}:\n{data}")
    return data


def main():
    write_json(food, path)
    data = read_json(path)
    print(data)


if __name__ == "__main__":
    main()
