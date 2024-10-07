from typing import Any

from pydantic import Field, field_validator, PostgresDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    API_V1_STR: str = "/api/v1"
    HOST: str = Field("0.0.0.0")
    PORT: int = Field(8000)

    # PostgresSQL Configuration
    POSTGRES_HOST: str = Field("0.0.0.0")
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_USER: str = Field("test")
    POSTGRES_PASSWORD: str = Field("password")
    POSTGRES_DB: str = Field("default_db")

    POSTGRES_DATABASE_URL: PostgresDsn | None = None

    @field_validator("POSTGRES_DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        options = {
            "scheme": "postgresql+asyncpg",
            "username": values.data.get("POSTGRES_USER"),
            "password": values.data.get("POSTGRES_PASSWORD"),
            "host": values.data.get("POSTGRES_HOST"),
            "port": values.data.get("POSTGRES_PORT"),
            "path": f'{values.data.get("POSTGRES_DB") or ""}',
        }
        return PostgresDsn.build(**options)

    # auth
    SECRET_KEY: str = Field("09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


project_settings: ProjectSettings = ProjectSettings()
