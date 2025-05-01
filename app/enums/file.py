from enum import StrEnum


class ContentType(StrEnum):
    XML = "text/xml"
    TS = "text/plain"


class TranslationFileFormat(StrEnum):
    XML = ".xml"
    TS = ".ts"


class ImageFileFormat(StrEnum):
    JPEG = ".jpg"
    PNG = ".png"
