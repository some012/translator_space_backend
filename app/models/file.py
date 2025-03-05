from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.postgres.schema import Schemas
from app.models.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import ProjectModel, LineModel


class FileModel(CoreModel):
    __tablename__ = "file"

    __table_args__ = {
        "schema": f"{Schemas.PROJECTS.value}",
    }

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )

    name: Mapped[str] = mapped_column(VARCHAR(length=225), index=True, unique=True)

    project_sid: Mapped[UUID] = mapped_column(
        ForeignKey("projects.project.sid", ondelete="CASCADE"), primary_key=True
    )

    path: Mapped[str] = mapped_column(VARCHAR(length=225), nullable=True)

    # relations

    project: Mapped["ProjectModel"] = relationship(back_populates="files")

    lines: Mapped[list["LineModel"]] = relationship(back_populates="file")
