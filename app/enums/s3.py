from enum import StrEnum


class S3BucketName(StrEnum):
    TRANSLATION = "translation"
    IMAGES = "images"


class S3FolderName(StrEnum):
    TRANSLATION = "translation"
    PROJECT = "project"
    USER = "user"
