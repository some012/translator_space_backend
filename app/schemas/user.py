from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB
from app.schemas.role import Role


class UserBase(CoreSchema):
    name: str
    middle_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserRegistration(UserCreate):
    role_sid: UUID


class UserUpdate(UserCreate):
    pass


class User(UserBase, CoreSchemaInDB):
    img: str | None
    hashed_password: str
    role_sid: UUID
    last_activity: datetime


class UserRole(User):
    role: Role
