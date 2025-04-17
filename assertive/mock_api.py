"""
This is a test bed for the assertive-mock-api.
"""

from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel

from assertive.core import Criteria
from assertive.criteria.basic import is_gte
from assertive.serialize import serialize, deserialize


class ApiRequest(BaseModel):
    path: str
    method: str
    headers: dict
    body: Any
    host: str
    query: dict


class ApiAssertion(BaseModel):
    path: Any
    method: Any
    headers: Any
    body: Any
    host: Any
    query: Any
    times: Any

    def _request_criteria(self) -> dict:
        request_dict = self.model_dump()
        return deserialize(request_dict)  # type: ignore

    def _matches_request(self, request: ApiRequest, criteria: dict) -> bool:
        """
        Check if the request matches the stub.
        """

        fields_to_check = ["method", "path", "headers", "body", "host", "query"]
        for field in fields_to_check:
            if criteria[field] is not None:
                if getattr(request, field) != criteria[field]:
                    return False
        return True

    def matches_requests(self, requests: list[ApiRequest]) -> bool:
        criteria = self._request_criteria()
        matches = [
            requests for request in requests if self._matches_request(request, criteria)
        ]

        return len(matches) == criteria["times"]


class StubRequest(BaseModel):
    """
    A stub request object for testing purposes.
    """

    method: Any | None = None
    path: Any | None = None
    headers: Any | None = None
    body: Any | None = None
    host: Any | None = None
    query: Any | None = None

    class Config:
        arbitrary_types_allowed = True


class StubResponse(BaseModel):
    """
    A stub response object for testing purposes.
    """

    status_code: int
    headers: dict
    body: Any

    class Config:
        arbitrary_types_allowed = True


class StubAction(BaseModel):
    """
    A stub action object for testing purposes.
    """

    response: StubResponse

    class Config:
        arbitrary_types_allowed = True


@dataclass
class StubMatch:
    strength: int
    stub: "Stub"


class Stub(BaseModel):
    """
    A stub object for testing purposes.
    """

    request: StubRequest
    action: StubAction

    def _request_criteria(self) -> dict:
        request_dict = self.request.model_dump()
        return deserialize(request_dict)  # type: ignore

    def matches_request(self, request: ApiRequest) -> StubMatch:
        """
        Check if the request matches the stub.
        """
        request_dict = self._request_criteria()
        strength = 0
        fields_to_check = ["method", "path", "headers", "body", "host", "query"]

        for field in fields_to_check:
            if request_dict[field] is not None:
                if getattr(request, field) != request_dict[field]:
                    return StubMatch(strength=0, stub=self)
                strength += 1

        return StubMatch(strength=strength, stub=self)


class RequestLog:
    def __init__(self):
        self.requests: list[ApiRequest] = []

    def add(self, request: ApiRequest) -> None:
        """
        Adds a request to the log.
        """
        self.requests.append(request)

    def get_requests(self) -> list[ApiRequest]:
        """
        Finds all requests that match the given assertion.
        """
        return self.requests


class StubRepository:
    def __init__(self):
        self.stubs: list[Stub] = []

    def add(self, stub: Stub) -> None:
        """
        Adds a stub to the repository.
        """
        self.stubs.append(stub)

    def find_best_match(self, request: ApiRequest) -> Stub | None:
        """
        Finds the best match for the given request.
        """
        best_match = None
        best_strength = 0

        for stub in self.stubs:
            match = stub.matches_request(request)
            if match.strength > best_strength:
                best_strength = match.strength
                best_match = match.stub

        return best_match

    class Config:
        arbitrary_types_allowed = True


class PreStubbedRequest:
    def __init__(self, mock_api: "MockApiClient", request: StubRequest):
        self.mock_api = mock_api
        self.request = request

    def respond_with(self, status_code: int, headers: dict, body: Any) -> None:
        """
        Responds with the given response.
        """
        response = StubResponse(
            status_code=status_code,
            headers=headers,
            body=body,
        )

        action = StubAction(response=response)
        stub = Stub(request=self.request, action=action)
        self.mock_api.stub(stub)


