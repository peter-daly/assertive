import re
from fluent_assertions.assertions import Criteria
from fluent_assertions.criteria.utils import TimesMixin


class StringCriteria(Criteria):
    def _before_run(self, subject):
        if not isinstance(subject, str):
            raise TypeError(f"{subject} needs to be a string")

    def failure_message(self, subject) -> str:
        return f"Expected '{subject}' to match: {self.description}"

    def negated_failure_message(self, subject) -> str:
        return f"Expected '{subject}' to not match: {self.description}"


class regex(StringCriteria):
    def __init__(self, pattern):
        self.pattern = pattern

    def _match(self, subject) -> bool:
        return bool(re.match(self.pattern, subject))

    @property
    def description(self) -> str:
        return f"regex pattern '{self.pattern}'"


class starts_with(StringCriteria):
    def __init__(self, prefix):
        self.prefix = prefix

    def _match(self, subject: str) -> bool:
        return subject.startswith(self.prefix)

    @property
    def description(self):
        return f"starts with '{self.prefix}'"


class ends_with(StringCriteria):
    def __init__(self, suffix):
        self.suffix = suffix

    def _match(self, subject: str) -> bool:
        return subject.endswith(self.suffix)

    @property
    def description(self):
        return f"ends with '{self.suffix}'"


class contains_substring(TimesMixin, StringCriteria):
    def __init__(self, substring: str):
        super().__init__()
        self.substring = substring

    def _match(self, subject: str) -> bool:
        return self.times_criteria.run_match(subject.count(self.substring))

    @property
    def description(self):
        return f"contains '{self.substring}' with number of times matching: {self.times_criteria.description}"
