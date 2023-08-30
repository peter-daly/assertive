from fluent_assertions.assertions import assert_that
from fluent_assertions.criteria.numeric import (
    as_absolute_matches,
    is_a_perfect_square,
    is_a_power_of,
    is_multiple_of,
    is_even,
    is_odd,
    is_positive,
    is_negative,
    is_non_positive,
    is_non_negative,
    is_approximatly_equal,
    zero,
    approximatly_zero,
    is_a_factorial_of,
)
from fluent_assertions.criteria.exception import raises_exception

# is_multiple_of
def test_is_multiple_of_matches_pass():
    assert_that(2).matches(is_multiple_of(4))
    assert_that(3).matches(is_multiple_of(3))
    assert_that(3).matches(is_multiple_of(6))


def test_is_multiple_of_does_not_match_pass():
    assert_that(0).does_not_match(is_multiple_of(5))
    assert_that(5).does_not_match(is_multiple_of(6))


def test_is_equal_to_matches_fail():
    with raises_exception(AssertionError, "Expected 0 to match: is multiple of 5"):
        assert_that(0).matches(is_multiple_of(5))


def test_is_equal_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 5 to not match: is multiple of 10"):
        assert_that(5).does_not_match(is_multiple_of(10))


# is_even
def test_is_even_matches_pass():
    assert_that(2).matches(is_even())
    assert_that(100).matches(is_even())
    assert_that(0).matches(is_even())
    assert_that(-2).matches(is_even())


def test_is_even_does_not_match_pass():
    assert_that(1).does_not_match(is_even())
    assert_that(-1).does_not_match(is_even())
    assert_that(101).does_not_match(is_even())


def test_is_even_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: is even"):
        assert_that(1).matches(is_even())


def test_is_even_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 50 to not match: is even"):
        assert_that(50).does_not_match(is_even())


# is_odd
def test_is_odd_matches_pass():
    assert_that(21).matches(is_odd())
    assert_that(101).matches(is_odd())
    assert_that(1).matches(is_odd())
    assert_that(-1).matches(is_odd())


def test_is_odd_does_not_match_pass():
    assert_that(12).does_not_match(is_odd())
    assert_that(0).does_not_match(is_odd())
    assert_that(100).does_not_match(is_odd())


def test_is_odd_matches_fail():
    with raises_exception(AssertionError, "Expected 12 to match: is odd"):
        assert_that(12).matches(is_odd())


def test_is_odd_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 51 to not match: is odd"):
        assert_that(51).does_not_match(is_odd())


# is_approximatly_equal
def test_is_approximatly_equal_matches_pass():
    assert_that(1).matches(is_approximatly_equal(1.00000000000000000000000001))
    assert_that(1).matches(is_approximatly_equal(1.01).with_epsilon(0.1))
    assert_that(1).matches(is_approximatly_equal(1.01).with_epsilon(1e-1))


def test_is_approximatly_equal_does_not_match_pass():
    assert_that(1).does_not_match(is_approximatly_equal(1.1))
    assert_that(1).does_not_match(is_approximatly_equal(1.01).with_epsilon(0.001))
    assert_that(1).does_not_match(is_approximatly_equal(1.01).with_epsilon(1e-2))


def test_is_approximatly_equal_matches_fail():
    with raises_exception(
        AssertionError, "Expected 1 to match: ~= 1.1; with epsilon 1e-10"
    ):
        assert_that(1).matches(is_approximatly_equal(1.1))
    with raises_exception(
        AssertionError, "Expected 1 to match: ~= 1.01; with epsilon 0.001"
    ):
        assert_that(1).matches(is_approximatly_equal(1.01).with_epsilon(0.001))


def test_is_approximatly_equal_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected 1 to not match: ~= 1.01; with epsilon 0.1"
    ):
        assert_that(1).does_not_match(is_approximatly_equal(1.01).with_epsilon(0.1))


# is_positive
def test_is_positive_matches_pass():
    assert_that(1).matches(is_positive())
    assert_that(12).matches(is_positive())


def test_is_positive_does_not_match_pass():
    assert_that(-1).does_not_match(is_positive())
    assert_that(0).does_not_match(is_positive())
    assert_that(-0.5).does_not_match(is_positive())


def test_is_positive_matches_fail():
    with raises_exception(AssertionError, "Expected -1 to match: is positive"):
        assert_that(-1).matches(is_positive())


def test_is_positive_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: is positive"):
        assert_that(1).does_not_match(is_positive())


# is_non_negative
def test_is_non_negative_matches_pass():
    assert_that(1).matches(is_non_negative())
    assert_that(12).matches(is_non_negative())
    assert_that(0).matches(is_non_negative())


def test_is_non_negative_does_not_match_pass():
    assert_that(-1).does_not_match(is_non_negative())
    assert_that(-0.5).does_not_match(is_non_negative())


def test_is_non_negative_matches_fail():
    with raises_exception(AssertionError, "Expected -1 to match: is non-negative"):
        assert_that(-1).matches(is_non_negative())


def test_is_non_negative_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 0 to not match: is non-negative"):
        assert_that(0).does_not_match(is_non_negative())


# is_negative
def test_is_negative_matches_pass():
    assert_that(-1).matches(is_negative())
    assert_that(-12).matches(is_negative())


def test_is_negative_does_not_match_pass():
    assert_that(12).does_not_match(is_negative())
    assert_that(1).does_not_match(is_negative())
    assert_that(0).does_not_match(is_negative())


