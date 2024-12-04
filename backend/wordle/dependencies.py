from backend.exceptions import HTTP400BadRequest
from backend.wordle.constants import MAX_WORD_LENGTH
from backend.wordle.crud import check_game_session_exists, get_word_id_by_word
from backend.wordle.schemas import WordleRequestCheckWord


async def validate_word_data(
    word_data: WordleRequestCheckWord,
) -> WordleRequestCheckWord:
    if not await check_game_session_exists(word_data.session_id):
        raise HTTP400BadRequest(
            detail='This session does not exist or finished',
        )

    if not len(word_data.word) == MAX_WORD_LENGTH:
        raise HTTP400BadRequest(
            detail=f'The word length must be {MAX_WORD_LENGTH} characters long',
        )

    if await get_word_id_by_word(word=word_data.word) is None:
        raise HTTP400BadRequest(
            detail='Not in word list',
        )

    return word_data
