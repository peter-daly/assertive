from assertive.assertions import Criteria, ensure_criteria
from assertive.criteria.utils import WrappedCriteria, joined_keyed_descriptions


class has_attributes(Criteria):
    """
    A criteria that checks if an object has the specified attributes.

    Args:
        **attributes: Keyword arguments representing the attributes to check. The key is the attribute name
            and the value is the criteria to apply to the attribute value.

    Attributes:
        attributes (dict): A dictionary containing the attribute names as keys and the corresponding criteria
            as values.

    Methods:
        _match(subject): Checks if the subject object has all the specified attributes and if the attribute
            values match the corresponding criteria.
        description: Returns a string describing the criteria.

    Example:
        criteria = has_attributes(name=has_length(5), age=is_greater_than(18))
        result = criteria._match(obj)
        description = criteria.description
    """

    def __init__(self, **attributes):
        self.attributes = {k: ensure_criteria(v) for k, v in attributes.items()}

    def _match(self, subject):
        for attr_name, criteria in self.attributes.items():
            if not hasattr(subject, attr_name):
                return False

            attr_value = getattr(subject, attr_name)
            if not criteria._match(attr_value):
                return False

        return True

    @property
    def description(self) -> str:
        return f"has attributes ({joined_keyed_descriptions(self.attributes)})"


class is_type(Criteria):
    """
    A criteria that checks if the subject is an instance of a specific type.

    Args:
        expected (type): The expected type.

    Returns:
        bool: True if the subject is an instance of the expected type, False otherwise.
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

    Attributes:
        expected (type): The expected type of the subject.

    Methods:
        _match(subject) -> bool: Checks if the subject is of the expected type.
        description() -> str: Returns a description of the criteria.

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
        >>> obj = MyClass()
        >>> criteria = class_match(MyClass, attr1=10, attr2='hello')
        >>> criteria.matches(obj)
        True
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
        >>> obj = MyClass()
        >>> criteria = strict_class_match(MyClass, attr1='value1', attr2='value2')
        >>> criteria(obj)
        True
    """

    def __init__(self, cls: type, **attributes):
        super().__init__(is_exact_type(cls) & has_attributes(**attributes))
