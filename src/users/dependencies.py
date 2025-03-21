from src.core.dependencies import get_session
from fastapi import Request, HTTPException, status, Depends

from src.users.errors import AuthError
from src.users.repository import UsersRepository
from src.users.service import AuthService


def get_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


async def check_auth(token: str = Depends(get_token), session=Depends(get_session)):
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

    return user


async def get_current_user_id(
    token: str = Depends(get_token), session=Depends(get_session)
) -> int | None:
    user_repo = UsersRepository(session=session)
    auth_service = AuthService(user_repo=user_repo)

    try:
        user_id = auth_service.check_access_token(token=token)
        return user_id
    except AuthError as e:
        return None
