from fastapi.testclient import TestClient
from pytest import FixtureRequest
from fastapi import status


def test_get_lessons(test_client: TestClient, request: FixtureRequest) -> None:

    response = test_client.get(f"/lessons/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
