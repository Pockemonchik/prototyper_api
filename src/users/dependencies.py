from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.users.errors import AuthError
from src.users.repository import UsersRepository
from src.users.service import AuthService, UsersService


async def get_auth_service_dep(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthService:
    """Получение сервиса auth"""
    users_repo = UsersRepository(session=session)

    service = AuthService(
        user_repo=users_repo,
    )
    return service


async def get_users_service_dep(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthService:
    """Получение сервиса auth"""
    users_repo = UsersRepository(session=session)

    service = UsersService(
        user_repo=users_repo,
    )
    return service


def get_token_dep(request: Request) -> str:
    """Получение токена  для роутов где обязатльно авторизоваться"""
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


def get_token_or_none_dep(request: Request) -> str | None:
    """Получение токена или None, для роутов где необязатльно авторизоваться"""
    token = request.headers.get("Authorization")
    if not token:
        return None
    return token


async def is_auth_dep(
    auth_service: Annotated[AuthService, Depends(get_auth_service_dep)],
    users_service: Annotated[UsersService, Depends(get_users_service_dep)],
    token: Annotated[str, Depends(get_token_dep)],
) -> bool:
    """Проверка авторизации пользователя"""

    try:
        user_id = auth_service.check_access_token(token=token)

    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

    user = await users_service.get_user_by_id()(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return True  # type: ignore


async def get_current_user_id_dep(
    token: Annotated[str, Depends(get_token_or_none_dep)],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dep)],
) -> int | None:
    """Получение id пользователя"""
    if not token:
        return None
    try:
        user_id = auth_service.check_access_token(token=token)
        return user_id
    except AuthError:
        return None


async def get_current_user_dep(
    token: Annotated[str, Depends(get_token_or_none_dep)],
    auth_service: Annotated[AuthService, Depends(get_auth_service_dep)],
) -> int | None:
    """Получение id пользователя"""
    if not token:
        return None
    try:
        user_id = auth_service.check_access_token(token=token)
        return user_id
    except AuthError:
        return None


async def is_current_user_admin_dep(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(get_token_dep)],
    is_auth_dep: Annotated[str, Depends(is_auth_dep)],
) -> bool:
    """Проверка авторизации пользователя"""
    user_repo = UsersRepository(session=session)
    auth_service = AuthService(user_repo=user_repo)

    try:
        user_id = auth_service.check_access_token(token=token)

    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)

    user = await user_repo.get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return True  # type: ignore
