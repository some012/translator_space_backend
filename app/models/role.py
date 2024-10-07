from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.postgres.schema import Schemas
from app.models.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import UserModel


class RoleModel(CoreModel):
    __tablename__ = "role"

    __table_args__ = {
        "schema": f"{Schemas.SECURITY.value}",
    }

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        VARCHAR(length=225), unique=True, index=True, comment="name of role"
    )

    # relations

    users: Mapped[list["UserModel"]] = relationship(back_populates="role")
