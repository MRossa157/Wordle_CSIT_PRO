import uuid
from datetime import datetime

from src.account.crud import (
    create_game_session,
    get_random_word_id_from_db,
    update_game_session_finish_time,
)


async def create_new_game_session(owner_id: int) -> uuid.UUID:
    """
    Создает новую игровую сессию для пользователя.
    """

    created_at = datetime.utcnow()
    session_id = uuid.uuid4()
    guess_word_id = await get_random_word_id()
    return await create_game_session(
        session_id=session_id,
        owner_id=owner_id,
        created_at=created_at,
        guess_word_id=guess_word_id,
    )


async def get_random_word_id() -> int:
    """
    Возвращает случайный ID слова из базы данных.
    """
    return await get_random_word_id_from_db()


async def update_finish_game_session(
    session_id: uuid.UUID,
    finish_time: datetime,
) -> None:
    """
    Обновляет время окончания игровой сессии, идентифицированной session_id.
    """
    await update_game_session_finish_time(session_id, finish_time)
