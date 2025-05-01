from app.schemas.core_schema import CoreSchema


class DownloanLinkSchemaOut(CoreSchema):
    download_link: str


class UploadUrlSchemaOut(CoreSchema):
    url: str
    s3_object_path: str


class ViewUrlSchemaOut(CoreSchema):
    url: str


class MessageResponseSchemaOut(CoreSchema):
    message: str
