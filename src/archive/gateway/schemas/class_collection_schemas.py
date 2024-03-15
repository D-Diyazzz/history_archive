from pydantic import BaseModel


class ClassCollectionRequest(BaseModel):
    name: str


class ClassCollectionResponse(BaseModel):
    id: int
    name: str