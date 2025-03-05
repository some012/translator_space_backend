from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, VARCHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.postgres.schema import Schemas
from app.models.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import FileModel


class LineModel(CoreModel):
    __tablename__ = "line"

    __table_args__ = {
        "schema": f"{Schemas.PROJECTS.value}",
    }

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )

    file_sid: Mapped[UUID] = mapped_column(
        ForeignKey("projects.file.sid", ondelete="CASCADE"), primary_key=True
    )

    group: Mapped[str] = mapped_column(VARCHAR(length=225), index=True)

    filename: Mapped[str] = mapped_column(
        VARCHAR(length=1024), nullable=True, index=True
    )

    line: Mapped[Optional[int]] = mapped_column(nullable=True)

    meaning: Mapped[str] = mapped_column(index=True)

    translation: Mapped[str] = mapped_column(index=True)

    translated: Mapped[bool] = mapped_column(
        Boolean, server_default="false", nullable=False
    )

    # relations

    file: Mapped["FileModel"] = relationship(back_populates="lines")
