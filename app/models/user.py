from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.postgres.schema import Schemas
from app.models.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import SettingsModel, RoleModel, ProjectModel


class UserModel(CoreModel):
    __tablename__ = "user"

    __table_args__ = {
        "schema": f"{Schemas.USERS.value}",
    }

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )

    name: Mapped[str] = mapped_column(index=True, comment="name of user")
    middle_name: Mapped[str] = mapped_column(comment="middle name of user")
    last_name: Mapped[str] = mapped_column(comment="last name of user")

    email: Mapped[str] = mapped_column(index=True, unique=True, comment="email")
    phone: Mapped[str | None] = mapped_column(unique=True, comment="phone")
    hashed_password: Mapped[str] = mapped_column(comment="password")

    role_sid: Mapped[UUID] = mapped_column(
        ForeignKey("security.role.sid", ondelete="RESTRICT"), primary_key=True
    )

    img: Mapped[str] = mapped_column(nullable=True)

    last_activity: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))

    # relations

    settings: Mapped["SettingsModel"] = relationship(back_populates="user")

    role: Mapped["RoleModel"] = relationship(back_populates="users")

    projects: Mapped[list["ProjectModel"]] = relationship(back_populates="user")
