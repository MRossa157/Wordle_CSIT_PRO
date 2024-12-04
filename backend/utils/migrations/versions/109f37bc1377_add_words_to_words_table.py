"""Add words to words table

Revision ID: 109f37bc1377
Revises: 9ce58efd7a70
Create Date: 2024-11-13 01:01:35.420522

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = "109f37bc1377"
down_revision: Union[str, None] = "9ce58efd7a70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with open("wordle-bank.txt", "r") as file:
        words = file.read().splitlines()

    # Удаляем дубликаты, если такие есть
    unique_words = set(words)

    # Подготавливаем строку для массовой вставки
    conn = op.get_bind()
    values_clause = ", ".join(f"(:word_{i})" for i in range(len(unique_words)))
    params = {f"word_{i}": word for i, word in enumerate(unique_words)}

    insert_query = f"INSERT INTO words (word) VALUES {values_clause}"
    conn.execute(text(insert_query), params)


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("DELETE FROM words"))
