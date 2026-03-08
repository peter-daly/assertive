# What Is Criteria?

A **criteria** is an object that answers one question:

"Does this subject match the expectation?"

In Assertive, criteria are first-class values. You can pass them around, compose them, and reuse them.

## Mental model

- A **subject** is the value under test.
- A **criteria** is the expectation.
- `subject == criteria` runs the criteria match logic.

```python
from assertive import is_gte, is_lte

age = 21
assert age == is_gte(18) & is_lte(65)
```

## Why this style works

Inline assertions are fine for simple checks, but test intent often gets buried as checks grow.

Criteria keeps expectations declarative:

```python
from assertive import has_attributes, is_type

assert user == is_type(User) & has_attributes(active=True)
```

## Core properties

- Criteria can be negated with `~`.
- Criteria can be combined with `&`, `|`, and `^`.
- Most built-ins accept values **or other criteria** for nested matching.
- You can create custom criteria by subclassing `Criteria`.

Continue to [Built-in Criteria](built-ins.md) and [Composition](composition.md).
