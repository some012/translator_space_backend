from datetime import datetime
from uuid import UUID

from app.schemas.core_schema import CoreSchema


class RoleBase(CoreSchema):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleCreate):
    pass


class RoleInDBBase(RoleBase):
    sid: UUID

    created: datetime
    updated: datetime


class Role(RoleInDBBase):
    pass
