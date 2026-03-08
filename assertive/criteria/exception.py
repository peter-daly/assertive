from types import TracebackType
from typing import Callable, Optional, Union

from assertive.core import Criteria, ensure_criteria
from assertive.criteria.basic import as_string_matches
from assertive.criteria.object import is_exact_type, is_type
from assertive.criteria.utils import ANY


class ExceptionCriteria(Criteria):
    """
    Base criteria for exception assertions.

    Supports two usage styles:
    1. Direct matching against an exception instance or callable.
    2. Context manager (sync or async) around code expected to raise.

    Subclasses provide the actual exception matching rules.
    """

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
    """
    Generic exception matcher driven by a nested criteria.

    Args:
        criteria: Criteria evaluated against the captured exception instance.
    """

    def __init__(self, criteria: Criteria):
        super().__init__()
        self.criteria = criteria

    def _match(self, subject: Callable) -> bool:
        if self.raised:
            return self.criteria.run_match(self.exception)
        return False


class raises_exception(raises):
    """
    Match raised exceptions by type compatibility and message criteria.

    The exception type check uses ``isinstance`` semantics (subclasses pass).
    The message check is performed against ``str(exception)`` and can be a
    plain string or any criteria.

    This criteria can be used directly, as a context manager, or as an async
    context manager.

    Example:
        ```python
        def do_something():
            raise SpecificError("Something went wrong")

        with raises_exception(Exception):
            do_something() # passes

        with raises_exception(Exception, "Something went wrong"):
            do_something() # passes

        with raises_exception(SpecificError, "Something went wrong"):
            do_something() # passes

        with raises_exception(SpecificError, "Something went very wrong"):
            do_something() # fails

        with raises_exception(SpecificError, starts_with("Something went")):
            do_something() # passes
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
    Match raised exceptions by exact type and message criteria.

    Unlike ``raises_exception``, this requires ``exception.__class__ == type``
    and does not allow subclasses.

    This criteria can be used directly, as a context manager, or as an async
    context manager.

    Example:
        ```python
        def do_something():
            raise SpecificError("Something went wrong")

        with raises_exact_exception(Exception):
            do_something() # fails

        with raises_exact_exception(Exception, "Something went wrong"):
            do_something() # fails

        with raises_exact_exception(SpecificError, "Something went wrong"):
            do_something() # passes

        with raises_exact_exception(SpecificError, "Something went very wrong"):
            do_something() # fails

        with raises_exact_exception(SpecificError, starts_with("Something went")):
            do_something() # passes
        ```

    """

    def __init__(
        self, type: type[Exception], string_critera: Union[str, Criteria] = ANY
    ):
        super().__init__(
            is_exact_type(type) & as_string_matches(ensure_criteria(string_critera))
        )
