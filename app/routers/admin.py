from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.config.auth.current_user import get_current_admin
from app.enums.role import RoleTypes
from app.schemas.role import RoleCreate, Role
from app.schemas.user import UserCreate, UserRole
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.utils.custom_options.user_options import UserCustomOptions

router = APIRouter(dependencies=[Depends(get_current_admin)])


@router.post(path="/")
async def create_admin(
    user_in: UserCreate,
    user_service: UserService.register_deps(),
) -> UserRole:
    await user_service.create_user(user_in=user_in, user_role=RoleTypes.ADMIN)

    user = await user_service.get_user_by_email(
        user_in.email, custom_options=UserCustomOptions.with_role()
    )

    return user


@router.post(path="/role")
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
