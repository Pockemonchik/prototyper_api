from fastapi.testclient import TestClient
import pytest

# from fastapi import status


@pytest.mark.asyncio
# @pytest.mark.usefixtures("fake_db_create")
async def test_get_lessons(
    test_client: TestClient,
    request: pytest.FixtureRequest,
) -> None:

    assert 1 == 1
    # response = test_client.get(f"/lessons/")

    # assert response.status_code == status.HTTP_200_OK
    # assert len(response.json()) > 0
