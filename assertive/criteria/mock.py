from unittest.mock import Mock

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.utils import (
    TimesMixin,
    WrappedCriteria,
)


class was_called_with(TimesMixin, Criteria):
    """
    A criteria that checks if a Mock object was called with specific arguments and keyword arguments.

    Args:
        *args: The expected positional arguments.
        **kwargs: The expected keyword arguments.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2, a=3, b=4)


        assert mock == was_called_with(1, 2, a=3) # Passes
        assert mock == was_called_with(1, 2, b=4) # Passes
        assert mock == was_called_with(is_odd(), is_even(), a=3) # Passes
        assert mock == was_called_with(is_odd(), is_even(), a=3).once() # Passes
        assert mock == was_called_with(is_odd(), is_even(), a=3).twice() # Fails
        assert mock == was_called_with(5, 3).never() # Passes

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
    A criteria that checks if a Mock object was called with specific arguments and keyword arguments.

    Args:
        *args: The expected positional arguments.
        **kwargs: The expected keyword arguments.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2, a=3, b=4)


        assert mock == was_called_exactly_with(1, 2, a=3) # Fails
        assert mock == was_called_exactly_with(1, 2, a=is_odd(), b=4) # Passes
        assert mock == was_called_exactly_with(is_odd(), is_even(), a=3).never() # Passes
        assert mock == was_called_exactly_with(is_odd(), is_even(), a=3, b=4).once() # Passes
        assert mock == was_called_exactly_with(1, 2).never() # Fails


        assert mock = was_called_exactly_with(1, 2, a=3, b=4) # Passes
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
    A criteria that checks if a mock object was called.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2)
        mock(3, 4)


        assert mock == was_called() # Passes
        assert mock == was_called().once() # Fails
        assert mock == was_called().never() # Fails
        assert mock == was_called().twice() # Passes
        assert mock == was_called().times(3) # Fails
        assert mock == was_called().at_least_times(1) # Passes


        assert mock = was_called() # Passes
        ```
    """

    def __init__(self):
        super().__init__()

    def _match(self, subject: Mock):
        return self.times_criteria.run_match(subject.call_count)


class was_called_once(WrappedCriteria):
    """
    A criteria that checks if a mock object was called once.

    Example:
        ```python
        # Simple usage
        mock1 = Mock()
        mock1(1, 2)

        mock2 = Mock()
        mock2(1, 2)
        mock2(3, 4)


        assert mock1 == was_called_once() # Passes
        assert mock2 == was_called_once() # Fails


        assert mock1 == was_called_once() # Passes
        assert mock2 == was_called_once() # Fails
        ```
    """

    def __init__(self):
        super().__init__(was_called().once())


class was_called_once_with(WrappedCriteria):
    """
    A criteria that checks if a mock object was called once, with args and kwargs.

    Args:
        *args: The expected positional arguments.
        **kwargs: The expected keyword arguments.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2)
        mock(3, 4)


        assert mock == was_called_once_with(1, 2) # Passes
        assert mock == was_called_once_with(4, 5) # Fails

        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_with(*args, **kwargs).once())


class was_called_once_exactly_with(WrappedCriteria):
    """
    A criteria that checks if a mock object was called once with strict matching on kwargs

    Args:
        *args: The expected positional arguments.
        **kwargs: The expected keyword arguments.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2, a=1, b=2)


        assert mock == was_called_once_exactly_with(1, 2, a=1, b=2) # Passes
        assert mock == was_called_once_exactly_with(1, 2, a=1) # Fails

        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_exactly_with(*args, **kwargs).once())


class was_not_called(WrappedCriteria):
    """
    A criteria that checks if a mock object was not called.

    Example:
        ```python
        # Simple usage
        mock0 = Mock()

        mock1 = Mock()
        mock1()


        assert mock0 == was_not_called() # Passes
        assert mock1 == was_not_called() # Fails

        ```
    """

    def __init__(self):
        super().__init__(was_called().never())


class was_not_called_with(WrappedCriteria):
    """
    A criteria that checks if a mock object was not called with args and kwargs.

    Args:
        *args: The expected positional arguments.
        **kwargs: The expected keyword arguments.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2)


        assert mock == was_not_called_with(3, 4) # Passes
        assert mock == was_not_called_with(1, 2) # Fails
        assert mock == was_not_called_with(is_odd(), is_even()) # Passes

        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_with(*args, **kwargs).never())


class was_not_called_exactly_with(WrappedCriteria):
    """
    A criteria that checks if a mock object was not called, with strict matching on kwargs

    Args:
        *args: The expected positional arguments.
        **kwargs: The expected keyword arguments.

    Example:
        ```python
        # Simple usage
        mock = Mock()
        mock(1, 2, a=3, b=4)


        assert mock == was_not_called_exactly_with(1, 2) # Passes
        assert mock == was_not_called_exactly_with(1, 2, a=3, b=4) # Fails
        assert mock == was_not_called_exactly_with(is_odd(), 2, a=3, b=is_even()) # Fails

        ```
    """

    def __init__(self, *args, **kwargs):
        super().__init__(was_called_exactly_with(*args, **kwargs).never())
