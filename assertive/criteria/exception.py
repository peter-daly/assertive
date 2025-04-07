from types import TracebackType
from typing import Callable, Optional, Union

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.basic import as_string_matches
from assertive.criteria.object import is_exact_type, is_type
from assertive.criteria.utils import ANY


class ExceptionCriteria(Criteria):
    def __init__(self):
        self.exception = None
        self.raised = False

    def _before_run(self, subject):
        if callable(subject):
            try:
                subject()
            except Exception as ex:
                self.exception = ex
                self.raised = True
            return

        if not isinstance(subject, Exception):
            raise TypeError(f"{subject} needs to be an Exception or Callable")
        self.raised = True
        self.exception = subject

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        if not self.run_match(exc_val):
            raise AssertionError(
                f"Expected exception of type {self.exception.__class__.__name__}, but got {exc_val}"
            )
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        if not self.run_match(exc_val):
            raise AssertionError(
                f"Expected exception of type {self.exception.__class__.__name__}, but got {exc_val}"
            )
        return True


class raises(ExceptionCriteria):
    def __init__(self, criteria: Criteria):
        super().__init__()
        self.criteria = criteria

    def _match(self, subject: Callable) -> bool:
        if self.raised:
            return self.criteria.run_match(self.exception)
        return False


class raises_exception(raises):
    """
    Checks that an exception has been raised that is a subclass and message matches

    It can be used as a context manager or an async context manager

    Example:
        ```python
        def do_something():
            raise SpecificError("Something went wrong")

        with raises_exception(Exception):
            do_something() # Passes

        with raises_exception(Exception, "Something went wrong"):
            do_something() # Passes

        with raises_exception(SpecificError, "Something went wrong"):
            do_something() # Passes

        with raises_exception(SpecificError, "Something went very wrong"):
            do_something() # Fails

        with raises_exception(SpecificError, starts_with("Something went")):
            do_something() # Passes
        ```

    """

    def __init__(
        self, type: type[Exception], string_criteria: Union[str, Criteria] = ANY
    ):
        super().__init__(
            is_type(type) & as_string_matches(ensure_criteria(string_criteria))
        )


class raises_exact_exception(raises):
    """
    Strict type on the exception has been raised that has been raised

    It can be used as a context manager or an async context manager

    Example:
        ```python
        def do_something():
            raise SpecificError("Something went wrong")

        with raises_exact_exception(Exception):
            do_something() # Fails

        with raises_exact_exception(Exception, "Something went wrong"):
            do_something() # Fails

        with raises_exact_exception(SpecificError, "Something went wrong"):
            do_something() # Passes

        with raises_exact_exception(SpecificError, "Something went very wrong"):
            do_something() # Fails

        with raises_exact_exception(SpecificError, starts_with("Something went")):
            do_something() # Passes
        ```

    """

    def __init__(
        self, type: type[Exception], string_critera: Union[str, Criteria] = ANY
    ):
        super().__init__(
            is_exact_type(type) & as_string_matches(ensure_criteria(string_critera))
        )
