from assertive.criteria.basic import is_between, is_gt, is_lt
from assertive.criteria.mapping import has_exact_key_values, has_key_values
from assertive.criteria.numeric import is_even
from assertive.criteria.string import regex, as_json_matches
from assertive.criteria.list import contains
from assertive.serialize import deserialize, serialize

import json


def test_basic_serialize():
    """
    Test the serialization of basic criteria
    """
    assert serialize(is_gt(1)) == {"$gt": {"value": 1}}


def test_complex_serialize():
    """
    Test the serialization of basic criteria
    """

    criteria = is_gt(1) & is_lt(10)

    assert serialize(criteria) == {
        "$and": {
            "items": [
                {"$gt": {"value": 1}},
                {"$lt": {"value": 10}},
            ]
        }
    }


def test_also_complex_serialize():
    """
    Test the serialization of basic criteria
    """

    criteria = is_gt(1) | 20

    serialized = serialize(criteria)
    assert serialized == {
        "$or": {
            "items": [
                {"$gt": {"value": 1}},
                {"$eq": {"value": 20}},
            ]
        }
    }


def test_complex_deserialize():
    """
    Test the serialization of basic criteria
    """
    start = {
        "$and": {
            "items": [
                {"$gt": {"value": 1}},
                {"$lt": {"value": 10}},
            ]
        }
    }

    result = deserialize(start)

    end = serialize(result)
    assert start == end


def test_basic_deserialize():
    """
    Test the serialization of basic criteria
    """
    start = {"$gt": {"value": 1}}

    result = deserialize(start)

    end = serialize(result)
    assert start == end


def test_simulate_json_serialization():
    """
    Test the serialization of basic criteria
    """

    request = {
        "status_code": is_between(200, 299),
    }

    serialized = serialize(request)
    serialized_json = json.dumps(serialized)

    deserialized = json.loads(serialized_json)
    deserialized_request = deserialize(deserialized)

    compare = {"status_code": 201}

    assert compare["status_code"] == deserialized_request["status_code"]  # type: ignore


def test_json_matches():
    """
    Test the serialization of basic criteria
    """

    body = {
        "key": "value",
    }

    criteria = as_json_matches(body)

    serialized = serialize(criteria)

    deserialized = deserialize(serialized)

    assert deserialized == json.dumps(body)


def test_contains_serialized():
    items = [1, 2, 3, 4, 5]

    criteria = contains(1, 2, 3)

    serialized = serialize(criteria)
    deserialized = deserialize(serialized)
    assert deserialized == items


def test_regex_pattern():
    item = "hello world"
    pattern = "hello"

    criteria = regex(pattern)

    serialized = serialize(criteria)
    deserialized = deserialize(serialized)
    assert deserialized == item


def test_is_even():
    """
    Test the serialization of basic criteria
    """

    item = 4
    criteria = is_even()

    serialized = serialize(criteria)
    deserialized = deserialize(serialized)
    assert deserialized == item


def test_very_nested_criteria():
    """
    Test the serialization of basic criteria
    """

    item = 4
    criteria = has_exact_key_values(
        {
            "key1": is_even(),
            "key2": has_key_values(
                {
                    "keya": is_between(1, 10),
                    "keyb": is_gt(20),
                }
            ),
            "key3": regex("hello"),
        }
    )

    item = {
        "key1": 4,
        "key2": {"keya": 5, "keyb": 21},
        "key3": "hello world",
    }

    serialized = serialize(criteria)
    deserialized = deserialize(serialized)
    assert deserialized == item
