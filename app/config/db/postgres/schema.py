from enum import Enum


class Schemas(str, Enum):
    USERS = "users"
    SECURITY = "security"
    PROJECTS = "projects"
