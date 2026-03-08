from typing import Union

from assertive.core import Criteria, ensure_criteria


class IterableCriteria(Criteria):
    """
    Base class for criteria that operate on iterable-like subjects.

    Subclasses require the subject to expose ``__len__``. A ``TypeError``
    is raised when that contract is not met.
    """

    def _before_run(self, subject):
        if not hasattr(subject, "__len__"):
            raise TypeError(f"{subject} needs to be an Iterable")


class has_length(IterableCriteria):
    """
    Match subjects whose length satisfies ``value``.

    ``value`` can be a concrete integer or another criteria for advanced
    length checks.

    Args:
        value: Expected length or criteria evaluated against ``len(subject)``.

    Example:
        ```python
        assert [1, 2, 3] == has_length(3)      # passes
        assert "hello" == has_length(5)        # passes
        assert [1, 2, 3] == has_length(is_gt(2)) # passes
        ```
    """

    def __init__(self, value: Union[int, Criteria]):
        self.value = ensure_criteria(value)

    def _match(self, subject):
        count = len(subject)
        return self.value.run_match(count)


class is_empty(IterableCriteria):
    """
    Match empty iterables (length ``0``).

    Example:
        ```python
        assert [] == is_empty()       # passes
        assert "" == is_empty()       # passes
        assert [1] == is_empty()      # fails
        ```
    """

    def _match(self, subject):
        count = len(subject)
        return count == 0


class contains(IterableCriteria):
    """
    Match when each expected item is found somewhere in the subject.

    Items are treated as criteria. This means you can mix exact values
    and nested criteria objects.

    Args:
        *items: Expected values/criteria that must each match at least one element.

    Example:
        ```python
        assert [1, 2, 3] == contains(1, 2)          # passes
        assert [1, 2, 3] == contains(is_gt(2), 1)   # passes
        assert [1, 2, 3] == contains(4)             # fails
        ```
    """

    @classmethod
    def from_serialized(cls, serialized):
        items = serialized["items"]
        return cls(*items)

    def __init__(self, *items):
        self.items = [ensure_criteria(item) for item in items]

    def _match(self, subject):
        for item in self.items:
            matches = [item.run_match(s) for s in subject]
            if not any(matches):
                return False
        return True


class contains_exactly(IterableCriteria):
    """
    Match when the subject has exactly the expected items in the same order.

    Each expected entry can be either a plain value or a criteria object.

    Args:
        *items: Ordered expected values/criteria.

    Example:
        ```python
        assert [1, 2, 3] == contains_exactly(1, 2, 3)        # passes
        assert [1, 2, 3] == contains_exactly(1, 2, is_gt(2)) # passes
        assert [1, 2, 3] == contains_exactly(1, 3, 2)        # fails
        ```
    """

    @classmethod
    def from_serialized(cls, serialized):
        items = serialized["items"]
        return cls(*items)

    def __init__(self, *items):
        self.items = [ensure_criteria(item) for item in items]

    def _match(self, subject):
        try:
            return all(
                item.run_match(sub_item)
                for item, sub_item in zip(self.items, subject, strict=True)
            )
        except ValueError:
            return False
