# Writing custom criteria

Assertive includes many built-in criteria, but you can create your own when you want domain-specific assertions.

The two most common approaches are:

1. Subclass `Criteria` and implement `_match`.
2. Subclass `WrappedCriteria` and compose existing criteria.

## 1) Subclassing `Criteria`

Implement `_match(subject) -> bool` with your matching rule.

```python
from assertive import Criteria


class is_uuid_like(Criteria):
    def _match(self, subject) -> bool:
        if not isinstance(subject, str):
            return False

        parts = subject.split("-")
        return len(parts) == 5 and all(parts)


assert "123e4567-e89b-12d3-a456-426614174000" == is_uuid_like()
assert "not-a-uuid" != is_uuid_like()
```

## 2) Subclassing `WrappedCriteria`

`WrappedCriteria` is useful when your custom criteria should delegate to existing criteria.

```python
from assertive import WrappedCriteria, is_gt, is_lt


class is_small_positive_number(WrappedCriteria):
    def __init__(self):
        super().__init__(is_gt(0) & is_lt(10))


assert 5 == is_small_positive_number()
```

## Composition with built-ins

All criteria can be composed using `&`, `|`, `^`, and `~`.

```python
from assertive import is_gt, is_lt

is_percentage = is_gt(0) & is_lt(101)

assert 42 == is_percentage
assert 120 != is_percentage
```

## Serialization support

If your criteria should work with `assertive.serialize.serialize()` and `deserialize()`, implement:

- `to_serialized(self) -> dict`
- `from_serialized(cls, serialized: dict) -> Criteria`

and add the class to `SERIALIZABLE_CRITERIA` in `assertive/serialize.py`.

## Common pitfalls

- **Type handling**: check `isinstance` when your criteria assumes a type.
- **Mutable state**: avoid keeping state that changes match outcomes across assertions.
- **Negation behavior**: if needed, override `_negated_match` for optimized or custom negation logic.
