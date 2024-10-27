from datetime import datetime

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import UserModel
from app.schemas.user import UserCreate, UserUpdate
from app.services.repositories.crud import CrudRepository
from app.utils.helpers.password_helper import password_helper


class UserRepository(CrudRepository[UserModel, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)

    async def get_by_email(
        self, email: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        query = select(self.model).where(self.model.email == email)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_username(
        self, username: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        query = select(self.model).where(self.model.name == username)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, c_obj: UserCreate) -> UserModel:
        try:
            db_obj = c_obj.model_dump()
            db_obj["hashed_password"] = password_helper.get_password_hash(
                c_obj.password
            )
            db_obj.pop("password")
            db_obj = self.model(**db_obj)

            self.db.add(db_obj)

            # TODO: Добавить refresh в отдельную функцию в репозитории

            db_obj.last_activity = datetime.now()

            await self.db.commit()
            await self.db.refresh(db_obj)

            return db_obj

        # TODO: Поправить except на более нормальный вывод, в detail выводится куча непонятной инфы о ошибке
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def authenticate(
        self,
        email: EmailStr,
        password: str,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> UserModel | None:
        user = await self.get_by_email(email=email, custom_options=custom_options)

        if not user:
            return None

        if not password_helper.verify_password(password, user.hashed_password):
            return None

        user.last_activity = datetime.now()

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def add_and_refresh_user(self, user: UserModel) -> UserModel:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
