from typing import Any
from assertive.core import (
    AndCriteria,
    Criteria,
    InvertedCriteria,
    OrCriteria,
    XorCriteria,
    is_eq,
)
from assertive.criteria.mapping import has_exact_key_values, has_key_values
from assertive.criteria.numeric import is_even, is_odd
from .criteria.basic import (
    is_gt,
    is_lt,
    is_gte,
    is_lte,
    is_neq,
    is_between,
)

from .criteria.string import as_json_matches, ignore_case, regex

from .criteria.list import (
    contains,
    contains_exactly,
    has_length,
)

from bidict import bidict


SERIALIZABLE_CRITERIA = bidict(
    {
        "$gt": is_gt,
        "$gte": is_gte,
        "$lt": is_lt,
        "$lte": is_lte,
        "$between": is_between,
        "$eq": is_eq,
        "$neq": is_neq,
        "$and": AndCriteria,
        "$or": OrCriteria,
        "$xor": XorCriteria,
        "$not": InvertedCriteria,
        "$json": as_json_matches,
        "$contains": contains,
        "$contains_exactly": contains_exactly,
        "$regex": regex,
        "$length": has_length,
        "$key_values": has_key_values,
        "$exact_key_values": has_exact_key_values,
        "$even": is_even,
        "$odd": is_odd,
        "$ignore_case": ignore_case,
    }
)


def serialize(item: Any) -> Any:
    """
    Serializes a criteria object or any other item into a dictionary representation.
    """
    if isinstance(item, Criteria) and type(item) in SERIALIZABLE_CRITERIA.inverse:
        serial_key = SERIALIZABLE_CRITERIA.inverse[type(item)]  # type: ignore
        serialized_dict = item.to_serialized()
        serialized_dict = {k: serialize(v) for k, v in serialized_dict.items()}
        return {serial_key: serialized_dict}

    if isinstance(item, list):
        return [serialize(i) for i in item]

    if isinstance(item, dict):
        return {k: serialize(v) for k, v in item.items()}

    return item


def deserialize(item: Any) -> Criteria | Any:
    """
    Deserializes representation of criteria into a criteria object or a plain object.
    """

    if isinstance(item, dict):
        return_dict = {}
        for key, value in item.items():
            if key in SERIALIZABLE_CRITERIA:
                criteria_class = SERIALIZABLE_CRITERIA[key]
                kwargs = deserialize(value)
                return criteria_class.from_serialized(kwargs)  # type: ignore
            else:
                return_dict[key] = deserialize(value)
        return return_dict

    if isinstance(item, list):
        return [deserialize(item) for item in item]

    return item
