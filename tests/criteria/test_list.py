from assertive.core import assert_that
from assertive.criteria.basic import is_greater_than
from assertive.criteria.list import (
    contains,
    contains_exactly,
    has_length,
    is_empty,
)
from assertive.criteria.exception import raises_exception


# type_failires
def test_type_failures():
    with raises_exception(TypeError):
        assert_that(1).matches(has_length(3))


# has_length
def test_has_length_matches_pass():
    assert_that([1, 2, 3]).matches(has_length(3))
    assert_that([1, 2, 3]).matches(has_length(is_greater_than(2)))
    assert_that("hello").matches(has_length(5))
    assert_that({"hello": "world"}).matches(has_length(1))


def test_has_length_does_not_match_pass():
    assert_that([1, 2, 3]).does_not_match(has_length(2))
    assert_that([1, 2, 3]).does_not_match(has_length(is_greater_than(4)))


def test_has_length_matches_fail():
    with raises_exception(
        AssertionError, "Expected [1, 2, 3] to match: has length matching: 4"
    ):
        assert_that([1, 2, 3]).matches(has_length(4))


def test_has_length_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected [1, 2, 3] to not match: has length matching: 3"
    ):
        assert_that([1, 2, 3]).does_not_match(has_length(3))


# is_empty
def test_is_empty_matches_pass():
    assert_that([]).matches(is_empty())
    assert_that({}).matches(is_empty())
    assert_that("").matches(is_empty())


def test_is_empty_does_not_match_pass():
    assert_that([1]).does_not_match(is_empty())
    assert_that({"hello": "world"}).does_not_match(is_empty())
    assert_that("hello").does_not_match(is_empty())


def test_is_empty_matches_fail():
    with raises_exception(AssertionError, "Expected [1, 2, 3] to match: is empty"):
        assert_that([1, 2, 3]).matches(is_empty())


def test_is_empty_does_not_match_fail():
    with raises_exception(AssertionError, "Expected [] to not match: is empty"):
        assert_that([]).does_not_match(is_empty())


# contains
def test_contains_matches_pass():
    assert_that([1, 2, 3]).matches(contains(2))
    assert_that([1, 2, 3]).matches(contains(is_greater_than(1)))
    assert_that([1, 2, 3]).matches(contains(1, 3))


def test_contains_does_not_match_pass():
    assert_that([1, 2, 3]).does_not_match(contains(4))
    assert_that([1, 2, 3]).does_not_match(contains(1, 2, 4))
    assert_that([1, 2, 3]).does_not_match(contains(1, 2, is_greater_than(3)))


def test_contains_matches_fail():
    with raises_exception(
        AssertionError, "Expected [1, 2, 3] to match: contains [1, 2, 4]"
    ):
        assert_that([1, 2, 3]).matches(contains(1, 2, 4))


def test_contains_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected [1, 2, 3] to not match: contains [> 0]"
    ):
        assert_that([1, 2, 3]).does_not_match(contains(is_greater_than(0)))


# contains_exactly
def test_contains_exactly_matches_pass():
    assert_that([1, 2, 3]).matches(contains_exactly(1, 2, 3))
    assert_that([1, 2, 3]).matches(
        contains_exactly(1, is_greater_than(1), is_greater_than(2))
    )


def test_contains_exactly_does_not_match_pass():
    assert_that([1, 2, 3]).does_not_match(contains_exactly(1))
    assert_that([1, 2, 3]).does_not_match(contains_exactly(3, 2, 1))
    assert_that([1, 2, 3]).does_not_match(contains_exactly(1, 3, 2))
    assert_that([1, 2, 3]).does_not_match(contains_exactly(1, 2, 3, 4))


def test_contains_exactly_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected [1, 2, 3] to match: contains exactly [1, 2, 3, 4]",
    ):
        assert_that([1, 2, 3]).matches(contains_exactly(1, 2, 3, 4))


def test_contains_exactly_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected [1, 2, 3] to not match: contains exactly [> 0, 2, 3]",
    ):
        assert_that([1, 2, 3]).does_not_match(
            contains_exactly(is_greater_than(0), 2, 3)
        )