def test_is_negative_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: is negative"):
        assert_that(1).matches(is_negative())


def test_is_negative_does_not_match_fail():
    with raises_exception(AssertionError, "Expected -1 to not match: is negative"):
        assert_that(-1).does_not_match(is_negative())


# is_non_positive
def test_is_non_positive_matches_pass():
    assert_that(-1).matches(is_non_positive())
    assert_that(-12).matches(is_non_positive())
    assert_that(0).matches(is_non_positive())


def test_is_non_positive_does_not_match_pass():
    assert_that(12).does_not_match(is_non_positive())
    assert_that(1).does_not_match(is_non_positive())


def test_is_non_positive_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: is non-positive"):
        assert_that(1).matches(is_non_positive())


def test_is_non_positive_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 0 to not match: is non-positive"):
        assert_that(0).does_not_match(is_non_positive())


# zero
def test_zero_matches_pass():
    assert_that(0).matches(zero())


def test_zero_does_not_match_pass():
    assert_that(-1).does_not_match(zero())
    assert_that(1).does_not_match(zero())


def test_zero_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: is zero"):
        assert_that(1).matches(zero())


def test_zero_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 0 to not match: is zero"):
        assert_that(0).does_not_match(zero())


# approximatly_zero
def test_approximatly_zero_matches_pass():
    assert_that(0).matches(approximatly_zero())
    assert_that(0.000000000000000001).matches(approximatly_zero())
    assert_that(0.01).matches(approximatly_zero().with_epsilon(0.1))
    assert_that(-0.01).matches(approximatly_zero().with_epsilon(0.1))


def test_approximatly_zero_does_not_match_pass():
    assert_that(-1).does_not_match(approximatly_zero())
    assert_that(1).does_not_match(approximatly_zero())
    assert_that(0.01).does_not_match(approximatly_zero().with_epsilon(0.00001))
    assert_that(-0.01).does_not_match(approximatly_zero().with_epsilon(0.00001))


def test_approximatly_zero_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 0.1 to match: is approximatly zero with epsilon: 0.01",
    ):
        assert_that(0.1).matches(approximatly_zero().with_epsilon(0.01))


def test_approximatly_zero_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 0.001 to not match: is approximatly zero with epsilon: 0.01",
    ):
        assert_that(0.001).does_not_match(approximatly_zero().with_epsilon(0.01))


# is_a_perfect_square
def test_is_a_perfect_square_matches_pass():
    assert_that(4).matches(is_a_perfect_square())
    assert_that(9).matches(is_a_perfect_square())
    assert_that(16).matches(is_a_perfect_square())
    assert_that(1).matches(is_a_perfect_square())


def test_is_a_perfect_square_does_not_match_pass():
    assert_that(5).does_not_match(is_a_perfect_square())
    assert_that(3).does_not_match(is_a_perfect_square())


def test_is_a_perfect_square_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 3 to match: is a perfect square",
    ):
        assert_that(3).matches(is_a_perfect_square())


def test_is_a_perfect_square_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 4 to not match: is a perfect square",
    ):
        assert_that(4).does_not_match(is_a_perfect_square())


# is_a_power_of
def test_is_a_power_of_matches_pass():
    assert_that(4).matches(is_a_power_of(2))
    assert_that(9).matches(is_a_power_of(3))
    assert_that(16).matches(is_a_power_of(2))
    assert_that(16).matches(is_a_power_of(4))
    assert_that(8).matches(is_a_power_of(2))
    assert_that(1).matches(is_a_power_of(1))


def test_is_a_power_of_does_not_match_pass():
    assert_that(10).does_not_match(is_a_power_of(2))


def test_is_a_power_of_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 10 to match: is a power of 2",
    ):
        assert_that(10).matches(is_a_power_of(2))


def test_is_a_power_of_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 9 to not match: is a power of 3",
    ):
        assert_that(9).does_not_match(is_a_power_of(3))


# is_factorial_of
def test_is_a_factorial_of_matches_pass():
    assert_that(6).matches(is_a_factorial_of(3))
    assert_that(6).matches(is_a_factorial_of(4))
    assert_that(24).matches(is_a_factorial_of(4))
    assert_that(24).matches(is_a_factorial_of(5))
    assert_that(120).matches(is_a_factorial_of(5))


def test_is_a_factorial_of_does_not_match_pass():
    assert_that(120).does_not_match(is_a_factorial_of(4))


def test_is_a_factorial_of_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 120 to match: is a factorial of 4",
    ):
        assert_that(120).matches(is_a_factorial_of(4))


def test_is_a_factorial_of_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 6 to not match: is a factorial of 5",
    ):
        assert_that(6).does_not_match(is_a_factorial_of(5))


# as_absolute_matches
def test_as_absolute_matches_matches_pass():
    assert_that(-6).matches(as_absolute_matches(6))
    assert_that(-2).matches(as_absolute_matches(is_positive()))
    assert_that(2).matches(as_absolute_matches(2))


def test_as_absolute_matches_does_not_match_pass():
    assert_that(-4).does_not_match(as_absolute_matches(is_negative()))
    assert_that(-2).does_not_match(as_absolute_matches(-2))


def test_as_absolute_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected abs(-6) to match: is negative",
    ):
        assert_that(-6).matches(as_absolute_matches(is_negative()))


def test_as_absolute_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected abs(-6) to not match: == 6",
    ):
        assert_that(-6).does_not_match(as_absolute_matches(6))
