from datetime import datetime
from typing import Dict, List
from uuid import UUID

from src.wordle import constants as con
from src.wordle.crud import (
    add_attempt,
    finish_game_by_session_id,
    get_game_session_info_by_session_id,
    get_game_sessions_by_user_id,
)
from src.wordle.dtos import UserGameSession
from src.wordle.schemas import WordleResponseCheckWord


async def check_word_service(
    session_id: UUID,
    word: str,
) -> WordleResponseCheckWord:
    """
    Проверяет слово на соответствие правилам игры Wordle.
    """
    current_time = datetime.utcnow()

    game_session_info = await get_game_session_info_by_session_id(session_id)
    # текущая попытка = предыдущая + 1
    current_attempt_number = (
        max(game_session_info.attempts_info.keys()) + 1
        if game_session_info.attempts_info
        else 0
    )

    check_result = compare_words(guess=word, target=game_session_info.word)

    await add_attempt(
        session_id=game_session_info.session_id,
        owner_id=game_session_info.owner_id,
        created_at=current_time,
        attempt_number=current_attempt_number,
        word=word,
    )

    game_status: str = con.GameStatus.IN_PROGRESS.value

    if all(
        value == con.WordTypes.CORRECT.value for value in check_result.values()
    ):
        game_status = con.GameStatus.WIN.value

    # -1, т.к. подсчёт попыток идет с 0
    elif current_attempt_number >= con.MAX_ATTEMPT_NUMBER - 1:
        game_status = con.GameStatus.LOSS.value

    if game_status != con.GameStatus.IN_PROGRESS.value:
        await finish_game_by_session_id(
            session_id=session_id,
            finished_at=current_time,
            game_state=game_status,
        )

    return WordleResponseCheckWord(
        game_status=game_status,
        check_result=check_result,
        attempt_number=current_attempt_number + 1,  # Т.к. отсчёт идет с нуля
    )


def compare_words(guess: str, target: str) -> Dict[str, con.WordTypes]:
    result = {}
    target_letters = list(target)

    for i, letter in enumerate(guess):
        if letter == target[i]:
            result[letter] = con.WordTypes.CORRECT.value
            target_letters[i] = None

    for letter in guess:
        if letter not in result:
            if letter in target_letters:
                result[letter] = con.WordTypes.WRONG_PLACE.value
                target_letters[target_letters.index(letter)] = None
            else:
                result[letter] = con.WordTypes.NOT_CORRECT.value

    return result


async def get_all_user_gamesessions(user_id: int) -> List[UserGameSession]:
    """
    Возвращает все игровые сессии пользователя и базовую информацию по ним.
    """
    return await get_game_sessions_by_user_id(user_id)
