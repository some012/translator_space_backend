from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db import get_db
from app.models import SettingsModel
from app.schemas.settings import SettingsCreate
from app.services.repositories.settings_repository import SettingsRepository


class SettingsService:
    def __init__(self, db: AsyncSession):
        self._settings_repository = SettingsRepository(db=db)

    async def create_settings(self, settings: SettingsCreate) -> SettingsModel:
        return await self._settings_repository.create(c_obj=settings)

    @staticmethod
    def register(db: AsyncSession):
        return SettingsService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[SettingsService, Depends(get_settings_service)]


async def get_settings_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return SettingsService(db=db)
