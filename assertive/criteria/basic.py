from typing import Union

from assertive.core import (
    Criteria,
    _default_ensured_criteria,
    ensure_criteria,
)


class is_eq(_default_ensured_criteria):
    """
    Checks subject is equal to the expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python
        # Using assert_that
        assert_that(2).matches(is_eq(1)) # Fails
        assert_that(1).matches(is_eq(1)) # Passes
        assert_that(1).matches(1) # Sames as using is_eq
        ```
    """

    pass


class is_gt(Criteria):
    """
    Checks subject is greater than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python
        # Using assert_that
        assert_that(2).matches(is_gt(1))

        # Using basic assert
        assert 2 == is_gt(1)
        ```

    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject > self.expected

    @property
    def description(self) -> str:
        return f"> {self.expected}"


class is_gte(Criteria):
    """
    Checks subject is greater or equal than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python
        # Using assert_that
        assert_that(2).matches(is_gte(2))

        # Using basic assert
        assert 2 == is_gte(1)
        ```
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject >= self.expected

    @property
    def description(self) -> str:
        return f">= {self.expected}"


class is_lt(Criteria):
    """
    Checks subject is less than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(is_lt(2))

        # Using basic assert
        assert 0 == is_lt(1)
        ```

    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject < self.expected

    @property
    def description(self) -> str:
        return f"< {self.expected}"


class is_lte(Criteria):
    """
    Checks subject is less or equal than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(is_lte(2))

        # Using basic assert
        assert 1 == is_lte(1)
        ```

    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject <= self.expected

    @property
    def description(self) -> str:
        return f"<= {self.expected}"


class is_between(Criteria):
    """
    Checks subject is between an upper bound or lower bound.

    Args:
        lower: The lower bound
        upper: The upper bound

    Attributes:
        is_inclusive: If the upper and lower bounds are included in the accepted range

    Example:
        ```python
        # Using assert_that
        assert_that(2).matches(is_between(1, 3)) # Passes
        assert_that(2).matches(is_between(1, 2)) # Passes
        assert_that(2).matches(is_between(1, 2).inclusive()) # Passes
        assert_that(2).matches(is_between(1, 2).exclusive()) # Fails

        # Using basic assert
        assert 5 == is_between(1, 10)
        ```
    """

    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.is_inclusive = True

    def inclusive(self):
        """
        Upper and lower are included in the accepted range
        """
        self.is_inclusive = True
        return self

    def exclusive(self):
        """
        Upper and lower are excluded from the accepted range
        """
        self.is_inclusive = False
        return self

    def _match(self, subject) -> bool:
        if self.is_inclusive:
            return subject >= self.lower and subject <= self.upper
        return subject > self.lower and subject < self.upper

    @property
    def description(self) -> str:
        inclusivness = "inclusive" if self.is_inclusive else "exclusive"
        return f"is between {self.lower} and {self.upper}; {inclusivness}"


class is_same_instance_as(Criteria):
    """
    Checks that the subject is the same instance as the expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python
        class MyClass:
            pass

        x = MyClass()
        y = MyClass()
        z = x

        # Using assert_that

        assert_that(x).matches(is_same_instance_as(z)) # Passes
        assert_that(x).matches(is_same_instance_as(y)) # Fails

        # Using basic assert
        assert x == is_same_instance_as(z)
        ```
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject is self.expected

    @property
    def description(self) -> str:
        return f"is same instance as {self.expected}"


class as_string_matches(Criteria):
    """
    Converts the subject to a string using str() and then checks the criteria

    Args:
        criteria: The criteria to compare the str(subject) against

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(as_string_matches("1")) # Passes

        # Using basic assert
        assert 1 == as_string_matches("1")
        ```
    """

    def __init__(self, criteria: Union[Criteria, str]):
        self.criteria = ensure_criteria(criteria)

    def _match(self, subject) -> bool:
        return self.criteria._match(str(subject))

    @property
    def description(self) -> str:
        return self.criteria.description

    def failure_message(self, subject) -> str:
        return f"Expected str({subject}) to match: {self.description}"

    def negated_failure_message(self, subject) -> str:
        return f"Expected str({subject}) to not match: {self.description}"


class is_none(Criteria):
    """
    Checks the subject is None

    Example:
        ```python
        x = None
        y = 4

        # Using assert_that
        assert_that(x).matches(is_none()) # Passes
        assert_that(y).matches(is_none()) # Fails

        # Using basic assert
        assert x == is_none()
        ```
    """

    def _match(self, subject) -> bool:
        return subject is None

    @property
    def description(self) -> str:
        return "is None"


class is_not_none(Criteria):
    """
    Checks the subject is not None

    Example:
        ```python
        x = None
        y = 4

        # Using assert_that
        assert_that(x).matches(is_not_none()) # Fails
        assert_that(y).matches(is_not_none()) # Passes

        # Using basic assert
        assert y == is_not_none()
        ```
    """

    def _match(self, subject) -> bool:
        return subject is not None

    @property
    def description(self) -> str:
        return "is not None"
