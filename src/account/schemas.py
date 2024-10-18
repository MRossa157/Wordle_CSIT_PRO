from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    username: str


class UserInfo(BaseModel):
    username: Optional[str] = None


class GameSessionResponse(BaseModel):
    session_id: UUID
