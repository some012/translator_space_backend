import asyncio
import sys

from app.config.db.postgres.session import async_session

sys.path = ["", ".."] + sys.path[1:]

from app.config.db.init import init_db


async def init_psql() -> None:
    db = async_session
    await init_db(db)
    await db.close()


async def main() -> None:
    await init_psql()


if __name__ == "__main__":
    asyncio.run(main())
