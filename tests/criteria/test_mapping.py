from assertive.criteria.basic import is_gt
from assertive.criteria.exception import raises_exception
from assertive.criteria.mapping import (
    contains_exact_keys,
    contains_keys,
    has_exact_key_values,
    has_key_and_value,
    has_key_values,
)
from assertive.criteria.string import regex


# type_failires
def test_type_failures():
    with raises_exception(TypeError):
        assert 1 == has_key_values({"x": 1})


# has_key_values
def test_has_key_values_matches_pass():
    assert {"x": 1, "y": 2} == has_key_values({"x": is_gt(0)})
    assert {"x": 1, "y": 2} == has_key_values({"x": 1})


def test_has_key_values_does_not_match_pass():
    assert {"x": 1, "y": 2} != has_key_values({"x": is_gt(1)})
    assert {"x": 1, "y": 2} != has_key_values({"y": 1})


# has_key_values
def test_has_key_and_value_matches_pass():
    assert {"x": 1, "y": 2} == has_key_and_value("x", is_gt(0))
    assert {"x": 1, "y": 2} == has_key_and_value("x", 1)


def test_has_key_and_value_does_not_match_pass():
    assert {"x": 1, "y": 2} != has_key_and_value("x", is_gt(1))
    assert {"x": 1, "y": 2} != has_key_and_value("y", 1)


# has_exact_key_values
def test_has_exact_key_values_matches_pass():
    assert {"x": 1, "y": 2} == has_exact_key_values({"x": 1, "y": is_gt(1)})


def test_has_exact_key_values_does_not_match_pass():
    assert {"x": 1, "y": 2} != has_exact_key_values({"x": is_gt(0)})

    assert {"x": 1, "y": 2} != has_exact_key_values({"x": 1, "y": 2, "z": 3})


# contains_keys
def test_contains_keys_matches_pass():
    assert {"x": 1, "y": 2} == contains_keys("x")
    assert {"x": 1, "y": 2} == contains_keys(regex(r"y|z"))


def test_contains_keys_does_not_match_pass():
    assert {"x": 1, "y": 2} != contains_keys(regex(r"a|b"))


# contains_exact_keys
def test_contains_exact_keys_matches_pass():
    assert {"x": 1, "y": 2} == contains_exact_keys("x", "y")
    assert {"x": 1, "y": 2} == contains_exact_keys(regex(r"y|z"), regex(r"x|z"))


def test_contains_exact_keys_does_not_match_pass():
    assert {"x": 1, "y": 2} != contains_exact_keys(regex(r"x|y"))
