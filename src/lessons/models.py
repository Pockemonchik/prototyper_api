from sqlalchemy.orm import Mapped

from src.database.base_model import BaseModel


class LessonModel(BaseModel):
    __tablename__ = "lessons"
    name: Mapped[str]

    def __str__(self) -> str:
        return str(self.name)
