from pydantic import BaseModel, ConfigDict

from src.database.base_schemas import DbEntityBaseSchema


class UserSchema(DbEntityBaseSchema):
    username: str | None = None
    password: str | None = None
    is_admin: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class UserLessonsStats(BaseModel):
    completed_lessons_count: int | None = None
    lessons_count: int | None = None
    total_time_spent: int | None = None
    model_config = ConfigDict(from_attributes=True)


class UserProfileSchema(DbEntityBaseSchema):
    username: str | None = None
    is_admin: bool | None = None
    lessons_stats: UserLessonsStats | None = None
    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(DbEntityBaseSchema):
    username: str | None = None
    password: str | None = None


class CreateUserSchema(BaseModel):
    username: str
    password: str


class SuccessAuthResponseSchema(BaseModel):
    token: str


class AuthRequestSchema(BaseModel):
    username: str
    password: str
