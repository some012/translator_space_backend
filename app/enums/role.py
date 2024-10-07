from enum import Enum


class RoleTypes(str, Enum):
    ADMIN = "ADMIN"
    SUPERUSER = "SUPERUSER"
    USER = "USER"
