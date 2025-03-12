from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

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
