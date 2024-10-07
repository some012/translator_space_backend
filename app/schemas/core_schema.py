from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CoreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class CoreSchemaInDB(CoreSchema):
    sid: UUID

    created: datetime
    updated: datetime
