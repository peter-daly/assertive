from typing import Union
from assertive.assertions import Criteria, ensure_criteria


class is_multiple_of(Criteria):
    """
    Checks if the subject is a multiple of a number
    """

    def __init__(self, number: int):
        self.number = number

    def _match(self, subject) -> bool:
        if subject == 0:
            return False
        return self.number % subject == 0

    @property
    def description(self) -> str:
        return f"is multiple of {self.number}"


class is_even(Criteria):
    """A criteria that checks if a number is even."""

    def _match(self, subject) -> bool:
        return subject % 2 == 0

    @property
    def description(self) -> str:
        return "is even"


class is_odd(Criteria):
    """
    A criteria class that checks if a number is odd.
    """

    def _match(self, subject) -> bool:
        return subject % 2 == 1

    @property
    def description(self) -> str:
        return "is odd"


class as_absolute_matches(Criteria):
    """
    A criteria that checks if the absolute value of a subject matches the inner criteria.

    Args:
        inner_criteria (Union[int, float, complex, Criteria]): The inner criteria to match against.

    Attributes:
        criteria (Criteria): The inner criteria.

    """

    def __init__(self, inner_criteria: Union[int, float, complex, Criteria]):
        self.criteria = ensure_criteria(inner_criteria)

    def _match(self, subject) -> bool:
        return self.criteria.run_match(abs(subject))

    @property
    def description(self) -> str:
        return self.criteria.description

    def failure_message(self, subject) -> str:
        return f"Expected abs({subject}) to match: {self.description}"

    def negated_failure_message(self, subject) -> str:
        return f"Expected abs({subject}) to not match: {self.description}"


class is_approximatly_equal(Criteria):
    """
    A criteria class that checks if a number is approximately equal to a given value.

    Args:
        number (float): The value to compare against.

    Attributes:
        epsilon (float): The tolerance value for the approximation. Default is 1e-10.

    Methods:
        with_epsilon(epsilon): Sets the tolerance value for the approximation.
        _match(subject): Checks if the subject is approximately equal to the given number.
        description: Returns a string describing the criteria.

    """

    def __init__(self, number):
        self.number = number
        self.epsilon = 1e-10

    def with_epsilon(self, epsilon):
        self.epsilon = epsilon
        return self

    def _match(self, subject) -> bool:
        return abs(subject - self.number) < self.epsilon

    @property
    def description(self) -> str:
        return f"~= {self.number}; with epsilon {self.epsilon}"


class is_positive(Criteria):
    """A criteria that checks if a number is positive."""

    def _match(self, subject) -> bool:
        return subject > 0

    @property
    def description(self) -> str:
        return "is positive"


class is_non_negative(Criteria):
    """
    A criteria class that checks if a number is non-negative.
    """

    def _match(self, subject) -> bool:
        return subject >= 0

    @property
    def description(self) -> str:
        return "is non-negative"


class is_negative(Criteria):
    """
    A criteria class that checks if a number is negative.
    """

    def _match(self, subject) -> bool:
        return subject < 0

    @property
    def description(self) -> str:
        return "is negative"


class is_non_positive(Criteria):
    """
    A criteria class that checks if the subject is non-positive.

    Attributes:
        None

    Methods:
        _match(subject) -> bool: Checks if the subject is non-positive.
        description() -> str: Returns the description of the criteria.

    Usage:
        criterion = is_non_positive()
        result = criterion._match(subject)
        desc = criterion.description()
    """

    def _match(self, subject) -> bool:
        return subject <= 0

    @property
    def description(self) -> str:
        return "is non-positive"


class zero(Criteria):
    """A criteria that checks if the subject is zero."""

    def _match(self, subject) -> bool:
        return subject == 0

    @property
    def description(self) -> str:
        return "is zero"


class approximatly_zero(Criteria):
    """
    A criteria class that checks if a number is approximately zero.

    Attributes:
        epsilon (float): The tolerance value for determining if a number is approximately zero.

    Methods:
        with_epsilon(epsilon): Sets the tolerance value for determining if a number is approximately zero.
        _match(subject) -> bool: Checks if the given subject is approximately zero.
        description() -> str: Returns a description of the criteria.
    """

    def __init__(self):
        self.epsilon = 1e-10

    def with_epsilon(self, epsilon):
        self.epsilon = epsilon
        return self

    def _match(self, subject) -> bool:
        return abs(subject) < self.epsilon

    @property
    def description(self) -> str:
        return f"is approximately zero with epsilon: {self.epsilon}"


class is_a_perfect_square(Criteria):
    """
    A criteria class that checks if a number is a perfect square.
    """

    def _match(self, subject) -> bool:
        root = int(subject**0.5)
        return root * root == subject

    @property
    def description(self) -> str:
        return "is a perfect square"


class is_a_power_of(Criteria):
    """
    Represents a criteria that checks if a number is a power of a given base.
    """

    def __init__(self, base):
        self.base = base

    def _match(self, subject) -> bool:
        if self.base == 1:
            return subject == 1
        power = 1
        while power < subject:
            power *= self.base
        return power == subject

    @property
    def description(self) -> str:
        return f"is a power of {self.base}"


class is_a_factorial_of(Criteria):
    """
    A criteria class that checks if a number is a factorial of a given factor.
    """

    def __init__(self, factor):
        self.factor = factor

    def _match(self, subject) -> bool:
        if subject == 0:
            return self.factor == 1
        product = 1

        for i in range(1, self.factor + 1):
            product *= i
            if product == subject:
                return True
        return False

    @property
    def description(self) -> str:
        return f"is a factorial of {self.factor}"
