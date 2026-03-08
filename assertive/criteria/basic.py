from typing import Mapping, Union


from assertive.core import (
    Criteria,
    ensure_criteria,
    is_eq,  # noqa: F401
)


class is_neq(Criteria):
    """
    Match values that are not equal to ``value``.

    This is the inverse of ``is_eq`` and uses normal Python inequality
    semantics (``subject != value``), so custom ``__eq__`` implementations
    on your objects are respected.

    Args:
        value: Value that the subject must not be equal to.

    Example:
        ```python
        assert 2 == is_neq(1)        # passes
        assert "abc" == is_neq("x")  # passes
        assert 1 == is_neq(1)        # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return subject != self.value


class is_gt(Criteria):
    """
    Match values that are strictly greater than ``value``.

    Args:
        value: Lower bound (exclusive) for the subject.

    Example:
        ```python
        assert 10 == is_gt(9)  # passes
        assert 10 == is_gt(10) # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return subject > self.value


class is_gte(Criteria):
    """
    Match values greater than or equal to ``value``.

    Args:
        value: Lower bound (inclusive) for the subject.

    Example:
        ```python
        assert 2 == is_gte(2) # passes
        assert 3 == is_gte(2) # passes
        assert 1 == is_gte(2) # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return subject >= self.value


class is_lt(Criteria):
    """
    Match values that are strictly less than ``value``.

    Args:
        value: Upper bound (exclusive) for the subject.

    Example:
        ```python
        assert 1 == is_lt(2) # passes
        assert 2 == is_lt(2) # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return subject < self.value


class is_lte(Criteria):
    """
    Match values less than or equal to ``value``.

    Args:
        value: Upper bound (inclusive) for the subject.

    Example:
        ```python
        assert 1 == is_lte(2) # passes
        assert 1 == is_lte(1) # passes
        assert 2 == is_lte(1) # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return subject <= self.value


class is_between(Criteria):
    """
    Match values that fall between ``lower`` and ``upper``.

    By default the range is inclusive on both ends. Call ``exclusive()``
    to require strict inequality at both ends.

    Args:
        lower: Lower bound value.
        upper: Upper bound value.

    Example:
        ```python
        assert 2 == is_between(1, 3)              # passes
        assert 2 == is_between(1, 2).inclusive()  # passes
        assert 2 == is_between(1, 2).exclusive()  # fails
        ```
    """

    @classmethod
    def from_serialized(cls, serialized: Mapping) -> Criteria:
        criteria = cls(
            serialized["lower"],
            serialized["upper"],
        )

        if serialized.get("is_inclusive", True):
            criteria.inclusive()
        else:
            criteria.exclusive()

        return criteria

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
    Match only when the subject is the exact same object as ``value``.

    This is an identity check (``is``), not an equality check (``==``).

    Args:
        value: Object instance the subject must be identical to.

    Example:
        ```python
        class MyClass:
            pass

        x = MyClass()
        y = MyClass()
        z = x

        assert x == is_same_instance_as(z) # passes
        assert x == is_same_instance_as(y) # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return subject is self.value


class as_string_matches(Criteria):
    """
    Convert the subject to ``str`` and evaluate another criteria against it.

    Useful when the canonical form you care about is textual, for example
    matching IDs, enum values, or object ``__str__`` output.

    Args:
        criteria: String value or criteria to match against ``str(subject)``.

    Example:
        ```python
        assert 1 == as_string_matches("1")              # passes
        assert 42 == as_string_matches(is_eq("42"))     # passes
        assert 42 == as_string_matches("0042")          # fails
        ```
    """

    def __init__(self, criteria: Union[Criteria, str]):
        self.criteria = ensure_criteria(criteria)

    def _match(self, subject) -> bool:
        return self.criteria.run_match(str(subject))


class is_none(Criteria):
    """
    Match only when the subject is ``None``.

    Example:
        ```python
        x = None
        y = 4

        assert x == is_none() # passes
        assert y == is_none() # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject is None


class is_not_none(Criteria):
    """
    Match values that are not ``None``.

    Example:
        ```python
        x = None
        y = 4

        assert x == is_not_none() # fails
        assert y == is_not_none() # passes
        ```
    """

    def _match(self, subject) -> bool:
        return subject is not None
