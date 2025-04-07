from abc import ABC, abstractmethod
from typing import Any, final


def ensure_criteria(value: Any) -> "Criteria":
    if isinstance(value, Criteria):
        return value
    return _default_ensured_criteria(value)


class Criteria(ABC):
    """
    Base class for defining criteria used in assertions.

    Subclasses of `Criteria` should override the `_match` method to determine if the subject matches the criteria.
    """

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
        Determine if the subject matches this criteria (negated).
        Should be overridden by child classes.

        Args:
            subject: The object to match against this criteria.

        Returns:
            bool: True if the subject does not match, False otherwise.
        """
        return not self.run_match(subject)

    def __and__(self, other):
        return AndCriteria([self, ensure_criteria(other)])

    def __or__(self, other):
        return OrCriteria([self, ensure_criteria(other)])

    def __xor__(self, other):
        return XorCriteria(self, ensure_criteria(other))

    def __invert__(self):
        return InvertedCriteria(self)

    def __eq__(self, other):
        return self.run_match(other)

    def __neq__(self, other):
        return self.run_negated_match(other)


class AndCriteria(Criteria):
    def __init__(self, criteras: list[Criteria]):
        self.criterias = criteras

    def _match(self, subject) -> bool:
        return all(criteria.run_match(subject) for criteria in self.criterias)


class OrCriteria(Criteria):
    def __init__(self, criterias: list[Criteria]):
        self.criterias = criterias

    def _match(self, subject) -> bool:
        return any(criteria.run_match(subject) for criteria in self.criterias)


class XorCriteria(Criteria):
    def __init__(self, left: Criteria, right: Criteria):
        self.left = left
        self.right = right

    def _match(self, subject) -> bool:
        return self.left.run_match(subject) ^ self.right.run_match(subject)


class InvertedCriteria(Criteria):
    def __init__(self, criteria: Criteria):
        self.criteria = criteria

    def _match(self, subject) -> bool:
        return self.criteria.run_negated_match(subject)

    def _negated_match(self, subject) -> bool:
        return self.criteria.run_match(subject)


class _default_ensured_criteria(Criteria):
    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject == self.expected
