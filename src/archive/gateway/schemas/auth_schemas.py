from pydantic import BaseModel


class RegistrationForm(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str


class LoginForm(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str