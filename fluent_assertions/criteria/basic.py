from typing import Union
from fluent_assertions.assertions import Criteria, ensure_criteria


class is_equal_to(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject == self.expected

    @property
    def description(self) -> str:
        return f"== {self.expected}"


class is_greater_than(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject > self.expected

    @property
    def description(self) -> str:
        return f"> {self.expected}"


class is_greater_than_or_equal(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject >= self.expected

    @property
    def description(self) -> str:
        return f">= {self.expected}"


class is_less_than(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject < self.expected

    @property
    def description(self) -> str:
        return f"< {self.expected}"


class is_less_than_or_equal(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject <= self.expected

    @property
    def description(self) -> str:
        return f"<= {self.expected}"


class is_between(Criteria):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.is_inclusive = True

    @property
    def inclusive(self):
        self.is_inclusive = True
        return self

    @property
    def exclusive(self):
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
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return id(subject) == id(self.expected)

    @property
    def description(self) -> str:
        return f"is same instance as {self.expected}"


class is_true(Criteria):
    def _match(self, subject) -> bool:
        return subject is True

    @property
    def description(self) -> str:
        return "is True"


class is_false(Criteria):
    def _match(self, subject) -> bool:
        return subject is False

    @property
    def description(self) -> str:
        return "is False"


class as_string_matches(Criteria):
    """When the subject called with the str the subject matches the criteria"""

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
