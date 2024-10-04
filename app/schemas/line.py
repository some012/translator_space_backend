from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB


class LineBase(CoreSchema):
    file_sid: UUID
    meaning: str
    translation: str
    translated: bool


class LineCreate(LineBase):
    pass


class LineUpdate(LineCreate):
    pass


class Line(LineBase, CoreSchemaInDB):
    pass
