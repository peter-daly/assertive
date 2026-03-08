from unittest.mock import AsyncMock, Mock

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import (
    TimesMixin,
    WrappedCriteria,
)


class was_called_with(TimesMixin, Criteria):
    """
    Match ``Mock`` instances with calls that include the given args/kwargs.

    Positional arguments must match exactly in count and order. Keyword
    arguments are treated as a subset match: expected keys must exist and
    match, but additional kwargs on the actual call are allowed.

    This criteria works with ``TimesMixin``. By default it expects at least
    one matching call.

    Args:
        *args: Expected positional arguments (values or criteria).
        **kwargs: Expected keyword arguments (values or criteria).

    Example:
        ```python
        mock = Mock()
        mock(1, 2, a=3, b=4)

        assert mock == was_called_with(1, 2, a=3)       # passes
        assert mock == was_called_with(1, 2, b=4)       # passes
        assert mock == was_called_with(1, 2, a=3).once() # passes
        assert mock == was_called_with(1, 2, a=3).twice() # fails
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.expected_args = tuple(ensure_criteria(arg) for arg in args)
        self.expected_kwargs = {
            key: ensure_criteria(value) for key, value in kwargs.items()
        }

    def _get_matching_calls(self, mock_obj: Mock):
        return [
            call_args
            for call_args in mock_obj.call_args_list
            if self._match_single_call(call_args)
        ]

    def _match(self, subject):
        matching_calls = self._get_matching_calls(subject)
        return self.times_criteria.run_match(len(matching_calls))

    def _match_single_call(self, call_args):
        actual_args, actual_kwargs = call_args

        # Validate positional arguments
        if len(actual_args) != len(self.expected_args):
            return False

        for actual, expected in zip(actual_args, self.expected_args):
            if not expected.run_match(actual):
                return False

        # Validate keyword arguments
        for key, expected in self.expected_kwargs.items():
            if key not in actual_kwargs or not expected.run_match(actual_kwargs[key]):
                return False

        return True


class was_called_exactly_with(TimesMixin, Criteria):
    """
    Match ``Mock`` calls with strict args and kwargs equality.

    Positional args must match in count and order. Keyword args must match
    exactly, including key set size (no missing or extra keys).

    This criteria also supports ``TimesMixin`` for call-count assertions.

    Args:
        *args: Expected positional arguments (values or criteria).
        **kwargs: Exact expected keyword arguments (values or criteria).

    Example:
        ```python
        mock = Mock()
        mock(1, 2, a=3, b=4)

        assert mock == was_called_exactly_with(1, 2, a=3, b=4) # passes
        assert mock == was_called_exactly_with(1, 2, a=3)      # fails
        assert mock == was_called_exactly_with(1, 2).never()   # passes
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.expected_args = tuple(ensure_criteria(arg) for arg in args)
        self.expected_kwargs = {
            key: ensure_criteria(value) for key, value in kwargs.items()
        }

    def _get_matching_calls(self, mock_obj: Mock):
        return [
            call_args
            for call_args in mock_obj.call_args_list
            if self._match_single_call(call_args)
        ]

    def _match(self, subject):
        matching_calls = self._get_matching_calls(subject)
        return self.times_criteria.run_match(len(matching_calls))

    def _match_single_call(self, call_args):
        actual_args, actual_kwargs = call_args

        # Validate positional arguments
        if len(actual_args) != len(self.expected_args):
            return False

        for actual, expected in zip(actual_args, self.expected_args):
            if not expected.run_match(actual):
                return False

        # Validate keyword arguments

        if len(self.expected_kwargs) != len(actual_kwargs):
            return False

        for key, expected in self.expected_kwargs.items():
            if key not in actual_kwargs or not expected.run_match(actual_kwargs[key]):
                return False

        return True


class was_called(TimesMixin, Criteria):
    """
    Match based on total ``Mock.call_count``.

    Default behavior is "called at least once". Use ``once()``, ``never()``,
    ``times(n)``, or other ``TimesMixin`` helpers to refine expectations.

    Example:
        ```python
        mock = Mock()
        mock(1, 2)
        mock(3, 4)

        assert mock == was_called()                 # passes
        assert mock == was_called().once()          # fails
        assert mock == was_called().twice()         # passes
        assert mock == was_called().at_least_times(1) # passes
        ```
    """

    def __init__(self):
        super().__init__()

    def _match(self, subject: Mock):
        return self.times_criteria.run_match(subject.call_count)


class was_called_once(WrappedCriteria):
    """
    Convenience wrapper for ``was_called().once()``.

    Example:
        ```python
        mock1 = Mock()
        mock1(1, 2)

        mock2 = Mock()
        mock2(1, 2)
        mock2(3, 4)

        assert mock1 == was_called_once() # passes
        assert mock2 == was_called_once() # fails
        ```
    """

    def __init__(self):
        super().__init__(was_called().once())


class was_called_once_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_called_with(...).once()``.

    Args:
        *args: Expected positional arguments.
        **kwargs: Expected keyword arguments (subset matching).

    Example:
        ```python
        mock = Mock()
        mock(1, 2)
        assert mock == was_called_once_with(1, 2) # passes
        assert mock == was_called_once_with(4, 5) # fails
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_with(*args, **kwargs).once())


