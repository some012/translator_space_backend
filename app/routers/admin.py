from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.config.auth.current_user import get_current_admin
from app.schemas.role import RoleCreate, Role
from app.services.role_service import RoleService

router = APIRouter(dependencies=[Depends(get_current_admin)])


@router.post(path="/")
async def create_role(
        role: RoleCreate, role_service: RoleService.register_deps()
) -> Role:
    return await role_service.create_role(role=role)


@router.get(path="/{sid}")
async def get_one_role(
        sid: UUID, role_service: RoleService.register_deps()
) -> Role | None:
    return await role_service.get_one_role(role_sid=sid)


@router.get(path="/")
async def get_all_roles(role_service: RoleService.register_deps()) -> List[Role]:
    return await role_service.get_all_roles()
