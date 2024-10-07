from app.schemas.core_schema import CoreSchema


class Token(CoreSchema):
    access_token: str
    token_type: str


class TokenData(CoreSchema):
    username: str | None = None
