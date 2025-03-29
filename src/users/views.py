from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

import src.lessons.dependencies as lessons_deps
import src.users.dependencies as users_deps
from src.core.schemas import APIErrorMessage
from src.lessons.service import LessonsService
from src.users.schemas import (
    AuthRequestSchema,
    CreateUserSchema,
    SuccessAuthResponseSchema,
    UserProfileSchema,
)
from src.users.service import AuthService, UsersService

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@users_router.get(
    "/profile",
    response_model=UserProfileSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
    dependencies=[Depends(users_deps.get_token_dep)],
)
@cache(expire=100)
async def get_user_profile(
    users_service: Annotated[
        UsersService,
        Depends(users_deps.get_users_service_dep),
    ],
    lessons_service: Annotated[
        LessonsService, Depends(lessons_deps.get_lesson_service_dep)
    ],
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
) -> JSONResponse:
    """Получение профиля авторизованного пользователя"""

    user = await users_service.get_user_by_id(id=user_id)

    stats = await lessons_service.get_user_lessons_stats(user_id=user_id)
    response_data = UserProfileSchema.model_validate(
        {
            **user.__dict__,
            "lessons_stats": stats.model_dump(),
        }
    ).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@users_router.get(
    "/",
    response_model=List[UserProfileSchema],
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_users_list(
    users_service: Annotated[
        UsersService,
        Depends(users_deps.get_users_service_dep),
    ],
) -> JSONResponse:
    """Получение списка пользователей"""
    user_list = await users_service.get_users_list()
    response_data = [
        UserProfileSchema.model_validate(user).model_dump() for user in user_list
    ]

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@users_router.get(
    "/{id}",
    response_model=UserProfileSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_user_by_id(
    users_service: Annotated[
        UsersService,
        Depends(users_deps.get_users_service_dep),
    ],
    id: int,
) -> JSONResponse:
    """Получение пользователя по id"""
    user = await users_service.get_user_by_id(id=id)
    response_data = UserProfileSchema.model_validate(user).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@users_router.delete(
    "/{id}",
    response_model=str,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
async def delete_user_by_id(
    users_service: Annotated[
        UsersService,
        Depends(users_deps.get_users_service_dep),
    ],
    id: int,
) -> JSONResponse:
    """Удаление пользователя по id"""
    deleted_user_id = await users_service.delete_user_by_id(id=id)
    response_data = {"deleted": deleted_user_id}

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@auth_router.post(
    "/registration",
    response_model=SuccessAuthResponseSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
async def registration(
    request: CreateUserSchema,
    auth_service: Annotated[
        AuthService,
        Depends(users_deps.get_auth_service_dep),
    ],
) -> JSONResponse:
    """Регистрация пользователя"""
    token = await auth_service.register_user(request)

    return JSONResponse(content=token.model_dump(), status_code=status.HTTP_200_OK)


@auth_router.post(
    "/login",
    response_model=SuccessAuthResponseSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
async def login(
    request: AuthRequestSchema,
    auth_service: Annotated[
        AuthService,
        Depends(users_deps.get_auth_service_dep),
    ],
) -> JSONResponse:
    """Авторизация пользователя"""

    token = await auth_service.auth_user(request)

    return JSONResponse(content=token.model_dump(), status_code=status.HTTP_200_OK)
