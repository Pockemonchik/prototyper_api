from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from src.database.base_model import BaseSqlAlchemyModel

if TYPE_CHECKING:
    from src.lessons.models import LessonResultModel, LessonStepResultModel


class UserModel(BaseSqlAlchemyModel):
    __tablename__ = "users"
    username: Mapped[str]
    password: Mapped[str]
    lessons_results: Mapped[List["LessonResultModel"]] = relationship(
        back_populates="user"
    )
    lessons_steps_results: Mapped[List["LessonStepResultModel"]] = relationship(
        back_populates="user"
    )

    def __str__(self) -> str:
        return str(self.id) + self.username
