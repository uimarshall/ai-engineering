# What is inheritance?

# class inheritance is a fundamental concept in object-oriented programming (OOP) that allows a class (called the child or subclass) to inherit attributes and methods from another class (called the parent or superclass). This promotes code reusability and establishes a hierarchical relationship between classes. The child class can extend or override the behavior of the parent class, enabling polymorphism and allowing for more specialized implementations.

# Inheritance is a fundamental concept in object-oriented programming (OOP) that allows a class (called the child or subclass) to inherit attributes and methods from another class (called the parent or superclass). This promotes code reusability and establishes a hierarchical relationship between classes. The child class can extend or override the behavior of the parent class, enabling polymorphism and allowing for more specialized implementations.

# Example of inheritance in Python.


class User:  # parent class
    def __init__(self, username, email):
        self.username = username
        self.email = email

    @staticmethod
    def cleared(credentials):
        credentials = tuple(credentials)
        return credentials[0] in credentials and credentials[1] in credentials

    @staticmethod
    def cleared_flexible(*args, **kwargs):
        credentials = tuple(args) + tuple(kwargs.values())
        username = kwargs.get("username", args[0] if len(args) > 0 else None)
        email = kwargs.get("email", args[1] if len(args) > 1 else None)

        if username is None or email is None:
            return False

        return username in credentials and email in credentials

    def get_info(self):
        return f"Username: {self.username}, Email: {self.email}"

    def logged_in(self):
        print(f"{self.username} is logged in with {self.email}.")


class AdminUser(User):  # child class that inherits from the User class
    def __init__(self, username, email, role):
        # calls the constructor of the parent class (User) to initialize the username and email attributes, it inherits the properties and methods of the User class, allowing the Admin class to reuse and extend the functionality of the User class.
        super().__init__(username, email)
        self.role = role  # additional attribute specific to the Admin class

    # This method overrides the get_info method from the User class to include the role attribute in the returned information. It provides a more specific implementation for Admin objects, demonstrating polymorphism.
    def get_info(self):
        return (
            f"Admin Username: {self.username}, Email: {self.email}, Role: {self.role}"
        )

    def logged_out(self):
        print(
            f"Admin {self.username} is logged out with {self.email} and had the role of {self.role}."
        )


class Animal:
    def __init__(self, name):
        self.name = name

    # This method 'speak(self)' is intended to be overridden by subclasses. It raises a NotImplementedError to indicate that subclasses must provide their own implementation of the speak method. This is a pattern for defining an abstract method — a method that exists only to force subclasses to provide their own implementation.

    # Animal is a base/parent class. It says: "every animal should be able to speak, but I don't know how each animal speaks — that's up to each subclass to define."

    # In short: it's a contract — it enforces that any class inheriting from Animal must define its own speak method, or it will crash at runtime with a clear, readable error.
    def speak(self):
        raise NotImplementedError("Subclasses must implement this method")


class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"


def main():
    print("Inheritance Example:")

    admin = AdminUser("admin_user", "admin@email.com", "superadmin")
    print(
        admin.get_info()
    )  # Output: Admin Username: admin_user, Email:admin@email.com, Role: superadmin
    admin.logged_in()  # Output: admin_user is logged in with admin@email.com

    admin.logged_out()  # Output: Admin admin_user is logged out with admin@email.com and had the role of superadmin

    admin_user = AdminUser("Grey", "admin@email.com", "superadmin")

    admin_user.logged_out()

    #  If you try to call speak() on a raw Animal instance, it will raise a NotImplementedError, because the base class Animal does not provide an implementation for speak(). This is a way to enforce that subclasses must implement this method.:
    a = Animal("Cat")
    try:
        a.speak()  # raises NotImplementedError!
    except NotImplementedError as e:
        print(e)
    # Create an instance of Dog
    my_dog = Dog("Buddy")

    # But on a Dog (which overrides speak), it works fine:
    print(my_dog.speak())  # Output: Buddy says Woof!
    if isinstance(my_dog, Animal):
        print(f"{my_dog.name} is an instance of Animal.")

    print(User.cleared(["marshall", "marshall@email.com"]))

    # Quick examples

    print(User.cleared_flexible("marshall", "marshall@email.com"))
    print(User.cleared_flexible("marshall", "marshall@email.com", username="marshall"))
    print(User.cleared_flexible(username="marshall", email="marshall@email.com"))


if __name__ == "__main__":
    main()
