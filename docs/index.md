# Assertive

Assertive is a testing library that provides declarative assertions to you python tests.



## Criteria
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
