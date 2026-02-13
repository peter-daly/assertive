# Assertive

Assertive is a lightweight Python assertion library for writing declarative, composable test expectations.

## Getting started

Install:

```bash
pip install assertive
```

Use criteria objects directly with `assert`:

```python
from assertive import (
    contains,
    has_key_values,
    is_even,
    is_gt,
    is_lt,
    regex,
)

assert 5 == is_gt(4)
assert 5 == is_gt(4) & is_lt(6)
assert 4 == is_even()
assert "hello" == regex(r"^h.*o$")
assert [1, 2, 3] == contains(2)
assert {"name": "Ada", "age": 37} == has_key_values({"name": "Ada"})
```

You can compose criteria with logical operators:

```python
assert 5 == is_gt(4) & is_lt(6)  # AND
assert 5 == is_even() | is_lt(6)  # OR
assert 5 == is_even() ^ is_lt(6)  # XOR
assert 5 == ~is_even()  # NOT
```

## Next steps

- Browse built-in criteria: [Criteria reference](criteria/)
- Build your own criteria: [Writing custom criteria](criteria/writing-custom-criteria/)
