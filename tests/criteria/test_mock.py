# from __future__ import annotations
from unittest.mock import Mock
from assertive.assertions import assert_that
from assertive.criteria import was_called_with, was_called
from assertive.criteria.basic import is_greater_than, is_less_than
from assertive.criteria.utils import ANY
from assertive.criteria.exception import raises_exception
from assertive.criteria.string import ends_with


def test_mock_matches_passes():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    assert_that(mock1).matches(was_called_with(1, 2).once)
    assert_that(mock1).matches(was_called_with(3, 4).once)
    assert_that(mock1).matches(was_called().twice)
    assert_that(mock1).matches(
        was_called_with(is_less_than(2), is_greater_than(1)).once
    )

    mock2 = Mock()
    mock2(1, 2, x=3)
    mock2(1, 2, x=4)

    assert_that(mock2).matches(was_called_with(1, 2, x=3).once)
    assert_that(mock2).matches(was_called_with(1, 2, x=5).never)
    assert_that(mock2).matches(was_called_with(1, 2, x=is_greater_than(2)).twice)

    mock3 = Mock()
    mock3(1, 2, x=3)
    mock3(1, 2, x=2)
    mock3(1, 2, x=3)
    mock3(1, 2, x=4)

    assert_that(mock3).matches(was_called_with(1, 2, x=ANY).at_least_times(4))


def test_mock_does_not_match_passes():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    assert_that(mock1).does_not_match(was_called_with(1, 2).twice)
    assert_that(mock1).does_not_match(was_called_with(3, 4).twice)
    assert_that(mock1).does_not_match(was_called().once)


def test_mock_matches_fails():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    with raises_exception(
        AssertionError,
        ends_with(
            "to match: to be called with args=(5, 6), kwargs=() and call count should match >= 1"
        ),
    ):
        assert_that(mock1).matches(was_called_with(5, 6))


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
