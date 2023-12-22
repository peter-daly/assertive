from typing import Union
from fluent_assertions.assertions import Criteria, ensure_criteria


class is_multiple_of(Criteria):
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
    def _match(self, subject) -> bool:
        return subject % 2 == 0

    @property
    def description(self) -> str:
        return "is even"


class is_odd(Criteria):
    def _match(self, subject) -> bool:
        return subject % 2 == 1

    @property
    def description(self) -> str:
        return "is odd"


class as_absolute_matches(Criteria):
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
    def _match(self, subject) -> bool:
        return subject > 0

    @property
    def description(self) -> str:
        return "is positive"


class is_non_negative(Criteria):
    def _match(self, subject) -> bool:
        return subject >= 0

    @property
    def description(self) -> str:
        return "is non-negative"


class is_negative(Criteria):
    def _match(self, subject) -> bool:
        return subject < 0

    @property
    def description(self) -> str:
        return "is negative"


class is_non_positive(Criteria):
    def _match(self, subject) -> bool:
        return subject <= 0

    @property
    def description(self) -> str:
        return "is non-positive"


class zero(Criteria):
    def _match(self, subject) -> bool:
        return subject == 0

    @property
    def description(self) -> str:
        return "is zero"


class approximatly_zero(Criteria):
    def __init__(self):
        self.epsilon = 1e-10

    def with_epsilon(self, epsilon):
        self.epsilon = epsilon
        return self

    def _match(self, subject) -> bool:
        return abs(subject) < self.epsilon

    @property
    def description(self) -> str:
        return f"is approximatly zero with epsilon: {self.epsilon}"


class is_a_perfect_square(Criteria):
    def _match(self, subject) -> bool:
        root = int(subject**0.5)
        return root * root == subject

    @property
    def description(self) -> str:
        return "is a perfect square"


class is_a_power_of(Criteria):
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
