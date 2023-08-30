from unittest.mock import Mock
from fluent_assertions.assertions import Criteria, ensure_criteria

from fluent_assertions.criteria.utils import (
    TimesMixin,
    joined_descriptions,
    joined_keyed_descriptions,
)


class was_called_with(TimesMixin, Criteria):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.expected_args = tuple(ensure_criteria(arg) for arg in args)
        self.expected_kwargs = {
            key: ensure_criteria(value) for key, value in kwargs.items()
        }

    def _match(self, mock_obj: Mock):
        if not isinstance(mock_obj, Mock):
            raise TypeError(f"Expected a Mock object, but got {type(mock_obj)}")

        matching_calls = [
            call_args
            for call_args in mock_obj.call_args_list
            if self._match_single_call(call_args)
        ]

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

    @property
    def description(self) -> str:
        args_str = joined_descriptions(self.expected_args)
        kw_args_str = joined_keyed_descriptions(self.expected_kwargs)

        return f"to be called with args=({args_str}), kwargs=({kw_args_str}) and call count should match {self.times_criteria.description}"


class was_called(TimesMixin, Criteria):
    def __init__(self):
        super().__init__()

    def _match(self, subject: Mock):
        return self.times_criteria.run_match(subject.call_count)

    @property
    def description(self) -> str:
        return f"to be called number of times: {self.times_criteria.description}"
