from typing import Any, Callable, Union

from assertive.core import Criteria, ensure_criteria

from .basic import is_gte


class AnyCriteria(Criteria):
    """
    Criteria that always matches.

    This is useful as a wildcard when you only care about selected fields
    and want the rest to pass unconditionally.
    """

    def _match(self, subject) -> bool:
        return True

    def _negated_match(self, subject) -> bool:
        return True


ANY = AnyCriteria()


class PredicateCriteria(Criteria):
    """
    Wrap an arbitrary predicate function as a criteria.

    Args:
        predicate: Callable that returns ``True`` when the subject matches.
        description: Human-readable label describing the predicate.
    """

    def __init__(self, predicate: Callable[[Any], bool], description: str):
        self.predicate = predicate
        self._description = description

    def _match(self, subject) -> bool:
        return self.predicate(subject)


class WrappedCriteria(Criteria):
    """
    Delegate matching behavior to another criteria instance.

    This is commonly used for creating named convenience criteria from
    composed expressions.
    """

    def __init__(self, inner_criteria: Criteria):
        self.inner_criteria = inner_criteria

    def _match(self, subject):
        return self.inner_criteria.run_match(subject)

    def _negated_match(self, subject) -> bool:
        return self.inner_criteria.run_negated_match(subject)


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
