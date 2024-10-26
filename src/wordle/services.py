from typing import Dict, Literal
from uuid import UUID

from src.wordle.constants import word_types
from src.wordle.crud import get_game_session_word_id, get_word_by_id

WordStatus = Literal[
    word_types.CORRECT,
    word_types.NOT_CORRECT,
    word_types.WRONG_PLACE,
]


async def check_word_service(
    session_id: UUID,
    word: str,
) -> Dict[str, WordStatus]:
    """
    Проверяет слово на соответствие правилам игры Wordle.
    """
    guess_word = await get_word_by_id(
        await get_game_session_word_id(session_id),
    )

    # TODO: Добавить запись попытки в БД

    return compare_words(guess=word, target=guess_word)


def compare_words(guess: str, target: str) -> Dict[str, WordStatus]:
    result = {}
    target_letters = list(target)

    for i, letter in enumerate(guess):
        if letter == target[i]:
            result[letter] = word_types.CORRECT
            target_letters[i] = None

    for letter in guess:
        if (
            letter not in result
        ):
            if letter in target_letters:
                result[letter] = word_types.WRONG_PLACE
                target_letters[target_letters.index(letter)] = None
            else:
                result[letter] = word_types.NOT_CORRECT

    return result
