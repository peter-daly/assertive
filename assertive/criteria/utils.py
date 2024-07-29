from collections.abc import Sequence
from typing import Any, Callable, Iterable, Mapping, Union

from assertive.core import Criteria, ensure_criteria

from .basic import is_gte


def joined_descriptions(criteria_list: Iterable[Criteria], delimiter=", "):
    return delimiter.join([c.description for c in criteria_list])


def joined_keyed_descriptions(
    mapping: Mapping[Any, Criteria], delimiter=", ", relationship=": "
):
    return delimiter.join(
        [f"{key}{relationship}{c.description}" for key, c in mapping.items()]
    )


def get_failures_messages(failures_dict: Mapping[str, str]) -> Sequence[str]:
    return [f"{attr} -> {message}" for attr, message in failures_dict.items()]


def get_failures_summary(failures_dict: Mapping[str, str]) -> str:
    messages = get_failures_messages(failures_dict)
    return "Failures:\n" + "\n".join(messages)


class AnyCriteria(Criteria):
    """Represents a criteria that matches any subject."""

    def _match(self, subject) -> bool:
        return True

    def _negated_match(self, subject) -> bool:
        return True

    @property
    def description(self) -> str:
        return "ANY"


ANY = AnyCriteria()


class PredicateCriteria(Criteria):
    def __init__(self, predicate: Callable[[Any], bool], description: str):
        self.predicate = predicate
        self._description = description

    def _match(self, subject) -> bool:
        return self.predicate(subject)

    @property
    def description(self) -> str:
        return self._description


class WrappedCriteria(Criteria):
    def __init__(self, inner_criteria: Criteria):
        self.inner_criteria = inner_criteria

    def _match(self, subject):
        return self.inner_criteria.run_match(subject)

    def _negated_match(self, subject) -> bool:
        return self.inner_criteria.run_negated_match(subject)

    @property
    def description(self) -> str:
        return self.inner_criteria.description

    def failure_message(self, subject) -> str:
        return self.inner_criteria.failure_message(subject)

    def negated_failure_message(self, subject) -> str:
        return self.inner_criteria.negated_failure_message(subject)


class TimesMixin:
    """
    Mixin class that provides methods for specifying the number of times an action should occur.
    """

    def __init__(self):
        self.times_criteria = is_gte(1)

    def times(self, number: Union[int, Criteria]):
        """
        Specifies the exact number of times an action should occur.

        Args:
            number: The number of times the action should occur. Can be an integer or a Criteria object.

        Returns:
            self: The current instance of the class, allowing for method chaining.
        """
        self.times_criteria = ensure_criteria(number)
        return self

    def once(self):
        """
        Specifies that the action should occur exactly once.

        Returns:
            self: The current instance of the class, allowing for method chaining.
        """
        return self.times(1)

    def twice(self):
        """
        Specifies that the action should occur exactly twice.

        Returns:
            self: The current instance of the class, allowing for method chaining.
        """
        return self.times(2)

    def never(self):
        """
        Specifies that the action should never occur.

        Returns:
            self: The current instance of the class, allowing for method chaining.
        """
        return self.times(0)

    def at_least_times(self, number: int):
        """
        Specifies that the action should occur at least the specified number of times.

        Args:
            number: The minimum number of times the action should occur.

        Returns:
            self: The current instance of the class, allowing for method chaining.
        """
        return self.times(is_gte(number))
