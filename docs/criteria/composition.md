# Composition

Composition is the main advantage of criteria. You build larger expectations from smaller ones.

## Boolean operators

```python
from assertive import is_gt, is_lt, is_even

# AND: both must match
assert 8 == is_gt(0) & is_lt(10)

# OR: at least one must match
assert 8 == is_even() | is_lt(0)

# XOR: exactly one side must match
assert 8 == is_even() ^ is_lt(0)

# NOT: invert the condition
assert 8 == ~is_lt(0)
```

## Nest criteria inside criteria

Many criteria accept plain values or criteria objects.

```python
from assertive import class_match, is_gt, starts_with

assert user == class_match(User, age=is_gt(17), name=starts_with("A"))
```

## Compose collection rules

```python
from assertive import contains, has_length, is_gt

assert [1, 3, 5] == has_length(3) & contains(is_gt(0), 3)
```

## Compose mock behavior

```python
from assertive import was_called_with, is_gt

assert service_call == was_called_with("create", retry=is_gt(0)).once()
```

## Reuse composed criteria

```python
from assertive import is_gt, is_lt

adult_range = is_gt(17) & is_lt(66)

assert 25 == adult_range
assert 70 != adult_range
```

Composition works exactly the same for your own custom criteria.
