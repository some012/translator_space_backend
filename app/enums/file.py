from enum import StrEnum


class ContentType(StrEnum):
    XML = "text/xml"
    TS = "text/plain"


class FileFormat(StrEnum):
    XML = ".xml"
    TS = ".ts"
