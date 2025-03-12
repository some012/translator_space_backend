from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.postgres.schema import Schemas
from app.models.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import UserModel, FileModel


class ProjectModel(CoreModel):
    __tablename__ = "project"

    __table_args__ = {
        "schema": f"{Schemas.PROJECTS.value}",
    }

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )

    user_sid: Mapped[UUID] = mapped_column(
        ForeignKey("users.user.sid", ondelete="CASCADE"), primary_key=True
    )

    name: Mapped[str] = mapped_column(VARCHAR(length=225), index=True, unique=True)

    description: Mapped[str] = mapped_column()

    # relations

    user: Mapped["UserModel"] = relationship(back_populates="projects")

    files: Mapped[list["FileModel"]] = relationship(back_populates="project")
