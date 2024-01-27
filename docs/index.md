# Assertive

Assertive is an assertions library that makes it easier to have flexible and intuative asserts for python.
Assertive has 2 main components.

:::assertive.assertions.Assertion
    options:
        members: false
        show_root_heading: true
        show_root_full_path: false
        show_bases: false
        show_source: false

:::assertive.assertions.Criteria
    options:
        members: false
        show_root_heading: true
        show_root_full_path: false
        show_bases: false
        show_source: false


## Assertions

```python
assert_that(5).matches(is_greater_than(4))
assert_that(5).matches(is_odd())
assert_that(5).matches(is_greater_than(4) & is_odd())
assert_that(5).does_not_match(is_even())
```


## Criteria
Criteria can be used with assertions or the class assert syntax
```python
assert_that(5).matches(is_greater_than(4))
assert_that(5).matches(is_odd())
assert_that(5).matches(is_greater_than(4) & is_odd())
assert_that(5).does_not_match(is_even())

assert 5 == is_greater_than(4)
assert 5 == is_odd()
assert 5 == is_greater_than(4) & is_odd()
assert 5 != is_even()
```