class was_called_once_exactly_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_called_exactly_with(...).once()``.

    Args:
        *args: Expected positional arguments.
        **kwargs: Exact expected keyword arguments.

    Example:
        ```python
        mock = Mock()
        mock(1, 2, a=1, b=2)

        assert mock == was_called_once_exactly_with(1, 2, a=1, b=2) # passes
        assert mock == was_called_once_exactly_with(1, 2, a=1)      # fails
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_exactly_with(*args, **kwargs).once())


class was_not_called(WrappedCriteria):
    """
    Convenience wrapper for ``was_called().never()``.

    Example:
        ```python
        mock0 = Mock()

        mock1 = Mock()
        mock1()

        assert mock0 == was_not_called() # passes
        assert mock1 == was_not_called() # fails
        ```
    """

    def __init__(self):
        super().__init__(was_called().never())


class was_not_called_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_called_with(...).never()``.

    Args:
        *args: Positional arguments that must not be observed.
        **kwargs: Keyword arguments that must not be observed.

    Example:
        ```python
        mock = Mock()
        mock(1, 2)

        assert mock == was_not_called_with(3, 4) # passes
        assert mock == was_not_called_with(1, 2) # fails
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_with(*args, **kwargs).never())


class was_not_called_exactly_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_called_exactly_with(...).never()``.

    Args:
        *args: Positional arguments that must not be observed.
        **kwargs: Exact keyword argument set that must not be observed.

    Example:
        ```python
        mock = Mock()
        mock(1, 2, a=3, b=4)

        assert mock == was_not_called_exactly_with(1, 2)             # passes
        assert mock == was_not_called_exactly_with(1, 2, a=3, b=4)   # fails
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_exactly_with(*args, **kwargs).never())


class was_awaited_with(TimesMixin, Criteria):
    """
    Async equivalent of ``was_called_with`` for ``AsyncMock`` awaits.

    Positional args are exact by position and count. Keyword args are subset
    matched (expected keys must exist and match; extras are allowed).

    Args:
        *args: Expected positional await arguments.
        **kwargs: Expected keyword await arguments.

    Example:
        ```python
        mock = AsyncMock()
        await mock(1, x=2, y=3)

        assert mock == was_awaited_with(1, x=2)      # passes
        assert mock == was_awaited_with(1, x=2).once() # passes
        assert mock == was_awaited_with(1, x=9)      # fails
        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.expected_args = tuple(ensure_criteria(arg) for arg in args)
        self.expected_kwargs = {
            key: ensure_criteria(value) for key, value in kwargs.items()
        }

    def _get_matching_calls(self, mock_obj: AsyncMock):
        return [
            call_args
            for call_args in mock_obj.await_args_list
            if self._match_single_call(call_args)
        ]

    def _match(self, subject):
        matching_calls = self._get_matching_calls(subject)
        return self.times_criteria.run_match(len(matching_calls))

    def _match_single_call(self, call_args):
        actual_args, actual_kwargs = call_args

        if len(actual_args) != len(self.expected_args):
            return False

        for actual, expected in zip(actual_args, self.expected_args):
            if not expected.run_match(actual):
                return False

        for key, expected in self.expected_kwargs.items():
            if key not in actual_kwargs or not expected.run_match(actual_kwargs[key]):
                return False

        return True