class MockApiResponse(BaseModel):
    status_code: int
    headers: dict
    body: Any

    @staticmethod
    def no_stub_found() -> "MockApiResponse":
        """
        Returns a response indicating that no stub was found.
        """
        return MockApiResponse(
            status_code=404,
            headers={},
            body="NO_STUB_MATCH_FOUND",
        )

    @staticmethod
    def from_stub(stub: Stub, request: ApiRequest) -> "MockApiResponse":
        """
        Converts a stub to a MockApiResponse.

        If a body_template is provided and a request object is available,
        the template will be rendered using Jinja2 with the request as context.
        """
        body = None
        if stub.action.response.body:
            body = stub.action.response.body

        return MockApiResponse(
            status_code=stub.action.response.status_code,
            headers=stub.action.response.headers,
            body=body,
        )


class MockApiServer:
    """
    A mock API server for testing purposes.
    """

    def __init__(self):
        self.stub_repository: StubRepository = StubRepository()
        self.request_log: RequestLog = RequestLog()

    def handle_request(self, request: ApiRequest) -> MockApiResponse:
        """
        Handles the given request and returns a response.
        """
        self.request_log.add(request)

        best_match = self.stub_repository.find_best_match(request)
        if best_match is None:
            return MockApiResponse.no_stub_found()
        return MockApiResponse.from_stub(best_match, request)

    def stub(self, stub: Stub) -> None:
        """
        Stubs a request with the given parameters.
        """
        self.stub_repository.add(stub)

    def confirm(self, assertion: ApiAssertion) -> bool:
        # Simulate it going over the wire

        requests = self.request_log.get_requests()
        return assertion.matches_requests(requests)


class MockApiClient:
    def __init__(self):
        self.mock_api_server = MockApiServer()

    def when_requested_with(
        self,
        host: str | Criteria | None = None,
        headers: dict | Criteria | None = None,
        path: str | Criteria | None = None,
        method: str | Criteria | None = None,
        body: Any | None = None,
    ) -> "PreStubbedRequest":
        return PreStubbedRequest(
            self,
            StubRequest(
                headers=serialize(headers),
                path=serialize(path),
                method=serialize(method),
                body=serialize(body),
                host=serialize(host),
            ),
        )

    def stub(self, stub: Stub) -> None:
        """
        Stubs a request with the given parameters.
        """
        # Simulate an API call
        serialized_stub = stub.model_dump_json()
        de_stub = Stub.model_validate_json(serialized_stub)

        self.mock_api_server.stub(de_stub)

    def confirm(
        self,
        host: str | Criteria | None = None,
        path: str | Criteria | None = None,
        method: str | Criteria | None = None,
        headers: dict | Criteria | None = None,
        body: Any | None = None,
        query: dict | Criteria | None = None,
        times: int | Criteria | None = is_gte(1),
    ) -> bool:
        """
        Confirms that the request was made.
        """

        assertion = ApiAssertion(
            path=serialize(path),
            method=serialize(method),
            headers=serialize(headers),
            body=serialize(body),
            times=serialize(times),
            host=serialize(host),
            query=serialize(query),
        )
        # Simulate an API call
        serialized_assertion = assertion.model_dump_json()
        de_assertion = ApiAssertion.model_validate_json(serialized_assertion)

        return self.mock_api_server.confirm(de_assertion)

    def fake_api_call(
        self,
        *,
        method: str,
        path: str,
        host: str = "localhost",
        body: str | bytes | None = None,
        query: dict = {},
        headers: dict = {},
    ) -> MockApiResponse:
        """
        This is faking an actual API call that will happen on the mock API Server
        Fakes an API call and returns the response.
        This will simulate how it exists in the real world.
        """

        request = ApiRequest(
            method=method,
            path=path,
            headers=headers,
            body=body,
            host=host,
            query=query,
        )
        return self.mock_api_server.handle_request(request)
