from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB
from app.schemas.line import Line


class FileBase(CoreSchema):
    project_sid: UUID
    path: str


class FileCreate(FileBase):
    pass


class FileUpdate(FileCreate):
    pass


class File(FileBase, CoreSchemaInDB):
    pass


class FileLines(File):
    lines: list[Line]
