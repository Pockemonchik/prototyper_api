from fastapi.testclient import TestClient
from pytest import FixtureRequest
from fastapi import status


def test_register(test_client: TestClient, request: FixtureRequest) -> None:

    payload = {"username": "test", "password": "test"}
    response = test_client.post(f"/auth/registration", data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()
