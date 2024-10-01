from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RoleModel
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.repositories.crud import CrudRepository


class RoleRepository(CrudRepository[RoleModel, RoleCreate, RoleUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(RoleModel, db)
