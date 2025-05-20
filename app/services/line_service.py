from typing import Annotated, Sequence, List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.deps.db import get_db
from app.models import LineModel
from app.schemas.line import LineCreate, LineUpdate
from app.services.repositories.line_repository import LineRepository


class LineService:
    def __init__(self, db: AsyncSession):
        self._line_repository = LineRepository(db=db)

    async def create_from_list(
        self, list_lines: list[LineCreate]
    ) -> Sequence[LineCreate]:
        return await self._line_repository.create_all(c_objects=list_lines)

    async def create_line(self, line_in: LineCreate) -> LineModel:
        return await self._line_repository.create(c_obj=line_in)

    async def update_line(self, line: LineModel, update_line: LineUpdate) -> LineModel:
        return await self._line_repository.update(db_obj=line, u_obj=update_line)

    async def get_one_line(
        self,
        line_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> LineModel | None:
        return await self._line_repository.get_one(
            sid=line_sid, custom_options=custom_options
        )

    async def get_all_lines(
        self,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[LineModel]:
        return await self._line_repository.get_all(custom_options=custom_options)

    async def get_all_lines_by_file_sid(
        self,
        file_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[LineModel]:
        return await self._line_repository.get_many_by_file_sid(
            file_sid=file_sid, custom_options=custom_options
        )

    async def get_many(
        self, sids: List[UUID], custom_options: tuple[ExecutableOption, ...] = None
    ) -> Sequence[LineModel]:
        lines = await self._line_repository.get_many_by_sids(
            sids=sids, custom_options=custom_options
        )

        if len(sids) != len(lines):
            raise HTTPException(status_code=404, detail="Lines not found")

        return lines

    async def delete_line(self, line_sid: UUID):
        return await self._line_repository.delete(sid=line_sid)

    @staticmethod
    def register(db: AsyncSession):
        return LineService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[LineService, Depends(get_line_service)]


async def get_line_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return LineService(db=db)
