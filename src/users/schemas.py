from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    username: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(BaseModel):
    id: int
    name: str | None = None


class CreateUserSchema(BaseModel):
    name: str
    password: str


class AuthResponseSchema(BaseModel):
    token: str
