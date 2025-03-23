from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.dependencies as core_deps
import src.users.dependencies as users_deps
from src.core.schemas import APIErrorMessage
from src.users.repository import UsersRepository
from src.users.schemas import (
    AuthRequestSchema,
    CreateUserSchema,
    SuccessAuthResponseSchema,
    UserProfileSchema,
    UserSchema,
)
from src.users.service import AuthService

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
    response_model=UserSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
    dependencies=[Depends(users_deps.get_token_dep)],
)
@cache(expire=100)
async def get_user_profile(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
) -> JSONResponse:
    """Получение профиля авторизованного пользователя"""
    repository = UsersRepository(session=session)
    user = await repository.get_one(id=user_id)
    response_data = UserProfileSchema.model_validate(user).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@users_router.get(
    "/",
    response_model=List[UserSchema],
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_users_list(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
) -> JSONResponse:
    """Получение списка пользователей"""
    repository = UsersRepository(session=session)
    user_list = await repository.get_all()
    response_data = [UserSchema.model_validate(user).model_dump() for user in user_list]

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@users_router.get(
    "/{id}",
    response_model=UserSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_user_by_id(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    id: int,
) -> JSONResponse:
    """Получение пользователя по id"""
    repository = UsersRepository(session=session)
    user = await repository.get_one(id=id)
    response_data = UserSchema.model_validate(user).model_dump()

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
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    id: int,
) -> JSONResponse:
    """Удаление пользователя по id"""
    repository = UsersRepository(session=session)
    deleted_user_id = await repository.delete_one(id=id)
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
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
) -> JSONResponse:
    """Регистрация пользователя"""
    repository = UsersRepository(session=session)
    service = AuthService(user_repo=repository)
    token = await service.register_user(request)

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
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
) -> JSONResponse:
    """Авторизация пользователя"""
    repository = UsersRepository(session=session)
    service = AuthService(user_repo=repository)
    token = await service.auth_user(request)

    return JSONResponse(content=token.model_dump(), status_code=status.HTTP_200_OK)
