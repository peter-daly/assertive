from assertive.criteria.basic import is_gt
from assertive.criteria.exception import raises_exception
from assertive.criteria.list import (
    contains,
    contains_exactly,
    has_length,
    is_empty,
)


# type_failires
def test_type_failures():
    with raises_exception(TypeError):
        assert 1 == has_length(3)


# has_length
def test_has_length_matches_pass():
    assert [1, 2, 3] == has_length(3)
    assert [1, 2, 3] == has_length(is_gt(2))
    assert "hello" == has_length(5)
    assert {"hello": "world"} == has_length(1)


def test_has_length_does_not_match_pass():
    assert [1, 2, 3] != has_length(2)
    assert [1, 2, 3] != has_length(is_gt(4))


# is_empty
def test_is_empty_matches_pass():
    assert [] == is_empty()
    assert {} == is_empty()
    assert "" == is_empty()


def test_is_empty_does_not_match_pass():
    assert [1] != is_empty()
    assert {"hello": "world"} != is_empty()
    assert "hello" != is_empty()


# contains
def test_contains_matches_pass():
    assert [1, 2, 3] == contains(2)
    assert [1, 2, 3] == contains(is_gt(1))
    assert [1, 2, 3] == contains(1, 3)


def test_contains_does_not_match_pass():
    assert [1, 2, 3] != contains(4)
    assert [1, 2, 3] != contains(1, 2, 4)
    assert [1, 2, 3] != contains(1, 2, is_gt(3))


# contains_exactly
def test_contains_exactly_matches_pass():
    assert [1, 2, 3] == contains_exactly(1, 2, 3)
    assert [1, 2, 3] == contains_exactly(1, is_gt(1), is_gt(2))


def test_contains_exactly_does_not_match_pass():
    assert [1, 2, 3] != contains_exactly(1)
    assert [1, 2, 3] != contains_exactly(3, 2, 1)
    assert [1, 2, 3] != contains_exactly(1, 3, 2)
    assert [1, 2, 3] != contains_exactly(1, 2, 3, 4)
