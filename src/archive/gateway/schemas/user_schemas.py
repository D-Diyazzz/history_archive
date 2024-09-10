from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    firstname: str
    lastname: str
    role: str
    email: str

