from functools import wraps
from unittest import mock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import text

from src.core.dependencies import get_session
from src.core.logger import logger
from src.database.base_model import BaseSqlAlchemyModel
from src.database.db_manager import AsyncPostgresDatabaseManager


def mock_cache(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            return await func(*args, **kwargs)

        return inner

    return wrapper


mock.patch("fastapi_cache.decorator.cache", mock_cache).start()


TEST_DB_URL = "postgresql+asyncpg://prototyper:prototyper@postgres:5432/prototyper_test"
TEST_DB_NAME = "prototyper_test"


@pytest.fixture()
def test_client() -> TestClient:

    from src.core.api import api  # обязательно импортим после мока редиса

    override_get_session = AsyncPostgresDatabaseManager(
        url=TEST_DB_URL,
        echo=True,
    ).get_async_session
    api.dependency_overrides[get_session] = override_get_session
    return TestClient(api)


# def run_migrations(connection) -> None:
#     logger.debug(f"Running DB migrations in {TEST_DB_URL}")
#     alembic_cfg = Config()
#     alembic_cfg.set_main_option("script_location", "src/database/migrations")
#     alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
#     alembic_cfg.attributes["connection"] = connection
#     command.upgrade(alembic_cfg, "head")


# @pytest_asyncio.fixture(autouse=True)
# async def migrate():
#     engine = AsyncPostgresDatabaseManager(
#         url=TEST_DB_URL,
#         echo=True,
#     ).engine
#     async with engine.begin() as conn:
#         await conn.run_sync(run_migrations)
#     yield


@pytest_asyncio.fixture()
async def fake_db_create():
    logger.debug(f"Database {TEST_DB_NAME} create start")
    engine = AsyncPostgresDatabaseManager(
        url=TEST_DB_URL,
        echo=True,
    ).engine

    try:
        conn = await engine.connect()
        await conn.close()
        logger.debug(f"Database {TEST_DB_NAME} exist")
    except Exception as exc:
        if "does not exist" in exc.__str__():
            logger.debug(f"Database {TEST_DB_NAME} NOT exist!")
            engine = AsyncPostgresDatabaseManager(
                url=TEST_DB_URL.replace(TEST_DB_NAME, ""),
                echo=True,
            ).engine
            async with engine.connect() as conn:
                await conn.execute(text("COMMIT"))
                await conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))  # type: ignore

            logger.debug(f"Database {TEST_DB_NAME} created")

        else:
            raise exc

    try:
        async with engine.begin() as conn:
            await conn.run_sync(BaseSqlAlchemyModel.metadata.create_all)
            await engine.dispose()
            yield
    except Exception as e:
        logger.error(f"err migrate {e}")
        raise e
    # TODO проверить работу
    # async with engine.begin() as conn:
    #     await conn.run_sync(BaseSqlAlchemyModel.metadata.drop_all)
    #     await engine.dispose()
