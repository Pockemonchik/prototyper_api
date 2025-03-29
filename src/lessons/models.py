from typing import List
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import BaseSqlAlchemyModel
from src.users.models import UserModel

# ------------ lesson -------------------


class LessonModel(BaseSqlAlchemyModel):
    """Урок по обучению печати"""

    __tablename__ = "lessons"
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(nullable=True)
    steps: Mapped[List["LessonStepModel"]] = relationship(back_populates="lesson")

    def __str__(self) -> str:
        return str(self.name)


# ------------ lesson step -------------------


class LessonStepModel(BaseSqlAlchemyModel):
    """Этап урока по обучению печати"""

    __tablename__ = "lesson_steps"
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    lesson: Mapped["LessonModel"] = relationship(back_populates="steps")

    texts: Mapped[List["LessonStepTextModel"]] = relationship(
        back_populates="lesson_step"
    )

    results: Mapped[List["LessonStepResultModel"]] = relationship(
        back_populates="lesson_step"
    )

    def __str__(self) -> str:
        return str(self.name)


class LessonStepTextModel(BaseSqlAlchemyModel):
    """Текст этапа урока"""

    __tablename__ = "lesson_step_texts"
    name: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)
    lesson_step_id: Mapped[int] = mapped_column(ForeignKey("lesson_steps.id"))
    lesson_step: Mapped["LessonStepModel"] = relationship(back_populates="texts")

    def __str__(self) -> str:
        return str(self.name)


class LessonStepResultModel(BaseSqlAlchemyModel):
    """Результаты этапа урока"""

    __tablename__ = "lesson_step_results"
    percentage: Mapped[int] = mapped_column(nullable=True)
    wpm: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        nullable=True
    )  # success" | "fail" | "notchecked"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="lessons_steps_results")

    lesson_step_id: Mapped[int] = mapped_column(ForeignKey("lesson_steps.id"))
    lesson_step: Mapped["LessonStepModel"] = relationship(back_populates="results")

    timings: Mapped[List["LessonStepTimingModel"]] = relationship(
        back_populates="lesson_step_result"
    )

    def __str__(self) -> str:
        return f"{str(self.user_id,)} {self.status}"


class LessonStepTimingModel(BaseSqlAlchemyModel):
    """Временные результаты прохождения этапа урока"""

    __tablename__ = "lesson_step_timings"
    seconds: Mapped[int] = mapped_column(nullable=True)
    created_date: Mapped[datetime] = mapped_column(server_default=func.now())

    lesson_step_result_id: Mapped[int] = mapped_column(
        ForeignKey("lesson_step_results.id")
    )
    lesson_step_result: Mapped["LessonStepResultModel"] = relationship(
        back_populates="timings"
    )

    def __str__(self) -> str:
        return str(self.id)
