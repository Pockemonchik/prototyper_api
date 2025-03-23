from typing import List

from sqlalchemy import ForeignKey
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
    results: Mapped[List["LessonResultModel"]] = relationship(back_populates="lesson")
    steps: Mapped[List["LessonStepModel"]] = relationship(back_populates="lesson")

    def __str__(self) -> str:
        return str(self.name)


class LessonResultModel(BaseSqlAlchemyModel):
    """Результат прохождения урока пользователем"""

    __tablename__ = "lesson_results"
    percentage: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        nullable=True
    )  # success" | "fail" | "notchecked"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="lessons_results")

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    lesson: Mapped["LessonModel"] = relationship(back_populates="results")

    def __str__(self) -> str:
        return f"{str(self.user_id,)} {self.status}"


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
    name: Mapped[str]
    text: Mapped[str] = mapped_column(nullable=True)
    lesson_step_id: Mapped[int] = mapped_column(ForeignKey("lesson_steps.id"))
    lesson_step: Mapped["LessonStepModel"] = relationship(back_populates="texts")

    def __str__(self) -> str:
        return str(self.name)


class LessonStepResultModel(BaseSqlAlchemyModel):
    """Результаты этапа урока"""

    __tablename__ = "lesson_step_results"
    percentage: Mapped[int] = mapped_column(nullable=True)
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
    time: Mapped[str]
    date: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[str] = mapped_column(nullable=True)

    lesson_step_result_id: Mapped[int] = mapped_column(
        ForeignKey("lesson_step_results.id")
    )
    lesson_step_result: Mapped["LessonStepResultModel"] = relationship(
        back_populates="timings"
    )

    def __str__(self) -> str:
        return str(self.id)
