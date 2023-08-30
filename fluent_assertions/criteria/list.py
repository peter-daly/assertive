from typing import Union
from fluent_assertions.assertions import Criteria, ensure_criteria

from fluent_assertions.criteria.utils import (
    joined_descriptions,
)


class IterableCriteria(Criteria):
    def _before_run(self, subject):
        if not hasattr(subject, "__len__"):
            raise TypeError(f"{subject} needs to be an Iterable")


class has_length(IterableCriteria):
    def __init__(self, count_criteria: Union[int, Criteria]):
        """
        Initializes the criteria with the count_criteria to match against the number of items.

        Args:
            count_criteria (Criteria): A criteria to match against the number of items in the list.
        """
        self.count_criteria = ensure_criteria(count_criteria)

    def _match(self, subject):
        count = len(subject)
        return self.count_criteria._match(count)

    @property
    def description(self) -> str:
        return f"has length matching: {self.count_criteria.description}"


class is_empty(IterableCriteria):
    def _match(self, subject):
        count = len(subject)
        return count == 0

    @property
    def description(self) -> str:
        return "is empty"


class contains(IterableCriteria):
    def __init__(self, *items):
        """
        Initializes the criteria with the items (or criteria) to be checked for presence.

        Args:
            items: A tuple of items or criteria to be checked for their presence in the iterable.
        """
        self.items = [ensure_criteria(item) for item in items]

    def _match(self, subject):
        """
        Checks if the subject contains all the specified items or matches the criteria.

        Args:
            subject (iterable): The list or iterable to match against this criteria.

        Returns:
            bool: True if all specified items are present or criteria matched, False otherwise.
        """

        for item in self.items:
            matches = [item._match(s) for s in subject]
            if not any(matches):
                return False
        return True

    @property
    def description(self) -> str:
        return f"contains [{joined_descriptions(self.items)}]"


class contains_exactly(IterableCriteria):
    def __init__(self, *items):
        """
        Initializes the criteria with the items (or criteria) to be checked for presence.

        Args:
            items: A tuple of items or criteria to be checked for their presence in the iterable.
        """
        self.items = [ensure_criteria(item) for item in items]

    def _match(self, subject):
        """
        Checks if the subject contains all the specified items or matches the criteria.

        Args:
            subject (iterable): The list or iterable to match against this criteria.

        Returns:
            bool: True if all specified items are present or criteria matched, False otherwise.
        """

        try:
            return all(
                item._match(sub_item)
                for item, sub_item in zip(self.items, subject, strict=True)
            )
        except ValueError:
            return False

    @property
    def description(self) -> str:
        return f"contains exactly [{joined_descriptions(self.items)}]"
