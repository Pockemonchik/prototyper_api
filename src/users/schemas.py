from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    username: str | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    id: int
    username: str | None = None
    password: str | None = None


class CreateUserSchema(BaseModel):
    username: str
    password: str


class SuccessAuthResponseSchema(BaseModel):
    token: str
    id: int
    username: str


class AuthRequestSchema(BaseModel):
    username: str
    password: str
