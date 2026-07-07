"""make file item_id nullable

Revision ID: cf8c11e06714
Revises: 30c06c5cf1df
Create Date: 2026-07-07 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf8c11e06714"
down_revision: Union[str, Sequence[str], None] = "30c06c5cf1df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("files", recreate="always") as batch_op:
        batch_op.alter_column(
            "item_id",
            existing_type=sa.BigInteger(),
            nullable=True,
        )


def downgrade() -> None:
    with op.batch_alter_table("files", recreate="always") as batch_op:
        batch_op.alter_column(
            "item_id",
            existing_type=sa.BigInteger(),
            nullable=False,
        )
