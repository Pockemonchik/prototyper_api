from pydantic import ConfigDict

from src.database.base_schemas import DbEntityBaseSchema


# ------------ Forms -------------------


class GetTextForm(DbEntityBaseSchema):
    punctuation: bool | None = None
    textType: str | None = None


# ------------ Texts -------------------


class TextConfigSchema(DbEntityBaseSchema):
    description: str | None = None
    punctuation: bool | None = None
    textType: str | None = None
    model_config = ConfigDict(from_attributes=True)


class TextSchema(DbEntityBaseSchema):
    config_id: int | None = None
    text: str | None = None
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class TextResultSchema(DbEntityBaseSchema):
    percentage: int | None = None
    wpm: int | None = None
    status: str | None = None
    user_id: int | None = None
    text_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TextTimingSchema(DbEntityBaseSchema):
    seconds: int
    lesson_step_result_id: int

    model_config = ConfigDict(from_attributes=True)
