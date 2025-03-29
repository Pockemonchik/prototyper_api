from typing import List

from pydantic import BaseModel, ConfigDict

from src.database.base_schemas import DbEntityBaseSchema

# Сущности Schema - DTO модели для выдачи данных
# Сущности Form - модели данных приходящих с фронта для выдачи данных

# EntityNameBaseShema - с полями без связанных сущностей,
# (для того чтобы исключить lazy load и работали базовые методы Repository)


# ------------ result of lesson step -------------------


class LessonStepStatsSchema(BaseModel):
    users_count: int | None = None  # количество пользователей

    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(from_attributes=True)


# ------------ timing of lesson step -------------------


class LessonStepTimingSchema(DbEntityBaseSchema):
    seconds: int
    lesson_step_result_id: int
    model_config = ConfigDict(from_attributes=True)


class CreateLessonStepTimingSchema(BaseModel):
    seconds: int
    lesson_step_result_id: int


class UpdateLessonStepTimingSchema(BaseModel):
    seconds: int
    lesson_step_result_id: int
    model_config = ConfigDict(from_attributes=True)


# ------------ lesson step -------------------


class LessonStepBaseSchema(DbEntityBaseSchema):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonStepSchema(LessonStepBaseSchema):
    stats: LessonStepStatsSchema | None = None
    texts: List[str] | None = None
    result: LessonStepResultSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateLessonStepSchema(BaseModel):
    name: str | None = None


class UpdateLessonStepSchema(BaseModel):
    name: str | None = None
    model_config = ConfigDict(from_attributes=True)


# ------------ lesson -------------------


class LessonStatsSchema(BaseModel):
    users_count: int | None = None  # количество пользователей
    steps_count: int | None = None  # количество шагов

    model_config = ConfigDict(from_attributes=True)


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
    stats: LessonStatsSchema | None = None
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
