from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from app.config.auth.token import validate_access_token
from app.config.auth.token_schema import TokenData
from app.enums.role import RoleTypes
from app.schemas.user import UserRole
from app.services.user_service import UserService
from app.utils.custom_options.user_options import UserCustomOptions


async def get_current_user(
    payload: Annotated[TokenData, Depends(validate_access_token)],
    user_service: UserService.register_deps(),
) -> UserRole:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    current_user = await user_service.get_user_by_email(
        email=payload.username, custom_options=UserCustomOptions.with_role()
    )

    if current_user is None:
        raise credentials_exception

    return current_user


async def get_current_admin(
    current_user: Annotated[UserRole, Depends(get_current_user)],
) -> UserRole:
    if current_user.role.name not in [
        RoleTypes.ADMIN,
        RoleTypes.SUPERUSER,
    ]:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED, detail="Not enough permissions"
        )

    return current_user
