from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.services.repositories.file_repository import FileRepository


class FileService:
    def __init__(self, db: AsyncSession):
        self._file_repository = FileRepository(db=db)

    @staticmethod
    def register(db: AsyncSession):
        return FileService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[FileService, Depends(get_file_service)]


async def get_file_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return FileService(db=db)
