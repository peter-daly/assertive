from collections.abc import Mapping
from typing import Any

from assertive.core import Criteria, ensure_criteria


class MappingCriteria(Criteria):
    """
    Base class for criteria that operate on mapping-like subjects.

    Subclasses require the subject to implement ``collections.abc.Mapping``.
    """

    def _before_run(self, subject):
        if not isinstance(subject, Mapping):
            raise TypeError(f"{subject} needs to be mapping")


class has_key_values(MappingCriteria):
    """
    Match mappings that contain at least the provided keys and value rules.

    Extra keys on the subject are allowed. Each expected value can be either
    a plain value or another criteria object.

    Args:
        key_values: Mapping of expected keys to expected value criteria.

    Example:
        ```python
        assert {"a": 1, "b": 2} == has_key_values({"a": 1})       # passes
        assert {"a": 1, "b": 2} == has_key_values({"a": is_odd()}) # passes
        assert {"a": 1} == has_key_values({"b": 1})               # fails
        ```
    """

    def __init__(self, key_values: Mapping):
        self.key_values = {k: ensure_criteria(v) for k, v in key_values.items()}

    def _match(self, subject: Mapping):
        for name, criteria in self.key_values.items():
            if name not in subject:
                return False

            value = subject[name]
            if not criteria.run_match(value):
                return False

        return True


class has_key_and_value(has_key_values):
    """
    Convenience wrapper for checking one key/value pair in a mapping.

    Args:
        key: Expected key.
        value: Expected value or criteria for that key.

    Example:
        ```python
        assert {"a": 1, "b": 2} == has_key_and_value("a", 1)        # passes
        assert {"a": 1, "b": 2} == has_key_and_value("a", is_odd()) # passes
        assert {"a": 2} == has_key_and_value("a", is_odd())         # fails
        ```
    """

    def __init__(self, key: Any, value: Any):
        super().__init__({key: value})


class has_exact_key_values(has_key_values):
    """
    Match mappings whose keys and values exactly match ``key_values``.

    Unlike ``has_key_values``, this criteria fails when the subject has
    missing or additional keys.

    Args:
        key_values: Complete set of keys and value criteria expected.

    Example:
        ```python
        assert {"a": 1, "b": 2} == has_exact_key_values({"a": 1, "b": 2}) # passes
        assert {"a": 1, "b": 2} == has_exact_key_values({"a": 1})         # fails
        assert {"a": 1, "b": 2} == has_exact_key_values({"a": is_odd(), "b": is_even()}) # passes
        ```
    """

    def __init__(self, key_values):
        self.key_values = {k: ensure_criteria(v) for k, v in key_values.items()}

    def _match(self, subject: Mapping):
        if len(subject.keys()) != len(self.key_values):
            return False

        return super()._match(subject)


class contains_keys(MappingCriteria):
    """
    Match mappings that include all requested keys.

    Keys themselves can be values or criteria objects.

    Args:
        *keys: Required keys or key criteria.

    Example:
        ```python
        assert {"a": 1, "b": 2} == contains_keys("a", "b")    # passes
        assert {"a": 1, "b": 2} == contains_keys(starts_with("a")) # passes
        assert {"a": 1, "b": 2} == contains_keys("c")         # fails
        ```
    """

    def __init__(self, *keys):
        self.key_criteria = [(ensure_criteria(k)) for k in keys]

    def _match(self, subject: Mapping):
        keys = subject.keys()
        for criteria in self.key_criteria:
            if not any([criteria.run_match(key) for key in keys]):
                return False
        return True


class contains_exact_keys(contains_keys):
    """
    Match mappings whose key set exactly matches the requested keys.

    Args:
        *keys: Expected full key set.

    Example:
        ```python
        assert {"a": 1, "b": 2} == contains_exact_keys("a", "b") # passes
        assert {"a": 1, "b": 2} == contains_exact_keys("a")      # fails
        assert {"a": 1, "b": 2} == contains_exact_keys("a", "b", "c") # fails
        ```
    """

    def _match(self, subject: Mapping):
        if len(subject.keys()) != len(self.key_criteria):
            return False
        return super()._match(subject)
