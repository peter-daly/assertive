from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import (
    WrappedCriteria,
)


class has_attributes(Criteria):
    """
    A criteria that checks if an object has the specified attributes.

    Args:
        **attributes: Keyword arguments representing the attributes to check. The key is the attribute name
            and the value is the criteria to apply to the attribute value.

    Example:
        ```python
        @dataclass
        class Person:
            name: str
            age: int


        assert Person(name="Alice", age=30) == has_attributes(name="Alice", age=30) # Passes
        assert Person(name="Alice", age=30) == has_attributes(name="Alice") # Passes
        assert Person(name="Alice", age=30) == has_attributes(name="Bob") # Fails


        assert Person(name="Bob", age=30) == has_attributes(name="Bob", age=30) # Passes
        ```
    """

    def __init__(self, **attributes):
        self.attributes = {k: ensure_criteria(v) for k, v in attributes.items()}

    def _match(self, subject):
        for attr_name, criteria in self.attributes.items():
            if not hasattr(subject, attr_name):
                return False

            attr_value = getattr(subject, attr_name)
            if not criteria.run_match(attr_value):
                return False
        return True


class is_type(Criteria):
    """
    A criteria that checks if the subject is an instance of a specific type.

    Args:
        expected (type): The expected type.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str


        assert Employee(name="Alice", age=30, job="Engineer") == is_type(Person) # Passes
        assert Employee(name="Alice", age=30, job="Engineer") == is_type(Employee) # Passes
        assert Person(name="Alice", age=30) == is_type(Employee) # Fails


        assert Person(name="Bob", age=30) == is_type(Person) # Passes
        ```
    """

    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return isinstance(subject, self.expected)


class is_exact_type(Criteria):
    """
    A criteria that checks if the subject is of the exact specified type.

    Args:
        expected (type): The expected type of the subject.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str


        assert Employee(name="Alice", age=30, job="Engineer") == is_exact_type(Person) # Fails
        assert Employee(name="Alice", age=30, job="Engineer") == is_exact_type(Employee) # Passes
        assert Person(name="Alice", age=30) == is_exact_type(Employee) # Fails


        assert Person(name="Bob", age=30) == is_exact_type(Person) # Passes
        ```
    """

    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject.__class__ == self.expected


class class_match(WrappedCriteria):
    """
    Represents a criteria that matches objects of a specific class with specified attributes.

    Args:
        cls (type): The class to match.
        **attributes: The attributes to match on the class.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str


        assert Employee(name="Alice", age=30, job="Engineer") == class_match(Person, name="Alice") # Passes
        assert Employee(name="Alice", age=30, job="Engineer") == class_match(Employee, job="Engineer") # Passes
        assert Person(name="Alice", age=30) == class_match(Person, age=40) # Fails


        assert Person(name="Bob", age=30) == class_match(Employee, name="bob") # Fails
        assert Person(name="Bob", age=30) == class_match(Person, name="bob") # Passes
        ```
    """

    def __init__(self, cls: type, **attributes):
        super().__init__(is_type(cls) & has_attributes(**attributes))


class strict_class_match(WrappedCriteria):
    """
    A criteria that checks if an object is an exact instance of a given class
    and has the specified attributes.

    Args:
        cls (type): The class to match against.
        **attributes: The attributes to check for.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str


        assert Employee(name="Alice", age=30, job="Engineer") == strict_class_match(Person, name="Alice") # Fails
        assert Employee(name="Alice", age=30, job="Engineer") == strict_class_match(Employee, job="Engineer") # Passes
        assert Person(name="Alice", age=30) == strict_class_match(Person, age=40) # Fails


        assert Employee(name="Bob", age=30, job="Developer") == strict_class_match(Person, name="bob") # Fails
        assert Person(name="Bob", age=30) == strict_class_match(Person, name="bob") # Passes
        ```
    """

    def __init__(self, cls: type, **attributes):
        super().__init__(is_exact_type(cls) & has_attributes(**attributes))