class was_awaited_exactly_with(TimesMixin, Criteria):
    """
    Async equivalent of ``was_called_exactly_with`` for ``AsyncMock`` awaits.

    Keyword args are strict: expected and actual key sets must match exactly.

    Args:
        *args: Expected positional await arguments.
        **kwargs: Exact expected keyword await arguments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.expected_args = tuple(ensure_criteria(arg) for arg in args)
        self.expected_kwargs = {
            key: ensure_criteria(value) for key, value in kwargs.items()
        }

    def _get_matching_calls(self, mock_obj: AsyncMock):
        return [
            call_args
            for call_args in mock_obj.await_args_list
            if self._match_single_call(call_args)
        ]

    def _match(self, subject):
        matching_calls = self._get_matching_calls(subject)
        return self.times_criteria.run_match(len(matching_calls))

    def _match_single_call(self, call_args):
        actual_args, actual_kwargs = call_args

        if len(actual_args) != len(self.expected_args):
            return False

        for actual, expected in zip(actual_args, self.expected_args):
            if not expected.run_match(actual):
                return False

        if len(self.expected_kwargs) != len(actual_kwargs):
            return False

        for key, expected in self.expected_kwargs.items():
            if key not in actual_kwargs or not expected.run_match(actual_kwargs[key]):
                return False

        return True


class was_awaited(TimesMixin, Criteria):
    """
    Match based on total ``AsyncMock.await_count``.

    Default behavior is "awaited at least once". Use ``TimesMixin`` methods
    to express exact or minimum await counts.
    """

    def __init__(self):
        super().__init__()

    def _match(self, subject: AsyncMock):
        return self.times_criteria.run_match(subject.await_count)


class was_awaited_once(WrappedCriteria):
    """
    Convenience wrapper for ``was_awaited().once()``.
    """

    def __init__(self):
        super().__init__(was_awaited().once())


class was_awaited_once_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_awaited_with(...).once()``.

    Args:
        *args: Expected positional await arguments.
        **kwargs: Expected keyword await arguments (subset matching).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_awaited_with(*args, **kwargs).once())


class was_awaited_once_exactly_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_awaited_exactly_with(...).once()``.

    Args:
        *args: Expected positional await arguments.
        **kwargs: Exact expected keyword await arguments.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_awaited_exactly_with(*args, **kwargs).once())


class was_not_awaited(WrappedCriteria):
    """
    Convenience wrapper for ``was_awaited().never()``.
    """

    def __init__(self):
        super().__init__(was_awaited().never())


class was_not_awaited_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_awaited_with(...).never()``.

    Args:
        *args: Positional await arguments that must not occur.
        **kwargs: Keyword await arguments that must not occur.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_awaited_with(*args, **kwargs).never())


class was_not_awaited_exactly_with(WrappedCriteria):
    """
    Convenience wrapper for ``was_awaited_exactly_with(...).never()``.

    Args:
        *args: Positional await arguments that must not occur.
        **kwargs: Exact keyword await arguments that must not occur.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_awaited_exactly_with(*args, **kwargs).never())
