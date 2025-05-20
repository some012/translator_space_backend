from typing import Optional
from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB


class LineBase(CoreSchema):
    file_sid: UUID
    meaning: str
    translation: str
    translated: bool
    group: str
    filename: Optional[str] = None
    line: Optional[int] = None


class LineCreate(LineBase):
    pass


class LineUpdate(LineCreate):
    pass


class Line(LineBase, CoreSchemaInDB):
    pass


class ChangeLine(CoreSchema):
    meaning: str
    translation: str


class TranslationMLLine(CoreSchema):
    sid: UUID
    meaning: str
    translation: str
