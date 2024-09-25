from typing import Any

from pydantic import Field, field_validator, PostgresDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

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


project_settings: ProjectSettings = ProjectSettings()
