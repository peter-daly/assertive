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

        assert 2 == is_eq(1) # Fails
        assert 1 == is_eq(1) # Passes

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

        assert 2 == is_gt(1) # Passes
        assert 2 == is_gt(2) # Fails

        ```

    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject > self.expected


class is_gte(Criteria):
    """
    Checks subject is greater or equal than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python

        assert 2 == is_gte(2) # Passes
        assert 2 == is_gte(1) # Passes
        assert 1 == is_gte(2) # Fails
        ```
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject >= self.expected


class is_lt(Criteria):
    """
    Checks subject is less than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python

        assert 1 == is_lt(2)) # Passes
        assert 2 == is_lt(2) # Fails
        ```

    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject < self.expected


class is_lte(Criteria):
    """
    Checks subject is less or equal than expected value

    Args:
        expected: The expected value to compare against

    Example:
        ```python

        assert 1 == is_lte(2) # Passes
        assert 1 == is_lte(1) # Passes
        assert 2 == is_lte(1) # Fails
        ```

    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject <= self.expected


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

        assert 2 == is_between(1, 3) # Passes
        assert 2 == is_between(1, 2) # Passes
        assert 2 == is_between(1, 2).inclusive() # Passes
        assert 2 == is_between(1, 2).exclusive() # Fails

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

        assert x == is_same_instance_as(z) # Passes
        assert x == is_same_instance_as(y) # Fails

        ```
    """

    def __init__(self, expected):
        self.expected = expected

    def _match(self, subject) -> bool:
        return subject is self.expected


class as_string_matches(Criteria):
    """
    Converts the subject to a string using str() and then checks the criteria

    Args:
        criteria: The criteria to compare the str(subject) against

    Example:
        ```python

        assert 1 == as_string_matches("1") # Passes

        ```
    """

    def __init__(self, criteria: Union[Criteria, str]):
        self.criteria = ensure_criteria(criteria)

    def _match(self, subject) -> bool:
        return self.criteria.run_match(str(subject))


class is_none(Criteria):
    """
    Checks the subject is None

    Example:
        ```python
        x = None
        y = 4


        assert x == is_none() # Passes
        assert y == is_none() # Fails

        ```
    """

    def _match(self, subject) -> bool:
        return subject is None


class is_not_none(Criteria):
    """
    Checks the subject is not None

    Example:
        ```python
        x = None
        y = 4

        assert x == is_not_none() # Fails
        assert y == is_not_none() # Passes

        ```
    """

    def _match(self, subject) -> bool:
        return subject is not None
