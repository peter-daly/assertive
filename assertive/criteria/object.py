from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import (
    WrappedCriteria,
    get_failures_summary,
    joined_keyed_descriptions,
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

        # Using assert_that
        assert_that(Person(name="Alice", age=30)).matches(has_attributes(name="Alice", age=30)) # Passes
        assert_that(Person(name="Alice", age=30)).matches(has_attributes(name="Alice")) # Passes
        assert_that(Person(name="Alice", age=30)).matches(has_attributes(name="Bob")) # Fails

        # Using basic assert
        assert Person(name="Bob", age=30) == has_attributes(name="Bob", age=30) # Passes
        ```
    """

    def __init__(self, **attributes):
        self.attributes = {k: ensure_criteria(v) for k, v in attributes.items()}

    def _get_failures(self, subject):
        failures = {}

        for attr_name, criteria in self.attributes.items():
            if not hasattr(subject, attr_name):
                failures[attr_name] = "not found"
                continue

            attr_value = getattr(subject, attr_name)
            if not criteria._match(attr_value):
                failures[attr_name] = criteria.failure_message(attr_value)

        return failures

    def _match(self, subject):
        failures = self._get_failures(subject)
        return not failures

    @property
    def description(self) -> str:
        return f"has attributes ({joined_keyed_descriptions(self.attributes)})"

    def failure_message(self, subject) -> str:
        headline = super().failure_message(subject)
        failures = self._get_failures(subject)
        failures_summary = get_failures_summary(failures)
        message = headline + "\n" + failures_summary

        return message


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

        # Using assert_that
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(is_type(Person)) # Passes
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(is_type(Employee)) # Passes
        assert_that(Person(name="Alice", age=30)).matches(is_type(Employee)) # Fails

        # Using basic assert
        assert Person(name="Bob", age=30) == is_type(Person) # Passes
        ```
    """

    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return isinstance(subject, self.expected)

    @property
    def description(self) -> str:
        return f"is an instance of {self.expected}"


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

        # Using assert_that
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(is_exact_type(Person)) # Fails
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(is_exact_type(Employee)) # Passes
        assert_that(Person(name="Alice", age=30)).matches(is_exact_type(Employee)) # Fails

        # Using basic assert
        assert Person(name="Bob", age=30) == is_exact_type(Person) # Passes
        ```
    """

    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject.__class__ == self.expected

    @property
    def description(self) -> str:
        return f"is of type {self.expected}"


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

        # Using assert_that
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(class_match(Person, name="Alice")) # Passes
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(class_match(Employee, job="Engineer")) # Passes
        assert_that(Person(name="Alice", age=30)).matches(class_match(Person, age=40)) # Fails

        # Using basic assert
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

        # Using assert_that
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(strict_class_match(Person, name="Alice")) # Fails
        assert_that(Employee(name="Alice", age=30, job="Engineer")).matches(strict_class_match(Employee, job="Engineer")) # Passes
        assert_that(Person(name="Alice", age=30)).matches(strict_class_match(Person, age=40)) # Fails

        # Using basic assert
        assert Employee(name="Bob", age=30, job="Developer") == strict_class_match(Person, name="bob") # Fails
        assert Person(name="Bob", age=30) == strict_class_match(Person, name="bob") # Passes
        ```
    """

    def __init__(self, cls: type, **attributes):
        super().__init__(is_exact_type(cls) & has_attributes(**attributes))
