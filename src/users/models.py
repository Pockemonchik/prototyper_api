from sqlalchemy.orm import Mapped

from src.database.base_model import BaseSqlAchemyModel
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship


if TYPE_CHECKING:
    from src.lessons.models import LessonResultModel
    from src.lessons.models import LessonStepResultModel


class UserModel(BaseSqlAchemyModel):
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
