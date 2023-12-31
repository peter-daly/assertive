from typing import Any, Callable, Iterable, Mapping, Union

from assertive.assertions import Criteria, ensure_criteria
from .basic import is_greater_than_or_equal


def joined_descriptions(criterias: Iterable[Criteria], delimiter=", "):
    return delimiter.join([c.description for c in criterias])


def joined_keyed_descriptions(
    mapping: Mapping[Any, Criteria], delimiter=", ", relationship=": "
):
    return delimiter.join(
        [f"{key}{relationship}{c.description}" for key, c in mapping.items()]
    )


class AnyCriteria(Criteria):
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
    def __init__(self):
        self.times_criteria = is_greater_than_or_equal(1)

    def times(self, number: Union[int, Criteria]):
        self.times_criteria = ensure_criteria(number)
        return self  # Return self to allow for chaining

    @property
    def once(self):
        return self.times(1)

    @property
    def twice(self):
        return self.times(2)

    @property
    def never(self):
        return self.times(0)

    def at_least_times(self, number: int):
        return self.times(is_greater_than_or_equal(number))
