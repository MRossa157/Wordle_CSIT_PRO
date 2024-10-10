from pydantic import BaseModel


class UserRegistration(BaseModel):
    username: str
    password: str


class UserAuthentication(BaseModel):
    username: str
    password: str


class ValidatedUserAuthentication(BaseModel):
    id: int
    username: str
    password: str


class JWTResponse(BaseModel):
    access_token: str | None
    refresh_token: str | None = None
    token_type: str = 'Bearer'
    message: str | None = None
