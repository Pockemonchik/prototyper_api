from pydantic import BaseModel, ConfigDict

# ------------ lesson -------------------


class LessonSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    language: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LessonResultSchema(BaseModel):
    id: int
    lesson_id: int
    user_id: int
    percentage: int | None = None
    status: str | None = None

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


# ------------ lesson step -------------------


class LessonStepSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    language: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ------------ lesson with adds -------------------


class LessonWithResultSchema(LessonSchema):

    result: LessonResultSchema

    model_config = ConfigDict(from_attributes=True)
