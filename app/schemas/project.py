from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB
from app.schemas.file import FileLines


class ProjectBase(CoreSchema):
    name: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class ProjectAdd(ProjectBase):
    user_sid: UUID


class ProjectUpdate(ProjectCreate):
    pass


class Project(ProjectBase, CoreSchemaInDB):
    user_sid: UUID


class ProjectAll(ProjectBase, CoreSchemaInDB):
    user_sid: UUID
    files: list[FileLines]
