from typing import Union
from assertive.assertions import Criteria, ensure_criteria

from assertive.criteria.utils import (
    joined_descriptions,
)


class IterableCriteria(Criteria):
    def _before_run(self, subject):
        """
        Checks if the subject has a __len__ attribute.

        Args:
            subject: The object to be checked.

        Raises:
            TypeError: If the subject does not have a __len__ attribute.
        """
        if not hasattr(subject, "__len__"):
            raise TypeError(f"{subject} needs to be an Iterable")


class has_length(IterableCriteria):
    """
    Checks if the subject has a length that matches the count_criteria.
    """

    @property
    def description(self) -> str:
        """
        Returns a description of the criteria.

        Returns:
            str: The description of the criteria.
        """
        return f"has length matching: {self.count_criteria.description}"

    def __init__(self, count_criteria: Union[int, Criteria]):
        """
        Initializes the criteria with the count_criteria to match against the number of items.

        Args:
            count_criteria (Criteria): A criteria to match against the number of items in the list.
        """
        self.count_criteria = ensure_criteria(count_criteria)

    def _match(self, subject):
        """
        Checks if the subject has a length that matches the count_criteria.

        Args:
            subject: The object to be checked.

        Returns:
            bool: True if the length of the subject matches the count_criteria, False otherwise.
        """
        count = len(subject)
        return self.count_criteria._match(count)

    @property
    def description(self) -> str:
        """
        Returns a description of the criteria.

        Returns:
            str: The description of the criteria.
        """
        return f"has length matching: {self.count_criteria.description}"


class is_empty(IterableCriteria):
    """
    Checks if the subject is empty.
    """

    def _match(self, subject):
        """
        Checks if the subject is empty.

        Args:
            subject: The object to be checked.

        Returns:
            bool: True if the subject is empty, False otherwise.
        """
        count = len(subject)
        return count == 0

    @property
    def description(self) -> str:
        """
        Returns a description of the criteria.

        Returns:
            str: The description of the criteria.
        """
        return "is empty"


class contains(IterableCriteria):
    """
    Checks if the subject contains all the specified items or matches the criteria.

    Args:
        subject (iterable): The list or iterable to match against this criteria.

    Returns:
            bool: True if all specified items are present or criteria matched, False otherwise.
    """

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
        """
        Returns a description of the criteria.

        Returns:
            str: The description of the criteria.
        """
        return f"contains [{joined_descriptions(self.items)}]"


class contains_exactly(IterableCriteria):
    """
    Checks if the subject contains all the specified items or matches the criteria.

    Args:
        subject (iterable): The list or iterable to match against this criteria.

    Returns:
        bool: True if all specified items are present or criteria matched, False otherwise.
    """

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
        """
        Returns a description of the criteria.

        Returns:
            str: The description of the criteria.
        """
        return f"contains exactly [{joined_descriptions(self.items)}]"
