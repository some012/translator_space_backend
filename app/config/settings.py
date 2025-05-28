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

    # S3
    S3_BUCKET_NAME: str = Field("translation")
    S3_EXTERNAL_HOST: str = Field("0.0.0.0")
    S3_PORT: int = Field(9000)
    S3_ACCESS_KEY: str = Field("access_key")
    S3_SECRET_KEY: str = Field("secret_key")
    S3_REGION: str = Field("us-east-1")
    S3_REQUIRE_TLS: bool = Field(False)
    IS_PROXY_REQUIRED: bool = Field(False)
    S3_INTERNAL_URL: str = Field("http://minio:9000")

    S3_ENDPOINT: str | None = None

    @field_validator("S3_ENDPOINT", mode="before")
    def assemble_s3_host(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return f'{values.data.get("S3_EXTERNAL_HOST")}:{values.data.get("S3_PORT")}'

    # auth
    SECRET_KEY: str = Field(
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # redis
    REDIS_HOST: str = Field("0.0.0.0")
    REDIS_PORT: int = Field(6379)
    ACTIVITY_COUNT_EXPIRE_SECONDS: int = 86400 * 2

    # superuser
    SUPERUSER_NAME: str = Field("name")
    SUPERUSER_MIDDLE_NAME: str = Field("middle_name")
    SUPERUSER_LAST_NAME: str = Field("last_name")
    SUPERUSER_LOGIN: str = Field("superuser@gmail.com")
    SUPERUSER_PASSWORD: str = Field("123123")


project_settings: ProjectSettings = ProjectSettings()
