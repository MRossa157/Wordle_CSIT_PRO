"""Initial migration

Revision ID: efab7b407db5
Revises: 
Create Date: 2024-10-05 20:26:23.678190

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "efab7b407db5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment="ID записи",
        ),
        sa.Column(
            "username",
            sa.String(length=32),
            nullable=False,
            comment="Имя пользователя",
        ),
        sa.Column(
            "password_hash",
            postgresql.BYTEA(),
            nullable=False,
            comment="Hash пароля пользователя",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
