from dataclasses import dataclass

from assertive.core import assert_that
from assertive.criteria.basic import is_greater_than
from assertive.criteria.exception import raises_exception
from assertive.criteria.object import (
    class_match,
    has_attributes,
    is_exact_type,
    is_type,
)
from assertive.criteria.string import starts_with


@dataclass(kw_only=True)
class Parent:
    x: str
    y: int


@dataclass(kw_only=True)
class Child(Parent):
    z: float


# has_attributes
def test_has_attributes_matches_pass():
    assert_that(Parent(x="1", y=2)).matches(has_attributes(x="1", y=2))
    assert_that(Parent(x="1", y=2)).matches(has_attributes(x="1", y=is_greater_than(1)))


def test_has_attributes_does_not_match_pass():
    assert_that(Parent(x="1", y=2)).does_not_match(has_attributes(x="hello", y=2))
    assert_that(Parent(x="1", y=2)).does_not_match(
        has_attributes(x="1", y=is_greater_than(4))
    )


def test_has_attributes_matches_fail():
    with raises_exception(
        AssertionError,
        starts_with("Expected Parent(x='1', y=2) to match: has attributes (x: hello)"),
    ):
        assert_that(Parent(x="1", y=2)).matches(has_attributes(x="hello"))


def test_has_attributes_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected Parent(x='1', y=2) to not match: has attributes (y: 2)",
    ):
        assert_that(Parent(x="1", y=2)).does_not_match(has_attributes(y=2))


# is_type
def test_is_type_matches_pass():
    assert_that(Child(x="1", y=2, z=1.2)).matches(is_type(Child))
    assert_that(Child(x="1", y=2, z=1.2)).matches(is_type(Parent))
    assert_that("hello").matches(is_type(str))
    assert_that(1).matches(is_type(int))
    assert_that(1.2).matches(is_type(float))


def test_is_type_does_not_match_pass():
    assert_that("123").does_not_match(is_type(int))


def test_is_type_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 123 to match: is an instance of <class 'int'>",
    ):
        assert_that("123").matches(is_type(int))


def test_is_type_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 123 to not match: is an instance of <class 'str'>",
    ):
        assert_that("123").does_not_match(is_type(str))


# is_exact_type
def test_is_exact_type_matches_pass():
    assert_that(Child(x="1", y=2, z=1.2)).matches(is_exact_type(Child))
    assert_that("hello").matches(is_exact_type(str))
    assert_that(1).matches(is_exact_type(int))
    assert_that(1.2).matches(is_exact_type(float))


def test_is_exact_type_does_not_match_pass():
    assert_that("123").does_not_match(is_exact_type(int))
    assert_that(Child(x="1", y=2, z=1.2)).does_not_match(is_exact_type(Parent))


def test_is_exact_type_matches_fail():
    with raises_exception(
        AssertionError,
        "Expected 123 to match: is of type <class 'int'>",
    ):
        assert_that("123").matches(is_exact_type(int))


def test_is_exact_type_does_not_match_fail():
    with raises_exception(
        AssertionError,
        "Expected 123 to not match: is of type <class 'str'>",
    ):
        assert_that("123").does_not_match(is_exact_type(str))


# class_match
def test_class_match_matches_pass():
    instance = Child(x="1", y=2, z=1.2)

    assert_that(instance).matches(class_match(Child, z=1.2))
    assert_that(instance).matches(class_match(Parent, y=2))

    assert instance == class_match(Child, z=1.2)
    assert instance == class_match(Parent, y=2)
