from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from starlette import status
from starlette.responses import JSONResponse

from app.config.consts.msg import Msg
from app.deps.db import get_db
from app.models import UserModel
from app.schemas.user import UserCreate, UserRegistration, UserUpdate, UserRole
from app.services.repositories.role_repository import RoleRepository
from app.services.repositories.user_repository import UserRepository
from app.utils.custom_options.user_options import UserCustomOptions
from app.utils.helpers.password_helper import password_helper


class UserService:
    def __init__(self, db: AsyncSession):
        self._user_repository = UserRepository(db=db)
        self._role_repository = RoleRepository(db=db)

    async def authenticate_user(
        self,
        email: str,
        password: str,
        custom_options: tuple[ExecutableOption, ...] = None,
    ):
        return await self._user_repository.authenticate(
            email=email, password=password, custom_options=custom_options
        )

    async def get_user_by_email(
        self,
        email: str,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> UserModel | None:
        return await self._user_repository.get_by_email(
            email=email, custom_options=custom_options
        )

    async def get_user_by_username(
        self, username: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        return await self._user_repository.get_by_username(
            username=username, custom_options=custom_options
        )

    async def create_user(self, user_in: UserCreate, user_role: str) -> UserModel:
        user = await self._user_repository.get_by_email(email=user_in.email)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже существует",
            )

        role = await self._role_repository.get_by_name(name=user_role)

        if not role:  # noqa
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Роль не найдена"
            )

        create_user = UserRegistration(**user_in.__dict__, role_sid=role.sid)

        user = await self._user_repository.create(c_obj=create_user)

        return user

    async def change_user_password(
        self, user_sid: UUID, new_password: str, myself: bool, old_password: str = None
    ) -> JSONResponse:
        user = await self._user_repository.get_one(
            sid=user_sid, custom_options=UserCustomOptions.with_role()
        )
        if myself:
            if not password_helper.verify_password(old_password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пароли не совпадают",
                )

        hashed_password = password_helper.get_password_hash(new_password)
        user.hashed_password = hashed_password

        await self._user_repository.add_and_refresh_user(user=user)

        return JSONResponse(
            content=Msg(msg="Пароль успешно обновлён").model_dump(),
            status_code=status.HTTP_200_OK,
        )

    async def reset_user_password(
        self, user_sid: UUID, new_password: str
    ) -> JSONResponse:
        user = await self._user_repository.get_one(
            sid=user_sid, custom_options=UserCustomOptions.with_role()
        )

        hashed_password = password_helper.get_password_hash(new_password)
        user.hashed_password = hashed_password

        await self._user_repository.add_and_refresh_user(user=user)

        return JSONResponse(
            content=Msg(msg="Пароль успешно обновлён").model_dump(),
            status_code=status.HTTP_200_OK,
        )

    async def update_user(self, user_sid: UUID, update_user: UserUpdate) -> UserModel:
        user = await self._user_repository.get_one(sid=user_sid)

        if user is None:
            raise HTTPException(status_code=400, detail="Пользователь не найден")

        return await self._user_repository.update(db_obj=user, u_obj=update_user)

    async def soft_delete_user_by_sid(self, user_sid: UUID):
        user = await self._user_repository.get_one(
            sid=user_sid, custom_options=UserCustomOptions.with_role()
        )
        user.is_active = False

        return await self._user_repository.add_and_refresh_user(user=user)

    async def is_active(self, user: UserRole) -> bool:  # noqa
        return user.is_active

    @staticmethod
    def register(db: AsyncSession):
        return UserService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[UserService, Depends(get_user_service)]


async def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return UserService(db=db)
