# Fluent Assertions
A DSL like assertion library that enables concise high quality assertions in your tests

## Assertions

Assertions follow a simple pattern

```python
assert_that(subject).matches(comparison) # object or criteria
assert_that(subject).does_not_match(comparison) # object or criteria

# Same as above
assert_that(subject) == comparison # object or criteria
assert_that(subject) != comparison # object or criteria
```

Using matchers without criteria, just use classic asserts
```python
assert 2 == is_greater_than(1)
```

## Critera Objects

Critera helps define complex assertions in a concise manner

Some examples of criteria

```python
assert_that(5).matches(is_greater_than(4))
assert_that(5).matches(is_greater_than_or_equal(5))
assert_that(5).matches(is_odd())
```


### Logical criteria operations

```python
assert_that(5).matches(is_odd() & is_greater_than(4)) # And
assert_that(5).matches(is_odd() | is_greater_than(10)) # Or
assert_that(5).matches(~is_even()) # Inverted
```

## Matching

### Basic

#### is_equal_to
```python
assert_that(5).matches(5)
assert_that(5).matches(is_equal_to(5))

assert_that("hello").matches("hello")
assert_that("hello").matches(is_equal_to("hello"))
```

#### is_greater_than
```python
assert_that(5).matches(is_greater_than(3))
assert_that(5) == is_greater_than(3)
```


#### is_greater_than_or_equal
```python
assert_that(5).matches(is_greater_than_or_equal(5))
```

#### is_less_than
```python
assert_that(5).matches(is_less_than(10))
```

#### is_less_than_or_equal
```python
assert_that(5).matches(is_less_than_or_equal(10))
assert_that(5).matches(is_less_than_or_equal(5))
```


#### is_between
```python
assert_that(5).matches(is_between(5, 10)) # passes
assert_that(5).matches(is_between(5, 10).exclusive) # fails
assert_that(5).matches(is_between(5, 10).inclusive) # passes
```


#### is_same_instance_as
```python
x = "hello"
y = x

assert_that(x).matches(is_same_instance_as(y)) # passes
```

#### as_string_matches
When the subject called with the str the subject matches the criteria
```python
assert_that(5).matches(as_string_matches("5")) # passes
assert_that(12345).matches(as_string_matches(ends_with("45"))) # passes
```

### Exceptions
Exceptions can be tested in two different ways.
1. As a callable
```python
assert_that(lambda: my_exception_raising_method(123)).matches(raises_exception(Exception))
```

2. As a context manager
```python

with raises_exception(Exception):
    my_exception_raising_method(123)
```
