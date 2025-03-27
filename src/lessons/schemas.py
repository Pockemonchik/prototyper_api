from typing import List

from pydantic import BaseModel, ConfigDict

from src.database.base_schemas import DbEntityBaseSchema

# Сущности Schema - DTO модели для выдачи данных
# Сущности Form - модели данных приходящих с фронта для выдачи данных

# EntityNameBaseShema - с полями без связанных сущностей,
# (для того чтобы исключить lazy load и работали базовые методы Repository)


# ------------ lesson step -------------------


class LessonStepResultSchema(DbEntityBaseSchema):
    lesson_step_id: int
    user_id: int
    percentage: int | None = None
    status: str | None = None
    wpm: int | None = None

    timing_list: int | List[int] | None = None

    model_config = ConfigDict(from_attributes=True)


class SetLessonStepResultForm(BaseModel):
    percentage: int | None = None
    status: str | None = None
    wpm: int | None = None
    timing: int | None = None


class CreateLessonStepResultSchema(BaseModel):
    lesson_step_id: int
    user_id: int
    percentage: int | None = None
    status: str | None = None
    wpm: int | None = None


class UpdateLessonStepResultSchema(BaseModel):
    lesson_step_id: int | None = None
    user_id: int | None = None
    percentage: int | None = None
    status: str | None = None
    wpm: int | None = None


class LessonStepBaseSchema(DbEntityBaseSchema):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonStepSchema(LessonStepBaseSchema):

    texts: List[str] | None = None
    result: LessonStepResultSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateLessonStepSchema(BaseModel):
    name: str | None = None


class UpdateLessonStepSchema(DbEntityBaseSchema):
    name: str | None = None


# ------------ lesson -------------------


class LessonResultSchema(BaseModel):
    lesson_id: int
    user_id: int
    percentage: int | None = None  # процент прохождения
    status: str | None = None  # статус в процессе , готово, провален
    average_wpm: int | None = None  # в среднем слов в минуту
    total_time_spent: int | None = None  # всего времени проведено в уроке
    total_time_best: int | None = None  # сумма всех лучших времен

    model_config = ConfigDict(from_attributes=True)


class LessonBaseSchema(DbEntityBaseSchema):
    name: str | None = None
    description: str | None = None
    language: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonSchema(LessonBaseSchema):

    result: LessonResultSchema | None = None
    steps: List[LessonStepSchema] | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateLessonSchema(DbEntityBaseSchema):
    name: str | None = None
    description: str | None = None
    language: str | None = None


class CreateLessonSchema(BaseModel):
    name: str
    description: str | None = None
    language: str | None = None
