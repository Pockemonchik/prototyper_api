from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_model import BaseSqlAlchemyModel

if TYPE_CHECKING:
    from src.users.models import UserModel


class TextConfigModel(BaseSqlAlchemyModel):
    __tablename__ = "text_configs"
    description: Mapped[str] = mapped_column(nullable=True)
    punctuation: Mapped[bool] = mapped_column(default=False, nullable=True)
    textType: Mapped[str] = mapped_column(nullable=True)
    texts: Mapped[List["TextModel"]] = relationship(back_populates="config")

    def __str__(self) -> str:
        return str(self.id)


class TextModel(BaseSqlAlchemyModel):
    __tablename__ = "texts"
    text: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    config_id: Mapped[int] = mapped_column(ForeignKey("text_configs.id"))
    config: Mapped["TextConfigModel"] = relationship(back_populates="texts")
    results: Mapped[List["TextResultModel"]] = relationship(back_populates="text")

    def __str__(self) -> str:
        return str(self.id)


class TextResultModel(BaseSqlAlchemyModel):
    """Результаты набора текста"""

    __tablename__ = "text_results"
    percentage: Mapped[int] = mapped_column(nullable=True)
    wpm: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        nullable=True
    )  # success" | "fail" | "notchecked"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="text_results")

    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id"))
    text: Mapped["TextModel"] = relationship(back_populates="results")

    timings: Mapped[List["TextTimingModel"]] = relationship(
        back_populates="text_result"
    )

    def __str__(self) -> str:
        return f"{str(self.user_id,)} {self.status}"


class TextTimingModel(BaseSqlAlchemyModel):
    """Временные результаты прохождения этапа урока"""

    __tablename__ = "text_timings"
    seconds: Mapped[int] = mapped_column(nullable=True)
    created_date: Mapped[datetime] = mapped_column(server_default=func.now())

    text_result_id: Mapped[int] = mapped_column(ForeignKey("text_results.id"))
    text_result: Mapped["TextResultModel"] = relationship(back_populates="timings")

    def __str__(self) -> str:
        return str(self.id)
