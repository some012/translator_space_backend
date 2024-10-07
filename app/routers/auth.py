from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.config.auth.current_user import get_current_user
from app.config.auth.token_helper import token_helper
from app.config.auth.token_schema import Token
from app.config.settings.project import project_settings
from app.enums.role import RoleTypes
from app.schemas.user import UserCreate, UserRole
from app.services.user_service import UserService
from app.utils.custom_options.user_options import UserCustomOptions

router = APIRouter()


@router.post(path="/register")
async def create_user(
    user_in: UserCreate,
    user_service: UserService.register_deps(),
) -> UserRole:
    await user_service.create_user(user_in=user_in, user_role=RoleTypes.USER)

    user = await user_service.get_user_by_email(
        user_in.email, custom_options=UserCustomOptions.with_role()
    )

    return user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService.register_deps(),
) -> Token:
    user = await user_service.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=project_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = token_helper.create_access_token(
        data={"sub": str(user.email)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def get_me(
    current_user: Annotated[UserRole, Depends(get_current_user)],
) -> UserRole:
    return current_user
