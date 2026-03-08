# Assertive

Assertive is a lightweight Python assertion library for writing declarative, composable test expectations.

## Install

```bash
pip install assertive
```

## Basic usage

Criteria are objects that implement a match operation. You compare a subject to criteria with `==`.

```python
from assertive import is_eq, is_gt, is_odd

assert 5 == is_eq(5)
assert 5 == is_gt(4)
assert 5 == is_odd()
```

## Composition

```python
from assertive import is_gt, is_lt, is_even

assert 8 == is_gt(0) & is_lt(10)
assert 8 == is_even() | is_lt(0)
assert 8 == ~is_lt(0)
```

## Nested Criteria

You can nest criteria inside other criteria. This is especially useful for dicts and lists.

### Dict values can be criteria

```python
from assertive import has_key_values, is_gt, starts_with

user = {"name": "Ada", "age": 37, "team": "platform"}

assert user == has_key_values({
    "name": starts_with("A"),
    "age": is_gt(18),
})
```

### List positions can be criteria

Use `contains_exactly` when position/order matters. You can place criteria in specific slots.

```python
from assertive import contains_exactly, is_gt, starts_with

record = ["user_123", 42, "active"]

assert record == contains_exactly(
    starts_with("user_"),  # first item
    is_gt(40),             # second item
    "active",              # third item
)
```

## Asserting Mock Calls

You can assert on `Mock` and `AsyncMock` interactions with the same criteria style.

```python
from unittest.mock import Mock
from assertive import was_called, was_called_once, was_called_once_with, was_called_with

gateway = Mock()
gateway.charge(customer_id="cus_123", amount=2500, currency="USD")

assert gateway.charge == was_called().once()
assert gateway.charge == was_called_once()
assert gateway.charge == was_called_with(customer_id="cus_123", amount=2500, currency="USD").once()
assert gateway.charge == was_called_once_with(amount=2500, currency="USD")
```

### Advanced example 1: rich argument matching with call-count constraints

```python
from unittest.mock import Mock
from assertive import is_gt, starts_with, was_called_with

gateway = Mock()
gateway.charge("cus_001", amount=1200, currency="USD", retry_count=1)
gateway.charge("cus_002", amount=2600, currency="USD", retry_count=2)

assert gateway.charge == was_called_with(
    starts_with("cus_"),
    amount=is_gt(1000),
    currency="USD",
    retry_count=is_gt(0),
).twice()
```

### Advanced example 2: async await assertions with nested criteria

```python
import asyncio
from unittest.mock import AsyncMock
from assertive import has_key_values, is_gt, was_awaited_once_with

publisher = AsyncMock()

async def publish():
    await publisher.send(
        "/events",
        payload={"type": "purchase", "amount": 4999, "meta": {"source": "checkout"}},
    )

asyncio.run(publish())

assert publisher.send == was_awaited_once_with(
    "/events",
    payload=has_key_values({"type": "purchase", "amount": is_gt(0)}),
)
```

## Documentation

- Docs site: <https://peter-daly.github.io/assertive/>
- Getting started page: <https://peter-daly.github.io/assertive/getting-started/>
- Criteria overview: <https://peter-daly.github.io/assertive/criteria/>
- Built-in criteria: <https://peter-daly.github.io/assertive/criteria/built-ins/>
- Composition guide: <https://peter-daly.github.io/assertive/criteria/composition/>
- Writing custom criteria: <https://peter-daly.github.io/assertive/criteria/writing-custom-criteria/>
