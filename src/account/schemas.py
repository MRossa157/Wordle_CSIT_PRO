from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.wordle.dtos import UserGameSession


class UserInfoResponse(BaseModel):
    username: str


class UserInfo(BaseModel):
    username: Optional[str] = None


class GameSessionResponse(BaseModel):
    session_id: UUID


class GameSessionsResponse(BaseModel):
    user_sessions: List[UserGameSession]
