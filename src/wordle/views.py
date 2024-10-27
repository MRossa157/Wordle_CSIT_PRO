
from typing import Annotated

from fastapi import APIRouter, Depends

from src.wordle.dependencies import validate_word_data
from src.wordle.schemas import WordleRequestCheckWord, WordleResponseCheckWord
from src.wordle.services import check_word_service

router = APIRouter()


@router.post(
        path='/check_word',
        summary='Проверить слово',
)
async def check_word(
        word_data: Annotated[
            WordleRequestCheckWord,
            Depends(validate_word_data),
        ],
) -> WordleResponseCheckWord:
    return await check_word_service(
        session_id=word_data.session_id,
        word=word_data.word,
    )
