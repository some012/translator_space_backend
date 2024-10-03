from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import RoleModel
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.repositories.crud import CrudRepository


class RoleRepository(CrudRepository[RoleModel, RoleCreate, RoleUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(RoleModel, db)

    async def get_by_name(
            self,
            name: str,
            custom_options: tuple[ExecutableOption, ...] = None
    ) -> RoleModel | None:
        query = select(self.model).where(self.model.name == name)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().first()
