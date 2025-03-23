from pydantic import BaseModel


class DbEntityBaseSchema(BaseModel):
    id: int
