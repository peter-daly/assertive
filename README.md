# Assertive

Assertive is a testing library that provides declarative assertions to you python tests.


## Core of assertive

Assertive is built on two core concepts:

 1. Criteria
 2. Assertions


### Criteria
Criteria are declarative statements that can be used with assert statements to give a richer test experience.

```python
assert 5 == is_greater_than(4)
assert 5 == is_odd()
assert 5 != is_even()
```

Criteria can also be composed with logical operators to give a richer experience in writing tests

```python
assert 5 == is_greater_than(4) & is_less_than(6) # Using AND
assert 5 == is_even() | is_less_than(6) # Using OR
assert 5 == is_even() ^ is_odd() # Using XOR
assert 5 == ~is_even()  # Using INVERT
```


### Assertions
`Criteria` can be used with python's inbuilt `assert` statement or you can also use `Assertions` from the assertive library.
The key difference between `assert` and `Assertions` is that `Assertions` give a more detailed Assertion Error when the test fails.

To use `Assertions` you simple use the `assert_that()` function

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