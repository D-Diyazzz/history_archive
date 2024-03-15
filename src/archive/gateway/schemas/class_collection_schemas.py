from pydantic import BaseModel
from datetime import date


class ClassCollectionRequest(BaseModel):
    name: str


class ClassCollectionResponse(BaseModel):
    id: int
    name: str