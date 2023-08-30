from abc import ABC, abstractmethod
from typing import Any, final


def ensure_criteria(value: Any) -> "Criteria":
    if isinstance(value, Criteria):
        return value
    return _default_ensured_criteria(value)


class Assertion:
    def __init__(self, subject):
        self._subject = subject

    def matches(self, comparison: Any):
        """Asserts that the subject matches the provided criteria."""
        criteria = ensure_criteria(comparison)
        if not criteria.run_match(self._subject):
            failure_msg = criteria.failure_message(self._subject)
            raise AssertionError(failure_msg)

    def does_not_match(self, comparison: Any):
        """Asserts that the subject does not match the provided criteria."""
        criteria = ensure_criteria(comparison)
        if not criteria.run_negated_match(self._subject):
            failure_msg = criteria.negated_failure_message(self._subject)
            raise AssertionError(failure_msg)

    def __eq__(self, other):
        self.matches(other)
        return self

    def __ne__(self, other):
        self.does_not_match(other)
        return self


def assert_that(subject):
    return Assertion(subject)


class Criteria(ABC):
    def _before_run(self, subject):
        pass

    @final
    def run_match(self, subject) -> bool:
        self._before_run(subject)
        return self._match(subject)

    @final
    def run_negated_match(self, subject) -> bool:
        self._before_run(subject)
        return self._negated_match(subject)

    @abstractmethod
    def _match(self, subject) -> bool:
        """
        Determine if the subject matches this criteria.
        Should be overridden by child classes.
        Args:
            subject: The object to match against this criteria.

        Returns:
            bool: True if the subject matches, False otherwise.
        """
        ...

    def _negated_match(self, subject) -> bool:
        """
        Determine if the subject matches this criteria.
        Should be overridden by child classes.
        Args:
            subject: The object to match against this criteria.

        Returns:
            bool: True if the subject matches, False otherwise.
        """
        return not self._match(subject)

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    def failure_message(self, subject) -> str:
        return f"Expected {subject} to match: {self.description}"

    def negated_failure_message(self, subject) -> str:
        """
        Generates a message to display when a negated assertion fails.

        Args:
            subject: The object that incorrectly matched this criteria.

        Returns:
            str: A message explaining why the negated match failed.
        """
        return f"Expected {subject} to not match: {self.description}"

    def __and__(self, other):
        return _AndCriteria(self, ensure_criteria(other))

    def __or__(self, other):
        return _OrCriteria(self, ensure_criteria(other))

    def __xor__(self, other):
        return _XorCriteria(self, ensure_criteria(other))

    def __invert__(self):
        return _NegatedCriteria(self)


class _AndCriteria(Criteria):
    def __init__(self, left: Criteria, right: Criteria):
        self.left = left
        self.right = right

    def _match(self, subject) -> bool:
        return self.left.run_match(subject) and self.right.run_match(subject)

    @property
    def description(self) -> str:
        return f"{self.left.description} AND {self.right.description}"

    def failure_message(self, subject) -> str:
        if not self.left._match(subject):
            return self.left.failure_message(subject)
        return self.right.failure_message(subject)


class _OrCriteria(Criteria):
    def __init__(self, left: Criteria, right: Criteria):
        self.left = left
        self.right = right

    def _match(self, subject) -> bool:
        return self.left.run_match(subject) or self.right.run_match(subject)

    @property
    def description(self) -> str:
        return f"{self.left.description} OR {self.right.description}"


class _XorCriteria(Criteria):
    def __init__(self, left: Criteria, right: Criteria):
        self.left = left
        self.right = right

    def _match(self, subject) -> bool:
        return self.left.run_match(subject) ^ self.right.run_match(subject)

    @property
    def description(self) -> str:
        return f"{self.left.description} XOR {self.right.description}"


class _NegatedCriteria(Criteria):
    def __init__(self, criteria: Criteria):
        self.criteria = criteria

    def _match(self, subject) -> bool:
        return self.criteria.run_negated_match(subject)

    def _negated_match(self, subject) -> bool:
        return self.criteria.run_match(subject)

    @property
    def description(self) -> str:
        return f"[NEGATED]: {self.criteria.description}"


class _default_ensured_criteria(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject == self.expected

    @property
    def description(self) -> str:
        return f"== {self.expected}"
