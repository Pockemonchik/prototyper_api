from sqlalchemy.orm import Mapped

from src.database.base_model import BaseSqlAchemyModel


class UserModel(BaseSqlAchemyModel):
    __tablename__ = "users"
    username: Mapped[str]
    password: Mapped[str]

    def __str__(self) -> str:
        return str(self.id) + self.username
