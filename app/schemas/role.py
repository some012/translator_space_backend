from app.schemas.core_schema import CoreSchema, CoreSchemaInDB


class RoleBase(CoreSchema):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleCreate):
    pass


class Role(RoleBase, CoreSchemaInDB):
    pass
