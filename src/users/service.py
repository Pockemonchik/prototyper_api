from src.users.errors import AuthError, UserError
from src.users.repository import UsersRepository
from src.users.schemas import (
    CreateUserSchema,
    SuccessAuthResponseSchema,
    AuthRequestSchema,
)
import os
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext


class AuthService:
    def __init__(
        self,
        user_repo: UsersRepository,
    ) -> None:
        self.user_repo = user_repo

    @staticmethod
    def get_auth_config() -> dict:
        """Получение конфиков для создания и проверки токенов"""

        auth_data = {
            "secret_key": os.environ.get(
                "SECRET_KEY",
                "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt",
            ),
            "algorithm": os.environ.get(
                "ALGORITHM",
                "HS256",
            ),
        }

        return auth_data

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Создание токена"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        auth_data = AuthService.get_auth_config()
        encode_jwt = jwt.encode(
            to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"]
        )
        return encode_jwt

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Создание хэша"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверка валидности пароля"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

    def check_access_token(self, token: str) -> int:
        """Проверяет токен, возвращает id пользователя"""
        try:
            auth_data = AuthService.get_auth_config()
            payload = jwt.decode(
                token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]]
            )
        except JWTError:
            raise AuthError("Токен не валидный!")

        expire = payload.get("exp")
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)  # type: ignore
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise AuthError("Токен истек")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthError("Не найден ID пользователя")

        return int(user_id)

    async def auth_user(self, creds: AuthRequestSchema) -> SuccessAuthResponseSchema:
        """Авторизация пользователя"""
        users = await self.user_repo.filter_by_field(username=creds.username)

        if not users:
            raise UserError("User with this username not found!")
        else:
            user = users[0]
        if not self.verify_password(
            plain_password=creds.password,
            hashed_password=user.password,  # type: ignore
        ):
            raise UserError("Wrong password")
        access_token = self.create_access_token({"sub": str(user.id)})  # type: ignore
        return SuccessAuthResponseSchema(
            id=user.id,  # type: ignore
            username=user.username,  # type: ignore
            token=access_token,
        )

    async def register_user(
        self, input_dto: CreateUserSchema
    ) -> SuccessAuthResponseSchema:
        """Регистрация пользователя"""
        exist_user = await self.user_repo.filter_by_field(username=input_dto.username)
        if exist_user:
            raise UserError("User with this username already exist!")

        new_user = await self.user_repo.add_one(
            CreateUserSchema(
                username=input_dto.username,
                password=self.get_password_hash(input_dto.password),
            )
        )
        auth_data = await self.auth_user(
            AuthRequestSchema(
                username=new_user.username,  # type: ignore
                password=input_dto.password,
            )
        )
        return auth_data
