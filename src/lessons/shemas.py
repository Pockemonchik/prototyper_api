from pydantic import BaseModel, ConfigDict


class LessonSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    text: str | None = None
    timing: int | None = None
    percentage: int | None = None
    language: str | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateLessonSchema(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    text: str | None = None
    timing: int | None = None
    percentage: int | None = None
    language: str | None = None
    status: str | None = None


class FilterLessonSchema(BaseModel):
    id: int | None = None
    name: str


class CreateLessonSchema(BaseModel):
    name: str
    description: str | None = None
    text: str | None = None
    timing: int | None = None
    percentage: int | None = None
    language: str | None = None
    status: str | None = None
