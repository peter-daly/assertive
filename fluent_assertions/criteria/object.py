from typing import Any
from fluent_assertions.assertions import Criteria, ensure_criteria
from fluent_assertions.criteria.utils import joined_keyed_descriptions


class has_attributes(Criteria):
    def __init__(self, **attributes):
        """
        Initializes the criteria with the attributes and their expected values (or criteria).

        Args:
            attributes: A dictionary of attribute names and their expected values (or criteria).
        """
        self.attributes = {k: ensure_criteria(v) for k, v in attributes.items()}

    def _match(self, subject):
        """
        Checks if the subject has the specified attributes, and if those attributes match the provided criteria.

        Args:
            subject: The object to match against this criteria.

        Returns:
            bool: True if all attribute criteria match, False otherwise.
        """
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
    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return isinstance(subject, self.expected)

    @property
    def description(self) -> str:
        return f"is an instance of {self.expected}"


class is_exact_type(Criteria):
    def __init__(self, expected: type):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject.__class__ == self.expected

    @property
    def description(self) -> str:
        return f"is of type {self.expected}"
