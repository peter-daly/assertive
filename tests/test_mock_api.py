import json
import random
from assertive.core import is_eq
from assertive.mock_api import ApiRequest, MockApiClient


def test_simple_stubbing():
    mock_api = MockApiClient()

    some_id = random.randint(1, 1000)

    mock_api.when_requested_with(
        method="GET",
        path=f"/api/v1/resource/{some_id}",
    ).respond_with(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps({"id": some_id, "key": "value"}),
    )

    # Here I would call my actual service do-something/123

    # Simulate a request from the service
    response = mock_api.fake_api_call(
        method="GET",
        path=f"/api/v1/resource/{some_id}",
        headers={"Accept": "application/json"},
    )

    assert response is not None
    assert response.status_code == 200
    assert response.headers == {"Content-Type": "application/json"}
    assert response.body == json.dumps({"id": some_id, "key": "value"})

    assert mock_api.confirm(method=is_eq("GET"), path="/api/v1/resource/123")


def test_template_stubbing():
    mock_api = MockApiClient()

    some_id = random.randint(1, 1000)

    mock_api.when_requested_with(
        method="GET",
        path=f"/api/v1/resource/{some_id}",
    ).respond_with(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps({"id": some_id, "key": "value"}),
    )

    # Here I would call my actual service do-something/123

    # Simulate a request from the service
    response = mock_api.fake_api_call(
        method="GET",
        path=f"/api/v1/resource/{some_id}",
        headers={"Accept": "application/json"},
    )

    assert response is not None
    assert response.status_code == 200
    assert response.headers == {"Content-Type": "application/json"}
    assert response.body == json.dumps({"id": some_id, "key": "value"})

    assert mock_api.confirm(method=is_eq("GET"), path="/api/v1/resource/123")
