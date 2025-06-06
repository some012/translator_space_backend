from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import ProjectModel
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.repositories.crud import CrudRepository


class ProjectRepository(CrudRepository[ProjectModel, ProjectCreate, ProjectUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProjectModel, db)

    async def get_by_name(
        self, name: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ProjectModel | None:
        query = select(self.model).where(self.model.name == name)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_user_sid(
        self, user_sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ProjectModel | None:
        query = select(self.model).where(self.model.user_sid == user_sid)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def search_by_all_fields(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        datetime_start: Optional[datetime] = None,
        datetime_end: Optional[datetime] = None,
    ) -> Sequence[ProjectModel]:
        conditions = []

        if name:
            conditions.append(self.model.name.ilike(f"%{name}%"))  # LIKE %name%
        if description:
            conditions.append(self.model.description.ilike(f"%{description}%"))
        if datetime_start:
            conditions.append(self.model.created >= datetime_start)
        if datetime_end:
            conditions.append(self.model.created <= datetime_end)

        query = select(self.model)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        return result.scalars().all()
