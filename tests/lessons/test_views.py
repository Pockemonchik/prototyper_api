import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.asyncio
@pytest.mark.usefixtures("fake_db_create")
async def test_get_lessons(
    test_client: TestClient,
    request: pytest.FixtureRequest,
) -> None:
    response = test_client.get("/lessons/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
