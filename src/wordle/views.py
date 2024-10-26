from uuid import UUID

from fastapi import APIRouter

from src.wordle.schemas import WordleResponseCheckWord
from src.wordle.services import check_word_service

router = APIRouter()


@router.post(
        path='/check_word',
        summary='Проверить слово',
        # responses={
        #     **API_RESPONSES['check_word'],
        # },
)
async def check_word(
        session_id: UUID,
        word: str,
) -> WordleResponseCheckWord:
    check_result = await check_word_service(session_id=session_id, word=word)
    return WordleResponseCheckWord(check_result=check_result)
