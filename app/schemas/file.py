from typing import Optional
from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB
from app.schemas.line import Line


class FileBase(CoreSchema):
    project_sid: UUID
    name: str
    source_bytes: Optional[bytes] = None


class FileCreate(FileBase):
    pass


class FileUpdate(FileCreate):
    pass


class File(FileBase, CoreSchemaInDB):
    pass


class FileLines(CoreSchemaInDB):
    project_sid: UUID
    name: str
    lines: list[Line]
