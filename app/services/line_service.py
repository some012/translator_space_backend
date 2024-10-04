from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.services.repositories.line_repository import LineRepository


class LineService:
    def __init__(self, db: AsyncSession):
        self._line_repository = LineRepository(db=db)

    @staticmethod
    def register(db: AsyncSession):
        return LineService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[LineService, Depends(get_line_service)]


async def get_line_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return LineService(db=db)
