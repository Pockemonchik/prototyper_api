from redis import asyncio as aioredis  # type: ignore

from src.core import settings
from src.services.lessons_service import LessonsService

lessons_service = LessonsService()


def get_graph_service() -> LessonsService:
    return lessons_service


async def get_cache():
    redis = await aioredis.from_url(
        f"redis://{settings.redis_settings.address}",
        encoding="utf-8",
    )
    return redis
