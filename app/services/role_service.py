from typing import Annotated, Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.models import RoleModel
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, db: AsyncSession):
        self._role_repository = RoleRepository(db=db)

    async def create_role(self, role: RoleCreate) -> RoleModel:
        return await self._role_repository.create(c_obj=role)

    async def update_role(self, role_sid: UUID, update_role: RoleUpdate) -> RoleModel:
        role = await self._role_repository.get_one(sid=role_sid)

        if role is None:
            raise HTTPException(status_code=400, detail="Role not found")

        return await self._role_repository.update(db_obj=role, u_obj=update_role)

    async def get_one_role(self, role_sid: UUID) -> RoleModel | None:
        return await self._role_repository.get_one(sid=role_sid)

    async def get_by_name(self, name: str) -> RoleModel | None:
        return await self._role_repository.get_by_name(name=name)

    async def get_all_roles(self) -> Sequence[RoleModel]:
        return await self._role_repository.get_all()

    async def delete_role(self, role_sid: UUID) -> RoleModel:
        return await self._role_repository.delete(sid=role_sid)

    @staticmethod
    def register(db: AsyncSession):
        return RoleService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[RoleService, Depends(get_role_service)]


async def get_role_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return RoleService(db=db)
