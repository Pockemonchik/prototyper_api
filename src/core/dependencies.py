from redis import asyncio as aioredis  # type: ignore

from src.core.settings import settings, redis_settings
from src.database.db_manager import AsyncPostgresDatabaseManager


get_session = AsyncPostgresDatabaseManager(
    url=settings.postgres_url,
    echo=settings.postgres_echo,
).get_async_session


async def get_cache():
    redis = await aioredis.from_url(
        f"redis://{redis_settings.address}",
        encoding="utf-8",
    )
    return redis
