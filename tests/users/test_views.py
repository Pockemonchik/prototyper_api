# from fastapi.testclient import TestClient
# from fastapi import status
# import pytest


# @pytest.mark.usefixtures("fake_db_create")
# def test_register(test_client: TestClient, request: pytest.FixtureRequest) -> None:

#     payload = {"username": "test", "password": "test"}
#     response = test_client.post(f"/auth/registration", data=payload)

#     assert response.status_code == status.HTTP_200_OK
#     assert "token" in response.json()
