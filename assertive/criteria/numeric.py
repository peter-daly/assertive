import math
from typing import Mapping, Union

from assertive.core import Criteria, ensure_criteria


class is_multiple_of(Criteria):
    """
    Match when the subject is a factor of ``value``.

    In other words, this criteria checks ``value % subject == 0``.
    This means ``is_multiple_of(12)`` matches ``1, 2, 3, 4, 6, 12``.

    Args:
        value: Number whose factors you want to match.

    Example:
        ```python
        assert 3 == is_multiple_of(12) # passes
        assert 5 == is_multiple_of(12) # fails
        ```
    """

    def __init__(self, value: int):
        self.value = value

    def _match(self, subject) -> bool:
        if subject == 0:
            return False
        return self.value % subject == 0


class is_even(Criteria):
    """
    Match even integers.

    Example:
        ```python
        assert 4 == is_even() # passes
        assert 5 == is_even() # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject % 2 == 0


class is_odd(Criteria):
    """
    Match odd integers.

    Example:
        ```python
        assert 3 == is_odd() # passes
        assert 4 == is_odd() # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject % 2 == 1


class as_absolute_matches(Criteria):
    """
    Match against ``abs(subject)`` using a nested criteria.

    This is useful for assertions where sign is irrelevant.

    Args:
        inner_criteria: Value or criteria to compare with ``abs(subject)``.

    Example:
        ```python
        assert -3 == as_absolute_matches(3)        # passes
        assert -7 == as_absolute_matches(is_odd()) # passes
        assert -4 == as_absolute_matches(2)        # fails
        ```
    """

    def __init__(self, inner_criteria: Union[int, float, complex, Criteria]):
        self.inner_criteria = ensure_criteria(inner_criteria)

    def _match(self, subject) -> bool:
        return self.inner_criteria.run_match(abs(subject))


class is_approximately_equal(Criteria):
    """
    Match numeric values within an epsilon of ``value``.

    Args:
        value: Target value for approximate comparison.

    Example:
        ```python
        assert 3.0000000001 == is_approximately_equal(3)                    # passes
        assert 3.01 == is_approximately_equal(3).with_epsilon(0.1)          # passes
        assert 3.01 == is_approximately_equal(3).with_epsilon(0.0001)       # fails
        ```
    """

    @classmethod
    def from_serialized(cls, serialized: Mapping) -> Criteria:
        value = serialized["value"]
        criteria = cls(value)

        criteria.with_epsilon(serialized["epsilon"])
        return criteria

    def __init__(self, value):
        self.value = value
        self.epsilon = 1e-10

    def with_epsilon(self, epsilon):
        self.epsilon = epsilon
        return self

    def _match(self, subject) -> bool:
        return abs(subject - self.value) < self.epsilon


class is_positive(Criteria):
    """
    Match numbers greater than zero.

    Example:
        ```python
        assert 1 == is_positive()  # passes
        assert 0 == is_positive()  # fails
        assert -1 == is_positive() # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject > 0


class is_non_negative(Criteria):
    """
    Match numbers greater than or equal to zero.

    Example:
        ```python
        assert 1 == is_non_negative()  # passes
        assert 0 == is_non_negative()  # passes
        assert -1 == is_non_negative() # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject >= 0


class is_negative(Criteria):
    """
    Match numbers less than zero.

    Example:
        ```python
        assert -1 == is_negative() # passes
        assert 0 == is_negative()  # fails
        assert 1 == is_negative()  # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject < 0


class is_non_positive(Criteria):
    """
    Match numbers less than or equal to zero.

    Example:
        ```python
        assert 1 == is_non_positive()  # fails
        assert 0 == is_non_positive()  # passes
        assert -1 == is_non_positive() # passes
        ```
    """

    def _match(self, subject) -> bool:
        return subject <= 0


class zero(Criteria):
    """
    Match exactly zero.

    Example:
        ```python
        assert 0 == zero()  # passes
        assert 1 == zero()  # fails
        assert -1 == zero() # fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject == 0


class approximately_zero(Criteria):
    """
    Match numbers that are close to zero within an epsilon tolerance.

    Example:
        ```python
        assert 1e-12 == approximately_zero()                         # passes
        assert 0.01 == approximately_zero().with_epsilon(0.1)       # passes
        assert 0.01 == approximately_zero().with_epsilon(0.0001)    # fails
        ```
    """

    @classmethod
    def from_serialized(cls, serialized: Mapping) -> Criteria:
        criteria = cls()
        criteria.with_epsilon(serialized["epsilon"])
        return criteria

    def __init__(self):
        self.epsilon = 1e-10

    def with_epsilon(self, epsilon):
        self.epsilon = epsilon
        return self

    def _match(self, subject) -> bool:
        return abs(subject) < self.epsilon


class is_a_perfect_square(Criteria):
    """
    Match positive integers that are perfect squares.

    Example:
        ```python
        assert 4 == is_a_perfect_square()  # passes
        assert 9 == is_a_perfect_square()  # passes
        assert 3 == is_a_perfect_square()  # fails
        ```
    """

    def _match(self, subject) -> bool:
        root = int(subject**0.5)
        return root * root == subject


class is_a_power_of(Criteria):
    """
    Match numbers that can be expressed as ``value ** n`` for integer ``n >= 0``.

    Args:
        value: Base to test powers against.

    Example:
        ```python
        assert 16 == is_a_power_of(2) # passes
        assert 9 == is_a_power_of(3)  # passes
        assert 10 == is_a_power_of(2) # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        if self.value == 1:
            return subject == 1
        power = 1
        while power < subject:
            power *= self.value
        return power == subject


class is_prime(Criteria):
    """
    Match prime integers.

    Values less than ``2`` are not considered prime.

    Example:
        ```python
        assert 2 == is_prime() # passes
        assert 5 == is_prime() # passes
        assert 9 == is_prime() # fails
        ```
    """

    def _match(self, subject) -> bool:
        if subject < 2:
            return False
        for i in range(2, int(subject**0.5) + 1):
            if subject % i == 0:
                return False
        return True


class is_coprime_with(Criteria):
    """
    Match numbers that are coprime with ``value``.

    Two numbers are coprime when their greatest common divisor is ``1``.

    Args:
        value: Number to compare the subject against.

    Example:
        ```python
        assert 10 == is_coprime_with(9) # passes
        assert 14 == is_coprime_with(15) # passes
        assert 9 == is_coprime_with(3)  # fails
        ```
    """

    def __init__(self, value):
        self.value = value

    def _match(self, subject) -> bool:
        return math.gcd(subject, self.value) == 1
