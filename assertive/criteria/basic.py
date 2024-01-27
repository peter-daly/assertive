from typing import Union
from assertive.assertions import (
    Criteria,
    ensure_criteria,
    _default_ensured_criteria,
)


class is_equal_to(_default_ensured_criteria):
    """
    Checks subject is equal to the expected value
    """

    pass


class is_greater_than(Criteria):
    """
    Checks subject is greater than expected value
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject > self.expected

    @property
    def description(self) -> str:
        return f"> {self.expected}"


class is_greater_than_or_equal(Criteria):
    """
    Checks subject is greater or equal than expected value
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject >= self.expected

    @property
    def description(self) -> str:
        return f">= {self.expected}"


class is_less_than(Criteria):
    """
    Checks subject is less than expected value
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject < self.expected

    @property
    def description(self) -> str:
        return f"< {self.expected}"


class is_less_than_or_equal(Criteria):
    """
    Checks subject is less or equal than expected value
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject <= self.expected

    @property
    def description(self) -> str:
        return f"<= {self.expected}"


class is_between(Criteria):
    """
    Checks subject is between an uper bound or lower bound.
    """

    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.is_inclusive = True

    @property
    def inclusive(self):
        """
        Upper and lower are included in the accepted range
        """
        self.is_inclusive = True
        return self

    @property
    def exclusive(self):
        """
        Upper and lower are excluded from the accepted range
        """
        self.is_inclusive = False
        return self

    def _match(self, subject) -> bool:
        if self.is_inclusive:
            return subject >= self.lower and subject <= self.upper
        return subject > self.lower and subject < self.upper

    @property
    def description(self) -> str:
        inclusivness = "inclusive" if self.is_inclusive else "exclusive"
        return f"is between {self.lower} and {self.upper}; {inclusivness}"


class is_same_instance_as(Criteria):
    """
    Checks that the subject is the same instance as the crtiteria
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return id(subject) == id(self.expected)

    @property
    def description(self) -> str:
        return f"is same instance as {self.expected}"


class as_string_matches(Criteria):
    """Converts the subject to a string using str() and then checs the criteria"""

    def __init__(self, criteria: Union[Criteria, str]):
        self.criteria = ensure_criteria(criteria)

    def _match(self, subject) -> bool:
        return self.criteria._match(str(subject))

    @property
    def description(self) -> str:
        return self.criteria.description

    def failure_message(self, subject) -> str:
        return f"Expected str({subject}) to match: {self.description}"

    def negated_failure_message(self, subject) -> str:
        return f"Expected str({subject}) to not match: {self.description}"


class is_none(Criteria):
    """Checks the subject is None"""

    def _match(self, subject) -> bool:
        return subject is None

    @property
    def description(self) -> str:
        return "is None"


class is_not_none(Criteria):
    """Checks the subject is not None"""

    def _match(self, subject) -> bool:
        return subject is not None

    @property
    def description(self) -> str:
        return "is not None"
