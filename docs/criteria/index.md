# Criteria

Criteria are reusable expectation objects used in assertions.

Instead of embedding all test logic inline, you describe the expected behavior once and compose it across tests.

## Quick example

```python
from assertive import has_key_values, is_gt, is_lt

assert {"age": 37} == has_key_values({"age": is_gt(17) & is_lt(66)})
```

## In this section

- [What Is Criteria?](what-is-criteria.md)
- [Built-in Criteria](built-ins.md)
- [Composition](composition.md)
- [Writing Custom Criteria](writing-custom-criteria.md)
