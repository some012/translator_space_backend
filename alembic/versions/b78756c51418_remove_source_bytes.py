"""remove_source_bytes

Revision ID: b78756c51418
Revises: 3f0d656b2dfb
Create Date: 2025-05-01 03:04:18.585885

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b78756c51418"
down_revision: Union[str, None] = "3f0d656b2dfb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("file", "source_bytes", schema="projects")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "file",
        sa.Column(
            "source_bytes", postgresql.BYTEA(), autoincrement=False, nullable=True
        ),
        schema="projects",
    )
    # ### end Alembic commands ###
