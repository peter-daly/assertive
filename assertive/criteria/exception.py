from types import TracebackType
from typing import Callable, Optional, Union
from assertive.assertions import Criteria, assert_that, ensure_criteria
from assertive.criteria.basic import as_string_matches
from assertive.criteria.object import is_type, is_exact_type
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

    def failure_message(self, subject) -> str:
        if not self.raised:
            return f"{subject} has not raised an exception"
        return f"{self.exception} should match {self.description}"

    def negated_failure_message(self, subject) -> str:
        if not self.raised:
            return f"{subject} has not raised an exception"
        return f"{self.exception} should not match {self.description}"

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        assert_that(exc_val).matches(self)
        return True


class raises(ExceptionCriteria):
    def __init__(self, critera: Criteria):
        super().__init__()
        self.criteria = critera

    def _match(self, subject: Callable) -> bool:
        if self.raised:
            return self.criteria.run_match(self.exception)
        return False

    @property
    def description(self) -> str:
        if not self.raised:
            return "exception has not been raised"

        return f"raises exception matching {self.criteria.description}"


class raises_exception(raises):
    """
    Checks that an exception has been raised that matchs
    """

    def __init__(
        self, type: type[Exception], string_critera: Union[str, Criteria] = ANY
    ):
        super().__init__(
            is_type(type) & as_string_matches(ensure_criteria(string_critera))
        )


class raises_exact_exception(raises):
    """
    Strict type on the exception has been raised that has been raised
    """

    def __init__(
        self, type: type[Exception], string_critera: Union[str, Criteria] = ANY
    ):
        super().__init__(
            is_exact_type(type) & as_string_matches(ensure_criteria(string_critera))
        )
