"""is_active_and_remove_settings

Revision ID: 360dc99e2c29
Revises: 5aedb8846e69
Create Date: 2025-05-21 00:48:13.103279

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "360dc99e2c29"
down_revision: Union[str, None] = "5aedb8846e69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("settings", schema="users")
    op.add_column(
        "user",
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default="true",
            nullable=False,
            comment="locked or unlocked",
        ),
        schema="users",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "is_active", schema="users")
    op.create_table(
        "settings",
        sa.Column("sid", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("user_sid", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "activity",
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=False,
            comment="Active account or not",
        ),
        sa.Column(
            "created",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_sid"],
            ["users.user.sid"],
            name="settings_user_sid_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("sid", "user_sid", name="settings_pkey"),
        sa.UniqueConstraint("sid", name="settings_sid_key"),
        schema="users",
    )
    # ### end Alembic commands ###
