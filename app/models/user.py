from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.core_model import CoreModel


class UserModel(CoreModel):
    __tablename__ = "user"

    __table_args__ = {
        "schema": "users",
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

    last_login: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
