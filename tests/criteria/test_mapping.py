from assertive.assertions import assert_that
from assertive.criteria.basic import is_greater_than
from assertive.criteria.string import regex
from assertive.criteria.mapping import (
    contains_exact_keys,
    contains_keys,
    has_exact_key_values,
    has_key_and_value,
    has_key_values,
)
from assertive.criteria.exception import raises_exception


# type_failires
def test_type_failures():
    with raises_exception(TypeError):
        assert_that(1).matches(has_key_values({"x": 1}))


# has_key_values
def test_has_key_values_matches_pass():
    assert_that({"x": 1, "y": 2}).matches(has_key_values({"x": is_greater_than(0)}))
    assert_that({"x": 1, "y": 2}).matches(has_key_values({"x": 1}))


def test_has_key_values_does_not_match_pass():
    assert_that({"x": 1, "y": 2}).does_not_match(
        has_key_values({"x": is_greater_than(1)})
    )
    assert_that({"x": 1, "y": 2}).does_not_match(has_key_values({"y": 1}))


def test_has_key_values_matches_fail():
    with raises_exception(
        AssertionError, "Expected {'x': 1, 'y': 2} to match: has key values: {x: > 1}"
    ):
        assert_that({"x": 1, "y": 2}).matches(has_key_values({"x": is_greater_than(1)}))


def test_has_key_values_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to not match: has key values: {y: > 1}",
    ):
        assert_that({"x": 1, "y": 2}).does_not_match(
            has_key_values({"y": is_greater_than(1)})
        )


# has_key_values
def test_has_key_and_value_matches_pass():
    assert_that({"x": 1, "y": 2}).matches(has_key_and_value("x", is_greater_than(0)))
    assert_that({"x": 1, "y": 2}).matches(has_key_and_value("x", 1))


def test_has_key_and_value_does_not_match_pass():
    assert_that({"x": 1, "y": 2}).does_not_match(
        has_key_and_value("x", is_greater_than(1))
    )
    assert_that({"x": 1, "y": 2}).does_not_match(has_key_and_value("y", 1))


def test_has_key_and_value_matches_fail():
    with raises_exception(
        AssertionError, "Expected {'x': 1, 'y': 2} to match: has key values: {x: > 1}"
    ):
        assert_that({"x": 1, "y": 2}).matches(
            has_key_and_value("x", is_greater_than(1))
        )


def test_has_key_and_value_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to not match: has key values: {y: > 1}",
    ):
        assert_that({"x": 1, "y": 2}).does_not_match(
            has_key_and_value("y", is_greater_than(1))
        )


# has_exact_key_values
def test_has_exact_key_values_matches_pass():
    assert_that({"x": 1, "y": 2}).matches(
        has_exact_key_values({"x": 1, "y": is_greater_than(1)})
    )


def test_has_exact_key_values_does_not_match_pass():
    assert_that({"x": 1, "y": 2}).does_not_match(
        has_exact_key_values({"x": is_greater_than(0)})
    )

    assert_that({"x": 1, "y": 2}).does_not_match(
        has_exact_key_values({"x": 1, "y": 2, "z": 3})
    )


def test_has_exact_key_values_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to match: has exact key values: {x: > 1}",
    ):
        assert_that({"x": 1, "y": 2}).matches(
            has_exact_key_values({"x": is_greater_than(1)})
        )


def test_has_exact_key_values_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to not match: has exact key values: {x: 1, y: > 1}",
    ):
        assert_that({"x": 1, "y": 2}).does_not_match(
            has_exact_key_values({"x": 1, "y": is_greater_than(1)})
        )


# contains_keys
def test_contains_keys_matches_pass():
    assert_that({"x": 1, "y": 2}).matches(contains_keys("x"))
    assert_that({"x": 1, "y": 2}).matches(contains_keys(regex(r"y|z")))


def test_contains_keys_does_not_match_pass():
    assert_that({"x": 1, "y": 2}).does_not_match(contains_keys(regex(r"a|b")))


def test_contains_keys_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to match: to have keys matching: [regex pattern 'a|b']",
    ):
        assert_that({"x": 1, "y": 2}).matches(contains_keys(regex(r"a|b")))


def test_contains_keys_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to not match: to have keys matching: [regex pattern 'x|y|z']",
    ):
        assert_that({"x": 1, "y": 2}).does_not_match(contains_keys(regex(r"x|y|z")))


# contains_exact_keys
def test_contains_exact_keys_matches_pass():
    assert_that({"x": 1, "y": 2}).matches(contains_exact_keys("x", "y"))
    assert_that({"x": 1, "y": 2}).matches(
        contains_exact_keys(regex(r"y|z"), regex(r"x|z"))
    )


def test_contains_exact_keys_does_not_match_pass():
    assert_that({"x": 1, "y": 2}).does_not_match(contains_exact_keys(regex(r"x|y")))


def test_contains_exact_keys_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to match: to have exact keys matching: [regex pattern 'a|b']",
    ):
        assert_that({"x": 1, "y": 2}).matches(contains_exact_keys(regex(r"a|b")))


def test_contains_exact_keys_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected {'x': 1, 'y': 2} to not match: to have exact keys matching: [regex pattern 'x|y|z', x]",
    ):
        assert_that({"x": 1, "y": 2}).does_not_match(
            contains_exact_keys(regex(r"x|y|z"), "x")
        )
