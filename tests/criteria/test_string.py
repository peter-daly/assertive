from assertive.assertions import assert_that
from assertive.criteria.basic import is_less_than
from assertive.criteria.string import (
    regex,
    ends_with,
    starts_with,
    contains_substring,
)
from assertive.criteria.exception import raises_exception

# type


def test_type_failure():
    with raises_exception(TypeError):
        assert_that(1).matches(ends_with("1"))

    with raises_exception(TypeError):
        assert_that(1).does_not_match(ends_with("2"))


# regex
def test_regex_matches_pass():
    assert_that("abc").matches(regex(r"abc"))
    assert_that("abc").matches(regex(r"abc|def"))


def test_regex_does_not_match_pass():
    assert_that("abc").does_not_match(regex(r"def"))


def test_regex_matches_fail():
    with raises_exception(
        AssertionError, "Expected 'abc' to match: regex pattern 'def'"
    ):
        assert_that("abc").matches(regex(r"def"))


def test_regex_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected 'abc' to not match: regex pattern 'abc'"
    ):
        assert_that("abc").does_not_match(regex(r"abc"))


# starts_with
def test_starts_with_matches_pass():
    assert_that("abc").matches(starts_with("ab"))


def test_starts_with_does_not_match_pass():
    assert_that("abc").does_not_match(starts_with("b"))


def test_starts_with_matches_fail():
    with raises_exception(AssertionError, "Expected 'abc' to match: starts with 'b'"):
        assert_that("abc").matches(starts_with("b"))


def test_starts_with_does_not_match_fail():
    with raises_exception(
        AssertionError, "Expected 'abc' to not match: starts with 'a'"
    ):
        assert_that("abc").does_not_match(starts_with("a"))


# ends_with
def test_ends_with_matches_pass():
    assert_that("abc").matches(ends_with("bc"))


def test_ends_with_does_not_match_pass():
    assert_that("abc").does_not_match(ends_with("b"))


def test_ends_with_matches_fail():
    with raises_exception(AssertionError, "Expected 'abc' to match: ends with 'b'"):
        assert_that("abc").matches(ends_with("b"))


def test_ends_with_does_not_match_fail():
    with raises_exception(AssertionError, "Expected 'abc' to not match: ends with 'c'"):
        assert_that("abc").does_not_match(ends_with("c"))


# contains_substring
def test_contains_substring_matches_pass():
    assert_that("abc").matches(contains_substring("bc"))
    assert_that("hello hello hello said the police officer").matches(
        contains_substring("hello")
    )
    assert_that("hello hello hello said the police officer").matches(
        contains_substring("hello").times(3)
    )
    assert_that("hello hello hello said the police officer").matches(
        contains_substring("hello").at_least_times(2)
    )
    assert_that("hello hello hello said the police officer").matches(
        contains_substring("hello").times(is_less_than(5))
    )
    assert_that("abc").matches(contains_substring("hello").never)


def test_contains_substring_does_not_match_pass():
    assert_that("abc").does_not_match(contains_substring("b").never)
    assert_that("abc").does_not_match(contains_substring("hello"))


def test_contains_substring_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 'abc' to match: contains 'hello' with number of times matching: >= 1",
    ):
        assert_that("abc").matches(contains_substring("hello"))

    with raises_exception(
        AssertionError,
        "Expected 'hello hello' to match: contains 'hello' with number of times matching: 1",
    ):
        assert_that("hello hello").matches(contains_substring("hello").once)


def test_contains_substring_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 'abc' to not match: contains 'c' with number of times matching: 1",
    ):
        assert_that("abc").does_not_match(contains_substring("c").once)
