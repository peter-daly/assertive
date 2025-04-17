from dataclasses import dataclass

from assertive.criteria.basic import is_gt
from assertive.criteria.object import (
    class_match,
    has_attributes,
    is_exact_type,
    is_type,
)


@dataclass(kw_only=True)
class Parent:
    x: str
    y: int


@dataclass(kw_only=True)
class Child(Parent):
    z: float


# has_attributes
def test_has_attributes_matches_pass():
    assert Parent(x="1", y=2) == has_attributes(x="1", y=2)
    assert Parent(x="1", y=2) == has_attributes(x="1", y=is_gt(1))


def test_has_attributes_does_not_match_pass():
    assert Parent(x="1", y=2) != has_attributes(x="hello", y=2)
    assert Parent(x="1", y=2) != has_attributes(x="1", y=is_gt(4))


# is_type
def test_is_type_matches_pass():
    assert Child(x="1", y=2, z=1.2) == is_type(Child)
    assert Child(x="1", y=2, z=1.2) == is_type(Parent)
    assert "hello" == is_type(str)
    assert 1 == is_type(int)
    assert 1.2 == is_type(float)


def test_is_type_does_not_match_pass():
    assert "123" != is_type(int)


# is_exact_type
def test_is_exact_type_matches_pass():
    assert Child(x="1", y=2, z=1.2) == is_exact_type(Child)
    assert "hello" == is_exact_type(str)
    assert 1 == is_exact_type(int)
    assert 1.2 == is_exact_type(float)


def test_is_exact_type_does_not_match_pass():
    assert "123" != is_exact_type(int)
    assert Child(x="1", y=2, z=1.2) != is_exact_type(Parent)


# class_match
def test_class_match_matches_pass():
    instance = Child(x="1", y=2, z=1.2)

    assert instance == class_match(Child, z=1.2)
    assert instance == class_match(Parent, y=2)

    assert instance == class_match(Child, z=1.2)
    assert instance == class_match(Parent, y=2)
