"""
File system operations in Python
In Python, you can perform various file system operations such as reading, writing, and manipulating files. Here are some common file system operations:
1. Reading a file:
You can read a file using the built-in open() function. The open() function takes the file name and the mode (e.g., 'r' for reading) as arguments. You can then use the read() method to read the content of the file.
Example is provided in the code snippet below.:

2. Writing to a file:
You can write to a file using the open() function with the mode 'w' (write) or 'a' (append). The write() method is used to write content to the file.
Example is provided in the code snippet below.:
# write to a file
def write_file():
    with open("notes.txt", "w") as file:
        file.write("This is a new note.\n")
        file.write("This is another note.\n")
        # close the file
        file.close()  # this is not necessary when using with statement, as it automatically closes the file after the block is executed.

3. Manipulating files:
You can also perform various file manipulations such as renaming, deleting, and checking if a file exists using the os module.
Example is provided in the code snippet below.:
import os
# rename a file
os.rename("old_file.txt", "new_file.txt")
# delete a file
os.remove("file_to_delete.txt")
# check if a file exists
if os.path.exists("file_to_check.txt"):
    print("The file exists.")

else:
    print("The file does not exist.")

4. Using with statement for file operations:
Using the with statement is a good practice when working with files, as it ensures that the file is properly closed after its suite finishes, even if an exception is raised. This helps to prevent resource leaks and ensures that the file is not left open unintentionally.

Great question. In Python, with is used for context management, which means Python automatically handles setup and cleanup for resources like files.

In your code at file_system.py, this line:

with open("notes.txt", "r") as file:

does two things safely:
1. Opens the file.
2. Guarantees the file is closed when the block ends, even if an error happens while reading.

Why not just use open alone?
1. If you do file = open(...), you must remember to close it yourself every time.
2. If an exception occurs before close runs, the file can stay open longer than intended and consume system resources unnecessarily.
3. with makes code shorter, safer, and clearer.

Without with, the safe version is usually:
- open the file
- use try/finally
- close in finally

So with is essentially the clean, Pythonic shortcut for that pattern.




"""

# read a file
from email.mime import text


def read_file():
    with open("notes.txt", "r") as file:
        # read the entire content of the file into a string variable called content
        content = file.read()
        # print(content)
        # close the file
        # file.close() -  # this is not necessary when using with statement, as it automatically closes the file after the block is executed


# read file without with statement
def read_file_without_with():
    file = open("article.txt", "r")
    content = file.read()
    print(content)
    file.close()  # you must remember to close the file manually when not using with statement


def read_and_print_line():

    file = open("article.txt", "r")
    # use readline() to read the file line by line - this is more memory efficient for large files as it does not load the entire file into memory at once
    lines = file.readline()
    for line in lines:
        print(f" Line: {line}")

    file.close()  # you must remember to close the file manually when not using with statement


# use readlines() to read the entire file into a list of lines - this is less memory efficient for large files as it loads the entire file into memory at once
def read_entire_file_with_readline():
    file = open("article.txt", "r")
    lines = file.readlines()
    for line in lines:
        print(f" Lines: {line}")

    file.close()


"""
Using try/finally to ensure the file is closed properly, even if an error occurs while reading the file.

It is initialized to "None" so the variable always exists before the try block runs.

Why this matters:

If open fails, Python jumps to except/finally immediately.
Without pre-initializing, file would never be assigned.
Then finally trying to close file would raise another error (UnboundLocalError).
With None, you can safely do:
if file is not None:
file.close()
So this pattern prevents a secondary crash during cleanup and makes finally safe in all cases.
"""


def read_file_try_finally():
    file = None
    try:
        file = open("note.txt", "r")
        content = file.read()
        print(content)
    except FileNotFoundError:
        print("Error: notes.txt was not found.")
    except OSError as error:
        print(f"Error reading notes.txt: {error}")
    finally:
        if file is not None:
            file.close()


# write to a file - An existing file will be overwritten, and a new file will be created if it does not exist.
def write_file():
    with open("notes.txt", "w") as file:
        file.write("This is a new note.\n")
        file.write("This is another note.\n")


# write to a file
def write_text_to_file(filename, text):

    # open a file
    file = open(filename, "w")
    # write text to the file
    file.write(text)
    # close the file
    file.close()


menus = ["Home", "About", "Contact", "Blog"]


def write_char_to_file(filename):
    # open a file in write mode
    file = open(filename, "w")
    # write text to the file
    for menu in menus:
        file.write(menu + "\n")
    # close the file
    file.close()


fruits = ["Apple", "Banana", "Cherry", "Date", "Strawberry"]


def write_and_read_file(filename):
    # open a file in write mode
    file = open(filename, "w")
    # write text to the file
    for fruit in fruits:
        file.write(fruit + "\n")

    # read the file back and print its content to the console, demonstrating that the file was written successfully
    with open(filename, "r") as file:
        content = file.read()
        if content:  # check if content is not empty
            print("file was written successfully!")
        print(content)


def append_text_to_file(filename, text):
    # open a file in append mode
    file = open(filename, "a")
    # write text to the file
    file.write(text)
    # close the file
    file.close()


def delete_file(filename):
    import os

    os.remove(filename)


def rename_file(old_name, new_name):
    import os

    os.rename(old_name, new_name)


def main():
    # read_file()
    # read_file_without_with()
    # read_file_try_finally()
    # read_and_print_line()
    # read_entire_file_with_readline()
    # write_file()
    # write_text_to_file("example.txt", "This is an example text written to the file.")
    # write_char_to_file("menus.txt")
    # append_text_to_file(
    #     "example.txt", "\nThis is an additional line appended to the file."
    # )
    write_and_read_file("fruits.txt")

    return


if __name__ == "__main__":
    main()
