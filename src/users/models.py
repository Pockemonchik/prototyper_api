from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import BaseSqlAlchemyModel

if TYPE_CHECKING:
    from src.texts.models import TextResultModel
    from src.lessons.models import LessonStepResultModel


class UserModel(BaseSqlAlchemyModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)
    lessons_steps_results: Mapped[List["LessonStepResultModel"]] = relationship(
        back_populates="user"
    )

    def __str__(self) -> str:
        return str(self.id) + self.username
