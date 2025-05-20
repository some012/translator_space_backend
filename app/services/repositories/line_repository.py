from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import LineModel
from app.schemas.line import LineCreate, LineUpdate
from app.services.repositories.crud import CrudRepository


class LineRepository(CrudRepository[LineModel, LineCreate, LineUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(LineModel, db)

    async def delete_all_by_file_sid(self, file_sid: UUID):
        query = delete(self.model).where(self.model.file_sid == file_sid)
        await self.db.execute(query)
        await self.db.commit()

    async def get_many_by_file_sid(
        self,
        file_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[LineModel]:
        query = select(self.model).where(self.model.file_sid == file_sid)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_many_by_sids(
        self,
        sids: Sequence[UUID],
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> Sequence[LineModel]:
        query = select(self.model).where(self.model.sid.in_(sids))

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().all()
