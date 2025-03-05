from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.deps.db import get_db
from app.models import FileModel
from app.schemas.file import FileUpdate, FileCreate
from app.services.repositories.file_repository import FileRepository


class FileService:
    def __init__(self, db: AsyncSession):
        self._file_repository = FileRepository(db=db)

    async def create_file(self, file_in: FileCreate) -> FileModel:
        return await self._file_repository.create(c_obj=file_in)

    async def update_file(self, file_sid: UUID, update_file: FileUpdate) -> FileModel:
        file = await self._file_repository.get_one(sid=file_sid)

        if file is None:
            raise HTTPException(status_code=400, detail="File not found")

        return await self._file_repository.update(db_obj=file, u_obj=update_file)

    async def get_one_file(
        self,
        file_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> FileModel | None:
        return await self._file_repository.get_one(
            sid=file_sid, custom_options=custom_options
        )

    async def get_all_files(
        self,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[FileModel]:
        return await self._file_repository.get_all(custom_options=custom_options)

    @staticmethod
    def register(db: AsyncSession):
        return FileService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[FileService, Depends(get_file_service)]


async def get_file_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return FileService(db=db)
