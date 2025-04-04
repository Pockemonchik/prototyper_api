from __future__ import annotations

from pydantic import BaseModel


class APIErrorMessage(BaseModel):
    type: str
    message: str
