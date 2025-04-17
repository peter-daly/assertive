from assertive.criteria.numeric import (
    approximately_zero,
    as_absolute_matches,
    is_a_perfect_square,
    is_a_power_of,
    is_approximately_equal,
    is_coprime_with,
    is_even,
    is_multiple_of,
    is_negative,
    is_non_negative,
    is_non_positive,
    is_odd,
    is_positive,
    is_prime,
    zero,
)


# is_multiple_of
def test_is_multiple_of_matches_pass():
    assert 2 == is_multiple_of(4)
    assert 3 == is_multiple_of(3)
    assert 3 == is_multiple_of(6)


def test_is_multiple_of_does_not_match_pass():
    assert 0 != is_multiple_of(5)
    assert 5 != is_multiple_of(6)


# is_even
def test_is_even_matches_pass():
    assert 2 == is_even()
    assert 100 == is_even()
    assert 0 == is_even()
    assert -2 == is_even()

    assert 2 == ~is_odd()


def test_is_even_does_not_match_pass():
    assert 1 != is_even()
    assert -1 != is_even()
    assert 101 != is_even()


# is_odd
def test_is_odd_matches_pass():
    assert 21 == is_odd()
    assert 101 == is_odd()
    assert 1 == is_odd()
    assert -1 == is_odd()


def test_is_odd_does_not_match_pass():
    assert 12 != is_odd()
    assert 0 != is_odd()
    assert 100 != is_odd()


# is_approximatly_equal
def test_is_approximatly_equal_matches_pass():
    assert 1 == is_approximately_equal(1.00000000000000000000000001)
    assert 1 == is_approximately_equal(1.01).with_epsilon(0.1)
    assert 1 == is_approximately_equal(1.01).with_epsilon(1e-1)


def test_is_approximatly_equal_does_not_match_pass():
    assert 1 != is_approximately_equal(1.1)
    assert 1 != is_approximately_equal(1.01).with_epsilon(0.001)
    assert 1 != is_approximately_equal(1.01).with_epsilon(1e-2)


# is_positive
def test_is_positive_matches_pass():
    assert 1 == is_positive()
    assert 12 == is_positive()


def test_is_positive_does_not_match_pass():
    assert -1 != is_positive()
    assert 0 != is_positive()
    assert -0.5 != is_positive()


# is_non_negative
def test_is_non_negative_matches_pass():
    assert 1 == is_non_negative()
    assert 12 == is_non_negative()
    assert 0 == is_non_negative()


def test_is_non_negative_does_not_match_pass():
    assert -1 != is_non_negative()
    assert -0.5 != is_non_negative()


# is_negative
def test_is_negative_matches_pass():
    assert -1 == is_negative()
    assert -12 == is_negative()


def test_is_negative_does_not_match_pass():
    assert 12 != is_negative()
    assert 1 != is_negative()
    assert 0 != is_negative()


# is_non_positive
def test_is_non_positive_matches_pass():
    assert -1 == is_non_positive()
    assert -12 == is_non_positive()
    assert 0 == is_non_positive()


def test_is_non_positive_does_not_match_pass():
    assert 12 != is_non_positive()
    assert 1 != is_non_positive()


# zero
def test_zero_matches_pass():
    assert 0 == zero()


def test_zero_does_not_match_pass():
    assert -1 != zero()
    assert 1 != zero()


# approximatly_zero
def test_approximatly_zero_matches_pass():
    assert 0 == approximately_zero()
    assert 0.000000000000000001 == approximately_zero()
    assert 0.01 == approximately_zero().with_epsilon(0.1)
    assert -0.01 == approximately_zero().with_epsilon(0.1)


def test_approximatly_zero_does_not_match_pass():
    assert -1 != approximately_zero()
    assert 1 != approximately_zero()
    assert 0.01 != approximately_zero().with_epsilon(0.00001)
    assert -0.01 != approximately_zero().with_epsilon(0.00001)


# is_a_perfect_square
def test_is_a_perfect_square_matches_pass():
    assert 4 == is_a_perfect_square()
    assert 9 == is_a_perfect_square()
    assert 16 == is_a_perfect_square()
    assert 1 == is_a_perfect_square()


def test_is_a_perfect_square_does_not_match_pass():
    assert 5 != is_a_perfect_square()
    assert 3 != is_a_perfect_square()


# is_a_power_of
def test_is_a_power_of_matches_pass():
    assert 4 == is_a_power_of(2)
    assert 9 == is_a_power_of(3)
    assert 16 == is_a_power_of(2)
    assert 16 == is_a_power_of(4)
    assert 8 == is_a_power_of(2)
    assert 1 == is_a_power_of(1)


def test_is_a_power_of_does_not_match_pass():
    assert 10 != is_a_power_of(2)


# as_absolute_matches
def test_as_absolute_matches_matches_pass():
    assert -6 == as_absolute_matches(6)
    assert -2 == as_absolute_matches(is_positive())
    assert 2 == as_absolute_matches(2)


def test_as_absolute_matches_does_not_match_pass():
    assert -4 != as_absolute_matches(is_negative())
    assert -2 != as_absolute_matches(-2)


# is_prime
def test_is_prime_matches_pass():
    assert 2 == is_prime()
    assert 3 == is_prime()
    assert 5 == is_prime()
    assert 7 == is_prime()
    assert 11 == is_prime()
    assert 13 == is_prime()
    assert 17 == is_prime()
    assert 617 == is_prime()


def test_is_prime_does_not_match_pass():
    assert 4 != is_prime()
    assert 100 != is_prime()


# is_coprime_with
def test_is_coprime_with_matches_pass():
    assert 10 == is_coprime_with(9)
    assert 15 == is_coprime_with(4)
    assert 21 == is_coprime_with(2)


def test_is_coprime_with_does_not_match_pass():
    assert 4 != is_coprime_with(2)
    assert 100 != is_coprime_with(10)
    assert 10 != is_coprime_with(5)
