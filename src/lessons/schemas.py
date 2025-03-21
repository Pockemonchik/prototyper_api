from typing import List
from pydantic import BaseModel, ConfigDict

# ------------ lesson step -------------------


class LessonStepResultSchema(BaseModel):
    id: int
    lesson_step_id: int
    user_id: int
    percentage: int | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonStepSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    texts: List[str] | None = None
    result: LessonStepResultSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateLessonStepSchema(BaseModel):
    name: str | None = None


class UpdateLessonStepSchema(BaseModel):
    id: int
    name: str | None = None


# ------------ lesson -------------------


class LessonResultSchema(BaseModel):
    id: int
    lesson_id: int
    user_id: int
    percentage: int | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    language: str | None = None
    result: LessonResultSchema | None = None
    steps: List[LessonStepSchema] | None = None
    model_config = ConfigDict(from_attributes=True)


class UpdateLessonSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    language: str | None = None


class CreateLessonSchema(BaseModel):
    name: str
    description: str | None = None
    language: str | None = None
