from typing import Generic, TypeVar, Type, Sequence
from uuid import UUID

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import CoreModel

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_one(
        self, sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all(
        self, custom_options: tuple[ExecutableOption, ...] = None
    ) -> Sequence[ModelType]:
        query = select(self.model)

        if custom_options:
            query = query.options(*custom_options)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, c_obj: CreateSchemaType) -> ModelType:
        try:
            db_obj = self.model(**c_obj.model_dump())

            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)

            return db_obj
        except IntegrityError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate entry detected. Ensure unique values for required fields.",
            ) from e

    async def update(self, db_obj: ModelType, u_obj: UpdateSchemaType) -> ModelType:
        try:
            obj = jsonable_encoder(db_obj)

            update_data = u_obj.model_dump(exclude_unset=True)

            for field in obj:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            self.db.add(db_obj)

            await self.db.commit()
            await self.db.refresh(db_obj)

            return db_obj

        except IntegrityError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate entry detected. Ensure unique values for required fields.",
            ) from e

    async def delete(self, sid: UUID) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)
        result = await self.db.execute(query)
        obj = result.scalars().first()

        await self.db.delete(obj)

        await self.db.commit()

        return obj
