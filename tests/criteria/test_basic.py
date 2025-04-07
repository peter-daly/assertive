from assertive.criteria.basic import (
    as_string_matches,
    is_between,
    is_eq,
    is_gt,
    is_gte,
    is_lt,
    is_lte,
    is_none,
    is_not_none,
    is_same_instance_as,
)


# is_equal
def test_is_equal_to_matches_pass():
    assert 1 == is_eq(1)


def test_is_equal_to_does_not_match_pass():
    assert 0 != is_eq(1)


# is_greater_than
def test_is_greater_than_to_matches_pass():
    assert 2 == is_gt(1)
    assert 2 == is_gt(1)


def test_is_greater_than_to_does_not_match_pass():
    assert 0 != is_gt(1)


# is_greater_than_or_equal
def test_is_greater_than_or_equal_to_matches_pass():
    assert 2 == is_gte(1)
    assert 2 == is_gte(2)


def test_is_greater_than_or_equal_to_does_not_match_pass():
    assert 0 != is_gte(1)


# is_less_than
def test_is_less_than_matches_pass():
    assert 2 == is_lt(3)


def test_is_less_than_does_not_match_pass():
    assert 1 != is_lt(0)


# is_less_than_or_equal
def test_is_less_than_or_equal_matches_pass():
    assert 2 == is_lte(3)
    assert 3 == is_lte(3)


def test_is_less_than_or_equal_does_not_match_pass():
    assert 1 != is_lte(0)


# is_between
def test_is_between_matches_pass():
    assert 4 == is_between(3, 5).exclusive()
    assert 4 == is_between(4, 5).inclusive()
    assert 4 == is_between(3, 5)


def test_is_between_does_not_match_pass():
    assert 4 != is_between(4, 5).exclusive()
    assert 3 != is_between(4, 5)
    assert 3 != is_between(4, 5).inclusive()


# is_same_instance_as
def test_is_same_instance_as_matches_pass():
    x = 4
    y = x
    assert x == is_same_instance_as(y)


def test_is_same_instance_as_does_not_match_pass():
    x = 4
    y = 5
    assert x != is_same_instance_as(y)


# as_string_matches
def test_as_string_matches_matches_pass():
    assert 4 == as_string_matches(is_eq("4"))
    assert 4 == as_string_matches("4")


def test_as_string_matches_does_not_match_pass():
    assert 4 != as_string_matches("hello")


# is_none
def test_is_none_matches_pass():
    assert None == is_none()  # noqa: E711


def test_is_none_matches_does_not_match_pass():
    assert "hello" != is_none()


# is_not_none
def test_is_not_none_matches_pass():
    assert "None" == is_not_none()


def test_is_not_none_matches_does_not_match_pass():
    assert None is not is_not_none()
