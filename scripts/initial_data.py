import asyncio
import sys

sys.path = ["", ".."] + sys.path[1:]

from app.config.db.init import init_db
from app.config.db.session import async_session


async def init_psql() -> None:
    db = async_session
    await init_db(db)
    await db.close()


async def main() -> None:
    await init_psql()


if __name__ == "__main__":
    asyncio.run(main())
