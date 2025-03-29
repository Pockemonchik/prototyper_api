from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from sqladmin import Admin

from redis import asyncio as aioredis  # type: ignore
from src.core import settings
from src.core.admin import (
    LessonModelAdmin,
    LessonStepModelAdmin,
    LessonStepResultModelAdmin,
    LessonStepTextModelAdmin,
    LessonStepTimingModelAdmin,
    UserModelAdmin,
)
from src.core.errors import ResourceNotFoundError
from src.core.logger import logger
from src.core.schemas import APIErrorMessage
from src.database.db_manager import AsyncPostgresDatabaseManager
from src.lessons.views import router as lessons_router
from src.texts.views import router as texts_router
from src.users.errors import AuthError
from src.users.views import auth_router, users_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Start redis session")
    redis = await aioredis.from_url(
        f"redis://{settings.redis_settings.address}:{settings.redis_settings.port}",
        decode_responses=False,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    logger.info("Close redis session")
    await redis.close()


api = FastAPI(
    title="API",
    description="API",
    version="1.0",
    lifespan=lifespan,
)


api.include_router(lessons_router)
api.include_router(texts_router)
api.include_router(users_router)
api.include_router(auth_router)

admin = Admin(
    api, AsyncPostgresDatabaseManager(url=settings.settings.postgres_url).engine
)

admin.add_view(UserModelAdmin)
admin.add_view(LessonModelAdmin)
admin.add_view(LessonStepModelAdmin)
admin.add_view(LessonStepTextModelAdmin)
admin.add_view(LessonStepResultModelAdmin)
admin.add_view(LessonStepTimingModelAdmin)


Instrumentator().instrument(api).expose(api)

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


@api.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__,
        message="Oops! Something went wrong, please try again later...",
    )
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content=error_msg.model_dump(),
    )


@api.exception_handler(ResourceNotFoundError)
async def resource_not_found_error_handler(
    request: Request, exc: ResourceNotFoundError
) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__,
        message=f"{exc.args}",
    )
    logger.error(exc)
    return JSONResponse(
        status_code=404,
        content=error_msg.model_dump(),
    )


@api.exception_handler(AuthError)
async def auth_error_handler(
    request: Request, exc: AuthError
) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__,
        message=f"{exc.args}",
    )
    logger.error(exc)
    return JSONResponse(
        status_code=401,
        content=error_msg.model_dump(),
    )
