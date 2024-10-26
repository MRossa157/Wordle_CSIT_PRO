from typing import Dict, Literal

from pydantic import BaseModel

from src.wordle.constants import word_types

WordStatus = Literal[
    word_types.CORRECT,
    word_types.NOT_CORRECT,
    word_types.WRONG_PLACE,
]


class WordleResponseCheckWord(BaseModel):
    check_result: Dict[str, WordStatus]  # type: ignore  # noqa: PGH003
