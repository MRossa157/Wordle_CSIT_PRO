"""Add created_at to users

Revision ID: 41adaf84cd4c
Revises: efab7b407db5
Create Date: 2024-10-10 14:04:13.942844

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "41adaf84cd4c"
down_revision: Union[str, None] = "efab7b407db5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            comment="Дата создания пользователя",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "created_at")
    # ### end Alembic commands ###
