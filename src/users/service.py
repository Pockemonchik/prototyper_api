from src.users.repository import UsersRepository
from src.users.schemas import AuthResponseSchema, CreateUserSchema


class AuthService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    async def register_user(self, user: CreateUserSchema) -> AuthResponseSchema:
        """Регистрация пользовталеля"""

        return AuthResponseSchema(token="123")

    async def auth_user(self, user: CreateUserSchema) -> AuthResponseSchema:
        """Регистрация пользовталеля"""

        return AuthResponseSchema(token="123")
