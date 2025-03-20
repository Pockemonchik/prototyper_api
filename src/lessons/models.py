from sqlalchemy.orm import Mapped, mapped_column

from src.database.base_model import BaseSqlAchemyModel


class LessonModel(BaseSqlAchemyModel):
    __tablename__ = "lessons"
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)
    timing: Mapped[int] = mapped_column(nullable=True)
    percentage: Mapped[int] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        nullable=True
    )  # success" | "fail" | "notchecked"

    def __str__(self) -> str:
        return str(self.name)
