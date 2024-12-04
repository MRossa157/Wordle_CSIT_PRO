from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID


@dataclass
class UserGameSession:
    session_id: UUID
    game_state: str
    attempts_info: Dict[int, str]


@dataclass
class GameSessionInfo:
    session_id: UUID
    owner_id: int
    created_at: datetime
    finished_at: Optional[datetime]
    word: str
    attempts_info: Dict[int, str]
