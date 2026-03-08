# Built-in Criteria

Assertive ships with criteria across common testing domains.

## Basic

- `is_eq`, `is_neq`
- `is_gt`, `is_gte`, `is_lt`, `is_lte`, `is_between`
- `is_same_instance_as`
- `is_none`, `is_not_none`
- `as_string_matches`

## Numeric

- `is_even`, `is_odd`, `is_multiple_of`
- `is_positive`, `is_non_negative`, `is_negative`, `is_non_positive`
- `zero`, `approximately_zero`, `is_approximately_equal`
- `is_a_perfect_square`, `is_a_power_of`, `is_prime`, `is_coprime_with`
- `as_absolute_matches`

## String

- `regex`, `starts_with`, `ends_with`, `contains_substring`
- `ignore_case`, `as_json_matches`

## Iterable / List

- `has_length`, `is_empty`
- `contains`, `contains_exactly`

## Mapping / Dict

- `has_key_values`, `has_exact_key_values`
- `has_key_and_value`
- `contains_keys`, `contains_exact_keys`

## Object

- `has_attributes`
- `is_type`, `is_exact_type`
- `class_match`, `strict_class_match`

## Mock and AsyncMock

- Call checks: `was_called`, `was_called_with`, `was_called_exactly_with`, and `was_not_*` variants
- Await checks: `was_awaited`, `was_awaited_with`, `was_awaited_exactly_with`, and `was_not_*` variants
- Convenience wrappers: `*_once`, `*_once_with`, `*_once_exactly_with`

## Exception

- `raises`, `raises_exception`, `raises_exact_exception`

## Utilities

- `ANY`
- `PredicateCriteria`

## API reference

For full signatures and docstrings, see:

- [Basic API](../reference/criteria/basic.md)
- [Numeric API](../reference/criteria/numeric.md)
- [String API](../reference/criteria/string.md)
- [Iterable API](../reference/criteria/list.md)
- [Mapping API](../reference/criteria/mapping.md)
- [Object API](../reference/criteria/object.md)
- [Mock API](../reference/criteria/mock.md)
- [Exception API](../reference/criteria/exception.md)
