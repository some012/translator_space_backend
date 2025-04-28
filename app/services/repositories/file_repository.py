from typing import Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import FileModel
from app.schemas.file import FileCreate, FileUpdate
from app.services.repositories.crud import CrudRepository


class FileRepository(CrudRepository[FileModel, FileCreate, FileUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(FileModel, db)

    async def get_many_by_project_sid(
        self,
        project_sid: UUID,
        custom_options: tuple[ExecutableOption, ...] = None,
        only_sids: bool = False,
    ) -> Sequence[UUID]:
        if only_sids:
            query_model = self.model.sid
        else:
            query_model = self.model

        query = select(query_model).where(self.model.project_sid == project_sid)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_all_by_project_sid(self, project_sid: UUID):
        query = delete(self.model).where(self.model.project_sid == project_sid)
        await self.db.execute(query)
        await self.db.commit()
