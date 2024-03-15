from pydantic import BaseModel
from datetime import date


class TypeRequest(BaseModel):
    name: str


class TypeResponse(BaseModel):
    id: int
    name: str