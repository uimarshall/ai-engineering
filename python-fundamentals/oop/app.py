# classes

# What is a class in Python?

# A class in Python is a blueprint for creating objects. It defines a set of attributes and methods that the created objects (instances) will have. Classes allow for encapsulation, inheritance, and polymorphism, enabling developers to model real-world entities and their behaviors in a structured way.

# It uses the `class` keyword to define a class, and the `__init__` method is used to initialize the attributes of the class when an object is created.

# The constructor method `__init__` is a special method in Python classes that is automatically called when a new instance of the class is created. It is used to initialize the attributes of the class with specific values provided during object creation. The `self` parameter refers to the instance being created and allows access to its attributes and methods.

# methods are functions defined within a class or attached to an object that describe the behaviors of the objects created from that class. They can operate on the attributes of the class and perform specific actions. Methods are defined using the `def` keyword and typically take `self` as their first parameter, which refers to the instance of the class.

# What is an object in Python?

# An object in Python is an instance of a class. It is a specific realization of the class, containing the attributes and methods defined by the class. Objects can hold data (attributes) and perform actions (methods) based on the class definition. Each object can have its own unique state, while sharing the structure and behavior defined by its class.

# Example of a class and object in Python:


class DogExample:
    # Class attribute
    species = "Canis familiaris"

    # self is a reference to the current instance of the class or an object that is created using this class, and it is used to access variables that belong to the class. It is a convention to name it self, but you can use any name you like. The self parameter must be the first parameter of any function in the class.
    def __init__(self, name, age):
        # Instance attributes
        # self.name is just like having a class variable or properties of the class that can be updated or changed. It is used to store the name of the dog instance.
        self.name = name
        self.age = age

    # Method to describe the dog
    def description(self):
        return f"{self.name} is {self.age} years old."

    # Method to make the dog bark
    def bark(self, sound):
        return f"{self.name} says {sound}."
    
    # static method that checks if an action is banned
    @staticmethod
    def is_banned(action, name):
        if action == "bark":
            print(f"{name} is banned in this area due to {action}.")
        elif action == "bite":
            print(f"{name} is banned in this area due to {action}.")
                
        else:
            print(f"{action} is allowed. You can proceed with the dog, {name}!.")     
        


# What is the difference between a class and an object?
# The main difference between a class and an object is that a class is a blueprint or template for creating objects, while an object is an instance of that class. A class defines the structure and behavior (attributes and methods) that its objects will have, but it does not hold any data itself. An object, on the other hand, is a concrete entity that has its own state (data) and can perform actions defined by its class.

# What is encapsulation?
# Encapsulation is a fundamental concept in object-oriented programming (OOP) that refers to the bundling of data (attributes) and methods (functions) that operate on that data into a single unit, which is the class. It restricts direct access to some of an object's components, which can prevent the accidental modification of data. Encapsulation allows for controlled access to an object's attributes and methods through public interfaces (methods), while keeping the internal representation hidden from the outside world.

# Example of encapsulation in Python:


# This class demonstrates encapsulation by using private attributes and providing public getter and setter methods to access and modify those attributes.
class Person:
    # This is the constructor method that runs when a new instance of the class is created. It initializes the private attributes name and age.
    # It constructs a new Person object with the provided name and age, storing them in private attributes to enforce encapsulation.
    def __init__(self, name, age):
        self.__name = name  # Private attribute
        self.__age = age  # Private attribute

    # Getter method for name
    def get_name(self):
        return self.__name

    # Setter method for name
    def set_name(self, name):
        self.__name = name

    # Getter method for age
    def get_age(self):
        return self.__age

    # Setter method for age
    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("Please enter a valid age.")





# What is polymorphism?

# Polymorphism is a fundamental concept in object-oriented programming (OOP) that allows objects of different classes to be treated as objects of a common superclass. It enables a single interface to represent different underlying forms (data types). In Python, polymorphism can be achieved through method overriding and duck typing, allowing for flexibility and extensibility in code design.


def main():
    # Create an instance of DogExample
    my_dog = DogExample("Buddy", 3)
    print("Species:", my_dog.species)  # Output: Canis familiaris
    print("Dog Name:", my_dog.name)  # Output: Buddy
    print("Dog Age:", my_dog.age)  # Output: 3
    print("Dog's description:", my_dog.description())  # Output: Buddy is 3 years old.
    print("Dog's sound:", my_dog.bark("Woof"))  # Output: Buddy says Woof.
    
    DogExample.is_banned("bark", my_dog.name)  # Output: Buddy is banned in this area due to bark.

    # # Create an instance of Person
    # person = Person("Alice", 30)
    # print(person.get_name())  # Output: Alice
    # print(person.get_age())  # Output: 30

    # # Update person's age using setter
    # person.set_age(31)
    # print(person.get_age())  # Output: 31

    # # Create an instance of Dog (inherited from Animal)
    # dog = Dog("Max")
    # print(dog.speak())  # Output: Max says Woof!


if __name__ == "__main__":
    main()
