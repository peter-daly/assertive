from fluent_assertions.assertions import assert_that
from fluent_assertions.criteria.basic import (
    as_string_matches,
    is_between,
    is_equal_to,
    is_greater_than,
    is_greater_than_or_equal,
    is_less_than,
    is_less_than_or_equal,
    is_false,
    is_same_instance_as,
    is_true,
)
from fluent_assertions.criteria.exception import raises_exception

# is_equal
def test_is_equal_to_matches_pass():
    assert_that(1).matches(is_equal_to(1))


def test_is_equal_to_does_not_match_pass():
    assert_that(0).does_not_match(is_equal_to(1))


def test_is_equal_to_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: == 2"):
        assert_that(1).matches(is_equal_to(2))


def test_is_equal_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: == 1"):
        assert_that(1).does_not_match(is_equal_to(1))


# is_greater_than
def test_is_greater_than_to_matches_pass():
    assert_that(2).matches(is_greater_than(1))


def test_is_greater_than_to_does_not_match_pass():
    assert_that(0).does_not_match(is_greater_than(1))


def test_is_greater_than_to_matches_fail():
    with raises_exception(AssertionError, "Expected 2 to match: > 2"):
        assert_that(2).matches(is_greater_than(2))


def test_is_greater_than_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: > 0"):
        assert_that(1).does_not_match(is_greater_than(0))


# is_greater_than_or_equal
def test_is_greater_than_or_equal_to_matches_pass():
    assert_that(2).matches(is_greater_than_or_equal(1))
    assert_that(2).matches(is_greater_than_or_equal(2))


def test_is_greater_than_or_equal_to_does_not_match_pass():
    assert_that(0).does_not_match(is_greater_than_or_equal(1))


def test_is_greater_than_or_equal_to_matches_fail():
    with raises_exception(AssertionError, "Expected 1 to match: >= 2"):
        assert_that(1).matches(is_greater_than_or_equal(2))


def test_is_greater_than_or_equal_to_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: >= 0"):
        assert_that(1).does_not_match(is_greater_than_or_equal(0))

    with raises_exception(AssertionError, "Expected 1 to not match: >= 1"):
        assert_that(1).does_not_match(is_greater_than_or_equal(1))


# is_less_than
def test_is_less_than_matches_pass():
    assert_that(2).matches(is_less_than(3))


def test_is_less_than_does_not_match_pass():
    assert_that(1).does_not_match(is_less_than(0))


def test_is_less_than_matches_fail():
    with raises_exception(AssertionError, "Expected 2 to match: < 1"):
        assert_that(2).matches(is_less_than(1))


def test_is_less_than_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: < 2"):
        assert_that(1).does_not_match(is_less_than(2))


# is_less_than_or_equal
def test_is_less_than_or_equal_matches_pass():
    assert_that(2).matches(is_less_than_or_equal(3))
    assert_that(3).matches(is_less_than_or_equal(3))


def test_is_less_than_or_equal_does_not_match_pass():
    assert_that(1).does_not_match(is_less_than_or_equal(0))


def test_is_less_than_or_equal_matches_fail():
    with raises_exception(AssertionError, "Expected 2 to match: <= 1"):
        assert_that(2).matches(is_less_than_or_equal(1))


def test_is_less_than_or_equal_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 1 to not match: <= 2"):
        assert_that(1).does_not_match(is_less_than_or_equal(2))

    with raises_exception(AssertionError, "Expected 2 to not match: <= 2"):
        assert_that(2).does_not_match(is_less_than_or_equal(2))


# is_false
def test_is_false_matches_pass():
    assert_that(False).matches(is_false())


def test_false_does_not_match_pass():
    assert_that(True).does_not_match(is_false())


def test_is_false_matches_fail():
    with raises_exception(AssertionError, "Expected True to match: is False"):
        assert_that(True).matches(is_false())


def test_is_false_does_not_match_fail():
    with raises_exception(AssertionError, "Expected False to not match: is False"):
        assert_that(False).does_not_match(is_false())


# is_true
def test_is_true_matches_pass():
    assert_that(True).matches(is_true())


def test_is_true_does_not_match_pass():
    assert_that(False).does_not_match(is_true())


def test_is_true_matches_fail():
    with raises_exception(AssertionError, "Expected False to match: is True"):
        assert_that(False).matches(is_true())


def test_is_true_does_not_match_fail():
    with raises_exception(AssertionError, "Expected True to not match: is True"):
        assert_that(True).does_not_match(is_true())


# is_between
def test_is_between_matches_pass():
    assert_that(4).matches(is_between(3, 5).exclusive)
    assert_that(4).matches(is_between(4, 5).inclusive)
    assert_that(4).matches(is_between(3, 5))


def test_is_between_does_not_match_pass():
    assert_that(4).does_not_match(is_between(4, 5).exclusive)
    assert_that(3).does_not_match(is_between(4, 5))
    assert_that(3).does_not_match(is_between(4, 5).inclusive)


def test_is_between_matches_fail():
    with raises_exception(
        AssertionError, "Expected 3 to match: is between 4 and 5; inclusive"
    ):
        assert_that(3).matches(is_between(4, 5))

    with raises_exception(
        AssertionError, "Expected 4 to match: is between 4 and 5; exclusive"
    ):
        assert_that(4).matches(is_between(4, 5).exclusive)


def test_is_between_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected 4 to not match: is between 4 and 5; inclusive"
    ):
        assert_that(4).does_not_match(is_between(4, 5).inclusive)

    with raises_exception(
        AssertionError, "Expected 5 to not match: is between 4 and 6; exclusive"
    ):
        assert_that(5).does_not_match(is_between(4, 6).exclusive)


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
def test_as_string_as_matches_matches_pass():
    assert_that(4).matches(as_string_matches(is_equal_to("4")))
    assert_that(4).matches(as_string_matches("4"))


def test_as_string_as_matches_does_not_match_pass():
    assert_that(4).does_not_match(as_string_matches("hello"))


def test_as_string_as_matches_matches_fail():
    with raises_exception(AssertionError, "Expected str(3) to match: == 4"):
        assert_that(3).matches(as_string_matches("4"))


def test_as_string_as_matches_not_match_fail():
    with raises_exception(AssertionError, "Expected str(3) to not match: == 3"):
        assert_that(3).does_not_match(as_string_matches("3"))
