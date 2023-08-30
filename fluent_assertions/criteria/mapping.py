from abc import abstractmethod
from typing import Any
from fluent_assertions.assertions import Criteria, ensure_criteria
from fluent_assertions.criteria.utils import (
    joined_descriptions,
    joined_keyed_descriptions,
)
from collections.abc import Mapping


class MappingCriteria(Criteria):
    def _before_run(self, subject):
        if not isinstance(subject, Mapping):
            raise TypeError(f"{subject} needs to be mapping")


class has_key_values(MappingCriteria):
    def __init__(self, key_values: Mapping):
        """
        Initializes the criteria with the attributes and their expected values (or criteria).

        Args:
            attributes: A dictionary of attribute names and their expected values (or criteria).
        """
        self.key_values = {k: ensure_criteria(v) for k, v in key_values.items()}

    def _match(self, subject: Mapping):
        """
        Checks if the subject has the specified attributes, and if those attributes match the provided criteria.

        Args:
            subject: The object to match against this criteria.

        Returns:
            bool: True if all attribute criteria match, False otherwise.
        """
        for name, criteria in self.key_values.items():
            if name not in subject:
                return False

            value = subject[name]
            if not criteria._match(value):
                return False

        return True

    @property
    def description(self):
        return f"has key values: {{{joined_keyed_descriptions(self.key_values)}}}"


class has_key_and_value(has_key_values):
    def __init__(self, key: Any, value: Any):
        """
        Initializes the criteria with the attributes and their expected values (or criteria).

        Args:
            attributes: A dictionary of attribute names and their expected values (or criteria).
        """
        super().__init__({key: value})


class has_exact_key_values(has_key_values):
    def __init__(self, key_values):
        """
        Initializes the criteria with the attributes and their expected values (or criteria).

        Args:
            attributes: A dictionary of attribute names and their expected values (or criteria).
        """
        self.key_values = {k: ensure_criteria(v) for k, v in key_values.items()}

    def _match(self, subject: Mapping):
        """
        Checks if the subject has the specified attributes, and if those attributes match the provided criteria.

        Args:
            subject: The object to match against this criteria.

        Returns:
            bool: True if all attribute criteria match, False otherwise.
        """
        if len(subject.keys()) != len(self.key_values):
            return False

        return super()._match(subject)

    @property
    def description(self):
        return f"has exact key values: {{{joined_keyed_descriptions(self.key_values)}}}"


class contains_keys(MappingCriteria):
    def __init__(self, *keys):
        """
        Initializes the criteria with the attributes and their expected values (or criteria).

        Args:
            attributes: A dictionary of attribute names and their expected values (or criteria).
        """
        self.key_criteria = [(ensure_criteria(k)) for k in keys]

    def _match(self, subject: Mapping):
        keys = subject.keys()
        for criteria in self.key_criteria:
            if not any([criteria._match(key) for key in keys]):
                return False
        return True

    @property
    def description(self) -> str:
        return f"to have keys matching: [{joined_descriptions(self.key_criteria)}]"


class contains_exact_keys(contains_keys):
    def _match(self, subject: Mapping):
        if len(subject.keys()) != len(self.key_criteria):
            return False
        return super()._match(subject)

    @property
    def description(self) -> str:
        return (
            f"to have exact keys matching: [{joined_descriptions(self.key_criteria)}]"
        )
