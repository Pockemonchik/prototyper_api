from src.core.dependencies import get_session
from fastapi import Request, HTTPException, status, Depends

from src.users.errors import AuthError
from src.users.repository import UsersRepository
from src.users.schemas import UserSchema
from src.users.service import AuthService


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


async def check_auth_dep(
    token: str = Depends(get_token_dep), session=Depends(get_session)
) -> UserSchema:
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

    return user  # type: ignore


async def get_current_user_id_dep(
    token: str = Depends(get_token_or_none_dep), session=Depends(get_session)
) -> int | None:
    """Получение id пользователя"""
    user_repo = UsersRepository(session=session)
    auth_service = AuthService(user_repo=user_repo)
    if not token:
        return None
    try:
        user_id = auth_service.check_access_token(token=token)
        return user_id
    except AuthError as e:
        return None
