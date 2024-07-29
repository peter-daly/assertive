from assertive.core import assert_that
from assertive.criteria.basic import (
    as_string_matches,
    is_between,
    is_eq,
    is_gt,
    is_gte,
    is_lt,
    is_lte,
    is_none,
    is_not_none,
    is_same_instance_as,
)
from assertive.criteria.exception import raises_exception


# is_equal
def test_is_equal_to_matches_pass():
    assert_that(1).matches(is_eq(1))


def test_is_equal_to_does_not_match_pass():
    assert_that(0).does_not_match(is_eq(1))


def test_is_equal_to_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: 2"):
        assert_that(1).matches(is_eq(2))


def test_is_equal_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: 1"):
        assert_that(1).does_not_match(is_eq(1))


# is_greater_than
def test_is_greater_than_to_matches_pass():
    assert_that(2).matches(is_gt(1))
    assert 2 == is_gt(1)


def test_is_greater_than_to_does_not_match_pass():
    assert_that(0).does_not_match(is_gt(1))


def test_is_greater_than_to_matches_fail():
    with raises_exception(AssertionError, "Expected 2 to match: > 2"):
        assert_that(2).matches(is_gt(2))


def test_is_greater_than_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: > 0"):
        assert_that(1).does_not_match(is_gt(0))


# is_greater_than_or_equal
def test_is_greater_than_or_equal_to_matches_pass():
    assert_that(2).matches(is_gte(1))
    assert_that(2).matches(is_gte(2))


def test_is_greater_than_or_equal_to_does_not_match_pass():
    assert_that(0).does_not_match(is_gte(1))


def test_is_greater_than_or_equal_to_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: >= 2"):
        assert_that(1).matches(is_gte(2))


def test_is_greater_than_or_equal_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: >= 0"):
        assert_that(1).does_not_match(is_gte(0))

    with raises_exception(AssertionError, "Expected 1 to not match: >= 1"):
        assert_that(1).does_not_match(is_gte(1))


# is_less_than
def test_is_less_than_matches_pass():
    assert_that(2).matches(is_lt(3))


def test_is_less_than_does_not_match_pass():
    assert_that(1).does_not_match(is_lt(0))


def test_is_less_than_matches_fail():
    with raises_exception(AssertionError, "Expected 2 to match: < 1"):
        assert_that(2).matches(is_lt(1))


def test_is_less_than_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: < 2"):
        assert_that(1).does_not_match(is_lt(2))


# is_less_than_or_equal
def test_is_less_than_or_equal_matches_pass():
    assert_that(2).matches(is_lte(3))
    assert_that(3).matches(is_lte(3))


def test_is_less_than_or_equal_does_not_match_pass():
    assert_that(1).does_not_match(is_lte(0))


def test_is_less_than_or_equal_matches_fail():
    with raises_exception(AssertionError, "Expected 2 to match: <= 1"):
        assert_that(2).matches(is_lte(1))


def test_is_less_than_or_equal_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: <= 2"):
        assert_that(1).does_not_match(is_lte(2))

    with raises_exception(AssertionError, "Expected 2 to not match: <= 2"):
        assert_that(2).does_not_match(is_lte(2))


# is_between
def test_is_between_matches_pass():
    assert_that(4).matches(is_between(3, 5).exclusive())
    assert_that(4).matches(is_between(4, 5).inclusive())
    assert_that(4).matches(is_between(3, 5))


def test_is_between_does_not_match_pass():
    assert_that(4).does_not_match(is_between(4, 5).exclusive())
    assert_that(3).does_not_match(is_between(4, 5))
    assert_that(3).does_not_match(is_between(4, 5).inclusive())


def test_is_between_matches_fail():
    with raises_exception(
        AssertionError, "Expected 3 to match: is between 4 and 5; inclusive"
    ):
        assert_that(3).matches(is_between(4, 5))

    with raises_exception(
        AssertionError, "Expected 4 to match: is between 4 and 5; exclusive"
    ):
        assert_that(4).matches(is_between(4, 5).exclusive())


def test_is_between_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected 4 to not match: is between 4 and 5; inclusive"
    ):
        assert_that(4).does_not_match(is_between(4, 5).inclusive())

    with raises_exception(
        AssertionError, "Expected 5 to not match: is between 4 and 6; exclusive"
    ):
        assert_that(5).does_not_match(is_between(4, 6).exclusive())


# is_same_instance_as
def test_is_same_instance_as_matches_pass():
    x = 4
    y = x
    assert_that(x).matches(is_same_instance_as(y))


def test_is_same_instance_as_does_not_match_pass():
    x = 4
    y = 5
    assert_that(x).does_not_match(is_same_instance_as(y))


def test_is_same_instance_as_matches_fail():
    with raises_exception(AssertionError, "Expected 3 to match: is same instance as 4"):
        assert_that(3).matches(is_same_instance_as(4))


def test_is_same_instance_as_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected 3 to not match: is same instance as 3"
    ):
        assert_that(3).does_not_match(is_same_instance_as(3))


# as_string_matches
def test_as_string_matches_matches_pass():
    assert_that(4).matches(as_string_matches(is_eq("4")))
    assert_that(4).matches(as_string_matches("4"))


def test_as_string_matches_does_not_match_pass():
    assert_that(4).does_not_match(as_string_matches("hello"))


def test_as_string_matches_matches_fail():
    with raises_exception(AssertionError, "Expected str(3) to match: 4"):
        assert_that(3).matches(as_string_matches("4"))


def test_as_string_matches_not_match_fail():
    with raises_exception(AssertionError, "Expected str(3) to not match: 3"):
        assert_that(3).does_not_match(as_string_matches("3"))


# is_none
def test_is_none_matches_pass():
    assert_that(None).matches(is_none())


def test_is_none_matches_does_not_match_pass():
    assert_that("hello").does_not_match(is_none())


def test_is_none_as_matches_matches_fail():
    with raises_exception(AssertionError, "Expected 3 to match: is None"):
        assert_that(3).matches(is_none())


def test_is_none_as_matches_not_match_fail():
    with raises_exception(AssertionError, "Expected None to not match: is None"):
        assert_that(None).does_not_match(is_none())


# is_not_none
def test_is_not_none_matches_pass():
    assert_that("None").matches(is_not_none())


def test_is_not_none_matches_does_not_match_pass():
    assert_that(None).does_not_match(is_not_none())


def test_is_not_none_as_matches_matches_fail():
    with raises_exception(AssertionError, "Expected None to match: is not None"):
        assert_that(None).matches(is_not_none())


def test_is_not_none_as_matches_not_match_fail():
    with raises_exception(AssertionError, "Expected 3 to not match: is not None"):
        assert_that(3).does_not_match(is_not_none())
