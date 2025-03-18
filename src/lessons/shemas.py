from pydantic import BaseModel, ConfigDict


class LessonSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UpdateLessonSchema(BaseModel):
    id: int
    name: str


class FilterLessonSchema(BaseModel):
    id: int | None = None
    name: str


class CreateLessonSchema(BaseModel):
    name: str
