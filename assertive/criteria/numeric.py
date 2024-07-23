import math
from typing import Union

from assertive.core import Criteria, ensure_criteria


class is_multiple_of(Criteria):
    """
    Checks if the subject is a multiple of a number

    Example:
        ```python
        # Using assert_that
        assert_that(4).matches(is_multiple_of(2)) # Passes
        assert_that(6).matches(is_multiple_of(2)) # Passes
        assert_that(5).matches(is_multiple_of(2)) # Fails

        # Using basic assert
        assert 4 == is_multiple_of(2) # Passes
        assert 2 == is_multiple_of(2) # Passes
        assert 5 == is_multiple_of(2) # Fails
        ```
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
    """
    A criteria that checks if a number is even.

    Example:
        ```python
        # Using assert_that
        assert_that(4).matches(is_even()) # Passes
        assert_that(6).matches(is_even()) # Passes
        assert_that(5).matches(is_even()) # Fails

        # Using basic assert
        assert 4 == is_even() # Passes
        assert 2 == is_even() # Passes
        assert 5 == is_even() # Fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject % 2 == 0

    @property
    def description(self) -> str:
        return "is even"


class is_odd(Criteria):
    """
    A criteria class that checks if a number is odd.

    Example:
        ```python
        # Using assert_that
        assert_that(3).matches(is_odd()) # Passes
        assert_that(7).matches(is_odd()) # Passes
        assert_that(4).matches(is_odd()) # Fails

        # Using basic assert
        assert 1 == is_odd() # Passes
        assert 9 == is_odd() # Passes
        assert 8 == is_odd() # Fails
        ```
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

    Example:
        ```python
        # Using assert_that
        assert_that(-3).matches(as_absolute_matches(3)) # Passes
        assert_that(-7).matches(as_absolute_matches(is_odd())) # Passes
        assert_that(-4).matches(as_absolute_matches(2)) # Fails

        # Using basic assert
        assert -1 == as_absolute_matches(1) # Passes
        assert -9 == as_absolute_matches(is_odd()) # Passes
        assert -5 == as_absolute_matches(10) # Fails
        ```
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


class is_approximately_equal(Criteria):
    """
    A criteria class that checks if a number is approximately equal to a given value.

    Args:
        number (float): The value to compare against.

    Attributes:
        epsilon (float): The tolerance value for the approximation. Default is 1e-10.

    Methods:
        with_epsilon(epsilon): Sets the tolerance value for the approximation.

    Example:
        ```python
        # Using assert_that
        assert_that(3.0000000000000000000000000001).matches(is_approximately_equal(3)) # Passes
        assert_that(3.01).matches(is_approximately_equal(3).with_epsilon(0.1)) # Passes
        assert_that(3.01).matches(is_approximately_equal(3).with_epsilon(0.0001)) # Fails

        # Using basic assert
        assert 3.0000000000000000000000000001 == is_approximately_equal(3) # Passes
        assert 3.01 == is_approximately_equal(3).with_epsilon(0.1) # Passes
        assert 3.01 == is_approximately_equal(3).with_epsilon(0.0001) # Fails
        ```
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
    """
    Checks if a number is positive.

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(is_positive()) # Passes
        assert_that(0).matches(is_positive()) # Fails
        assert_that(-1).matches(is_positive()) # Fails

        # Using basic assert
        assert 1 == is_positive() # Passes
        assert 0 == is_positive() # Fails
        assert -1 == is_positive() # Fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject > 0

    @property
    def description(self) -> str:
        return "is positive"


class is_non_negative(Criteria):
    """
    Checks if a number is non-negative.

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(is_non_negative()) # Passes
        assert_that(0).matches(is_non_negative()) # Passes
        assert_that(-1).matches(is_non_negative()) # Fails

        # Using basic assert
        assert 1 == is_non_negative() # Passes
        assert 0 == is_non_negative() # Passes
        assert -1 == is_non_negative() # Fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject >= 0

    @property
    def description(self) -> str:
        return "is non-negative"


class is_negative(Criteria):
    """
    Checks if a number is negative.

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(is_negative()) # Fails
        assert_that(0).matches(is_negative()) # Fails
        assert_that(-1).matches(is_negative()) # Passes

        # Using basic assert
        assert 1 == is_negative() # Fails
        assert 0 == is_negative() # Fails
        assert -1 == is_negative() # Passes
        ```
    """

    def _match(self, subject) -> bool:
        return subject < 0

    @property
    def description(self) -> str:
        return "is negative"


class is_non_positive(Criteria):
    """
    Checks if the subject is non-positive.

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(is_non_positive()) # Fails
        assert_that(0).matches(is_non_positive()) # Passes
        assert_that(-1).matches(is_non_positive()) # Passes

        # Using basic assert
        assert 1 == is_non_positive() # Fails
        assert 0 == is_non_positive() # Passes
        assert -1 == is_non_positive() # Passes
        ```

    """

    def _match(self, subject) -> bool:
        return subject <= 0

    @property
    def description(self) -> str:
        return "is non-positive"


class zero(Criteria):
    """
    Checks if the subject is zero.

    Example:
        ```python
        # Using assert_that
        assert_that(1).matches(zero()) # Fails
        assert_that(0).matches(zero()) # Passes
        assert_that(-1).matches(zero()) # Fails

        # Using basic assert
        assert 1 == zero() # Fails
        assert 0 == zero() # Passes
        assert -1 == zero() # Fails
        ```
    """

    def _match(self, subject) -> bool:
        return subject == 0

    @property
    def description(self) -> str:
        return "is zero"


class approximately_zero(Criteria):
    """
    A criteria class that checks if a number is approximately zero.

    Attributes:
        epsilon (float): The tolerance value for determining if a number is approximately zero.

    Methods:
        with_epsilon(epsilon): Sets the tolerance value for determining if a number is approximately zero.

    Example:
        ```python
        # Using assert_that
        assert_that(0.0000000000000000000000000001).matches(approximately_zero()) # Passes
        assert_that(0.01).matches(approximately_zero().with_epsilon(0.1)) # Passes
        assert_that(0.01).matches(approximately_zero().with_epsilon(0.0001)) # Fails

        # Using basic assert
        assert 0.0000000000000000000000000001 == approximately_zero() # Passes
        assert 0.01 == approximately_zero().with_epsilon(0.1) # Passes
        assert 0.01 == approximately_zero().with_epsilon(0.0001) # Fails
        ```
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
    Checks if a number is a perfect square.

    Example:
        ```python
        # Using assert_that
        assert_that(4).matches(is_a_perfect_square()) # Passes
        assert_that(9).matches(is_a_perfect_square()) # Passes
        assert_that(3).matches(is_a_perfect_square()) # Fails

        # Using basic assert
        assert 16 == is_a_perfect_square() # Passes
        assert 1 == is_a_perfect_square() # Passes
        assert 5 == is_a_perfect_square() # Fails
        ```
    """

    def _match(self, subject) -> bool:
        root = int(subject**0.5)
        return root * root == subject

    @property
    def description(self) -> str:
        return "is a perfect square"


class is_a_power_of(Criteria):
    """
    Checks if a number is a power of a given base.

    Args:
        base: The base to check what the number is a power of

    Example:
        ```python
        # Using assert_that
        assert_that(4).matches(is_a_power_of(2)) # Passes
        assert_that(9).matches(is_a_power_of(3)) # Passes
        assert_that(16).matches(is_a_power_of(2)) # Passes
        assert_that(10).matches(is_a_power_of(2)) # Fails

        # Using basic assert
        assert 16 == is_a_power_of(4) # Passes
        assert 1 == is_a_power_of(1) # Passes
        assert 5 == is_a_power_of(2) # Fails
        ```
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


class is_prime(Criteria):
    """
    Checks if a number is prime.

    Example:
        ```python
        # Using assert_that
        assert_that(5).matches(is_prime()) # Passes
        assert_that(2).matches(is_prime()) # Passes
        assert_that(9).matches(is_prime()) # Fails

        # Using basic assert
        assert 3 == is_prime() # Passes
        assert 7 == is_prime() # Passes
        assert 4 == is_prime() # Fails
        ```
    """

    def _match(self, subject) -> bool:
        if subject < 2:
            return False
        for i in range(2, int(subject**0.5) + 1):
            if subject % i == 0:
                return False
        return True

    @property
    def description(self) -> str:
        return "is prime"


class is_coprime_with(Criteria):
    """
    Checks if a number is co-prime with a base.
    Two numbers are co-prime if their greatest common divisor is 1.

    Args:
        base: The base to check if the number is co-prime with.

    Example:
        ```python
        # Using assert_that
        assert_that(5).matches(is_coprime_with(2)) # Passes
        assert_that(10).matches(is_coprime_with(9)) # Passes
        assert_that(9).matches(is_coprime_with(3)) # Fails

        # Using basic assert
        assert 10 == is_coprime_with(7) # Passes
        assert 9 == is_coprime_with(8) # Passes
        assert 10 == is_coprime_with(5) # Fails
        ```
    """

    def __init__(self, base):
        self.base = base

    def _match(self, subject) -> bool:
        return math.gcd(subject, self.base) == 1

    @property
    def description(self) -> str:
        return f"is co-prime with {self.base}"
