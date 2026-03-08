import re
from typing import Any

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import TimesMixin
import json


class StringCriteria(Criteria):
    """
    Base class for criteria that operate on string subjects.

    Subclasses inherit a pre-check that raises ``TypeError`` when the
    tested subject is not a string.
    """

    def _before_run(self, subject):
        if not isinstance(subject, str):
            raise TypeError(f"{subject} needs to be a string")


class regex(StringCriteria):
    """
    Match strings using a regular expression pattern.

    Matching uses ``re.match``, so the pattern is applied from the start
    of the string.

    Args:
        pattern: Regular expression pattern.

    Example:
        ```python
        assert "abc" == regex(r"abc")      # passes
        assert "abc" == regex(r"abc|def")  # passes
        assert "abc" == regex(r"def")      # fails
        ```
    """

    def __init__(self, pattern):
        self.pattern = pattern

    def _match(self, subject) -> bool:
        return bool(re.match(self.pattern, subject))


class starts_with(StringCriteria):
    """
    Match strings that start with ``prefix``.

    Args:
        prefix: Required prefix.

    Example:
        ```python
        assert "abc" == starts_with("a")   # passes
        assert "abc" == starts_with("ab")  # passes
        assert "abc" == starts_with("ba")  # fails
        ```
    """

    def __init__(self, prefix):
        self.prefix = prefix

    def _match(self, subject: str) -> bool:
        return subject.startswith(self.prefix)


class ends_with(StringCriteria):
    """
    Match strings that end with ``suffix``.

    Args:
        suffix: Required suffix.

    Example:
        ```python
        assert "abc" == ends_with("c")  # passes
        assert "abc" == ends_with("bc") # passes
        assert "abc" == ends_with("ac") # fails
        ```
    """

    def __init__(self, suffix):
        self.suffix = suffix

    def _match(self, subject: str) -> bool:
        return subject.endswith(self.suffix)


class contains_substring(TimesMixin, StringCriteria):
    """
    Match strings by counting occurrences of a substring.

    This criteria integrates with ``TimesMixin``. By default it expects
    at least one occurrence, and you can refine that with ``once()``,
    ``twice()``, ``times(n)``, or any numeric criteria.

    Args:
        substring: Substring to count within the subject.

    Example:
        ```python
        assert "banana" == contains_substring("an").twice() # passes
        assert "banana" == contains_substring("na").once()  # fails
        ```
    """

    def __init__(self, substring: str):
        super().__init__()
        self.substring = substring

    def _match(self, subject: str) -> bool:
        return self.times_criteria.run_match(subject.count(self.substring))


class ignore_case(StringCriteria):
    """
    Match strings case-insensitively against ``value``.

    Args:
        value: Expected string, ignoring case.

    Example:
        ```python
        assert "abc" == ignore_case("ABC") # passes
        assert "abc" == ignore_case("aBc") # passes
        assert "abc" == ignore_case("def") # fails
        ```
    """

    def __init__(self, value: str):
        self.value = value

    def _match(self, subject: str) -> bool:
        return subject.lower() == self.value.lower()


class as_json_matches(StringCriteria):
    """
    Parse the subject as JSON and match the parsed value with nested criteria.

    Args:
        inner_criteria: Value or criteria applied to ``json.loads(subject)``.

    Example:
        ```python
        assert '{"key": "value"}' == as_json_matches({"key": "value"}) # passes
        assert '{"n": 5}' == as_json_matches({"n": is_gt(0)})          # passes
        assert '{"key": "value"}' == as_json_matches({"key": "x"})     # fails
        ```
    """

    def __init__(self, inner_criteria: Criteria | Any):
        self.inner_criteria = ensure_criteria(inner_criteria)

    def _match(self, subject: str) -> bool:
        parsed_json = json.loads(subject)
        return self.inner_criteria.run_match(parsed_json)
