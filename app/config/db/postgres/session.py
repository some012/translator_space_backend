from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config.db.postgres.engine import db_engine

postgres_session = async_sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

async_session = postgres_session()
