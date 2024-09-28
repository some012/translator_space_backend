from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config.db.postgres.engine import db_engine


class DBSessionManager:
    def __init__(self):
        self.postgres_session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db_engine
        )

    def get_psql(self):
        return self.postgres_session()
