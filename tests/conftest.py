from functools import wraps
from unittest import mock

import pytest
from fastapi.testclient import TestClient


def mock_cache(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()


@pytest.fixture()
def test_client() -> TestClient:
    from src.core.api import api

    return TestClient(api)
