from assertive.criteria.basic import is_lt
from assertive.criteria.exception import raises_exception
from assertive.criteria.string import (
    contains_substring,
    ends_with,
    ignore_case,
    regex,
    starts_with,
)

# type


def test_type_failure():
    with raises_exception(TypeError):
        assert 1 == ends_with("1")

    with raises_exception(TypeError):
        assert 1 != ends_with("2")


# regex
def test_regex_matches_pass():
    assert "abc" == regex(r"abc")
    assert "abc" == regex(r"abc|def")


def test_regex_does_not_match_pass():
    assert "abc" != regex(r"def")


# starts_with
def test_starts_with_matches_pass():
    assert "abc" == starts_with("ab")


def test_starts_with_does_not_match_pass():
    assert "abc" != starts_with("b")


# ends_with
def test_ends_with_matches_pass():
    assert "abc" == ends_with("bc")


def test_ends_with_does_not_match_pass():
    assert "abc" != ends_with("b")


# contains_substring
def test_contains_substring_matches_pass():
    assert "abc" == contains_substring("bc")
    assert "hello hello hello said the police officer" == contains_substring("hello")

    assert "hello hello hello said the police officer" == contains_substring(
        "hello"
    ).times(3)

    assert "hello hello hello said the police officer" == contains_substring(
        "hello"
    ).at_least_times(2)

    assert "hello hello hello said the police officer" == contains_substring(
        "hello"
    ).times(is_lt(5))

    assert "abc" == contains_substring("hello").never()


def test_contains_substring_does_not_match_pass():
    assert "abc" != contains_substring("b").never
    assert "abc" != contains_substring("hello")


# ignore_case


def test_ignore_case_matches_pass():
    assert "abc" == ignore_case("ABC")
    assert "Hello World" == ignore_case("hello world")
    assert "MiXeD CaSe" == ignore_case("mixed case")


def test_ignore_case_does_not_match_pass():
    assert "abc" != ignore_case("def")
    assert "Hello" != ignore_case("Goodbye")


def test_ignore_case_type_failure():
    with raises_exception(TypeError):
        assert 123 == ignore_case("123")

    with raises_exception(TypeError):
        assert 123 != ignore_case("456")
