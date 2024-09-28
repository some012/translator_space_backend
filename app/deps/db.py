from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db.session import DBSessionManager


async def get_db() -> AsyncSession:
    session_manager = DBSessionManager()
    db = session_manager.get_psql()
    try:
        yield db
    finally:
        await db.close()
