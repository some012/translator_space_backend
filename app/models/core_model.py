from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class CoreModel(DeclarativeBase):
    sid: UUID

    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now().replace(microsecond=0)
    )

    updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now().replace(microsecond=0),
        onupdate=datetime.now().replace(microsecond=0)
    )
