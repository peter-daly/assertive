# Assertive

Assertive is a lightweight Python assertion library for writing declarative, composable test expectations.

## Install

```bash
pip install assertive
```

## Quickstart

```python
from assertive import (
    contains,
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
```

You can compose criteria with boolean operators:

```python
assert 5 == is_gt(4) & is_lt(6)  # AND
assert 5 == is_even() | is_lt(6)  # OR
assert 5 == is_even() ^ is_lt(6)  # XOR
assert 5 == ~is_even()  # NOT
```

## Documentation

- User guide: <https://peter-daly.github.io/assertive/>
- Criteria reference: <https://peter-daly.github.io/assertive/criteria/>
- Writing custom criteria: <https://peter-daly.github.io/assertive/criteria/writing-custom-criteria/>
