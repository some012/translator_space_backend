from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter()


@router.post(path="/")
async def create_role(
        role: RoleCreate,
        role_service: RoleService.register_deps()
) -> Role:
    return await role_service.create_role(role=role)


@router.get(path="/{sid}")
async def get_one_role(
        sid: UUID,
        role_service: RoleService.register_deps()
) -> Role | None:
    return await role_service.get_one_role(role_sid=sid)


@router.get(path="/")
async def get_all_roles(
        role_service: RoleService.register_deps()
) -> List[Role]:
    return await role_service.get_all_roles()


@router.put(path="/{sid}")
async def update_role(
        sid: UUID,
        update_data: RoleUpdate,
        role_service: RoleService.register_deps()
) -> Role | None:
    return await role_service.update_role(role_sid=sid, update_role=update_data)


@router.delete(path="/{sid}")
async def delete_one(
        sid: UUID,
        role_service: RoleService.register_deps()
) -> Role:
    return await role_service.delete_role(role_sid=sid)
