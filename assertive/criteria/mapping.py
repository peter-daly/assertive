from collections.abc import Mapping
from typing import Any

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import (
    get_failures_summary,
    joined_descriptions,
    joined_keyed_descriptions,
)


class MappingCriteria(Criteria):
    def _before_run(self, subject):
        if not isinstance(subject, Mapping):
            raise TypeError(f"{subject} needs to be mapping")


class has_key_values(MappingCriteria):
    """
    Checks if the subject has the specified attributes, and if those attributes match the provided criteria.

    Args:
        key_values: A dictionary of key value pairs to match against the subject.

    Example:
        ```python
        # Using assert_that
        assert_that({"a": 1, "b": 2}).matches(has_key_values({"a": 1})) # Passes
        assert_that({"a": 1, "b": 2}).matches(has_key_values({"a": is_odd()})) # Passes

        # Using basic assert
        assert {"a": 1, "b": 2} == has_key_values({"a": 1}) # Passes
        ```

    """

    def __init__(self, key_values: Mapping):
        self.key_values = {k: ensure_criteria(v) for k, v in key_values.items()}

    def _get_failures(self, subject: Mapping):
        failures = {}

        for name, criteria in self.key_values.items():
            if name not in subject:
                failures[name] = "not found"

            value = subject[name]
            if not criteria._match(value):
                failures[name] = criteria.failure_message(value)
        return failures

    def _match(self, subject: Mapping):
        failures = self._get_failures(subject)
        return not failures

    @property
    def description(self):
        return f"has key values: {{{joined_keyed_descriptions(self.key_values)}}}"

    def failure_message(self, subject) -> str:
        headline = super().failure_message(subject)
        failures = self._get_failures(subject)
        failures_summary = get_failures_summary(failures)

        return headline + "\n" + failures_summary


class has_key_and_value(has_key_values):
    """
    Checks if a Mapping has an single key and value

    Args:
        key: The key to match against the subject.
        value: The value to match against the subject.

    Example:
        ```python
        # Using assert_that
        assert_that({"a": 1, "b": 2}).matches(has_key_and_value("a", 1)) # Passes
        assert_that({"a": 1, "b": 2}).matches(has_key_and_value("a", is_odd())) # Passes

        # Using basic assert
        assert {"a": 1, "b": 2} == has_key_and_value("a", 1) # Passes
        ```

    """

    def __init__(self, key: Any, value: Any):
        super().__init__({key: value})


class has_exact_key_values(has_key_values):
    """
    Checks if the subject has the specified attributes, and if those attributes match the provided criteria.

    Args:
        key_values: A dictionary of key value pairs to match against the subject.

    Example:
        ```python
        # Using assert_that
        assert_that({"a": 1, "b": 2}).matches(has_exact_key_values({"a": 1, "b": 2})) # Passes
        assert_that({"a": 1, "b": 2}).matches(has_exact_key_values({"a": is_odd()})) # Fails

        # Using basic assert
        assert {"a": 1, "b": 2} == has_exact_key_values({"a": is_odd(), "b": is_even()}) # Passes
        ```
    """

    def __init__(self, key_values):
        self.key_values = {k: ensure_criteria(v) for k, v in key_values.items()}

    def _match(self, subject: Mapping):
        if len(subject.keys()) != len(self.key_values):
            return False

        return super()._match(subject)

    @property
    def description(self):
        return f"has exact key values: {{{joined_keyed_descriptions(self.key_values)}}}"


class contains_keys(MappingCriteria):
    """
    Determines if the given subject contains keys.

    Args:
        key: A list of keys to match against the subject.

    Example:
        ```python
        # Using assert_that
        assert_that({"a": 1, "b": 2}).matches(contains_keys("a", "b")) # Passes
        assert_that({"a": 1, "b": 2}).matches(contains_keys("c")) # Fails

        # Using basic assert
        assert {"a": 1, "b": 2} == contains_keys("a") # Passes
        ```
    """

    def __init__(self, *keys):
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
    """
    Determines if the given subject contains the exact keys.

    Args:
        key: A list of keys to match against the subject.

    Example:
        ```python
        # Using assert_that
        assert_that({"a": 1, "b": 2}).matches(contains_exact_keys("a", "b")) # Passes
        assert_that({"a": 1, "b": 2}).matches(contains_exact_keys("a")) # Fails

        # Using basic assert
        assert {"a": 1, "b": 2} == contains_exact_keys("a", "b") # Passes
        ```

    """

    def _match(self, subject: Mapping):
        if len(subject.keys()) != len(self.key_criteria):
            return False
        return super()._match(subject)

    @property
    def description(self) -> str:
        return (
            f"to have exact keys matching: [{joined_descriptions(self.key_criteria)}]"
        )
