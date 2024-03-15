from pydantic import BaseModel


class MethodCollectionRequest(BaseModel):
    name: str


class MethodCollectionResponse(BaseModel):
    id: int
    name: str