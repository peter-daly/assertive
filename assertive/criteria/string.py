import re
from typing import Any

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import TimesMixin
import json


class StringCriteria(Criteria):
    def _before_run(self, subject):
        if not isinstance(subject, str):
            raise TypeError(f"{subject} needs to be a string")


class regex(StringCriteria):
    """
    Represents a regular expression pattern matching criteria for strings.

    Args:
        pattern (str): The regular expression pattern to match.

    Example:
        ```python

        assert "abc" == regex(r"abc") # Passes
        assert "abc" == regex(r"abc|def") # Passes
        assert "abc" == regex(r"def") # Fails

        ```
    """

    def __init__(self, pattern):
        self.pattern = pattern

    def _match(self, subject) -> bool:
        return bool(re.match(self.pattern, subject))


class starts_with(StringCriteria):
    """
    A criteria class that checks if a string starts with a given prefix.

    Args:
        prefix (str): The prefix to check for.

    Example:
        ```python

        assert "abc" == starts_with("a") # Passes
        assert "abc" == starts_with("ab") # Passes
        assert "abc" == starts_with("abb") # Fails


        assert "abc" == starts_with("a") # Passes
        assert "abc" == starts_with("ab") # Passes
        assert "abc" == starts_with("ba") # Fails
        ```
    """

    def __init__(self, prefix):
        self.prefix = prefix

    def _match(self, subject: str) -> bool:
        return subject.startswith(self.prefix)


class ends_with(StringCriteria):
    """
    A criteria class that checks if a string ends with a specified suffix.

    Args:
        suffix (str): The suffix to check.

    Example:
        ```python
        assert "abc" == ends_with("c") # Passes
        assert "abc" == ends_with("bc") # Passes
        assert "abc" == ends_with("ac") # Fails
        ```
    """

    def __init__(self, suffix):
        self.suffix = suffix

    def _match(self, subject: str) -> bool:
        return subject.endswith(self.suffix)


class contains_substring(TimesMixin, StringCriteria):
    """
    A criteria that checks if a string contains a specific substring.

    Args:
        substring (str): The substring to search for.

    Example:
        ```python
        assert "hello" == contains_substring("ell") # Passes
        assert "hello" == contains_substring("hell") # Passes
        assert "hello" == contains_substring("goodbye") # Fails
        ```
    """

    def __init__(self, substring: str):
        super().__init__()
        self.substring = substring

    def _match(self, subject: str) -> bool:
        return self.times_criteria.run_match(subject.count(self.substring))


class as_json_matches(StringCriteria):
    """
    Converts the subject to a JSON object and then checks the criteria.
    Args:
        criteria: The criteria to compare the JSON object against.
    Example:
        ```python
        assert '{"key": "value"}' == as_json_matches({"key": "value"}) # Passes
        assert '{"key": "value"}' == as_json_matches({"key": "other_value"}) # Fails
        ```
    """

    def __init__(self, inner_criteria: Criteria | Any):
        self.inner_criteria = ensure_criteria(inner_criteria)

    def _match(self, subject: str) -> bool:
        parsed_json = json.loads(subject)
        return self.inner_criteria.run_match(parsed_json)
