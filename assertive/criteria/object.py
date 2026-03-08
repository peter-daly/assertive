from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import (
    WrappedCriteria,
)


class has_attributes(Criteria):
    """
    Match objects that expose given attributes with matching values.

    Each provided attribute value is converted with ``ensure_criteria``,
    so you can mix direct values and nested criteria.

    Args:
        **attributes: Attribute names and expected value criteria.

    Example:
        ```python
        @dataclass
        class Person:
            name: str
            age: int

        assert Person(name="Alice", age=30) == has_attributes(name="Alice", age=30) # passes
        assert Person(name="Alice", age=30) == has_attributes(name="Alice")          # passes
        assert Person(name="Alice", age=30) == has_attributes(name="Bob")            # fails
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
    Match objects that are instances of ``expected``.

    This uses ``isinstance`` and therefore accepts subclasses.

    Args:
        expected: Required base type.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str

        assert Employee(name="Alice", age=30, job="Engineer") == is_type(Person)   # passes
        assert Employee(name="Alice", age=30, job="Engineer") == is_type(Employee) # passes
        assert Person(name="Alice", age=30) == is_type(Employee)                    # fails
        ```
    """

    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return isinstance(subject, self.expected)


class is_exact_type(Criteria):
    """
    Match objects whose concrete class is exactly ``expected``.

    Unlike ``is_type``, subclasses do not match.

    Args:
        expected: Exact class required.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str

        assert Employee(name="Alice", age=30, job="Engineer") == is_exact_type(Person)   # fails
        assert Employee(name="Alice", age=30, job="Engineer") == is_exact_type(Employee) # passes
        assert Person(name="Alice", age=30) == is_exact_type(Employee)                     # fails
        ```
    """

    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject.__class__ == self.expected


class class_match(WrappedCriteria):
    """
    Match objects by class compatibility plus attribute rules.

    Internally this composes ``is_type(cls) & has_attributes(**attributes)``.

    Args:
        cls: Type that the subject must be an instance of.
        **attributes: Attribute expectations evaluated with nested criteria.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str

        assert Employee(name="Alice", age=30, job="Engineer") == class_match(Person, name="Alice")   # passes
        assert Employee(name="Alice", age=30, job="Engineer") == class_match(Employee, job="Engineer") # passes
        assert Person(name="Alice", age=30) == class_match(Person, age=40)                             # fails
        ```
    """

    def __init__(self, cls: type, **attributes):
        super().__init__(is_type(cls) & has_attributes(**attributes))


class strict_class_match(WrappedCriteria):
    """
    Match objects by exact class plus attribute rules.

    Internally this composes ``is_exact_type(cls) & has_attributes(**attributes)``.
    Use this when subclass instances should not match.

    Args:
        cls: Exact class required for the subject.
        **attributes: Attribute expectations evaluated with nested criteria.

    Example:
        ```python
        @dataclass(kw_only=True)
        class Person:
            name: str
            age: int

        @dataclass(kw_only=True)
        class Employee(Person):
            job: str

        assert Employee(name="Alice", age=30, job="Engineer") == strict_class_match(Person, name="Alice")   # fails
        assert Employee(name="Alice", age=30, job="Engineer") == strict_class_match(Employee, job="Engineer") # passes
        assert Person(name="Alice", age=30) == strict_class_match(Person, age=40)                             # fails
        ```
    """

    def __init__(self, cls: type, **attributes):
        super().__init__(is_exact_type(cls) & has_attributes(**attributes))
