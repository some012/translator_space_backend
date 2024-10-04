from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB


class ProjectBase(CoreSchema):
    user_sid: UUID
    name: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectCreate):
    pass


class Project(ProjectBase, CoreSchemaInDB):
    pass
