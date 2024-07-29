# from __future__ import annotations
from unittest.mock import Mock

from assertive.core import assert_that
from assertive.criteria import was_called, was_called_with
from assertive.criteria.basic import is_eq, is_gt, is_lt
from assertive.criteria.exception import raises_exception
from assertive.criteria.mock import (
    was_called_once_exactly_with,
    was_called_once_with,
    was_not_called_with,
)
from assertive.criteria.string import contains_substring, ends_with
from assertive.criteria.utils import ANY


def test_mock_matches_passes():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    assert_that(mock1).matches(was_called_with(1, 2).once())
    assert_that(mock1).matches(was_called_with(3, 4).once())
    assert_that(mock1).matches(was_called_once_with(1, 2))
    assert_that(mock1).matches(was_called().twice())
    assert_that(mock1).matches(was_not_called_with(5, 6))
    assert_that(mock1).matches(was_called_with(is_lt(2), is_gt(1)).once())

    mock2 = Mock()
    mock2(1, 2, x=3)
    mock2(1, 2, x=4)

    assert_that(mock2).matches(was_called_with(1, 2, x=3).once())
    assert_that(mock2).matches(was_not_called_with(1, 2, x=5))
    assert_that(mock2).matches(was_called_with(1, 2, x=is_gt(2)).twice())

    mock3 = Mock()
    mock3(1, 2, x=3)
    mock3(1, 2, x=2)
    mock3(1, 2, x=3)
    mock3(1, 2, x=4)

    assert_that(mock3).matches(was_called_with(1, 2, x=ANY).at_least_times(4))

    mock4 = Mock()
    mock4(1, 2, a=3, b=4)

    assert_that(mock4).matches(was_called_once_with(1, 2, a=3))
    assert_that(mock4).matches(was_called_once_exactly_with(1, 2, a=3, b=4))
    assert_that(mock4).matches(was_called_once_exactly_with(1, 2, a=3, b=~is_eq(5)))


def test_mock_does_not_match_passes():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    assert_that(mock1).does_not_match(was_called_with(1, 2).twice())
    assert_that(mock1).does_not_match(was_called_with(3, 4).twice())
    assert_that(mock1).does_not_match(was_called().once())


def test_mock_matches_fails():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)
    mock1(a=4, b=1)

    with raises_exception(
        AssertionError,
        contains_substring(
            "to match: to be called with args=(5, 6), kwargs=() and call count should match >= 1"
        ),
    ):
        assert_that(mock1).matches(was_called_with(5, 6))

    with raises_exception(
        AssertionError,
        contains_substring("to be called number of times: 4"),
    ):
        assert_that(mock1).matches(was_called().times(4))

    with raises_exception(
        AssertionError,
        contains_substring(
            "to be called with exact args and kwargs, args=(), kwargs=(a: 1) and call count should match 1"
        ),
    ):
        assert_that(mock1).matches(was_called_once_exactly_with(a=1))


def test_mock_does_not_match_matches_fails():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    with raises_exception(
        AssertionError,
        ends_with(
            "to not match: to be called with args=(1, 2), kwargs=() and call count should match >= 1"
        ),
    ):
        assert_that(mock1).does_not_match(was_called_with(1, 2))
