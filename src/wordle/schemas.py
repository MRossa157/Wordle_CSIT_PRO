from typing import Dict
from uuid import UUID

from pydantic import BaseModel, Field

from src.wordle.constants import GameStatus, WordTypes


class WordleResponseCheckWord(BaseModel):
    game_status: GameStatus = Field(description='Статус игры')
    check_result: Dict[str, WordTypes] = Field(
        description='Результат проверки слова',
    )


class WordleRequestCheckWord(BaseModel):
    session_id: UUID = Field(description='ID игровой сессии')
    word: str = Field(description='Слово для проверки')
