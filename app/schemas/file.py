from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB
from app.schemas.line import Line


class FileBase(CoreSchema):
    project_sid: UUID
    name: str


class FileCreate(FileBase):
    pass


class FileUpdate(CoreSchema):
    project_sid: UUID
    name: str


class File(FileUpdate, CoreSchemaInDB):
    pass


class FileLines(CoreSchemaInDB):
    project_sid: UUID
    name: str
    lines: list[Line]
