from uuid import UUID

from app.schemas.core_schema import CoreSchema, CoreSchemaInDB


class SettingsBase(CoreSchema):
    user_sid: UUID
    activity: bool


class SettingsCreate(SettingsBase):
    pass


class SettingsUpdate(SettingsCreate):
    pass


class Settings(SettingsBase, CoreSchemaInDB):
    pass
