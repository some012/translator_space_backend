from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings.project import project_settings

db_engine = create_async_engine(
    url=project_settings.POSTGRES_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=0,
)
