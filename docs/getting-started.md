# Getting Started

## Install

```bash
pip install assertive
```

## Basic usage

Criteria are objects that implement a match operation. You compare a subject to criteria with `==`.

```python
from assertive import is_eq, is_gt, is_odd

assert 5 == is_eq(5)
assert 5 == is_gt(3)
assert 5 == is_odd()
```

## Composition

```python
from assertive import is_gt, is_lt, is_even

assert 8 == is_gt(0) & is_lt(10)
assert 8 == is_even() | is_lt(0)
assert 8 == ~is_lt(0)
```

## Next steps

- Learn the concept: [What Is Criteria?](criteria/what-is-criteria.md)
- Explore built-ins: [Built-in Criteria](criteria/built-ins.md)
- Build your own: [Writing Custom Criteria](criteria/writing-custom-criteria.md)
