from typing import Union

from assertive.core import Criteria, ensure_criteria


class IterableCriteria(Criteria):
    def _before_run(self, subject):
        if not hasattr(subject, "__len__"):
            raise TypeError(f"{subject} needs to be an Iterable")


class has_length(IterableCriteria):
    """
    Checks if the subject has a length that matches the count_criteria.

    Args:
        count_criteria: The criteria to match the length against, can be a number or a criteria object

    Example:
        ```python

        assert [1, 2, 3] == has_length(3) # Passes
        assert "hello" == has_length(5) # Passes
        assert [1, 2, 3] == has_length(is_greater_than(2)) # Passes


        assert [1, 2, 3] == has_length(3) # Passes
        ```
    """

    def __init__(self, count_criteria: Union[int, Criteria]):
        self.count_criteria = ensure_criteria(count_criteria)

    def _match(self, subject):
        count = len(subject)
        return self.count_criteria.run_match(count)


class is_empty(IterableCriteria):
    """
    Checks if the subject is empty.

    Example:
        ```python

        assert [] == is_empty() # Passes

        assert [] == is_empty() # Passes
        ```
    """

    def _match(self, subject):
        count = len(subject)
        return count == 0


class contains(IterableCriteria):
    """
    Checks if the subject contains all the specified items or matches the criteria.

    Args:
        *items: The items to check if the subject contains or matches the criteria

    Example:
        ```python

        assert [1, 2, 3] == contains(1, 2) # Passes
        assert [1, 2, 3] == contains(1, 2, 3) # Passes
        assert [1, 2, 3] == contains(1, 2, is_greater_than(1)) # Passes

        assert [1, 2, 3] == contains(1, 2) # Passes
        ```

    """

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
    Checks if the subject contains all the specified items or matches the criteria.

    Args:
        *items: The items to check if the subject contains or matches the criteria

    Example:
        ```python

        assert [1, 2, 3] == contains_exactly(1, 2) # Fails
        assert [1, 2, 3] == contains_exactly(1, 2, 3) # Passes
        assert [1, 2, 3] == contains_exactly(1, 2, is_greater_than(1)) # Passes

        assert [1, 2, 3] == contains_exactly(1, 2, 3) # Passes
        ```

    """

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
