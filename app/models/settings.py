from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.db.postgres.schema import Schemas
from app.models.core_model import CoreModel

if TYPE_CHECKING:
    from app.models.user import UserModel


class SettingsModel(CoreModel):
    __tablename__ = "settings"

    __table_args__ = {
        "schema": f"{Schemas.USERS.value}",
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

    activity: Mapped[bool] = mapped_column(default=True, comment="Active account or not")

    # relations

    user: Mapped["UserModel"] = relationship(back_populates="settings")
