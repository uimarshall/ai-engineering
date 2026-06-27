from pathlib import Path

"""
This script demonstrates how to create a dynamic file path using the pathlib library in Python.

"-> Path" on line 13 is a return type hint (annotation).
It means: this function is expected to return a Path object.
It helps readers and tools (like Pylance/mypy) understand your code.
Python does not strictly enforce it at runtime by default, but type checkers use it to catch mistakes early.
"""


def create_dynamic_file_path(base_path: str, filename: str) -> Path:
    # Create a Path object for the base path
    # Converts the base_path string into a Path object so you can use path operations on it such as mkdir().
    base_dir = Path(base_path)

    # Ensure the base path exists, if not create it
    # parents=True means also create parent folders if needed.
    # exist_ok=True means do not crash if folder already exists.
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create a Path object for the full file path - Build the full file path by combining the base directory and the filename using the / operator, which is a convenient way to join paths in pathlib.

    # The slash here is a Path operator, not string math.
    file_path = base_dir / filename

    print(f"File path created: {file_path}")

    # Optionally, create the file and write some content to it
    file_path.touch(exist_ok=True)
    print(f"File created at: {file_path}")

    file_path.write_text("This is an example file created using a dynamic file path.\n")
    print(f"Content written to {file_path}:\n{file_path.read_text()}")

    # Clean up by removing the created file and directory
    # file_path.unlink()
    # file_path.parent.rmdir()

    return file_path


def create_dynamic_file_path_with_open(base_path: str, filename: str) -> Path:
    base_dir = Path(base_path)
    base_dir.mkdir(parents=True, exist_ok=True)

    file_path = base_dir / filename

    print(f"File path created: {file_path}")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("This is an example file created using open().\n")

    print(f"File created at: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    print(f"Content written to {file_path}:\n{content}")

    return file_path


def main():
    base_path = "my_files"
    create_dynamic_file_path(base_path, "example_pathlib.txt")
    create_dynamic_file_path_with_open(base_path, "example_open.txt")


if __name__ == "__main__":
    main()
