# from __future__ import annotations
from unittest.mock import Mock

from assertive.criteria import was_called, was_called_with
from assertive.criteria.basic import is_eq, is_gt, is_lt
from assertive.criteria.mock import (
    was_called_once_exactly_with,
    was_called_once_with,
    was_not_called_with,
)
from assertive.criteria.utils import ANY


def test_mock_matches_passes():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    assert mock1 == was_called_with(1, 2).once()
    assert mock1 == was_called_with(3, 4).once()
    assert mock1 == was_called_once_with(1, 2)
    assert mock1 == was_called().twice()
    assert mock1 == was_not_called_with(5, 6)
    assert mock1 == was_called_with(is_lt(2), is_gt(1)).once()

    mock2 = Mock()
    mock2(1, 2, x=3)
    mock2(1, 2, x=4)

    assert mock2 == was_called_with(1, 2, x=3).once()
    assert mock2 == was_not_called_with(1, 2, x=5)
    assert mock2 == was_called_with(1, 2, x=is_gt(2)).twice()

    mock3 = Mock()
    mock3(1, 2, x=3)
    mock3(1, 2, x=2)
    mock3(1, 2, x=3)
    mock3(1, 2, x=4)

    assert mock3 == was_called_with(1, 2, x=ANY).at_least_times(4)

    mock4 = Mock()
    mock4(1, 2, a=3, b=4)

    assert mock4 == was_called_once_with(1, 2, a=3)
    assert mock4 == was_called_once_exactly_with(1, 2, a=3, b=4)
    assert mock4 == was_called_once_exactly_with(1, 2, a=3, b=~is_eq(5))


def test_mock_does_not_match_passes():
    mock1 = Mock()
    mock1(1, 2)
    mock1(3, 4)

    assert mock1 != was_called_with(1, 2).twice()
    assert mock1 != was_called_with(3, 4).twice()
    assert mock1 != was_called().once()
