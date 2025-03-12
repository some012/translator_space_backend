from sqlalchemy import select
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
